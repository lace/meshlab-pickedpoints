# Adapted from
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/serialization/meshlab_pickedpoints.py
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/test_meshlab_pickedpoints.py

from lxml import etree, objectify
import numpy as np
import pytest
from ._core import dump, load, loads

example_xml_string = """
<!DOCTYPE PickedPoints>
<PickedPoints>
 <DocumentData>
  <DateTime time="16:00:00" date="2014-12-31"/>
  <User name="bodylabs"/>
  <DataFileName name="ignored.obj"/>
 </DocumentData>
 <point x="0.044259" y="0.467733" z="-0.060032" name="Femoral_epicon_med_lft"/>
<point x="0.017893" y="1.335375" z="0.01839" name="Clavicale_lft"/>
<point x="0.000625" y="1.124424" z="0.08093" name="Substernale"/>
</PickedPoints>
"""

example_points = {
    "Femoral_epicon_med_lft": np.array([0.044259, 0.467733, -0.060032]),
    "Clavicale_lft": np.array([0.017893, 1.335375, 0.018390]),
    "Substernale": np.array([0.000625, 1.124424, 0.080930]),
}


def test_load():
    from io import StringIO

    sample_f = StringIO(example_xml_string)

    try:
        result = load(sample_f)
    finally:
        sample_f.close()

    assert set(result.keys()) == set(example_points.keys())
    assert all(np.array_equal(v, result[k]) for k, v in example_points.items())


def test_loads():
    result = loads(example_xml_string)

    assert set(result.keys()) == set(example_points.keys())
    assert all(np.array_equal(v, result[k]) for k, v in example_points.items())


def test_loads_error():
    xml_with_empty_point = """
    <!DOCTYPE PickedPoints>
    <PickedPoints>
    <DocumentData>
    <DateTime time="16:00:00" date="2014-12-31"/>
    <User name="bodylabs"/>
    <DataFileName name="ignored.obj"/>
    </DocumentData>
    <point x="0.044259" y="0.467733" z="-0.060032" name="Femoral_epicon_med_lft"/>
    <point x=" " y=" " z=" " name="Clavicale_lft"/>
    <point x="0.000625" y="1.124424" z="0.08093" name="Substernale"/>
    </PickedPoints>
    """
    expected_points = {
        "Femoral_epicon_med_lft": np.array([0.044259, 0.467733, -0.060032]),
        "Substernale": np.array([0.000625, 1.124424, 0.080930]),
    }

    result = loads(xml_with_empty_point)

    assert set(result.keys()) == set(expected_points.keys())
    assert all(np.array_equal(v, result[k]) for k, v in expected_points.items())


def assert_equal_xml(value, expected):
    # This is fairly naive -- doesn't consider whitespace or that the points
    # could be in different order, and is strict about irrelevant parts like
    # the DateTime. But seems to work okay.
    value_normalized = etree.tostring(objectify.fromstring(value))
    expected_normalized = etree.tostring(objectify.fromstring(expected))

    assert value_normalized == expected_normalized


def test_dump():
    from io import StringIO

    result_f = StringIO()

    try:
        dump(example_points, result_f)
        result_str = result_f.getvalue()
    finally:
        result_f.close()

    assert_equal_xml(result_str, example_xml_string)


def test_dump_error():
    from io import StringIO

    result_f = StringIO()

    try:
        with pytest.raises(ValueError, match="obj should be a dictionary of points"):
            dump(-1, result_f)
    finally:
        result_f.close()
