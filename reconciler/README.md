# OneLab Payments Reconciler

This project implements the reconciliation exercise described in [IMPLEMENTATION.md](../IMPLEMENTATION.md) using Python, FastAPI, pandas, and a lightweight HTML upload UI.

## Assumptions

- All amounts are in USD with 2 decimal places.
- `transaction_id` is the primary join key between transactions and settlements.
- Settlement batches may cover multiple transactions, but this exercise provides one settlement row per transaction.
- "Month end" is the calendar month boundary.
- Rounding differences are meaningful when they are greater than `$0.005`.
- Refunds are negative transactions with `type == "refund"`.
- If `ref_transaction_id` is missing, refund rows fall back to the spec's convention and compare their own `transaction_id` against original payments.

## Project Layout

```text
reconciler/
├── backend/
│   ├── api/
│   ├── data/
│   ├── engine/
│   ├── tests/
│   ├── gaps_report.json      # Generated after /report or /reconcile runs
│   └── requirements.txt
└── frontend/
    └── index.html
```

## What Is Included

- Seed CSV files with 50 clean transaction/settlement matches
- Exactly 4 planted anomalies in the sample data:
  - 1 late settlement across the Jan/Feb boundary
  - 1 rounding gap of `$0.01`
  - 1 duplicate transaction row with the same `transaction_id`
  - 1 orphan refund with no matching original transaction
- Reconciliation engine with five reported gap types:
  - `late_settlement`
  - `rounding_gap`
  - `duplicate`
  - `orphan_refund`
  - `unmatched_transaction`
- FastAPI endpoints for uploaded CSVs and the bundled sample report
- Drag-and-drop HTML UI
- Four pytest detector tests using inline DataFrames

## Run It

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn api.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000` in the browser.

## API

- `GET /` serves the browser UI
- `GET /report` runs reconciliation on the bundled CSV files in `backend/data/`
- `POST /reconcile` accepts `transactions` and `settlements` CSV uploads

Both report endpoints persist a JSON artifact to `backend/gaps_report.json`.

## Test

```bash
cd backend
python -m pytest tests/ -v
```

## Production Caveats

The matcher assumes `transaction_id` is a reliable join key, but real payment processors sometimes remap IDs during retries, causing false-positive "unmatched" flags. Rounding detection uses a fixed $0.01 threshold, which breaks for non-USD currencies with different decimal conventions (e.g. JPY has no sub-unit). The duplicate detector compares only the ID field, so a legitimate re-submission with a corrected amount would be silently missed and counted as a clean match.
