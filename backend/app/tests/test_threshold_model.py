import pytest

from app.ml.threshold_model import (
    check_threshold_exceedance,
    ne_himalaya_moisture_threshold,
    sikkim_intensity_duration_threshold,
)


class TestNeHimalayaMoistureThreshold:
    def test_known_values(self):
        assert ne_himalaya_moisture_threshold(100) == pytest.approx(50.9, abs=0.1)
        assert ne_himalaya_moisture_threshold(50) == pytest.approx(19.9, abs=0.1)

    def test_boundary_25_hours(self):
        assert ne_himalaya_moisture_threshold(25) == pytest.approx(4.4, abs=0.1)

    def test_boundary_1439_hours(self):
        assert ne_himalaya_moisture_threshold(1439) == pytest.approx(881.08, abs=0.1)

    def test_below_24_raises(self):
        with pytest.raises(ValueError):
            ne_himalaya_moisture_threshold(24)

    def test_above_1440_raises(self):
        with pytest.raises(ValueError):
            ne_himalaya_moisture_threshold(1440)


class TestSikkimIntensityDurationThreshold:
    def test_known_values(self):
        assert sikkim_intensity_duration_threshold(1) == pytest.approx(43.26, abs=0.01)
        # 43.26 * 7^(-0.78) ≈ 9.48
        assert sikkim_intensity_duration_threshold(7) == pytest.approx(9.48, abs=0.01)

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            sikkim_intensity_duration_threshold(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            sikkim_intensity_duration_threshold(-1)


class TestCheckThresholdExceedance:
    def test_exceeds_ne_himalaya(self):
        result = check_threshold_exceedance(
            cumulative_rainfall_mm=60.0,
            duration_hours=100,
            region="ne_himalaya",
        )
        assert result["exceeded"] is True
        assert result["margin"] > 0

    def test_does_not_exceed_ne_himalaya(self):
        result = check_threshold_exceedance(
            cumulative_rainfall_mm=10.0,
            duration_hours=100,
            region="ne_himalaya",
        )
        assert result["exceeded"] is False
        assert result["margin"] < 0

    def test_exceeds_sikkim(self):
        result = check_threshold_exceedance(
            cumulative_rainfall_mm=50.0,
            duration_hours=24,
            region="sikkim",
        )
        assert result["exceeded"] is True

    def test_unknown_region_raises(self):
        with pytest.raises(ValueError):
            check_threshold_exceedance(50.0, 24, region="unknown")
