#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from pathlib import Path
import shlex

def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--method", choices=["re"], default="re")
    parser.add_argument("-g", "--global", dest="global_", action="store_true")
    parser.add_argument("-i", "--ignore-case", action="store_true")
    parser.add_argument("-d", "--dry-run", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("pattern")
    parser.add_argument("replacement")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()


    # Per method code
    if args.method == "re":
        import re

        def new_path(old):
            return old.with_name(
                re.sub(
                    args.pattern,
                    repl=args.replacement,
                    string=old.name,
                    flags=(re.I if args.ignore_case else 0),
                    count=(0 if args.global_ else 1),
                )
            )


    # Generic code
    moves = []
    for old in args.files:
        if old != (new := new_path(old)):
            moves.append(Namespace(old=old, new=new))

    if any(m.new.exists() for m in moves):
        raise Error  # Collides with pre-existing file

    if len({m.new for m in moves}) < len(moves):
        raise Error  # List has duplicates

    for move in moves:
        if not args.quiet:
            print(
                f"- {shlex.quote(str(move.old))}",
                f"+ {shlex.quote(str(move.new))}",
                sep="\n",
            )
        if not args.dry_run:
            move.old.rename(move.new)
