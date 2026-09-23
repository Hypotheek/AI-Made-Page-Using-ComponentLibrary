#!/usr/bin/env python3
"""
claude_usage.py -- Track token and time usage of Claude Code chat sessions.

Reads the JSONL session transcripts Claude Code already writes to
~/.claude/projects/<project>/<session-id>.jsonl and turns them into
human-readable reports: per-session totals, a per-prompt breakdown, and a
live "watch" mode that updates while you keep chatting.

No third-party dependencies -- stdlib only.

Usage:
    python claude_usage.py list [--all] [-n 20]
    python claude_usage.py show [SESSION] [--all-turns]
    python claude_usage.py watch [SESSION] [--interval 1.0]

SESSION can be omitted (defaults to the most recently active session in the
current project), a number from `list` output, or a session id / prefix.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Rough, approximate USD price per 1M tokens. Anthropic updates pricing over
# time and these numbers are best-effort placeholders based on historical
# Claude pricing tiers -- verify at https://anthropic.com/pricing and edit
# below if you want accurate dollar figures. If you're on a Pro/Max
# subscription rather than pay-per-token API billing, cost here is only a
# rough proxy for how "heavy" a session was, not what you were actually
# charged.
PRICING = {
    "opus":   {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "sonnet": {"input": 3.00,  "output": 15.00, "cache_write": 3.75,  "cache_read": 0.30},
    "haiku":  {"input": 0.80,  "output": 4.00,  "cache_write": 1.00,  "cache_read": 0.08},
    "fable":  {"input": 3.00,  "output": 15.00, "cache_write": 3.75,  "cache_read": 0.30},
}


def price_for_model(model: Optional[str]):
    if not model:
        return None
    m = model.lower()
    for key, rates in PRICING.items():
        if key in m:
            return rates
    return None


def parse_ts(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def fmt_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m{s:02d}s"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


def fmt_local(dt: Optional[datetime]) -> str:
    if dt is None:
        return "?"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def fmt_tokens(n: int) -> str:
    return f"{n:,}"


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


# --------------------------------------------------------------------------
# Project / session discovery
# --------------------------------------------------------------------------

def session_files(project_dir: Path):
    return sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)


def session_cwd(path: Path) -> Optional[str]:
    try:
        for i, entry in enumerate(iter_jsonl(path)):
            if "cwd" in entry:
                return entry["cwd"]
            if i > 20:
                break
    except OSError:
        pass
    return None


def find_project_dir(target: Path) -> Optional[Path]:
    """Find the ~/.claude/projects/<x> folder whose sessions were run from `target`."""
    if not CLAUDE_PROJECTS_DIR.exists():
        return None
    target_resolved = str(target.resolve())
    candidates = []
    for proj in CLAUDE_PROJECTS_DIR.iterdir():
        if not proj.is_dir():
            continue
        files = session_files(proj)
        if not files:
            continue
        cwd = session_cwd(files[0])
        if cwd and cwd.rstrip("\\/") == target_resolved.rstrip("\\/"):
            candidates.append((files[0].stat().st_mtime, proj))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def session_title(project_dir: Path, session_id: str) -> Optional[str]:
    title_file = project_dir / session_id / "custom-title.json"
    if title_file.exists():
        try:
            data = json.loads(title_file.read_text(encoding="utf-8"))
            return data.get("customTitle")
        except (OSError, json.JSONDecodeError):
            return None
    return None


def resolve_session(project_dir: Path, ref: Optional[str]) -> Path:
    files = session_files(project_dir)
    if not files:
        raise SystemExit(f"No sessions found in {project_dir}")
    if ref is None:
        return files[0]
    if ref.isdigit():
        idx = int(ref) - 1
        if 0 <= idx < len(files):
            return files[idx]
        raise SystemExit(f"No session #{ref} (only {len(files)} sessions found)")
    matches = [f for f in files if f.stem.startswith(ref)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise SystemExit(f"Ambiguous session id prefix '{ref}', matches: "
                         + ", ".join(m.stem for m in matches))
    raise SystemExit(f"No session matching '{ref}'")


# --------------------------------------------------------------------------
# Usage extraction
# --------------------------------------------------------------------------

@dataclass
class Turn:
    prompt: str
    start: Optional[datetime]
    end: Optional[datetime] = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_write: int = 0
    cache_read: int = 0
    models: set = field(default_factory=set)

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens + self.cache_write + self.cache_read

    @property
    def wall_seconds(self) -> float:
        if self.start and self.end:
            return (self.end - self.start).total_seconds()
        return 0.0


def is_real_user_prompt(entry: dict) -> bool:
    """True for an actual typed prompt, false for tool-result / meta entries."""
    if entry.get("type") != "user":
        return False
    if entry.get("isMeta"):
        return False
    msg = entry.get("message", {})
    content = msg.get("content")
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        # a real prompt's content list never starts with a tool_result block
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                return False
        return True
    return False


def prompt_preview(entry: dict, width: int = 60) -> str:
    msg = entry.get("message", {})
    content = msg.get("content")
    text = ""
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        text = " ".join(parts)
    text = " ".join(text.split())
    if len(text) > width:
        text = text[: width - 3] + "..."
    return text or "(no text)"


def load_turns(path: Path) -> list[Turn]:
    turns: list[Turn] = []
    current: Optional[Turn] = None

    for entry in iter_jsonl(path):
        etype = entry.get("type")
        ts = parse_ts(entry.get("timestamp"))

        if is_real_user_prompt(entry):
            current = Turn(prompt=prompt_preview(entry), start=ts)
            turns.append(current)
            continue

        if etype == "assistant":
            msg = entry.get("message", {})
            usage = msg.get("usage")
            if not usage:
                continue
            if current is None:
                current = Turn(prompt="(session start)", start=ts)
                turns.append(current)
            current.input_tokens += usage.get("input_tokens", 0) or 0
            current.output_tokens += usage.get("output_tokens", 0) or 0
            current.cache_write += usage.get("cache_creation_input_tokens", 0) or 0
            current.cache_read += usage.get("cache_read_input_tokens", 0) or 0
            model = msg.get("model")
            if model:
                current.models.add(model)
            if ts:
                current.end = ts

    return turns


@dataclass
class SessionSummary:
    turns: list
    started: Optional[datetime]
    ended: Optional[datetime]

    @property
    def input_tokens(self):
        return sum(t.input_tokens for t in self.turns)

    @property
    def output_tokens(self):
        return sum(t.output_tokens for t in self.turns)

    @property
    def cache_write(self):
        return sum(t.cache_write for t in self.turns)

    @property
    def cache_read(self):
        return sum(t.cache_read for t in self.turns)

    @property
    def total_tokens(self):
        return self.input_tokens + self.output_tokens + self.cache_write + self.cache_read

    @property
    def duration_seconds(self):
        if self.started and self.ended:
            return (self.ended - self.started).total_seconds()
        return 0.0

    @property
    def models(self):
        m = set()
        for t in self.turns:
            m |= t.models
        return m

    def estimate_cost(self):
        total = 0.0
        priced_any = False
        for t in self.turns:
            for model in (t.models or {None}):
                rates = price_for_model(model)
                if not rates:
                    continue
                priced_any = True
                n_models = max(len(t.models), 1)
                total += (t.input_tokens / n_models / 1_000_000) * rates["input"]
                total += (t.output_tokens / n_models / 1_000_000) * rates["output"]
                total += (t.cache_write / n_models / 1_000_000) * rates["cache_write"]
                total += (t.cache_read / n_models / 1_000_000) * rates["cache_read"]
        return total if priced_any else None


def summarize(turns: list[Turn]) -> SessionSummary:
    starts = [t.start for t in turns if t.start]
    ends = [t.end for t in turns if t.end] + [t.start for t in turns if t.start and not t.end]
    return SessionSummary(
        turns=turns,
        started=min(starts) if starts else None,
        ended=max(ends) if ends else None,
    )


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_list(args):
    target = Path(args.path).resolve() if args.path else Path.cwd()

    if args.all:
        project_dirs = [p for p in CLAUDE_PROJECTS_DIR.iterdir() if p.is_dir()]
    else:
        proj = find_project_dir(target)
        if not proj:
            print(f"No Claude Code sessions found for {target}")
            print("(try --all to list sessions from every project)")
            return
        project_dirs = [proj]

    rows = []
    for proj in project_dirs:
        for f in session_files(proj)[: args.number]:
            turns = load_turns(f)
            summ = summarize(turns)
            title = session_title(proj, f.stem) or (turns[0].prompt if turns else "(empty)")
            rows.append((f.stat().st_mtime, proj.name, f.stem, title, summ))

    if not rows:
        print("No sessions found.")
        return

    rows.sort(reverse=True)
    rows = rows[: args.number]

    print(f"{'#':<3} {'Last active':<20} {'Dur':>8} {'Turns':>6} {'Tokens':>13}  Title")
    print("-" * 90)
    for i, (mtime, proj_name, sid, title, summ) in enumerate(rows, 1):
        last = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"{i:<3} {last:<20} {fmt_duration(summ.duration_seconds):>8} "
              f"{len(summ.turns):>6} {fmt_tokens(summ.total_tokens):>13}  {title}")
        if args.all:
            print(f"     project: {proj_name}  id: {sid}")

    print()
    print("Run `python claude_usage.py show <#>` for details, or `watch` to track live.")


def print_session_header(proj: Path, path: Path, summ: SessionSummary):
    title = session_title(proj, path.stem)
    print(f"Session: {path.stem}")
    if title:
        print(f"Title:   {title}")
    print(f"Project: {proj}")
    print(f"Started: {fmt_local(summ.started)}")
    print(f"Ended:   {fmt_local(summ.ended)}")
    print(f"Elapsed: {fmt_duration(summ.duration_seconds)}")
    models = ", ".join(sorted(summ.models)) or "?"
    print(f"Model(s):{'':1}{models}")
    print()


def print_totals(summ: SessionSummary):
    print(f"{'Input':<14}{fmt_tokens(summ.input_tokens):>12}")
    print(f"{'Output':<14}{fmt_tokens(summ.output_tokens):>12}")
    print(f"{'Cache write':<14}{fmt_tokens(summ.cache_write):>12}")
    print(f"{'Cache read':<14}{fmt_tokens(summ.cache_read):>12}")
    print(f"{'-'*26}")
    print(f"{'Total':<14}{fmt_tokens(summ.total_tokens):>12}")
    cost = summ.estimate_cost()
    if cost is not None:
        print(f"{'Est. cost':<14}{'$' + format(cost, ',.4f'):>12}  (approximate -- see PRICING in script)")


def cmd_show(args):
    target = Path(args.path).resolve() if args.path else Path.cwd()
    proj = find_project_dir(target)
    if not proj:
        raise SystemExit(f"No Claude Code sessions found for {target}")
    path = resolve_session(proj, args.session)
    turns = load_turns(path)
    summ = summarize(turns)

    print_session_header(proj, path, summ)

    max_turns = None if args.all_turns else 25
    shown = turns if max_turns is None else turns[-max_turns:]
    if max_turns and len(turns) > max_turns:
        print(f"(showing last {max_turns} of {len(turns)} turns -- use --all-turns to see all)\n")

    print(f"{'#':<4}{'Time':>8}  {'In':>10}{'Out':>10}{'CacheW':>12}{'CacheR':>12}{'Total':>13}  Prompt")
    print("-" * 110)
    offset = len(turns) - len(shown)
    for i, t in enumerate(shown, offset + 1):
        print(f"{i:<4}{fmt_duration(t.wall_seconds):>8}  {fmt_tokens(t.input_tokens):>10}"
              f"{fmt_tokens(t.output_tokens):>10}{fmt_tokens(t.cache_write):>12}"
              f"{fmt_tokens(t.cache_read):>12}{fmt_tokens(t.total):>13}  {t.prompt}")

    print()
    print_totals(summ)


def cmd_watch(args):
    target = Path(args.path).resolve() if args.path else Path.cwd()
    proj = find_project_dir(target)
    if not proj:
        raise SystemExit(f"No Claude Code sessions found for {target}")
    path = resolve_session(proj, args.session)

    print(f"Watching {path.stem}  (project: {proj})")
    print("Press Ctrl+C to stop.\n")

    session_start = None
    last_size = 0
    last_totals = (0, 0, 0, 0)

    try:
        while True:
            size = path.stat().st_size
            if size != last_size:
                turns = load_turns(path)
                summ = summarize(turns)
                if session_start is None:
                    session_start = summ.started or datetime.now(timezone.utc)

                totals = (summ.input_tokens, summ.output_tokens, summ.cache_write, summ.cache_read)
                if totals != last_totals and turns:
                    latest = turns[-1]
                    now_str = datetime.now().strftime("%H:%M:%S")
                    elapsed = fmt_duration(summ.duration_seconds)
                    print(f"[{now_str}] turn {len(turns)}: \"{latest.prompt}\"  "
                          f"+{fmt_tokens(latest.total)} tok  "
                          f"(running total {fmt_tokens(summ.total_tokens)} tok, {elapsed} elapsed)")
                    last_totals = totals
                last_size = size
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.\n")
        turns = load_turns(path)
        summ = summarize(turns)
        print_session_header(proj, path, summ)
        print_totals(summ)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("--path", help="project directory to look up (default: current directory)")
    sub = p.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="list recent chat sessions and their usage")
    p_list.add_argument("-n", "--number", type=int, default=15, help="how many sessions to show")
    p_list.add_argument("--all", action="store_true", help="list sessions across all projects")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="detailed token/time report for one session")
    p_show.add_argument("session", nargs="?", help="session # (from `list`) or session id / prefix")
    p_show.add_argument("--all-turns", action="store_true", help="show every prompt, not just the last 25")
    p_show.set_defaults(func=cmd_show)

    p_watch = sub.add_parser("watch", help="live-track a session as you keep chatting")
    p_watch.add_argument("session", nargs="?", help="session # (from `list`) or session id / prefix "
                                                    "(default: most recently active)")
    p_watch.add_argument("--interval", type=float, default=1.0, help="poll interval in seconds")
    p_watch.set_defaults(func=cmd_watch)

    return p


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if isinstance(e.code, str):
            print(f"Error: {e.code}", file=sys.stderr)
            sys.exit(1)
        sys.exit(e.code or 0)
    except KeyboardInterrupt:
        sys.exit(0)
