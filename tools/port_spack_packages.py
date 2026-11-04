#!/usr/bin/env python3
# Copyright (C) 2026 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Port commits between this repository and a spack-packages checkout.

By default, the commits of this repository (HEAD if none is given) are ported to a new branch of
the spack-packages checkout, one commit each, keeping their author, date and message.
With --reverse, commits of the spack-packages checkout are ported back to a new branch here, for
instance after a pull request was merged there with requested changes.

Only the recipes are ported: what lies under `packages/<name>/` here, under
`repos/spack_repo/builtin/packages/<name>/` there.
Each commit is applied with a 3-way merge, like `git cherry-pick`.
When it conflicts, the port stops: resolve the conflicts, `git add` the files, then run again with
--continue, or give up with --abort, or drop that commit with --skip, as with `git rebase`.

With --convert, the recipes are first converted to the spack-packages style, which drops the code
this repository keeps to support older versions of spack, before being merged: hunks next to that
code then merge cleanly instead of conflicting.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PDI_PREFIX = "packages"
SPACK_PACKAGES_PREFIX = "repos/spack_repo/builtin/packages"
STATE_NAME = "port-spack-packages"
REF_PREFIX = "refs/port-spack-packages/"
EXIT_STOPPED = 3

SPACK_HEADER = "# Copyright Spack Project Developers. See COPYRIGHT file for details.\n"


class PortError(Exception):
    pass


class Stop(Exception):
    """A commit that could not be applied, even with conflicts."""


# --------------------------------------------------------------------------------------------- git


def git(repo, *args, input=None, check=True, env=None, binary=False):
    """Run git in repo and return its stdout (str, or bytes if binary)."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input if binary or input is None else input.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=None if env is None else {**os.environ, **env},
    )
    if check and result.returncode != 0:
        raise PortError(
            f"git {' '.join(args)} failed in {repo}:\n{result.stderr.decode(errors='replace')}"
        )
    return result.stdout if binary else result.stdout.decode()


def git_status(repo, *args, input=None):
    """Run git in repo and return (returncode, stdout, stderr), all decoded."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode, result.stdout.decode(), result.stderr.decode(errors="replace")


def toplevel(path):
    code, out, _ = git_status(path, "rev-parse", "--show-toplevel")
    return Path(out.strip()) if code == 0 else None


def is_pdi_repo(top):
    yaml = top / "repo.yaml"
    return (
        (top / PDI_PREFIX).is_dir()
        and yaml.is_file()
        and re.search(r"namespace:\s*['\"]?pdi['\"]?\s*$", yaml.read_text(), re.M) is not None
    )


def is_spack_packages_repo(top):
    return (top / SPACK_PACKAGES_PREFIX).is_dir()


def current_branch(repo):
    code, out, _ = git_status(repo, "symbolic-ref", "--short", "-q", "HEAD")
    return out.strip() if code == 0 else None


def commit_url(repo, sha):
    """A URL of sha on GitHub, from the upstream or origin remote, or the bare sha."""
    for remote in ("upstream", "origin"):
        code, out, _ = git_status(repo, "remote", "get-url", remote)
        m = re.match(
            r"(?:https://github\.com/|git@github\.com:)([^/]+/[^/]+?)(?:\.git)?/?$", out.strip()
        )
        if code == 0 and m:
            return f"https://github.com/{m.group(1)}/commit/{sha}"
    return sha


# -------------------------------------------------------------------------------------- conversion


