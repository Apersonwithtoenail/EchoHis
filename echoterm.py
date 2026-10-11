#!/usr/bin/env python3
import time, argparse
from datetime import datetime
from pathlib import Path

HIST = Path.home() / ".bash_history"

def parse_history():
    if not HIST.exists():
        return []
    entries, cur = [], None
    with open(HIST, "r", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#") and line[1:].isdigit():
                cur = int(line[1:])
            elif line.strip():
                entries.append((cur, line))
    return entries

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--days", type=int, default=None)
    p.add_argument("-m", "--months", type=int, default=None)
    p.add_argument("-y", "--years", type=int, default=None)
    p.add_argument("-w", "--window", type=int, default=3600)
    a = p.parse_args()
    if a.days is None and a.months is None and a.years is None:
        p.error("need -d / -m / -y")
    e = parse_history()
    if not e:
        print("no history"); return
    if not any(ts for ts, _ in e):
        print("no timestamps in ~/.bash_history")
        print("add to ~/.bashrc:  export HISTTIMEFORMAT=\"%F %T \"")
        return
    dd = (a.days or 0) + (a.months or 0)*30 + (a.years or 0)*365
    t = time.time() - dd*86400
    lo, hi = t - a.window, t + a.window
    hits = [(ts, c) for ts, c in e if ts and lo <= ts <= hi]
    lbl = ""
    if a.years:  lbl += f"{a.years}y"
    if a.months: lbl += f"{a.months}mo"
    if a.days is not None: lbl += f"{a.days}d"
    print(f"--- {lbl} ago ---")
    if not hits:
        print("(nothing)")
    for ts, c in hits:
        print(f"  {datetime.fromtimestamp(ts).strftime('%H:%M')}  {c}")

main()
