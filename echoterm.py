#!/usr/bin/env python3
import time, argparse, random
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

HIST = Path.home() / ".bash_history"

NOISE_EXACT = {"PY","PYEOF","SH","MD","EOF","}","]","}","{","#",""}
NOISE_PREFIX = ("#!","def ","return ","import ","from ","class ",
                "elif ","else:","try:","except","finally:",
                "while ","with ","print(","async ","@","s = ","out = ")

def is_noise(cmd):
    if not cmd: return True
    if cmd[:1] in (" ", "\t"): return True
    s = cmd.strip()
    if s in NOISE_EXACT: return True
    if len(s) <= 1: return True
    for p in NOISE_PREFIX:
        if s.startswith(p): return True
    return False

def parse_history():
    if not HIST.exists(): return []
    entries, cur = [], None
    with open(HIST, "r", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#") and line[1:].isdigit():
                cur = int(line[1:])
            elif line.strip():
                entries.append((cur, line))
    return entries

def bar(title, sub=None):
    print()
    print("=" * 60)
    print(f"  {title}")
    if sub: print(f"  {sub}")
    print("=" * 60)
    print()

def show(hits, title, sub=None, show_timeless=True):
    bar(title, sub)
    dated   = [(t,c) for t,c in hits if t]
    undated = [(t,c) for t,c in hits if not t]
    if not hits:
        print("  (nothing found)"); print(); return
    for ts, c in dated:
        print(f"  {datetime.fromtimestamp(ts).strftime('%H:%M')}  {c}")
    if undated and show_timeless:
        print()
        print("  -- no timestamp (old history) --")
        for _, c in undated:
            print(f"  --:--  {c}")
    print()
    total = len(dated) + (len(undated) if show_timeless else 0)
    print(f"  {total} command(s)")
    print()

def main():
    p = argparse.ArgumentParser(prog="echoterm", add_help=False)
    p.add_argument("-h","--help", action="store_true")
    p.add_argument("-d","--days", type=int, default=None)
    p.add_argument("-m","--months", type=int, default=None)
    p.add_argument("-y","--years", type=int, default=None)
    p.add_argument("-w","--window", type=int, default=3600)
    p.add_argument("-f","--filter", type=str, default=None)
    p.add_argument("-s","--search", type=str, default=None)
    p.add_argument("--on", type=str, default=None)
    p.add_argument("--top", action="store_true")
    p.add_argument("--random", action="store_true")
    a = p.parse_args()

    e = parse_history()
    if not e:
        bar("echoterm"); print("  no history found\n"); return
    if not any(ts for ts,_ in e):
        bar("echoterm")
        print("  no timestamps in ~/.bash_history\n")
        print('  add to ~/.bashrc:  export HISTTIMEFORMAT="%F %T "\n')
        return

    e_clean = [(ts,c) for ts,c in e if not is_noise(c)]

    if a.search:
        hits = [(ts,c) for ts,c in e_clean if a.search.lower() in c.lower()]
        show(hits, f'search: "{a.search}"', f"{len(hits)} match(es)")
        return

    if a.on:
        try: day = datetime.strptime(a.on, "%Y-%m-%d")
        except ValueError:
            bar("echoterm"); print("  bad date, use YYYY-MM-DD\n"); return
        lo, hi = day.timestamp(), (day + timedelta(days=1)).timestamp()
        hits = [(ts,c) for ts,c in e_clean if ts and lo <= ts < hi]
        if a.filter: hits = [(ts,c) for ts,c in hits if a.filter in c]
        show(hits, a.on)
        return

    if a.random:
        dated = [(t,c) for t,c in e_clean if t]
        if not dated: bar("echoterm"); print("  (nothing)\n"); return
        ts, c = random.choice(dated)
        bar("random moment")
        print(f"  {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')}")
        print(f"  {c}\n")
        return

    if a.top:
        if a.days is None and a.months is None and a.years is None:
            hits = [c for _,c in e_clean]; label = "all time"
        else:
            dd = (a.days or 0)+(a.months or 0)*30+(a.years or 0)*365
            t = time.time() - dd*86400
            lo, hi = t - a.window, t + a.window
            hits = [c for ts,c in e_clean if ts and lo <= ts <= hi]; label = "window"
        if a.filter: hits = [c for c in hits if a.filter in c]
        cnt = Counter(hits)
        bar(f"top commands ({label})")
        if not cnt: print("  (nothing)\n"); return
        for cmd, n in cnt.most_common(20):
            print(f"  {n:4d}  {cmd}")
        print(); return

    if a.help or (a.days is None and a.months is None and a.years is None):
        bar("echoterm", "time-capsule shell")
        print("  echoterm -d 1              # 1 day ago")
        print("  echoterm -m 1              # 1 month ago")
        print("  echoterm -y 1              # 1 year ago")
        print("  echoterm -m 6 -w 7200      # 6mo ago, +/-2h")
        print("  echoterm -s git            # search all history")
        print("  echoterm -f sudo -d 0      # filter today")
        print("  echoterm --on 2026-10-11   # specific date")
        print("  echoterm --top             # most-used")
        print("  echoterm --random          # random moment")
        print(); return

    dd = (a.days or 0)+(a.months or 0)*30+(a.years or 0)*365
    t = time.time() - dd*86400
    lo, hi = t - a.window, t + a.window
    hits = [(ts,c) for ts,c in e_clean if ts and lo <= ts <= hi]
    if a.filter: hits = [(ts,c) for ts,c in hits if a.filter in c]
    lbl = ""
    if a.years:  lbl += f"{a.years}y "
    if a.months: lbl += f"{a.months}mo "
    if a.days is not None: lbl += f"{a.days}d"
    if a.filter: lbl += f"  [{a.filter}]"
    d = datetime.fromtimestamp(t)
    show(hits, f"{lbl.strip()} ago", f"around {d.strftime('%Y-%m-%d')}")

main()
