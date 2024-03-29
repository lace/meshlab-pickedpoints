# Adapted from
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/serialization/meshlab_pickedpoints.py
# https://github.com/lace/lace/blob/d3c191dffaeedc14aafa4af031d74743de9e632d/lace/test_meshlab_pickedpoints.py

import pytest
from ._core import dump, load, loads
from .testing_fixtures import EXAMPLE_PICKED_POINTS_XML_STRING, EXAMPLE_POINTS
from .testing_helpers import assert_equal_points, assert_equal_xml


def test_load():
    from io import StringIO

    sample_f = StringIO(EXAMPLE_PICKED_POINTS_XML_STRING)

    try:
        result = load(sample_f)
    finally:
        sample_f.close()

    assert_equal_points(result, EXAMPLE_POINTS)


def test_loads():
    result = loads(EXAMPLE_PICKED_POINTS_XML_STRING)

    assert_equal_points(result, EXAMPLE_POINTS)


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
    expected_points = [
        {
            "name": "Femoral_epicon_med_lft",
            "point": [0.044259, 0.467733, -0.060032],
        },
        {"name": "Substernale", "point": [0.000625, 1.124424, 0.080930]},
    ]

    result = loads(xml_with_empty_point)

    assert_equal_points(result, expected_points)


def test_dump():
    from io import StringIO

    result_f = StringIO()

    try:
        dump(EXAMPLE_POINTS, result_f)
        result_str = result_f.getvalue()
    finally:
        result_f.close()

    assert_equal_xml(result_str, EXAMPLE_PICKED_POINTS_XML_STRING)


def test_dump_errors():
    from io import StringIO

    result_f = StringIO()

    try:
        with pytest.raises(ValueError, match="obj should be a list of points"):
            dump(-1, result_f)
    finally:
        result_f.close()

    try:
        with pytest.raises(
            ValueError,
            match="Expected keys to include point and optional name; got name, point, badkey",
        ):
            dump([{"name": "foo", "point": None, "badkey": -1}], result_f)
    finally:
        result_f.close()
