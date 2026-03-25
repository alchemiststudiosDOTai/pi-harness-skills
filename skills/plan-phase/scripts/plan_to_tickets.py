#!/usr/bin/env python3
"""plan_to_tickets.py

Generate individual ticket markdown files from a PLAN.md document.

This script is designed to support the `plan-phase` skill output layout:

  .artifacts/plan/<timestamp>_<topic>/
    PLAN.md
    tickets/
      T001.md
      T002.md
      INDEX.md

Task parsing rules
------------------
A task starts at a Markdown heading (##..######) matching one of these forms:

  ### T001: Do thing
  ### Task T001: Do thing
  ## Task T001 - Do thing
  #### T001 – Do thing

Everything until the next matching task heading becomes the ticket body.

Plan index updating
-------------------
If PLAN.md contains the markers:

  <!-- TICKET_INDEX:START -->
  <!-- TICKET_INDEX:END -->

…the script replaces the content between them with a generated table linking to
all ticket files.

This script uses ONLY the Python standard library.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


TASK_HEADING_RE = re.compile(r"^(#{2,6})\s*(?:Task\s*)?(T\d{3})\s*[:\-–—]\s*(.+?)\s*$")


@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    body: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_tasks(plan_text: str) -> list[Task]:
    lines = plan_text.splitlines()

    spans: list[tuple[int, int, str, str]] = []  # (start_idx, end_idx, task_id, title)
    current: tuple[int, str, str] | None = None  # (start_idx, task_id, title)

    for i, line in enumerate(lines):
        m = TASK_HEADING_RE.match(line)
        if not m:
            continue

        task_id = m.group(2)
        title = m.group(3)

        if current is not None:
            start_idx, cur_id, cur_title = current
            spans.append((start_idx, i, cur_id, cur_title))

        current = (i, task_id, title)

    if current is not None:
        start_idx, task_id, title = current
        spans.append((start_idx, len(lines), task_id, title))

    tasks: list[Task] = []
    for start_idx, end_idx, task_id, title in spans:
        body_lines = lines[start_idx + 1 : end_idx]

        # Trim blank lines
        while body_lines and body_lines[0].strip() == "":
            body_lines.pop(0)
        while body_lines and body_lines[-1].strip() == "":
            body_lines.pop()

        body = "\n".join(body_lines).rstrip()
        if body:
            body += "\n"

        tasks.append(Task(task_id=task_id, title=title, body=body))

    return tasks


def render_ticket(task: Task, parent_plan_rel: str) -> str:
    created_at = _utc_now_iso()
    title = f"{task.task_id}: {task.title}"

    body = task.body if task.body.strip() else "(details pending)\n"

    return (
        "---\n"
        f'title: "{title}"\n'
        "type: plan_ticket\n"
        f'task_id: "{task.task_id}"\n'
        f'parent_plan: "{parent_plan_rel}"\n'
        f'created_at: "{created_at}"\n'
        "tags: [ticket, plan]\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{body}"
    )


def render_index(tasks: list[Task]) -> str:
    lines = [
        "| Task | Title | Ticket |",
        "|---|---|---|",
    ]
    for t in tasks:
        lines.append(f"| {t.task_id} | {t.title} | [{t.task_id}](./{t.task_id}.md) |")
    return "\n".join(lines) + "\n"


def update_plan_ticket_index(plan_text: str, index_table: str) -> tuple[str, bool]:
    start_marker = "<!-- TICKET_INDEX:START -->"
    end_marker = "<!-- TICKET_INDEX:END -->"

    start_pos = plan_text.find(start_marker)
    end_pos = plan_text.find(end_marker)

    if start_pos == -1 or end_pos == -1:
        return plan_text, False

    if end_pos <= start_pos:
        return plan_text, False

    insert_at = start_pos + len(start_marker)

    before = plan_text[:insert_at]
    after = plan_text[end_pos:]

    replacement = "\n\n" + index_table.strip() + "\n\n"
    return before + replacement + after, True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate individual ticket files from a PLAN.md document.")
    parser.add_argument("plan_file", help="Path to PLAN.md")
    parser.add_argument(
        "--tickets-dir",
        default=None,
        help="Output directory for tickets (default: <plan_dir>/tickets)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing ticket files",
    )
    parser.add_argument(
        "--no-update-plan",
        action="store_true",
        help="Do not update ticket index markers in PLAN.md",
    )

    args = parser.parse_args(argv)

    plan_path = Path(args.plan_file).expanduser().resolve()
    if not plan_path.exists():
        print(f"ERROR: plan file does not exist: {plan_path}", file=sys.stderr)
        return 2

    plan_text = plan_path.read_text(encoding="utf-8")
    tasks = parse_tasks(plan_text)

    if not tasks:
        print(
            "ERROR: no tasks found. Expected headings like '### T001: ...' or '### Task T001: ...' in PLAN.md.",
            file=sys.stderr,
        )
        return 3

    plan_dir = plan_path.parent
    tickets_dir = Path(args.tickets_dir).expanduser() if args.tickets_dir else plan_dir / "tickets"
    tickets_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0

    for task in tasks:
        ticket_path = tickets_dir / f"{task.task_id}.md"

        if ticket_path.exists() and not args.overwrite:
            skipped += 1
            continue

        parent_plan_rel = os.path.relpath(plan_path, ticket_path.parent)
        ticket_path.write_text(render_ticket(task, parent_plan_rel), encoding="utf-8")
        created += 1

    # Always (re)write index
    index_path = tickets_dir / "INDEX.md"
    index_created_at = _utc_now_iso()
    index_body = (
        "---\n"
        'title: "Ticket Index"\n'
        "type: ticket_index\n"
        f'parent_plan: "{os.path.relpath(plan_path, tickets_dir)}"\n'
        f'created_at: "{index_created_at}"\n'
        "tags: [ticket, plan]\n"
        "---\n\n"
        "# Ticket Index\n\n"
        + render_index(tasks)
    )
    index_path.write_text(index_body, encoding="utf-8")

    # Optionally update PLAN.md markers
    updated_plan = False
    if not args.no_update_plan:
        index_table = (
            "| Task | Title | Ticket |\n"
            "|---|---|---|\n"
            + "\n".join([f"| {t.task_id} | {t.title} | [tickets/{t.task_id}.md](tickets/{t.task_id}.md) |" for t in tasks])
            + "\n"
        )
        new_plan_text, updated_plan = update_plan_ticket_index(plan_text, index_table)
        if updated_plan:
            plan_path.write_text(new_plan_text, encoding="utf-8")
        else:
            print(
                "WARN: PLAN.md does not contain ticket index markers. Skipping PLAN.md update. "
                "Add <!-- TICKET_INDEX:START --> and <!-- TICKET_INDEX:END --> to enable.",
                file=sys.stderr,
            )

    print(f"Tickets dir: {tickets_dir}")
    print(f"Tasks found: {len(tasks)}")
    print(f"Tickets created: {created}")
    print(f"Tickets skipped (exists): {skipped}")
    print(f"Index written: {index_path}")
    print(f"PLAN.md updated: {'yes' if updated_plan else 'no'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
