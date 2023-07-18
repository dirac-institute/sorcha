import pandas as pd


def test_calcDetectionProbability():
    # Test caclDetetcionProbabilty function

    from sorcha.modules.PPDetectionProbability import calcDetectionProbability

    mag = 21.9
    limmag = 22.0

    nominal_result = 0.7310585786300077

    result = calcDetectionProbability(mag, limmag)

    assert result == nominal_result


def test_PPDetectionProbabilty():
    from sorcha.modules.PPDetectionProbability import PPDetectionProbability

    test_in = pd.DataFrame(
        {"FieldID": [0, 0], "MagnitudeInFilter": [21.9, 21.9], "fiveSigmaDepth": [22.0, 22.0]}
    )

    test_target = pd.DataFrame(
        {
            "FieldID": [0, 0],
            "MagnitudeInFilter": [21.9, 21.9],
            "detection_probability": [0.7310585786300077, 0.7310585786300077],
        }
    )

    test_out = test_in.copy()
    test_out["detection_probability"] = PPDetectionProbability(
        oif_df=test_in, magnitude_name="MagnitudeInFilter", limiting_magnitude_name="fiveSigmaDepth"
    )

    assert test_out["detection_probability"][0] == test_target["detection_probability"][0]
    return
