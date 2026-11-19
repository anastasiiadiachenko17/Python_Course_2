"""Validate an application config that a fixture provides."""

MAX_PORT = 65535


def test_input_data_is_valid(input_data):
    """The config has both sections with the right keys and values."""
    assert set(input_data) == {"server", "database"}

    server = input_data["server"]
    assert set(server) == {"host", "port", "debug"}
    assert isinstance(server["host"], str)
    assert server["host"]
    assert isinstance(server["port"], int)
    assert 1 <= server["port"] <= MAX_PORT
    assert isinstance(server["debug"], bool)

    database = input_data["database"]
    assert set(database) == {"name", "user", "timeout"}
    assert isinstance(database["name"], str)
    assert database["name"]
    assert isinstance(database["user"], str)
    assert database["user"]
    assert isinstance(database["timeout"], int)
    assert database["timeout"] > 0
