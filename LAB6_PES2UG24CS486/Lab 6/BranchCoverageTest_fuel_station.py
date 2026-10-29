
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# Fuel bill: validation and voucher coverage
def test_invalid_fuel_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 20, "silver")


def test_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_regular_silver_within_coverage():
    assert fuel_bill("regular", 10, "silver") == 0


def test_regular_gold_within_extended_coverage():
    assert fuel_bill("regular", 15, "gold") == 0


def test_regular_gold_extra_litres():
    assert fuel_bill("regular", 20, "gold") == 525


def test_premium_silver_extra_litres():
    assert fuel_bill("premium", 20, "silver") == 525


def test_diesel_gold_uses_standard_diesel_coverage():
    assert fuel_bill("diesel", 25, "gold") == 450


def test_diesel_silver_extra_litres():
    assert fuel_bill("diesel", 30, "silver") == 900


def test_extra_exactly_30_litres():
    assert fuel_bill("regular", 40, "silver") == 3150


def test_extra_more_than_30_litres_silver():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_extra_more_than_30_litres_gold():
    assert fuel_bill("regular", 50, "gold") == 3325


# Pump permission: fleet and non-fleet decisions
def test_fleet_at_limit():
    assert pump_allowed(200, 3, True) is True


def test_fleet_over_limit():
    assert pump_allowed(201, 3, True) is False


def test_non_fleet_at_litre_limit():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_over_litre_limit():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_one_container():
    assert pump_allowed(30, 1, False) is True


def test_non_fleet_multiple_containers():
    assert pump_allowed(30, 2, False) is False


# Session status: payment type, night mode and cutoff boundaries
def test_card_day_active():
    assert session_status(60, True, False) == "active"


def test_card_day_warning_boundary():
    assert session_status(45, True, False) == "warning"


def test_card_day_timed_out():
    assert session_status(44, True, False) == "timed_out"


def test_card_night_active():
    assert session_status(90, True, True) == "active"


def test_card_night_warning():
    assert session_status(75, True, True) == "warning"


def test_card_night_timed_out():
    assert session_status(74, True, True) == "timed_out"


def test_cash_day_active():
    assert session_status(30, False, False) == "active"


def test_cash_day_warning():
    assert session_status(15, False, False) == "warning"


def test_cash_day_timed_out():
    assert session_status(14, False, False) == "timed_out"


def test_cash_night_active():
    assert session_status(60, False, True) == "active"


def test_cash_night_warning():
    assert session_status(45, False, True) == "warning"


def test_cash_night_timed_out():
    assert session_status(44, False, True) == "timed_out"
