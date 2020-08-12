from dataclasses import dataclass


@dataclass
class Cue:
    no: int
    distance: float
    direction: str
    intersection: str
    sign: str
    road: str
    comment: str
    src: str
