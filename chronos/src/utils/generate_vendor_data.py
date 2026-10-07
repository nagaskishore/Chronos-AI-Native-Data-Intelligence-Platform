import json
import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Created: {path}")


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {path}")


# ---------------------------------------------------------
# Vendor A - JSON
# Version 1
# ---------------------------------------------------------

vendor_a_v1 = [
    {
        "vendor_record_id": "A-1001",
        "ticker": "AAPL",
        "event_date": "2026-01-05",
        "revenue": 125000,
        "currency": "USD",
        "status": "ACTIVE"
    },
    {
        "vendor_record_id": "A-1002",
        "ticker": "MSFT",
        "event_date": "2026-01-05",
        "revenue": 142000,
        "currency": "USD",
        "status": "ACTIVE"
    },
    {
        "vendor_record_id": "A-1003",
        "ticker": "GOOGL",
        "event_date": "2026-01-05",
        "revenue": 118000,
        "currency": "USD",
        "status": "ACTIVE"
    },
    {
        "vendor_record_id": "A-1004",
        "ticker": "AAPL",
        "event_date": "2026-01-06",
        "revenue": 127500,
        "currency": "USD",
        "status": "ACTIVE"
    }
]


# ---------------------------------------------------------
# Vendor A - JSON
# Version 2
#
# Schema evolution:
# event_date -> eventDate
# revenue -> revenue_amount
# status added/changed
# ---------------------------------------------------------

vendor_a_v2 = [
    {
        "vendor_record_id": "A-1005",
        "ticker": "MSFT",
        "eventDate": "2026/01/06",
        "revenue_amount": 145000,
        "currency": "USD",
        "status": "ACTIVE"
    },
    {
        "vendor_record_id": "A-1006",
        "ticker": "GOOGL",
        "eventDate": "2026/01/06",
        "revenue_amount": 121000,
        "currency": "USD",
        "status": "ACTIVE"
    },
    {
        "vendor_record_id": "A-1007",
        "ticker": "AAPL",
        "eventDate": "2026/01/07",
        "revenue_amount": 130000,
        "currency": "USD",
        "status": "UPDATED"
    }
]


# ---------------------------------------------------------
# Vendor B - CSV
#
# Different naming convention:
# security -> ticker
# trade_date -> event_date
# amount -> revenue
# ---------------------------------------------------------

vendor_b_rows = [
    {
        "record_id": "B-2001",
        "security": "AAPL",
        "trade_date": "01-05-2026",
        "amount": "124500",
        "ccy": "USD"
    },
    {
        "record_id": "B-2002",
        "security": "MSFT",
        "trade_date": "01-05-2026",
        "amount": "141500",
        "ccy": "USD"
    },
    {
        "record_id": "B-2003",
        "security": "GOOGL",
        "trade_date": "01-05-2026",
        "amount": "117500",
        "ccy": "USD"
    },
    {
        "record_id": "B-2004",
        "security": "AAPL",
        "trade_date": "01-06-2026",
        "amount": "127000",
        "ccy": "USD"
    },
    {
        # Intentional duplicate
        "record_id": "B-2004",
        "security": "AAPL",
        "trade_date": "01-06-2026",
        "amount": "127000",
        "ccy": "USD"
    }
]

vendor_b_fields = [
    "record_id",
    "security",
    "trade_date",
    "amount",
    "ccy"
]


# ---------------------------------------------------------
# Vendor C - JSON
#
# Different identifier convention
# Different date format
# Different amount representation
# ---------------------------------------------------------

vendor_c = [
    {
        "id": "C-3001",
        "symbol": "AAPL",
        "business_date": "2026-01-05T00:00:00Z",
        "value": 126000,
        "currency_code": "USD"
    },
    {
        "id": "C-3002",
        "symbol": "MSFT",
        "business_date": "2026-01-05T00:00:00Z",
        "value": 143000,
        "currency_code": "USD"
    },
    {
        "id": "C-3003",
        "symbol": "GOOGL",
        "business_date": "2026-01-05T00:00:00Z",
        "value": 119000,
        "currency_code": "USD"
    },
    {
        "id": "C-3004",
        "symbol": "AAPL",
        "business_date": "2026-01-06T00:00:00Z",
        "value": 127500,
        "currency_code": "USD"
    }
]


# ---------------------------------------------------------
# Write files
# ---------------------------------------------------------

write_json(
    DATA_DIR / "vendor_a" / "vendor_a_v1.json",
    vendor_a_v1
)

write_json(
    DATA_DIR / "vendor_a" / "vendor_a_v2.json",
    vendor_a_v2
)

write_csv(
    DATA_DIR / "vendor_b" / "vendor_b.csv",
    vendor_b_rows,
    vendor_b_fields
)

write_json(
    DATA_DIR / "vendor_c" / "vendor_c.json",
    vendor_c
)


print("\nVendor data generation completed.")