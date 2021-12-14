from click.testing import CliRunner
import json
import pytest
from .cli import convert_landmarks
from .testing_fixtures import EXAMPLE_PICKED_POINTS_XML_STRING, EXAMPLE_POINTS
from .testing_helpers import assert_equal_points


@pytest.fixture
def write_tmp_picked_points(tmp_path):
    def _write_tmp_picked_points(xml_contents, basename="example.pp"):
        out_path = str(tmp_path / basename)
        with open(out_path, "w") as f:
            f.write(xml_contents)
        return out_path

    return _write_tmp_picked_points

def test_convert_landmarks_specified_output(tmp_path, write_tmp_picked_points):
    picked_points_path = write_tmp_picked_points(EXAMPLE_PICKED_POINTS_XML_STRING)
    output_path = tmp_path / "my_points.json"

    runner = CliRunner()
    result = runner.invoke(convert_landmarks, [picked_points_path, "-o", output_path])

    assert result.exit_code == 0
    assert result.output == ''

    with open(output_path, "r") as f:
        loaded = json.load(f)
    
    assert_equal_points(loaded, EXAMPLE_POINTS)

def test_convert_landmarks_default_output(tmpdir, write_tmp_picked_points):
    with tmpdir.as_cwd():
        picked_points_path = write_tmp_picked_points(EXAMPLE_PICKED_POINTS_XML_STRING)

        runner = CliRunner()
        result = runner.invoke(convert_landmarks, [picked_points_path])

        assert result.exit_code == 0
        assert result.output == ''

        with open("example.json", "r") as f:
            loaded = json.load(f)
        
        assert_equal_points(loaded, EXAMPLE_POINTS)
