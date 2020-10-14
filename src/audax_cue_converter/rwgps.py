from typing import Tuple, List, Optional

import csv
import re

import requests
from bs4 import BeautifulSoup

try:
    from cue import Cue
except ModuleNotFoundError:  # This is for lambda...
    from .cue import Cue


_RE_INTERSECTION = re.compile(r"(\S+)（交差点）")
_RE_DIRECTION = re.compile(r"(右折|左折|斜め右|斜め左|Turn right|Turn left|Slight right|Slight left)")
_RE_ROAD = re.compile(r"(?:[し出]て|で|曲がり|折れて) ?(?:、?そのまま ?)?(\S+) ?(?:に入る|を進む|へ進む)|(?:onto |stay on )(\S+)")
_RE_ROAD_STRAIGHT = re.compile(r"^(\S+)を進む")
_RE_ROAD_TOWARD = re.compile(r"(\S+) に向かう|toward (\S+)")
_RE_SIGN = re.compile(r"\((?:(\S+) の表示|signs for (\S+))\)")

DIRECTION = {
    "右折": "R",
    "左折": "L",
    "斜め右": "Rf",
    "斜め左": "Lf",
    "Turn right": "R",
    "Turn left": "L",
    "Slight right": "Rf",
    "Slight left": "Lf",
}

ROAD_NO = (
    ("国道", "N"),
    ("県道", "D"),
    ("都道", "D"),
    ("府道", "D"),
    ("道道", "D"),
    ("市道", "CR"),
    ("号線", ""),
    ("号", ""),
)


def get_intersection(notes: str) -> str:
    intersection = ""
    m = _RE_INTERSECTION.search(notes)
    if m:
        intersection = m.groups()[0]

    return intersection


def get_direction(notes: str) -> str:
    direction = "St"

    m = _RE_DIRECTION.search(notes)
    if m:
        direction = DIRECTION[m.groups()[0]]
    elif notes == "Make a U-turn":
        direction = "U"

    return direction


def get_sign(notes: str) -> str:
    m = _RE_SIGN.search(notes)
    if m:
        sign = m.groups()[0] or m.groups()[1]
    else:
        sign = ""

    sign = sign.replace("/", "・")

    return sign


def parse_road_no(road_no: str) -> str:
    for src, dest in ROAD_NO:
        road_no = road_no.replace(src, dest)

    return road_no


def parse_road(road: str) -> Tuple[str, str]:
    if "/" in road:
        road_name, road_no = road.rsplit("/", 1)
    elif "号" in road:
        road_name = ""
        road_no = road
    else:
        road_name = road
        if "農道" in road_name:
            road_no = "AR"
        else:
            road_no = "CR"

    road_no = parse_road_no(road_no)

    return road_name, road_no


def get_road(notes: str) -> Tuple[str, str]:
    road_name = ""
    road_no = "CR"

    m = _RE_ROAD.search(notes)
    if m:
        match = m.groups()
        road = match[0] or match[1]

        road_name, road_no = parse_road(road)

    else:
        m = _RE_ROAD_STRAIGHT.search(notes)
        if m:
            match = m.groups()
            road = match[0]

            road_name, road_no = parse_road(road)

    # else:
    #     m = _RE_ROAD_TOWARD.search(notes)
    #     if m:
    #         match = m.groups()
    #         road = match[0] or match[1]

    #         road_name, road_no = parse_road(road)
    #         road_no = f"CR・{road_no}"

    return road_name, road_no


def put_title(cue_writer: csv.writer) -> None:
    cue_writer.writerow([
        "キュー", "区間距離", "PC毎距離", "総距離",
        "進路", "", "交差点", "信号", "道標の方面", "道路",
        "ランドマーク(注意事項)"])


class RideWithGPS:
    def read(self, route_id: str, privacy_code: Optional[str] = None) -> List[Cue]:
        headers = {"Accept-Language": "ja-JP"}
        if privacy_code:
            res = requests.get(f"https://ridewithgps.com/routes/{route_id}/cue_sheet?privacy_code={privacy_code}",
                               headers=headers)
        else:
            res = requests.get(f"https://ridewithgps.com/routes/{route_id}/cue_sheet",
                               headers=headers)

        bs = BeautifulSoup(res.content, "html.parser")
        # print(bs)

        cues: List[Cue] = []
        no = 1
        for line in bs.find("table").find("tbody").findAll("tr"):
            row = [_.get_text().strip() for _ in line.findAll("td")]

            notes = row[3].replace("\u200b", "")
            if notes == "直進する":
                continue

            distance = float(row[4].replace(",", "."))

            # print(row)

            intersection = get_intersection(notes)
            direction = get_direction(notes)
            sign = get_sign(notes)
            road = get_road(notes)

            cues.append(Cue(
                no,
                distance,
                direction,
                intersection,
                sign,
                road[1],
                road[0],
                notes,
            ))

            no += 1

        return cues
