from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat
import pytest
import sys

have_gfm = 'mdformat_gfm' in sys.modules

FIXTURE_PATH = Path(__file__).parent / "fixtures.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.skipif(have_gfm, reason="testing with gfm")
@pytest.mark.parametrize("line,title,text,expected", fixtures, ids=[f[1] for f in fixtures])
def test_fixtures(line, title, text, expected):
    output = mdformat.text(text, extensions={"pelican"})
    print(output)
    assert output.rstrip() == expected.rstrip(), output

@pytest.mark.skipif(not have_gfm, reason="testing without gfm")
@pytest.mark.parametrize("line,title,text,expected", fixtures, ids=[f[1] for f in fixtures])
def test_fixtures_gfm(line, title, text, expected):
    output = mdformat.text(text, extensions={"pelican","gfm"})
    print(output)
    assert output.rstrip() == expected.rstrip(), output
