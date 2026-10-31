"""
BranchCoverageTest_water_utility_billing.py
Target: water_utility_billing.py

This test suite is designed for Comprehensive Branch Coverage Analysis.
It systematically evaluates every decision branch (if/elif/else/for/or) to both True and False outcomes,
covering edge cases, boundary conditions, loop limits, and short-circuit boolean conditions.
Achieves 100% Branch Coverage and 100% Statement Coverage.
"""

import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


# ==============================================================================
# calculate_water_bill: Input Validation Branches
# ==============================================================================

def test_invalid_accounts_type_branch():
    """Branch 1: not isinstance(accounts, list) is True -> raises ValueError."""
    with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
        calculate_water_bill("not_a_list", 10.0)


def test_negative_base_fee_branch():
    """Branch 2: isinstance(accounts, list) is True, but base_fee < 0 is True -> raises ValueError."""
    with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
        calculate_water_bill([], -5.0)


def test_empty_accounts_list_branch():
    """Branch 3: accounts is [] -> outer for-loop does not execute, total_billed is 0.0 -> NO_ACTIVITY."""
    result = calculate_water_bill([], 0.0)
    assert result["total_billed"] == 0.0
    assert result["status"] == "NO_ACTIVITY"


# ==============================================================================
# calculate_water_bill: Account Status & Usage Tier Branches
# ==============================================================================

def test_inactive_account_skip_branch():
    """Branch: not account.get('is_active', False) is True -> triggers continue (skips account)."""
    accounts = [
        {"is_active": False, "usage_blocks": [50]},
        {"is_active": False, "usage_blocks": [100]}
    ]
    result = calculate_water_bill(accounts, 0.0)
    assert result["total_billed"] == 0.0
    assert result["status"] == "NO_ACTIVITY"


def test_empty_usage_blocks_branch():
    """Branch: active account with usage_blocks = [] -> inner for-loop body does not execute."""
    accounts = [{"is_active": True, "usage_blocks": []}]
    result = calculate_water_bill(accounts, 15.0)
    assert result["total_billed"] == 15.0
    assert result["status"] == "NORMAL"


