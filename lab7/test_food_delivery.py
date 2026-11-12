from hypothesis import given
from hypothesis import strategies as st

from food_delivery import coupon_discount, delivery_eta, parse_order


@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e}"


@given(st.text() | st.none())
def test_delivery_eta_no_crash(s):
    try:
        delivery_eta(s)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e}"


@given(st.text() | st.none())
def test_coupon_discount_no_crash(s):
    try:
        coupon_discount(s)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e}"
