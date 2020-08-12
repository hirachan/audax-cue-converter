#!/bin/env python3
import sys
import argparse

from .rwgps import RideWithGPS
from .nihonbashi import Nihonbashi


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert RWGPS to AR Nihonbashi Cue Sheet')
    parser.add_argument("route_id", action="store", metavar="ROUTE_ID")
    parser.add_argument("privacy_code", action="store", metavar="PRIVACY_CODE", nargs="?", default=None)
    parser.add_argument("-o", action="store", dest="output", default="output.xlsx", help="Default: output.xlsx")

    args = parser.parse_args()

    return args


def main() -> int:
    args = get_opt()

    rwgps = RideWithGPS()
    cues = rwgps.read(args.route_id, args.privacy_code)
    converter = Nihonbashi()
    converter.write(cues, args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
