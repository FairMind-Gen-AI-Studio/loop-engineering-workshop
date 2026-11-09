"""Pretend a fix just went to production, and write its error rate to a log.

Exercise 2 points an agent at the log it writes, four lines a minute:

    2026-09-22T10:04:15Z minute=4.25 error_rate=0.42% status=ok

A regression starts at --regression-at and lasts --regression-for minutes, then
the rate settles back. Values come from a fixed seed, so every run in the room
tells the same story.

    python3 scripts/fake_deploy.py                    # four lines a minute
    python3 scripts/fake_deploy.py --interval 1       # a fast rehearsal
"""

import argparse
import datetime
import random
import sys
import time

LINES_PER_MINUTE = 4


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="deploy.log")
    parser.add_argument("--minutes", type=float, default=12, help="how many minutes the log covers")
    parser.add_argument("--interval", type=float, default=60 / LINES_PER_MINUTE, help="seconds between lines")
    parser.add_argument("--regression-at", type=float, default=3, help="minute the regression starts")
    parser.add_argument("--regression-for", type=float, default=2.5, help="minutes it lasts")
    args = parser.parse_args(argv)

    lines = round(args.minutes * LINES_PER_MINUTE)
    rng = random.Random(42)
    with open(args.out, "a", encoding="utf-8") as log:
        for number in range(lines):
            minute = number / LINES_PER_MINUTE
            regressed = args.regression_at <= minute < args.regression_at + args.regression_for
            rate = rng.uniform(4.5, 8.0) if regressed else rng.uniform(0.2, 0.6)
            status = "degraded" if regressed else "ok"
            at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            line = f"{at} minute={minute:g} error_rate={rate:.2f}% status={status}"
            print(line, file=log, flush=True)
            print(line, flush=True)
            if number < lines - 1:
                time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    sys.exit(main())
