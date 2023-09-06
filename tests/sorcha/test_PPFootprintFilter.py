import numpy as np
import pandas as pd
from numpy.testing import assert_equal, assert_almost_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.modules.PPFootprintFilter import Detector


def dummy_detector():
    # making a square, 0.01 radians a side, bottom left corner at origin.
    # as it's quite small, projection onto focal plane causes minimal distortion (easier to test)
    # previous tests used a 1rad x 1rad unit square, which does not work well.
    return Detector(np.array(((0, 0.01, 0.01, 0), (0, 0, 0.01, 0.01))))


def test_ison():
    detector = dummy_detector()
    assert detector.units == "radians"

    points = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])
    points_ison = detector.ison(points)

    assert points_ison.shape == (10,)
    assert_equal(points_ison, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

    # Test with points where we have manually computed the distances.
    # Point locations are specified in radians.
    points = np.array(
        [
            [-0.01, 0.0],  # out
            [0.0, -0.01],  # out
            [0.005, 0.005],  # in
            [0.001, 0.005],  # in, but close to left edge
            [0.002, 0.002],  # in
            [0.008, 0.015],  # out
            [0.011, 0.005],  # out
            [0.005, 0.010],  # in, on top edge
            [0.015, 0.015],  # out
            [0.004, 0.006],  # in
            [0.006, 0.004],  # in
            [0.005, 0.001],  # in, but close to bottom edge
            [0.009, 0.005],  # in, but close to right edge
            [-0.015, 0.015],  # out
        ]
    ).T

    idx1 = detector.ison(points)
    assert idx1.tolist() == [2, 3, 4, 7, 9, 10, 11, 12]

    # Check with distance of 0.0015 radians (specified in arcseconds).
    idx2 = detector.ison(points, edge_thresh=(np.degrees(0.0015) * 3600))
    assert idx2.tolist() == [2, 4, 9, 10]

    # Check with distance of 0.000015 radians (specified in arcseconds).
    idx3 = detector.ison(points, edge_thresh=(np.degrees(0.000015) * 3600))
    assert idx3.tolist() == [2, 3, 4, 9, 10, 11, 12]

    # Math should hold if the detector is in degrees. Uses the same thresholds.
    detector.rad2deg()
    assert detector.units == "degrees"
    points_deg = np.degrees(points)

    idx1 = detector.ison(points_deg)
    assert idx1.tolist() == [2, 3, 4, 7, 9, 10, 11, 12]

    idx2 = detector.ison(points_deg, edge_thresh=(np.degrees(0.0015) * 3600))
    assert idx2.tolist() == [2, 4, 9, 10]

    idx3 = detector.ison(points_deg, edge_thresh=(np.degrees(0.000015) * 3600))
    assert idx3.tolist() == [2, 3, 4, 9, 10, 11, 12]


def test_areas():
    from sorcha.modules.PPFootprintFilter import radec2focalplane

    detector = dummy_detector()
    pointsin = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])
    pointsout = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)]) + 1

    for p in pointsin.T:
        pi = np.array(radec2focalplane(p[0], p[1], 0, 0))
        assert (
            np.abs(detector.segmentedArea(pi) - detector.trueArea()) < 1e-12
        )  # these are stricter tolerances than currently demanded in current use
    for p in pointsout.T:
        pi = np.array(radec2focalplane(p[0], p[1], 0, 0))
        assert np.abs(detector.segmentedArea(pi) - detector.trueArea()) > 1e-12


def test_trueArea():
    detector = dummy_detector()
    assert_almost_equal(detector.trueArea(), 0.0001, decimal=6)


def test_segmentedArea():
    detector = dummy_detector()

    points = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])

    for p in points.T:
        assert_almost_equal(0.0001, detector.segmentedArea(p), decimal=6)


def test_sortCorners():
    # have to rearrange the points for this one
    test_detector = Detector(np.array(((0.01, 0.01, 0, 0), (0, 0.01, 0.01, 0))))
    test_detector.sortCorners()

    assert_almost_equal(test_detector.x, np.array([0.0, 0.01, 0.01, 0.0]), decimal=5)
    assert_almost_equal(test_detector.y, np.array([0.0, 0.0, 0.01, 0.01]), decimal=5)