def _drop_version_conditions(lines):
    """Keep the body of `if spack_version_info...:` blocks, dedented, and drop their `else:`."""
    out = []
    i = 0
    while i < len(lines):
        m = re.match(r"^(\s*)if spack_version_info\b.*:\s*$", lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        indent = len(m.group(1))
        body, i = _block(lines, i + 1, indent)
        out.extend(line[4:] if line.strip() else line for line in body)
        if i < len(lines) and re.match(r"^\s{%d}else:\s*$" % indent, lines[i]):
            _, i = _block(lines, i + 1, indent)
    return out


def _block(lines, start, indent):
    """The lines indented deeper than indent from start on, and the index of the next one."""
    end = start
    last = start
    while end < len(lines):
        line = lines[end]
        if line.strip():
            if len(line) - len(line.lstrip()) <= indent:
                break
            last = end + 1
        end += 1
    return lines[start:last], last


def to_spack_packages(text):
    """Convert a recipe of this repository to the style of spack-packages."""
    text = re.sub(
        r"\A# Copyright \(C\)[^\n]*\n"
        r"# and others\. See the top-level COPYRIGHT file for details\.\n",
        SPACK_HEADER,
        text,
    )

    def try_import(m):
        return "" if "spack.hooks.sbang" in m.group(1) else m.group(1) + "\n"

    text = re.sub(
        r"^try:\n    ((?:from|import) [^\n]+)\nexcept BaseException:\n    [^\n]+\n",
        try_import,
        text,
        flags=re.M,
    )
    text = re.sub(r"^from spack import spack_version_info\n", "", text, flags=re.M)
    text = re.sub(r"^from \.(\w+) import ", r"from ..\1.package import ", text, flags=re.M)
    text = re.sub(
        r" if spack_version_info\b[^\n]*? else (?:\"[^\"\n]*\"|'[^'\n]*'|[\w.]+)", "", text
    )
    text = text.replace(
        "def setup_run_environment(self, env):",
        "def setup_run_environment(self, env: EnvironmentModifications) -> None:",
    )
    lines = _drop_version_conditions(text.splitlines(keepends=True))

    # imports are separated by single blank lines, and followed by two before the code
    out = []
    in_header = True
    for line in lines:
        if in_header and not line.strip() and out and not out[-1].strip():
            continue
        if in_header and line.strip() and not line.startswith(("#", "from ", "import ", " ", ")")):
            in_header = False
            while out and not out[-1].strip():
                out.pop()
            out.extend(["\n", "\n"])
        out.append(line)
    return "".join(out).rstrip("\n") + "\n"


# ------------------------------------------------------------------------------------------- state


class Port:
    """A port in progress, saved as JSON in the git directory of its target repository."""

    def __init__(self, data):
        self.__dict__.update(data)

    @staticmethod
    def state_dir(repo):
        return Path(git(repo, "rev-parse", "--absolute-git-dir").strip()) / STATE_NAME

    @classmethod
    def load(cls, repo):
        f = cls.state_dir(repo) / "state.json"
        return cls(json.loads(f.read_text())) if f.is_file() else None

    @staticmethod
    def pointer(repo):
        """Where this repository records a port in progress in another one."""
        return Path(git(repo, "rev-parse", "--absolute-git-dir").strip()) / f"{STATE_NAME}.target"

    @classmethod
    def find(cls, repo):
        """The port in progress in repo, or whose target repo points to."""
        port = cls.load(repo)
        if port:
            return port
        pointer = cls.pointer(repo)
        target = pointer.is_file() and toplevel(pointer.read_text().strip())
        return cls.load(target) if target else None

    def save(self):
        d = self.state_dir(self.target)
        d.mkdir(exist_ok=True)
        (d / "state.json").write_text(json.dumps(self.__dict__, indent=2) + "\n")
        if self.pdi != self.target:
            self.pointer(self.pdi).write_text(self.target + "\n")

    def drop(self):
        for sha in self.commits:
            git(self.target, "update-ref", "-d", REF_PREFIX + sha, check=False)
        shutil.rmtree(self.state_dir(self.target), ignore_errors=True)
        if self.pdi != self.target:
            self.pointer(self.pdi).unlink(missing_ok=True)

    @property
    def src_prefix(self):
        return SPACK_PACKAGES_PREFIX if self.reverse else PDI_PREFIX

    @property
    def dst_prefix(self):
        return PDI_PREFIX if self.reverse else SPACK_PACKAGES_PREFIX

    def command(self, option):
        return f"{sys.argv[0]} {option} {self.target}"


# -------------------------------------------------------------------------------------------- port


def changed_files(port, sha, rev="HEAD"):
    """The recipe files sha changes, [(status, path relative to the source prefix)], and the
    packages it changes that the target does not have at rev, which are not ported."""
    out = git(
        port.source,
        "diff-tree",
        "-r",
        "--root",
        "--no-commit-id",
        "--no-renames",
        "--name-status",
        "-z",
        sha,
        "--",
        f":(glob){port.src_prefix}/*/**",
    )
    fields = out.split("\0")[:-1]
    n = len(port.src_prefix) + 1
    files = [(fields[i], fields[i + 1][n:]) for i in range(0, len(fields), 2)]
    kept, ignored = [], set()
    for status, rel in files:
        package = rel.split("/", 1)[0]
        known = (
            git_status(port.target, "cat-file", "-e", f"{rev}:{port.dst_prefix}/{package}")[0] == 0
        )
        created = (
            git_status(port.source, "cat-file", "-e", f"{sha}^:{port.src_prefix}/{package}")[0]
            != 0
        )
        if known or created:
            kept.append((status, rel))
        else:
            ignored.add(package)
    return kept, sorted(ignored)


def pathspecs(port, files):
    packages = sorted({rel.split("/", 1)[0] for _, rel in files})
    return [f":(glob){port.src_prefix}/{p}/**" for p in packages]


def apply_plain(port, sha, files):
    """Apply the recipe changes of sha with a 3-way merge; return the conflicting paths."""
    patch = git(
        port.source,
        "show",
        "--format=",
        "--patch",
        "--binary",
        "--full-index",
        "--no-renames",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        f"--relative={port.src_prefix}",
        sha,
        "--",
        *pathspecs(port, files),
        binary=True,
    )
    code, _, err = git_status(
        port.target, "apply", "--3way", "--index", f"--directory={port.dst_prefix}", input=patch
    )
    if code == 0:
        return []
    conflicts = git(port.target, "diff", "--name-only", "--diff-filter=U").split()
    if conflicts:
        return conflicts
    saved = Port.state_dir(port.target) / f"{sha}.patch"
    saved.parent.mkdir(exist_ok=True)
    saved.write_bytes(patch)
    raise Stop(
        f"could not apply the changes of {sha[:10]}:\n{err}"
        f"The patch is saved as {saved}: apply it by hand, `git add` the result, then run\n"
        f"  {port.command('--continue')}\n"
        f"or drop this commit with --skip, or give up with --abort."
    )


def apply_converted(port, sha, files):
    """Merge the recipe changes of sha converted to spack-packages style; return the conflicts."""
    conflicts = []
    for status, rel in files:
        src = f"{port.src_prefix}/{rel}"
        dst = f"{port.dst_prefix}/{rel}"
        path = Path(port.target) / dst

        def read(rev):
            data = git(port.source, "show", f"{rev}:{src}", binary=True)
            return to_spack_packages(data.decode()).encode() if rel.endswith(".py") else data

        base = read(f"{sha}^") if status != "A" else b""
        theirs = read(sha) if status != "D" else None
        ours = path.read_bytes() if path.is_file() else None

        if theirs is None:  # deleted in the source
            if ours is None:
                continue
            if ours == base:
                git(port.target, "rm", "-q", "--", dst)
                continue
            _stage_conflict(port, dst, base, ours, None)
            conflicts.append(dst)
            continue
        if ours is None and status != "A":  # modified in the source, missing here
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(theirs)
            _stage_conflict(port, dst, base, None, theirs)
            conflicts.append(dst)
            continue
        merged, clean = _merge(ours or b"", base, theirs)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(merged)
        if clean:
            git(port.target, "add", "--", dst)
        else:
            _stage_conflict(port, dst, base, ours or b"", theirs)
            conflicts.append(dst)
    return conflicts


def _merge(ours, base, theirs):
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for name, data in (("ours", ours), ("base", base), ("theirs", theirs)):
            f = Path(tmp) / name
            f.write_bytes(data)
            files.append(str(f))
        result = subprocess.run(
            [
                "git",
                "merge-file",
                "-p",
                "-L",
                "spack-packages",
                "-L",
                "base",
                "-L",
                "ported",
                *files,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    if result.returncode < 0:
        raise PortError(f"git merge-file failed: {result.stderr.decode(errors='replace')}")
    return result.stdout, result.returncode == 0


def _stage_conflict(port, dst, base, ours, theirs):
    """Record dst as unmerged in the index, as git does, so that `git add` resolves it."""
    entries = [f"0 {'0' * 40}\t{dst}\n"]
    for stage, data in ((1, base), (2, ours), (3, theirs)):
        if data is not None:
            blob = (
                git(port.target, "hash-object", "-w", "--stdin", input=data, binary=True)
                .decode()
                .strip()
            )
            entries.append(f"100644 {blob} {stage}\t{dst}\n")
    git(port.target, "update-index", "--index-info", input="".join(entries))


def add_symlinks(port, sha):
    """In this repository, each package directory with an underscore has a hyphenated symlink."""
    dirs = {rel.split("/", 1)[0] for _, rel in changed_files(port, sha)[0]}
    for d in sorted(dirs):
        link = Path(port.target) / port.dst_prefix / d.replace("_", "-")
        if (
            "_" in d
            and (Path(port.target) / port.dst_prefix / d).is_dir()
            and not os.path.lexists(link)
        ):
            link.symlink_to(d)
            git(port.target, "add", "--", str(link.relative_to(port.target)))


def commit(port, sha):
    """Commit what is staged with the metadata of sha; return False if there was nothing."""
    if port.reverse:
        add_symlinks(port, sha)
    if git_status(port.target, "diff", "--cached", "--quiet")[0] == 0:
        return False
    meta = (
        git(port.source, "log", "-1", "--format=%an%x00%ae%x00%aI", sha).rstrip("\n").split("\0")
    )
    message = git(port.source, "log", "-1", "--format=%B", sha)
    if port.trailer:
        message = git(
            port.target,
            "interpret-trailers",
            "--trailer",
            f"Ported-from: {commit_url(port.source, sha)}",
            input=message,
        )
    git(
        port.target,
        "commit",
        "-q",
        "--cleanup=whitespace",
        "-F",
        "-",
        input=message,
        env={"GIT_AUTHOR_NAME": meta[0], "GIT_AUTHOR_EMAIL": meta[1], "GIT_AUTHOR_DATE": meta[2]},
    )
    return True


def subject(port, sha):
    return git(port.source, "log", "-1", "--format=%h %s", sha).strip()


def run(port):
    while port.done < len(port.commits):
        sha = port.commits[port.done]
        if not port.stopped:
            files, ignored = changed_files(port, sha)
            if ignored:
                print(f"ignoring  {', '.join(ignored)} in {sha[:10]}: not in {port.target}")
            if not files:
                print(f"skipped   {subject(port, sha)}: it changes no recipe to port")
                port.done += 1
                port.save()
                continue
            apply = apply_converted if port.convert else apply_plain
            try:
                conflicts = apply(port, sha, files)
            except Stop as e:
                port.stopped = ["*"]
                port.save()
                print(f"stopped   {subject(port, sha)}")
                print(e, file=sys.stderr)
                return EXIT_STOPPED
            if conflicts:
                port.stopped = conflicts
                port.save()
                print(f"stopped   {subject(port, sha)}")
                print("conflicts in:\n  " + "\n  ".join(conflicts), file=sys.stderr)
                print(
                    f"Resolve them in {port.target}, `git add` the files, then run\n"
                    f"  {port.command('--continue')}\n"
                    f"or drop this commit with --skip, or give up with --abort.",
                    file=sys.stderr,
                )
                return EXIT_STOPPED
        port.stopped = []
        if commit(port, sha):
            print(f"ported    {subject(port, sha)}")
        else:
            print(f"skipped   {subject(port, sha)}: nothing left to commit")
        port.done += 1
        port.save()
    port.drop()
    print(f"Branch {port.branch} of {port.target} holds the ported commits.")
    return 0


# ----------------------------------------------------------------------------------------- actions


def resolve_commits(repo, revisions):
    """The commits to port, oldest first: a range as git understands it, or a single commit."""
    commits = []
    for rev in revisions:
        if ".." in rev or rev.startswith("^"):
            listed = git(repo, "rev-list", "--reverse", "--topo-order", "--no-merges", rev).split()
            merges = git(repo, "rev-list", "--merges", "--count", rev).strip()
            if merges != "0":
                print(f"dropping  the {merges} merge commit(s) of {rev}, as git rebase does")
            if not listed:
                raise PortError(f"{rev} holds no commit to port")
            commits += listed
        else:
            sha = git(repo, "rev-parse", "--verify", "-q", f"{rev}^{{commit}}").strip()
            if len(git(repo, "rev-list", "--parents", "-n", "1", sha).split()) > 2:
                raise PortError(
                    f"{sha[:10]} is a merge commit: port the commits it merges instead"
                )
            commits.append(sha)
    return commits


def start(args, pdi):
    sp = toplevel(args.spack_packages)
    if sp is None or not is_spack_packages_repo(sp):
        raise PortError(f"{args.spack_packages} is not a spack-packages checkout")
    source, target = (sp, pdi) if args.reverse else (pdi, sp)
    if args.convert and args.reverse:
        raise PortError("--convert only works from this repository to spack-packages")
    if Port.find(pdi) or Port.load(target):
        raise PortError(f"a port is in progress in {target}: use --continue, --skip or --abort")

    commits = resolve_commits(source, args.revisions or ["HEAD"])
    branch = args.branch or current_branch(source)
    if not branch:
        raise PortError(f"{source} is on a detached HEAD: name the branch to create with --branch")
    base = args.base
    if base is None:
        code, out, _ = git_status(target, "rev-parse", "--abbrev-ref", "origin/HEAD")
        if code != 0:
            raise PortError(
                f"{target} has no origin/HEAD: give the base of the branch with --base"
            )
        base = out.strip()
    base_sha = git(target, "rev-parse", "--verify", "-q", f"{base}^{{commit}}").strip()
    previous = git_status(target, "rev-parse", "--verify", "-q", f"refs/heads/{branch}")[1].strip()
    if previous and not args.force:
        raise PortError(f"branch {branch} already exists in {target}: use --force to recreate it")

    port = Port(
        {
            "reverse": args.reverse,
            "convert": args.convert,
            "trailer": args.trailer,
            "pdi": str(pdi),
            "source": str(source),
            "target": str(target),
            "branch": branch,
            "base": base_sha,
            "previous": previous or None,
            "orig_branch": current_branch(target),
            "orig_head": git(target, "rev-parse", "HEAD").strip(),
            "commits": commits,
            "done": 0,
            "stopped": [],
        }
    )
    print(
        f"Porting {len(commits)} commit(s) from {source}"
        f" to branch {branch} of {target}, on {base}:"
    )
    for sha in commits:
        files, ignored = changed_files(port, sha, base_sha)
        print(f"  {subject(port, sha)}" + ("" if files else "  (changes no recipe to port)"))
        if args.dry_run:
            for status, rel in files:
                print(f"      {status} {port.dst_prefix}/{rel}")
            for package in ignored:
                print(f"      ignored: {package}, not in the target")
    if args.dry_run:
        return 0

    if git(target, "status", "--porcelain", "--untracked-files=no"):
        raise PortError(f"{target} has uncommitted changes: commit or stash them first")
    git(
        target,
        "fetch",
        "-q",
        "--no-tags",
        str(source),
        *[f"{sha}:{REF_PREFIX}{sha}" for sha in commits],
    )
    git(target, "switch", "-q", "-C", branch, base_sha)
    port.save()
    return run(port)


def find_port(args, pdi):
    candidates = [args.spack_packages, os.getcwd(), pdi]
    for c in candidates:
        top = c and toplevel(c)
        port = top and Port.find(top)
        if port:
            return port
    raise PortError("no port in progress")


def resume(args, pdi):
    port = find_port(args, pdi)
    if not port.stopped:
        return run(port)
    unmerged = git(port.target, "diff", "--name-only", "--diff-filter=U").split()
    if unmerged:
        raise PortError(
            "still unmerged, `git add` them once resolved:\n  " + "\n  ".join(unmerged)
        )
    for f in port.stopped:
        path = Path(port.target) / f
        if f != "*" and path.is_file() and re.search(rb"^(<{7}|>{7}) ", path.read_bytes(), re.M):
            raise PortError(f"{f} still holds conflict markers")
    return run(port)


def skip(args, pdi):
    port = find_port(args, pdi)
    git(port.target, "reset", "-q", "--hard")
    print(f"dropped   {subject(port, port.commits[port.done])}")
    port.stopped = []
    port.done += 1
    port.save()
    return run(port)


def abort(args, pdi):
    port = find_port(args, pdi)
    git(port.target, "reset", "-q", "--hard")
    if port.orig_branch:
        git(port.target, "switch", "-q", "--discard-changes", port.orig_branch)
    else:
        git(port.target, "switch", "-q", "--discard-changes", "--detach", port.orig_head)
    if port.orig_branch != port.branch:
        if port.previous:
            git(port.target, "branch", "-q", "-f", port.branch, port.previous)
        else:
            git(port.target, "branch", "-q", "-D", port.branch)
    elif port.previous:
        git(port.target, "reset", "-q", "--hard", port.previous)
    port.drop()
    print(f"Port aborted, {port.target} is back as it was.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="\n\n".join(__doc__.split("\n\n")[1:]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("spack_packages", nargs="?", help="the spack-packages checkout")
    parser.add_argument(
        "revisions",
        nargs="*",
        help="the commits to port, single ones or ranges like A..B (default: HEAD of the source)",
    )
    parser.add_argument(
        "--branch", help="the branch to create (default: the current branch of the source)"
    )
    parser.add_argument(
        "--base", help="where the branch starts (default: origin/HEAD of the target)"
    )
    parser.add_argument("--force", action="store_true", help="recreate the branch if it exists")
    parser.add_argument(
        "--reverse", action="store_true", help="port from spack-packages to this repository"
    )
    parser.add_argument(
        "--convert", action="store_true", help="convert the recipes to spack-packages style first"
    )
    parser.add_argument(
        "--no-trailer",
        dest="trailer",
        action="store_false",
        help="do not end the messages with a Ported-from: trailer",
    )
    parser.add_argument("--dry-run", action="store_true", help="only list what would be ported")
    action = parser.add_mutually_exclusive_group()
    for name, text in (
        ("continue", "resume the port once the conflicts are resolved and added"),
        ("skip", "drop the commit that stopped the port, and resume it"),
        ("abort", "give up the port, and restore the target as it was"),
    ):
        action.add_argument(
            f"--{name}", dest="action", action="store_const", const=name, help=text
        )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent.parent
    pdi = next((t for t in (toplevel(os.getcwd()), toplevel(here)) if t and is_pdi_repo(t)), None)
    if pdi is None:
        parser.error("run it from a checkout of the pdi spack repository")
    try:
        if args.action:
            return {"continue": resume, "skip": skip, "abort": abort}[args.action](args, pdi)
        if not args.spack_packages:
            parser.error("the spack-packages checkout is required")
        return start(args, pdi)
    except PortError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
