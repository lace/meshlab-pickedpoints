"""
Read and write a MeshLab picked points file. Files contain named points in 3D
space. A set of picked points can be saved alongside the mesh and loaded in
MeshLab (on the **Edit** menu, click **PickPoints**).
"""

# Adapted from
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/serialization/meshlab_pickedpoints.py
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/test_meshlab_pickedpoints.py

from io import StringIO
from xml.etree import ElementTree

__all__ = ["load", "dumps", "dump"]


def load(fp):
    """
    Deserialize the `.pp` file in `fp` to an object.

    Args:
        fp: An open file pointer.

    Return:
        dict: A dict with string keys and 3D NumPy points.
    """
    tree = ElementTree.parse(fp)

    points = []
    for e in tree.iter("point"):
        try:
            point = [float(e.attrib["x"]), float(e.attrib["y"]), float(e.attrib["z"])]
        except ValueError:
            # This may happen if landmarks are just spaces.
            continue
        points.append({"name": e.attrib["name"], "point": point})

    return points


def loads(xml_string):
    """
    Deserialize a `.pp` XML string to an object.

    Args:
        xml_string (str): The contents of a `.pp` file.

    Return:
        dict: A dict with string keys and 3D NumPy points.
    """
    f = StringIO(xml_string)
    try:
        return load(f)
    finally:
        f.close()


def dumps(points):
    """
    Render a list of points to a string containing the contents of a `.pp` file.

    Args:
        points (list): A list of dicts of the form `{"name": name, "point": point}`

    Return:
        str: A string containing the `.pp` file contents.
    """
    # TODO Maybe reconstruct this using xml.etree.
    if not isinstance(points, list):
        raise ValueError("obj should be a list of points")
    for point in points:
        if not set(point.keys()).issubset(set(["name", "point"])):
            raise ValueError(
                f"Expected keys to include point and optional name; got {', '.join(point.keys())}"
            )
        assert isinstance(point["point"], list)
        assert len(point["point"]) == 3

    points_xml_string = "\n".join(
        [
            '<point x="{}" y="{}" z="{}" name="{}"/>'.format(
                *point["point"], point["name"]
            )
            for point in points
        ]
    )

    return """
    <!DOCTYPE PickedPoints>
    <PickedPoints>
     <DocumentData>
      <DateTime time="16:00:00" date="2014-12-31"/>
      <User name="bodylabs"/>
      <DataFileName name="ignored.obj"/>
     </DocumentData>
     {}
    </PickedPoints>
    """.format(
        points_xml_string
    )


def dump(points, fp):
    """
    Render a list of points to an open file.

    Args:
        points (list): A list of dicts of the form `{"name": name, "point": point}`
        fp: An open file pointer.
    """
    xml_string = dumps(points)
    fp.write(xml_string)
