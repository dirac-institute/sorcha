from sorcha.lightcurves.lightcurve_registration import LC_METHODS


def test_send_error_message():
    identity_activity = LC_METHODS["identity"]()
    identity_activity._log_error_message("Test error")


def test_sent_exception():
    identity_activity = LC_METHODS["identity"]()
    identity_activity._log_error_message(KeyError("Test key error"))