def test_rotateDetector():
    detector = dummy_detector()
    detector_360 = detector.rotateDetector(2.0 * np.pi)

    assert_almost_equal(detector_360.x, detector.x, decimal=5)
    assert_almost_equal(detector_360.y, detector.y, decimal=5)

    detector_180 = detector.rotateDetector(np.pi)

    assert_almost_equal(detector_180.x, [0, -0.01, -0.01, 0], decimal=5)
    assert_almost_equal(detector_180.y, [0.0, 0.0, -0.01, -0.01], decimal=5)


def test_rad2deg_deg2rad():
    detector = dummy_detector()

    original_x = detector.x
    original_y = detector.y

    detector.rad2deg()

    degx_expected = np.array([0.0, 0.57297689, 0.57297689, 0.0])
    degy_expected = np.array([0.0, 0.0, 0.57300554, 0.57297689])

    assert_almost_equal(detector.x, degx_expected)
    assert_almost_equal(detector.y, degy_expected)

    detector.deg2rad()

    assert_almost_equal(detector.x, original_x)
    assert_almost_equal(detector.y, original_y)


def test_plots():
    from sorcha.modules.PPFootprintFilter import Footprint

    detector = dummy_detector()
    detector.plot()

    footprintf = Footprint(get_test_filepath("detectors_corners.csv"))
    footprintf.plot()


def test_radec2focalplane():
    from sorcha.modules.PPFootprintFilter import radec2focalplane

    out = radec2focalplane(1.0, 1.0, 0.0, 0.0)
    out_expected = (1.5574077, 2.8824746)

    assert len(out) == 2
    assert_almost_equal(out, out_expected, decimal=6)


def test_applyFootprint():
    from sorcha.modules.PPFootprintFilter import Footprint

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=10)

    # No edge threshold. Keep all points anywhere on a detector.
    footprintf = Footprint(get_test_filepath("detectors_corners.csv"))
    onSensor, detectorIDs = footprintf.applyFootprint(observations)

    assert_equal(onSensor, [1, 0, 2, 3, 8, 7, 4, 5, 6, 9])
    assert_equal(detectorIDs, [59.0, 66.0, 87.0, 87.0, 100.0, 106.0, 127.0, 131.0, 144.0, 152.0])

    # Setting an edge threshold to 0.0005 radians will further filter points 0, 7, 8, and 9.
    onSensor, detectorIDs = footprintf.applyFootprint(
        observations,
        edge_thresh=(np.degrees(0.0005) * 3600),  # as arcseconds
    )

    assert_equal(onSensor, [1, 2, 3, 4, 5, 6])
    assert_equal(detectorIDs, [59.0, 87.0, 87.0, 127.0, 131.0, 144.0])


def test_distToSegment():
    from sorcha.modules.PPFootprintFilter import distToSegment

    points = np.array([[0.0, 0.0], [0.5, 0.0], [0.0, 0.5], [1.0, 1.0], [0.8, 0.2]]).T

    # Vertical line from (0.8, 0.1) to (0.8, 0.9)
    dists = distToSegment(points, 0.8, 0.1, 0.8, 0.9)
    assert np.allclose(dists, [0.8062258, 0.3162278, 0.8, 0.2236068, 0.0])

    # Horizontal line from (0.0, 1.0) to (0.2, 1.0)
    dists = distToSegment(points, 0.0, 1.0, 0.2, 1.0)
    assert np.allclose(dists, [1.0, 1.044030, 0.5, 0.8, 1.0])

    # Line (0.0, 0.0) to (0.8, 0.8).
    dists = distToSegment(points, 0.0, 0.0, 0.8, 0.8)
    assert np.allclose(dists, [0.0, 0.3535534, 0.3535534, 0.2828427, 0.4242641])

    # Line (0.2, 0.6) to (0.6, 0.2).
    dists = distToSegment(points, 0.2, 0.6, 0.6, 0.2)
    assert np.allclose(dists, [0.5656854, 0.2236068, 0.2236068, 0.8485282, 0.2])

    # A point at (0.5, 0.5)
    dists = distToSegment(points, 0.5, 0.5, 0.5, 0.5)
    assert np.allclose(dists, [0.7071068, 0.5, 0.5, 0.7071068, 0.4242641])
