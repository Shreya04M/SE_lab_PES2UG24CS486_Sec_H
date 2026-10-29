import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# Fuel bill tests
def test_unknown_fuel_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 20, "silver")


def test_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_litres_within_voucher_coverage():
    assert fuel_bill("regular", 8, "silver") == 0


def test_gold_member_extra_litres():
    assert fuel_bill("regular", 20, "gold") == 5 * 105


def test_diesel_extra_litres():
    assert fuel_bill("diesel", 25, "silver") == 5 * 90


def test_regular_fuel_extra_litres_under_30():
    assert fuel_bill("regular", 20, "silver") == 10 * 105


def test_gold_member_large_fuel_bill():
    assert fuel_bill("regular", 50, "gold") == 35 * 95


# Pump permission tests
def test_fleet_request_allowed():
    assert pump_allowed(100, 3, True) is True


def test_fleet_request_exceeds_limit():
    assert pump_allowed(201, 3, True) is False


def test_non_fleet_request_exceeds_limit():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_single_container_allowed():
    assert pump_allowed(30, 1, False) is True


def test_non_fleet_multiple_containers_denied():
    assert pump_allowed(30, 2, False) is False


# Pump session status tests
def test_card_payment_active():
    assert session_status(60, True, False) == "active"


def test_card_payment_warning():
    assert session_status(45, True, False) == "warning"


def test_card_payment_timed_out():
    assert session_status(44, True, False) == "timed_out"


def test_cash_payment_active_at_night():
    assert session_status(60, False, True) == "active"


def test_cash_payment_warning_during_day():
    assert session_status(20, False, False) == "warning"


def test_cash_payment_timed_out_during_day():
    assert session_status(14, False, False) == "timed_out"