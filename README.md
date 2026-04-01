# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Sorting by time: tasks are ordered chronologically using HH:MM-to-minutes conversion.
- Priority-based scheduling: generated schedules prioritize higher-priority pending tasks first.
- Conflict warnings: overlapping task windows are detected with interval overlap checks and surfaced as warnings.
- Filtered task views: tasks can be filtered by status and by pet for focused planning.
- Daily recurrence automation: completing a daily recurring task creates a new task for the following day.
- Support for multiple recurrence types: once, daily, weekly, monthly, and as-needed recurrence behaviors.
- Time-budget validation: schedule generation/addition enforces the owner's available minutes per day.
- High-priority and recurring task retrieval: helper methods surface urgent and recurring pending tasks quickly.
- Per-pet and cross-pet task management: scheduler and owner APIs support querying tasks across all pets or a single pet.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

Current tests cover core scheduling behavior, including:

- Task lifecycle basics (status updates and completion counting)
- Task management on pets (adding one or multiple tasks)
- Sorting correctness (tasks returned in chronological order)
- Recurrence logic (completing a daily task creates the next-day task)
- Conflict detection (duplicate task times are flagged)

Confidence Level: 4/5 stars

Reasoning: all current tests pass (7/7), and they validate critical scheduling flows; however, broader edge-case coverage (for example DST boundaries, monthly date rollover, and larger multi-pet scenarios) would further improve reliability confidence.

## Demo

<a href="/1.jpg" target="_blank"><img src='1.jpg' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
<a href="/2.jpg" target="_blank"><img src='2.jpg' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
<a href="/3.jpg" target="_blank"><img src='3.jpg' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

