from tech_common import greet, reverse_string


def test_reverse_string():
    assert reverse_string("abc") == "cba"
    assert reverse_string("") == ""
    assert reverse_string("123") == "321"


def test_greet():
    assert greet("Admin") == "Hello, Admin! Welcome to 20206205tech-python-common."
    assert "Developer" in greet("Developer")
