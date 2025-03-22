"""Test SentinelResponse."""

import sentinelresponse


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(sentinelresponse.__name__, str)
