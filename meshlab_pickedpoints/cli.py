import click
from . import load


@click.command()
@click.argument("pp_file")
@click.option("-o", "--out", help="Output path")
def convert_landmarks(pp_file, out):
    import os
    import simplejson as json

    loaded = load(pp_file)

    result = [
        {"name": name, "point": coords.tolist()}
        for name, coords in loaded.items()
    ]

    if out is None:
        filename, _ = os.path.splitext(os.path.basename(pp_file))
        out = filename + ".json"
    
    with open(out, "w") as f:
        json.dump(result, f)

if __name__ == "__main__":  # pragma: no cover
    convert_landmarks()
