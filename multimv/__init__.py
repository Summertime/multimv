#!/usr/bin/env python3
from re import compile
from types import SimpleNamespace
from pathlib import Path
import shlex
import os.path
from pprint import pprint
from functools import reduce
import click

from .vendor.toposort import toposort

@click.group()
@click.option("-n", "--dry-run", is_flag=True)  # -n is more common
@click.pass_context
def main(ctx, dry_run):
    ctx.ensure_object(SimpleNamespace)
    ctx.obj.dry_run = dry_run


@main.command()
@click.option("-g", "--global", "global_", is_flag=True)
@click.option("--eval", "eval_", is_flag=True)
@click.argument("pattern")
@click.argument("replacement")
@click.argument("files", nargs=-1, type=click.Path())
@click.pass_context
def re(ctx, pattern, replacement, files, eval_, global_):
    if eval_:
        repl = replacement
        def replacement(match):
            local = {
                "m0": match.group(0),
                **{f"m{i}": g for i, g in enumerate(match.groups(), 1)},
                **match.groupdict(),
            }
            return str(eval(repl, {}, local))

    count = 0 if global_ else 1
    regex = compile(pattern)
    moves = {f: regex.sub(replacement, f, count=count) for f in files}
    perform_moves(ctx, moves)


def perform_moves(ctx, moves):
    unmoved = {k for k,v in moves.items() if k == v or v is None}
    if len(l := list(moves.keys())) != len(sources := set(l)):
        raise Exception('Duplicate sources')
    if len(l := list(moves.values())) != len(targets := set(l)):
        raise Exception('Duplicate destinations')
    if not ctx.obj.dry_run:
        if any(not os.path.exists(f) for f in sources - unmoved):
            raise Exception('Non-existant source')
        if any(os.path.exists(f) for f in targets - sources - unmoved):
            raise Exception('Pre-existing destination')
    topo = {k:{v} for k,v in moves.items() if k not in unmoved}
    changes = {k:next(iter(topo[k])) for ks in toposort(topo) for k in ks}
    for u in unmoved:
        print(f"~ {shlex.quote(u)}")
        
    for src,tgt in changes.items():
        print(
            f"- {shlex.quote(src)}",
            f"+ {shlex.quote(tgt)}",
            sep="\n",
        )
        if not ctx.obj.dry_run:
            os.rename(src,tgt)
if __name__ == "__main__":
    main()