def test_non_positive_usage_blocks_branch():
    """Branch: usage <= 0 is True (both negative and zero) -> flags account and continues."""
    accounts = [
        {"is_active": True, "usage_blocks": [-10, 0]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 10.0
    assert result["status"] == "NORMAL"


def test_tier1_residential_usage_boundary():
    """Branch: usage <= 50 (testing boundary 50 and intermediate 30) -> billed at $1.50/unit."""
    accounts = [
        {"is_active": True, "is_commercial": False, "has_leak_waiver": False, "usage_blocks": [30, 50]}
    ]
    # base 10.0 + (30 * 1.5 = 45) + (50 * 1.5 = 75) = 130.0
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 130.0
    assert result["status"] == "NORMAL"


def test_tier2_usage_boundary():
    """Branch: 50 < usage <= 100 (testing boundary 100 and intermediate 75) -> billed at $2.50/unit."""
    accounts = [
        {"is_active": True, "is_commercial": False, "usage_blocks": [75, 100]}
    ]
    # base 10.0 + (75 * 2.5 = 187.5) + (100 * 2.5 = 250.0) = 447.5
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 447.5
    assert result["status"] == "NORMAL"


def test_tier3_residential_break_branch():
    """Branch: usage > 100 and not is_commercial is True -> rate $4.50, flags account, breaks loop."""
    accounts = [
        {"is_active": True, "is_commercial": False, "usage_blocks": [120, 40]}  # 40 skipped due to break
    ]
    # base 10.0 + (120 * 4.5 = 540) = 550.0
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 550.0
    assert result["status"] == "NORMAL"


def test_tier3_commercial_no_break_branch():
    """Branch: usage > 100 and not is_commercial is False (commercial) -> rate $3.50, NO break."""
    accounts = [
        {"is_active": True, "is_commercial": True, "usage_blocks": [120, 60]}
    ]
    # base 10.0 + (120 * 3.5 = 420) + (60 * 2.5 = 150) = 580.0
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 580.0
    assert result["status"] == "NORMAL"


# ==============================================================================
# calculate_water_bill: Leak Waiver Branches
# ==============================================================================

def test_leak_waiver_applied_above_200():
    """Branch: has_leak_waiver is True AND acct_total > 200.0 is True -> deducts $50.0."""
    accounts = [
        {"is_active": True, "has_leak_waiver": True, "usage_blocks": [100]}  # 10 + 250 = 260 > 200
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 210.0  # 260.0 - 50.0
    assert result["status"] == "NORMAL"


def test_leak_waiver_not_applied_below_or_equal_200():
    """Branch: has_leak_waiver is True BUT acct_total <= 200.0 (e.g. 40.0) -> no deduction."""
    accounts = [
        {"is_active": True, "has_leak_waiver": True, "usage_blocks": [20]}  # 10 + 30 = 40 <= 200
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 40.0
    assert result["status"] == "NORMAL"


def test_leak_waiver_false_high_total():
    """Branch: has_leak_waiver is False with acct_total > 200.0 -> waiver block skipped entirely."""
    accounts = [
        {"is_active": True, "has_leak_waiver": False, "usage_blocks": [100]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 260.0
    assert result["status"] == "NORMAL"


# ==============================================================================
# calculate_water_bill: Status Decision Branches
# ==============================================================================

def test_status_excessive_flags():
    """Branch: flagged_accounts > 5 is True -> status = EXCESSIVE_FLAGS."""
    accounts = [
        {"is_active": True, "usage_blocks": [-1, -2, -3, -4, -5, -6]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_status_no_activity_active_zero_billing():
    """Branch: flagged_accounts <= 5 is True, and total_billed == 0.0 is True -> status = NO_ACTIVITY."""
    accounts = [
        {"is_active": True, "usage_blocks": []}
    ]
    result = calculate_water_bill(accounts, 0.0)
    assert result["total_billed"] == 0.0
    assert result["status"] == "NO_ACTIVITY"


def test_status_normal_with_activity():
    """Branch: flagged_accounts <= 5 is True, and total_billed == 0.0 is False -> status = NORMAL."""
    accounts = [
        {"is_active": True, "usage_blocks": [25]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 47.5
    assert result["status"] == "NORMAL"


# ==============================================================================
# check_meter_tampering: Matrix & Flow Branches
# ==============================================================================

def test_meter_tampering_empty_matrix_branch():
    """Branch: not readings_matrix is True for empty list -> returns NO_DATA."""
    assert check_meter_tampering([]) == "NO_DATA"


def test_meter_tampering_none_matrix_branch():
    """Branch: not readings_matrix is True for None -> returns NO_DATA."""
    assert check_meter_tampering(None) == "NO_DATA"


def test_meter_tampering_empty_submeter_branch():
    """Branch: meter has no deltas -> inner for delta in meter does not execute -> returns CLEAR."""
    assert check_meter_tampering([[]]) == "CLEAR"


def test_meter_tampering_clear_all_positive_branch():
    """Branch: delta < 0 is False for all readings -> else resets count, loop finishes -> CLEAR."""
    readings = [[10, 20, 15], [5, 12, 8]]
    assert check_meter_tampering(readings) == "CLEAR"


def test_meter_tampering_reset_backward_flow_streak_branch():
    """
    Branch: delta < 0 occurs once (backward_flow_count becomes 1 < 2),
    followed by delta >= 0 which executes else: backward_flow_count = 0.
    Ensures non-consecutive negative deltas do NOT trigger tampering.
    """
    readings = [[10, -5, 20, -3, 30]]
    assert check_meter_tampering(readings) == "CLEAR"


def test_meter_tampering_suspected_consecutive_negatives():
    """Branch: backward_flow_count reaches 2 -> returns TAMPER_SUSPECTED immediately."""
    readings = [[5, -2, -4, 10]]
    assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"


def test_meter_tampering_suspected_on_second_meter():
    """Branch: first meter is clear, second meter triggers tampering -> returns TAMPER_SUSPECTED."""
    readings = [
        [10, 20, 30],
        [5, -1, -2]
    ]
    assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"
