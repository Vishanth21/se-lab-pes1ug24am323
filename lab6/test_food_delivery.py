import pytest

from food_delivery import apply_coupon, delivery_charge, estimated_time


# Example test cases:
def test_nearby_small_order():
    assert delivery_charge(2, 200, False) == 20


def test_no_coupon():
    assert apply_coupon(300, None, False) == 300


# delivery_charge


def test_distance_based_charge():
    # <= 3 km
    assert delivery_charge(1, 100, False) == 20
    assert delivery_charge(3, 100, False) == 20
    # <= 8 km
    assert delivery_charge(4, 100, False) == 40
    assert delivery_charge(8, 100, False) == 40
    # > 8 km
    assert delivery_charge(9, 100, False) == 60
    assert delivery_charge(15, 100, False) == 60


def test_free_delivery_for_large_orders():
    # order_value >= 500 -> base charge is 0, distance is irrelevant
    assert delivery_charge(2, 500, False) == 0
    assert delivery_charge(7, 500, False) == 0
    assert delivery_charge(9, 500, False) == 0
    assert delivery_charge(15, 600, False) == 0


def test_rain_surcharge():
    assert delivery_charge(2, 100, True) == 50
    assert delivery_charge(7, 100, True) == 70
    assert delivery_charge(9, 100, True) == 90
    # rain surcharge also applies to free-delivery orders
    assert delivery_charge(2, 500, True) == 30


def test_delivery_out_of_range():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(0, 100, False)
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(-1, 100, False)
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(16, 100, False)


# apply_coupon


def test_no_coupon_returns_original_value():
    assert apply_coupon(300, None, False) == 300
    assert apply_coupon(100, None, True) == 100


def test_valid_coupons():
    assert apply_coupon(300, "SAVE50", False) == 250
    assert apply_coupon(300, "WELCOME", True) == 200


def test_invalid_coupon():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "FREEFOOD", False)


def test_welcome_only_for_first_order():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(300, "WELCOME", False)
    # SAVE50 has no first-order restriction
    assert apply_coupon(300, "SAVE50", False) == 250


def test_coupon_ignored_below_minimum_order():
    assert apply_coupon(150, "SAVE50", False) == 150
    assert apply_coupon(199, "WELCOME", True) == 199


# estimated_time


def test_base_estimated_time():
    # 15 + 2 * 4
    assert estimated_time(2, False, False) == 23


def test_estimated_time_peak_hour():
    # 15 + 2 * 4 + 10
    assert estimated_time(2, True, False) == 33


def test_estimated_time_busy_restaurant():
    # 15 + 2 * 4 + 15
    assert estimated_time(2, False, True) == 38


def test_estimated_time_peak_and_busy():
    # 15 + 2 * 4 + 10 + 15 + 5
    assert estimated_time(2, True, True) == 53