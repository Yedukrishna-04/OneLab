import pandas as pd
import pytest

from engine.detectors import (
    detect_duplicates,
    detect_late_settlements,
    detect_orphan_refunds,
    detect_rounding_gaps,
)


def test_late_settlement() -> None:
    txns = pd.DataFrame(
        [
            {
                "transaction_id": "txn_1",
                "customer_id": "cust_1",
                "amount": 100.00,
                "currency": "USD",
                "created_at": "2024-01-30",
                "status": "captured",
                "type": "payment",
            }
        ]
    )
    stls = pd.DataFrame(
        [
            {
                "settlement_id": "stl_1",
                "transaction_id": "txn_1",
                "settled_amount": 100.00,
                "settled_at": "2024-02-02",
                "bank_reference": "bank_1",
            }
        ]
    )

    txns["created_at"] = pd.to_datetime(txns["created_at"])
    stls["settled_at"] = pd.to_datetime(stls["settled_at"])

    result = detect_late_settlements(txns, stls)

    assert len(result) == 1
    assert result.iloc[0]["gap_type"] == "late_settlement"


def test_rounding_gap() -> None:
    txns = pd.DataFrame(
        [
            {
                "transaction_id": "txn_2",
                "customer_id": "cust_2",
                "amount": 100.00,
                "currency": "USD",
                "created_at": "2024-01-12",
                "status": "captured",
                "type": "payment",
            }
        ]
    )
    stls = pd.DataFrame(
        [
            {
                "settlement_id": "stl_2",
                "transaction_id": "txn_2",
                "settled_amount": 99.99,
                "settled_at": "2024-01-13",
                "bank_reference": "bank_2",
            }
        ]
    )

    txns["created_at"] = pd.to_datetime(txns["created_at"])
    stls["settled_at"] = pd.to_datetime(stls["settled_at"])

    result = detect_rounding_gaps(txns, stls)

    assert len(result) == 1
    assert result.iloc[0]["gap_type"] == "rounding_gap"
    assert result.iloc[0]["amount_diff"] == pytest.approx(0.01)


def test_duplicate_transaction() -> None:
    txns = pd.DataFrame(
        [
            {
                "transaction_id": "dup_1",
                "customer_id": "cust_3",
                "amount": 42.50,
                "currency": "USD",
                "created_at": "2024-01-15",
                "status": "captured",
                "type": "payment",
            },
            {
                "transaction_id": "dup_1",
                "customer_id": "cust_3",
                "amount": 42.50,
                "currency": "USD",
                "created_at": "2024-01-15",
                "status": "captured",
                "type": "payment",
            },
        ]
    )

    txns["created_at"] = pd.to_datetime(txns["created_at"])
    result = detect_duplicates(txns)

    assert len(result) == 2
    assert set(result["gap_type"]) == {"duplicate"}


def test_orphan_refund() -> None:
    txns = pd.DataFrame(
        [
            {
                "transaction_id": "sale_1",
                "customer_id": "cust_4",
                "amount": 72.00,
                "currency": "USD",
                "created_at": "2024-01-18",
                "status": "captured",
                "type": "payment",
            },
            {
                "transaction_id": "refund_missing_1",
                "customer_id": "cust_4",
                "amount": -72.00,
                "currency": "USD",
                "created_at": "2024-01-19",
                "status": "posted",
                "type": "refund",
            },
        ]
    )

    txns["created_at"] = pd.to_datetime(txns["created_at"])
    result = detect_orphan_refunds(txns)

    assert len(result) == 1
    assert result.iloc[0]["gap_type"] == "orphan_refund"
