def assert_equal_points(first, second):
    assert len(first) == len(second)
    for first_item, second_item in zip(first, second):
        assert first_item["name"] == second_item["name"]
        assert first_item["point"] == second_item["point"]

def assert_equal_xml(value, expected):
    from lxml import etree, objectify

    # This is fairly naive -- doesn't consider whitespace or that the points
    # could be in different order, and is strict about irrelevant parts like
    # the DateTime. But seems to work okay.
    value_normalized = etree.tostring(objectify.fromstring(value))
    expected_normalized = etree.tostring(objectify.fromstring(expected))

    assert value_normalized == expected_normalized
