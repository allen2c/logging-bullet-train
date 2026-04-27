import logging_bullet_train as lbt


def test_resolve_timezone_uses_tz_env(monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Taipei")

    timezone = lbt.resolve_timezone()

    assert str(timezone) == "Asia/Taipei"
