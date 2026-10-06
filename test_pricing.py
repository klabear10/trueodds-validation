from trueodds.pricing import (
    american_to_decimal,
    break_even_probability,
    expected_value,
    remove_two_way_vig,
)


def test_positive_american_odds():
    assert american_to_decimal(120) == 2.2


def test_negative_american_odds():
    assert round(american_to_decimal(-110), 6) == round(1 + 100 / 110, 6)


def test_break_even_plus_120():
    assert round(break_even_probability(120), 6) == round(1 / 2.2, 6)


def test_ev():
    assert round(expected_value(0.50, 120), 6) == 0.10


def test_vig_removal_sums_to_one():
    a, b = remove_two_way_vig(-110, -110)
    assert round(a + b, 12) == 1.0
    assert round(a, 6) == 0.5
