# L6_L7_01 — Water Utility Billing

Lab 6: Code and Branch Coverage Analysis

## About

A Python module that computes tiered water billing by customer type, handles usage blocks and leak-waiver deductions, and detects meter tampering via backflow sensor readings.

## Deliverables Summary

| File | Description | Coverage Target |
|---|---|---|
| [`water_utility_billing.py`](file:///Lab%206/water_utility_billing.py) | Application module under test | Source code |
| [`CodeCoverageTest_water_utility_billing.py`](file:///Lab%206/CodeCoverageTest_water_utility_billing.py) | Test cases targeting Line / Statement Coverage | **100% Code Coverage** (>90% requirement) |
| [`BranchCoverageTest_water_utility_billing.py`](file:///Lab%206/BranchCoverageTest_water_utility_billing.py) | Test cases targeting Branch Coverage | **100% Branch Coverage** (>90% requirement) |
| [`test_water_utility.py`](file:///Lab%206/test_water_utility.py) | Standard test discovery entry point running all test cases | **100% Statement & Branch Coverage** |
| [`CodeCoverage_Screenshot.png`](file:///Lab%206/CodeCoverage_Screenshot.png) | Terminal output screenshot for Code Coverage analysis | Visual verification |
| [`BranchCoverage_Screenshot.png`](file:///Lab%206/BranchCoverage_Screenshot.png) | Terminal output screenshot for Branch Coverage analysis | Visual verification |
| [`REPORT.md`](file:///Lab%206/REPORT.md) | Comprehensive Code & Branch Coverage Report | Technical analysis & rubric documentation |

---

## Running Coverage Commands

### 1. Code Coverage (Statement Coverage)
```bash
coverage run -m pytest CodeCoverageTest_water_utility_billing.py
coverage report -m
```

### 2. Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_water_utility_billing.py
coverage report -m
```

### 3. General Pytest Run
```bash
pytest -v
```

---

## Evaluation Rubric Compliance

- **Code Coverage analysis & report (2 marks):** Documented in `REPORT.md` and captured in `CodeCoverage_Screenshot.png`.
- **Branch Coverage analysis & report (2 marks):** Documented in `REPORT.md` with branch decision matrix and captured in `BranchCoverage_Screenshot.png`.
- **Commits and Testcases (>90% Coverage) (6 marks):** 2 separate commits milestone verifying >90% (achieved 100%) coverage on both metrics with passing test suites.
