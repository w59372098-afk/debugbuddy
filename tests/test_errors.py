from debugbuddy.errors import get_error_guide


def test_known_error_guide():
    guide = get_error_guide("TypeError")
    assert "incompatible type" in guide["explanation"]


def test_unknown_error_guide():
    guide = get_error_guide("FutureError")
    assert guide["suggestions"]
