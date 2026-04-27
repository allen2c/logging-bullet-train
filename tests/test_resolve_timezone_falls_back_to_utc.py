import logging_bullet_train as lbt


def test_resolve_timezone_falls_back_to_utc(monkeypatch):
    monkeypatch.setenv("TZ", "Invalid/Zone")

    timezone = lbt.resolve_timezone()

    assert str(timezone) == "UTC"
