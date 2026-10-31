"""
CodeCoverageTest_water_utility_billing.py
Target: water_utility_billing.py

This test suite is designed for Code Coverage Analysis (Statement / Line Coverage).
It exercises every executable statement across calculate_water_bill and check_meter_tampering,
achieving 100% statement (line) coverage (>90% requirement).
"""

import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


def test_single_active_residential():
    """Test standard residential account within tier 1 usage (<= 50 units)."""
    accounts = [
        {
            "is_active": True,
            "is_commercial": False,
            "has_leak_waiver": False,
            "usage_blocks": [30]
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 55.0  # 10.0 + (30 * 1.5)
    assert result["status"] == "NORMAL"


def test_invalid_accounts_type():
    """Test line 2-3: non-list accounts raises ValueError."""
    with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
        calculate_water_bill("invalid_type", 10.0)


def test_inactive_account_and_no_activity():
    """Test line 9-10 (continue on inactive) and lines 41-42 (status NO_ACTIVITY)."""
    accounts = [
        {
            "is_active": False,
            "usage_blocks": [50]
        }
    ]
    result = calculate_water_bill(accounts, 0.0)
    assert result["total_billed"] == 0.0
    assert result["status"] == "NO_ACTIVITY"


def test_residential_tier2_usage():
    """Test lines 27-28: usage between 51 and 100 units billed at $2.50/unit."""
    accounts = [
        {
            "is_active": True,
            "is_commercial": False,
            "usage_blocks": [75]
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 197.5  # 10.0 + (75 * 2.5)
    assert result["status"] == "NORMAL"


def test_residential_tier3_break():
    """Test lines 21-25: usage > 100 for residential account billed at $4.50 and breaks."""
    accounts = [
        {
            "is_active": True,
            "is_commercial": False,
            "usage_blocks": [120, 30]  # 30 should not be processed due to break
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 550.0  # 10.0 + (120 * 4.5)
    assert result["status"] == "NORMAL"


def test_commercial_tier3():
    """Test line 26: usage > 100 for commercial account billed at $3.50/unit."""
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "usage_blocks": [120]
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 430.0  # 10.0 + (120 * 3.5)
    assert result["status"] == "NORMAL"


def test_non_positive_usage():
    """Test lines 17-19: non-positive usage values are flagged and skipped."""
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [-5, 0]
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 10.0
    assert result["status"] == "NORMAL"


def test_leak_waiver_applied():
    """Test lines 32-34: leak waiver applies $50 deduction when acct_total > 200.0."""
    accounts = [
        {
            "is_active": True,
            "has_leak_waiver": True,
            "usage_blocks": [100]  # 100 * 2.5 = 250, acct_total = 260 > 200
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 210.0  # 260.0 - 50.0
    assert result["status"] == "NORMAL"


def test_excessive_flags_status():
    """Test lines 39-40: more than 5 flagged accounts triggers EXCESSIVE_FLAGS status."""
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [-1, -2, -3, -4, -5, -6]  # 6 non-positive usages
        }
    ]
    result = calculate_water_bill(accounts, 10.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_tampering_no_data():
    """Test lines 48-49: empty readings matrix returns NO_DATA."""
    assert check_meter_tampering([]) == "NO_DATA"


def test_tampering_clear():
    """Test lines 51-54, 58-60: all non-negative readings returns CLEAR."""
    readings = [[10, 20, 30]]
    assert check_meter_tampering(readings) == "CLEAR"


def test_tampering_suspected():
    """Test lines 54-57: two consecutive backward flow readings triggers TAMPER_SUSPECTED."""
    readings = [[-5, -10]]
    assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"
