import click
from . import load


@click.command()
@click.argument("pp_file")
@click.option("-o", "--out", help="Output path")
def convert_landmarks(pp_file, out):
    import json
    import os

    loaded = load(pp_file)

    if out is None:
        filename, _ = os.path.splitext(os.path.basename(pp_file))
        out = f"{filename}.json"

    with open(out, "w") as f:
        json.dump(loaded, f, indent=2)


if __name__ == "__main__":  # pragma: no cover
    convert_landmarks()
