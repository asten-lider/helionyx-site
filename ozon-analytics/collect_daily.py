import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from ozon_client import post

OUT = Path("data")
OUT.mkdir(exist_ok=True)

def iso(dt):
    return dt.isoformat().replace("+00:00", "Z")

def collect_fbo(since, to):
    cursor = ""
    result = []
    while True:
        data = post("/v3/posting/fbo/list", {
            "cursor": cursor,
            "filter": {"since": iso(since), "to": iso(to)},
            "limit": 1000,
            "sort_dir": "asc",
            "with": {
                "analytics_data": True,
                "financial_data": True,
                "legal_info": False
            },
        })
        block = data.get("result", {})
        postings = block.get("postings", [])
        result.extend(postings)
        cursor = block.get("cursor", "")
        if not postings or not cursor or block.get("has_next") is False:
            break
    return result

def collect_fbs(since, to):
    cursor = ""
    result = []
    while True:
        payload = {
            "filter": {"since": iso(since), "to": iso(to)},
            "limit": 1000,
            "sort_dir": "asc",
            "with": {
                "analytics_data": True,
                "barcodes": False,
                "financial_data": True,
                "legal_info": False
            }
        }
        if cursor:
            payload["cursor"] = cursor
        data = post("/v4/posting/fbs/list", payload)
        postings = data.get("postings", [])
        result.extend(postings)
        new_cursor = data.get("cursor", "")
        if not postings or not new_cursor or not data.get("has_next", False):
            break
        cursor = new_cursor
    return result

def collect_finance(day):
    last_id = ""
    result = []
    while True:
        data = post("/v1/finance/accrual/by-day", {
            "date": day.isoformat(),
            "last_id": last_id
        })
        rows = data.get("accruals", [])
        result.extend(rows)
        new_last = data.get("last_id") or ""
        if not rows or not new_last or new_last == last_id:
            break
        last_id = new_last
    return result

def collect_stocks():
    cursor = ""
    result = []
    while True:
        payload = {"limit": 1000, "filter": {"visibility": "ALL"}}
        if cursor:
            payload["cursor"] = cursor
        data = post("/v4/product/info/stocks", payload)
        items = data.get("items") or data.get("result", {}).get("items") or []
        result.extend(items)
        new_cursor = data.get("cursor") or data.get("result", {}).get("cursor") or ""
        if not items or not new_cursor or new_cursor == cursor:
            break
        cursor = new_cursor
    return result

def save(name, obj):
    (OUT / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(name, len(obj) if isinstance(obj, list) else "")

today = datetime.now(timezone.utc).date()
since = datetime.combine(today - timedelta(days=3), datetime.min.time(), tzinfo=timezone.utc)
to = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc)

save("fbo.json", collect_fbo(since, to))
save("fbs.json", collect_fbs(since, to))
save("finance.json", collect_finance(today - timedelta(days=1)))
save("stocks.json", collect_stocks())
save("manifest.json", {
    "collected_at_utc": datetime.now(timezone.utc).isoformat(),
    "orders_window_start": iso(since),
    "orders_window_end": iso(to),
    "finance_date": (today - timedelta(days=1)).isoformat()
})
