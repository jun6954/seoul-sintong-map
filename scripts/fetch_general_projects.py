#!/usr/bin/env python3
"""Fetch all Seoul business-search categories from Seoul's official cleanup site."""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import logging
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "general-projects.json"
LOG = ROOT / "logs" / "redevelopment-sync.log"
ENDPOINT = "https://cleanup.seoul.go.kr/cleanup/bsnssttus/lsubBsnsSttus.do"
SOURCE = "https://cleanup.seoul.go.kr/cleanup/bsnssttus/lscrMainIndx.do"
URBAN_POPUP = "https://urban.seoul.go.kr/view/map/mapPopup.html?recordCode={}"
URBAN_GEOMETRY = "https://urban.seoul.go.kr/api/map/pilji/getUpis.json"
TO_WGS84 = Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)
GU_CODES = {
    "11110": "종로구", "11140": "중구", "11170": "용산구", "11200": "성동구",
    "11215": "광진구", "11230": "동대문구", "11260": "중랑구", "11290": "성북구",
    "11305": "강북구", "11320": "도봉구", "11350": "노원구", "11380": "은평구",
    "11410": "서대문구", "11440": "마포구", "11470": "양천구", "11500": "강서구",
    "11530": "구로구", "11545": "금천구", "11560": "영등포구", "11590": "동작구",
    "11620": "관악구", "11650": "서초구", "11680": "강남구", "11710": "송파구",
    "11740": "강동구",
}
BUSINESS_CODES = ["100", "101", "102", "103", "104", "105", "106", "107"]


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.current, self.cell, self.in_td = [], [], [], False
        self.record, self.cafe = None, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.current, self.record, self.cafe = [], None, None
        elif tag == "td":
            self.in_td, self.cell = True, []
        elif tag == "a":
            href = attrs.get("href", "")
            record = re.search(r"mapOpenPopup\('([^']+)'\)", href)
            cafe = re.search(r"cafeOpenPopup\('([^']+)'\)", href)
            if record: self.record = record.group(1)
            if cafe: self.cafe = cafe.group(1)

    def handle_data(self, data):
        if self.in_td: self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.in_td:
            self.current.append(" ".join("".join(self.cell).split()))
            self.in_td = False
        elif tag == "tr" and len(self.current) >= 9 and self.current[0].isdigit():
            self.rows.append((self.current, self.record, self.cafe))


def post(params: list[tuple[str, str]], endpoint: str = ENDPOINT) -> str:
    body = urlencode(params).encode()
    request = Request(endpoint, data=body, headers={"User-Agent": "seoul-sintong-map/1.0"})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def official_center(record_code: str | None) -> tuple[float | None, float | None]:
    """Return a WGS84 center from Seoul Urban Space Portal's official geometry."""
    if not record_code:
        return None, None
    try:
        with urlopen(Request(URBAN_POPUP.format(record_code), headers={"User-Agent": "seoul-sintong-map/1.0"}), timeout=30) as response:
            popup = response.read().decode("utf-8", errors="replace")
        layer = re.search(r'id="layerCode"[^>]*value="([^"]+)"', popup)
        if not layer:
            return None, None
        raw = post([("layerCode", layer.group(1)), ("wtnncSn", record_code)], URBAN_GEOMETRY)
        rows = json.loads(raw)
        if not rows or not rows[0].get("shape"):
            return None, None
        geometry = rows[0]["shape"]["coordinates"]
        points: list[tuple[float, float]] = []
        def collect(value):
            if isinstance(value, list) and len(value) >= 2 and isinstance(value[0], (int, float)):
                points.append((value[0], value[1]))
            elif isinstance(value, list):
                for item in value: collect(item)
        collect(geometry)
        if not points:
            return None, None
        x = sum(p[0] for p in points) / len(points)
        y = sum(p[1] for p in points) / len(points)
        lng, lat = TO_WGS84.transform(x, y)
        return round(lat, 7), round(lng, 7)
    except Exception as exc:
        logging.warning("No official geometry for %s: %s", record_code, exc)
        return None, None


def fetch_gu(code: str, with_geometry: bool) -> list[dict]:
    base = [("scupBsnsSttus.signguCode", code)] + [("bsnsSeCodeList", x) for x in BUSINESS_CODES]
    first = post(base + [("cpage", "1"), ("pageSize", "100")])
    pages = [int(x) for x in re.findall(r"cpage=(\d+)", html.unescape(first))]
    last_page = max(pages, default=1)
    projects = []
    for page in range(1, last_page + 1):
        text = first if page == 1 else post(base + [("cpage", str(page)), ("pageSize", "100")])
        parser = TableParser(); parser.feed(text)
        for cells, record, cafe in parser.rows:
            lat, lng = official_center(record) if with_geometry else (None, None)
            projects.append({
                "id": record or f"{code}:{cells[2]}:{cells[3]}:{cells[4]}",
                "gu": cells[1], "business_type": cells[2], "name": cells[3],
                "address": cells[4], "stage": cells[5], "public_data_count": cells[6],
                "timeliness": cells[7], "completeness": cells[8],
                "map_record_code": record, "cafe_id": cafe,
                "source_url": f"{SOURCE}?scupBsnsSttus.signguCode={code}",
                "lat": lat, "lng": lng,
            })
    return projects


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gu", choices=GU_CODES.keys(), help="fetch one district only")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--with-geometry", action="store_true", help="resolve official map-record geometries")
    args = parser.parse_args()
    LOG.parent.mkdir(exist_ok=True)
    logging.basicConfig(filename=LOG, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        codes = [args.gu] if args.gu else list(GU_CODES)
        projects = [project for code in codes for project in fetch_gu(code, args.with_geometry)]
        payload = {"source": SOURCE, "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "projects": projects}
        if not args.dry_run:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        logging.info("Fetched %s projects for %s district(s)", len(projects), len(codes))
        print(json.dumps({"projects": len(projects), "districts": len(codes), "dry_run": args.dry_run}))
        return 0
    except Exception:
        logging.exception("Fetch failed")
        raise


if __name__ == "__main__":
    sys.exit(main())
