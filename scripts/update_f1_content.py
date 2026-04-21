#!/usr/bin/env python3
"""Refresh Pit Wall content from Ergast API.

Updates these parts of data/content.json:
- stats
- ticker
- meta
- first news item (headline/body) as a race recap
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONTENT_FILE = ROOT / "data" / "content.json"
API_BASE = "https://ergast.com/api/f1/current"


def fetch_json(url: str) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": "pitwall-updater/1.0 (+https://github.com)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def driver_standings() -> list[dict]:
    data = fetch_json(f"{API_BASE}/driverStandings.json")
    table = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not table:
        return []
    return table[0].get("DriverStandings", [])


def constructor_standings() -> list[dict]:
    data = fetch_json(f"{API_BASE}/constructorStandings.json")
    table = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not table:
        return []
    return table[0].get("ConstructorStandings", [])


def last_race_result() -> dict | None:
    data = fetch_json(f"{API_BASE}/last/results.json")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return None
    return races[0]


def next_race() -> dict | None:
    data = fetch_json(f"{API_BASE}/next.json")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return None
    return races[0]


def full_name(driver: dict) -> str:
    return f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip()


def build_updates() -> dict:
    drivers = driver_standings()
    constructors = constructor_standings()
    last_race = last_race_result()
    upcoming = next_race()

    if len(drivers) < 2 or not constructors:
        raise RuntimeError("Not enough standings data returned from Ergast API.")

    leader = drivers[0]
    second = drivers[1]
    leader_points = int(float(leader.get("points", "0")))
    second_points = int(float(second.get("points", "0")))
    gap = max(0, leader_points - second_points)

    leader_name = full_name(leader.get("Driver", {}))
    second_name = full_name(second.get("Driver", {}))

    top_constructor = constructors[0]
    top_constructor_name = top_constructor.get("Constructor", {}).get("name", "Unknown")
    top_constructor_points = top_constructor.get("points", "0")

    if last_race and last_race.get("Results"):
        winner = last_race["Results"][0]
        winner_name = full_name(winner.get("Driver", {}))
        race_name = last_race.get("raceName", "Last Grand Prix")
        circuit_name = last_race.get("Circuit", {}).get("circuitName", "")
    else:
        winner_name = leader_name
        race_name = "Latest race"
        circuit_name = ""

    if upcoming:
        next_race_name = upcoming.get("raceName", "TBA")
        next_race_date = upcoming.get("date", "TBA")
    else:
        next_race_name = "TBA"
        next_race_date = "TBA"

    updates = {
        "stats": [
            {
                "label": "Championship Lead",
                "valuePrefix": f"+{gap}",
                "valueEm": "",
                "valueSuffix": " pts",
                "sub": f"{leader_name} over {second_name}",
            },
            {
                "label": "Current Leader",
                "valuePrefix": leader_name,
                "valueEm": "",
                "valueSuffix": "",
                "sub": f"{leader_points} points after {race_name}",
            },
            {
                "label": "Constructors Lead",
                "valuePrefix": top_constructor_name,
                "valueEm": "",
                "valueSuffix": "",
                "sub": f"{top_constructor_points} points",
            },
            {
                "label": "Next Race",
                "valuePrefix": next_race_name,
                "valueEm": "",
                "valueSuffix": "",
                "sub": next_race_date,
            },
        ],
        "ticker": [
            {"sym": "LEADER", "val": leader_name.upper(), "pts": f"{leader_points} PTS"},
            {"sym": "P2", "val": second_name.upper(), "pts": f"{second_points} PTS"},
            {"sym": "CON", "val": top_constructor_name.upper(), "pts": f"{top_constructor_points} PTS"},
            {"sym": "LAST WIN", "val": winner_name.upper(), "pts": race_name.upper()},
            {"sym": "NEXT", "val": next_race_name.upper(), "pts": next_race_date},
        ],
        "leadStory": {
            "number": "01",
            "variant": "lead",
            "kicker": "Race Recap",
            "headline": f"{winner_name} takes {race_name} as title battle tightens",
            "body": f"{winner_name} won at {circuit_name or race_name}. Current championship leader is {leader_name} with {leader_points} points, {gap} clear of {second_name}.",
        },
    }

    return updates


def main() -> None:
    if not CONTENT_FILE.exists():
        raise FileNotFoundError(f"Missing file: {CONTENT_FILE}")

    content = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    updates = build_updates()

    content["stats"] = updates["stats"]
    content["ticker"] = updates["ticker"]

    news = content.get("news", [])
    if news:
        news[0] = updates["leadStory"]
        content["news"] = news

    content["meta"] = {
        "lastUpdatedUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": "ergast",
    }

    CONTENT_FILE.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")
    print("Updated data/content.json from Ergast API")


if __name__ == "__main__":
    main()
