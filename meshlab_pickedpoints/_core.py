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
import numpy as np
from vg.compat import v2 as vg

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

    points = {}
    for e in tree.iter("point"):
        try:
            point = np.array(
                [float(e.attrib["x"]), float(e.attrib["y"]), float(e.attrib["z"])]
            )
        except ValueError:
            # This may happen if landmarks are just spaces.
            continue
        points[e.attrib["name"]] = point

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


def dumps(obj):
    """
    Render a dictionary of points to a string containing the contents of a
    `.pp` file.

    Args:
        obj (dict): A mapping of names to 3D points.

    Return:
        str: A string containing the `.pp` file contents.
    """
    # TODO Maybe reconstruct this using xml.etree.
    if not isinstance(obj, dict):
        raise ValueError("obj should be a dictionary of points")
    for point in obj.values():
        vg.shape.check_value(point, (3,))

    points = "\n".join(
        [
            '<point x="{}" y="{}" z="{}" name="{}"/>'.format(x, y, z, name)
            for name, (x, y, z) in obj.items()
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
        points
    )


def dump(obj, fp):
    """
    Render a dictionary of points to an open file.

    Args:
        obj (dict): A mapping of names to 3D points.
        fp: An open file pointer.
    """
    xml_string = dumps(obj)
    fp.write(xml_string)
