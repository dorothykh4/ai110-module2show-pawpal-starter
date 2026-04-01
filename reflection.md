# PawPal+ Project Reflection

## 1. System Design

The user should be able to enter a pet and owner information, enter a task (name, duration, priority), edit a task, delete the task, view the generated plan

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design models a simple pet care scheduling system with four core classes that separate the user context, pet information, task definition, and scheduling logic. The design follows a clear structure where data (PetOwner, Pet, Task) is separated from decision-making (Scheduler), and the Scheduler coordinates everything to produce a prioritized daily plan.

- What classes did you include, and what responsibilities did you assign to each?

Class: PetOwner - name, attributes; available_time_per_day; method - update_available_time

Class: Pet - an animal; attributes - name, species, age, special_needs, owner; methods - update_info

Class: Task - a single task; attributes - name, duration, priority; methods - update_task, adjust_priority, estimate_urgency

Class: Scheduler - creates the plan; attributes - tasks, pet, constraints; methods - generate_schedule, add_task

The PetOwner class stores the user’s name and available daily time budget. The Pet class stores the pet’s profile information and links it to its owner. The Task class represents individual care activities, including their duration and priority, and includes logic for updating and estimating urgency. The Scheduler class manages all tasks for a given pet and is responsible for adding tasks and generating a schedule by sorting tasks based on priority.

**b. Design changes**

- Did your design change during implementation?

I changed a bit based on Copilot suggestions

- If yes, describe at least one change and why you made it.

Change 1: Added `owner` reference to Scheduler.
The original design required the Scheduler to access the owner indirectly through `Pet.owner`. By adding a direct `owner` parameter to the Scheduler's constructor, the scheduler can now directly check whether tasks fit within the owner's available time budget which created a straightforward way to validate that the total scheduled task duration doesn't exceed the owner's capacity.

Change 2: Enhanced `add_task()` with capacity validation. 
The original `add_task()` method accepted tasks without any constraints checking. Now it validates before adding any task, calculating the cumulative duration and raising an error if adding the task would exceed the owner's available time. The system was previously vulnerable to silently creating infeasible schedules so this helped control for it.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers three main constraints:

1. **Time Budget**: Owner's `available_time_per_day` (180 minutes in the example). The scheduler validates in `generate_schedule()` that total task duration doesn't exceed this limit, raising an error if infeasible.

2. **Priority**: Tasks have priority values (1-10). The `generate_schedule()` method sorts tasks by priority in descending order, ensuring highest-priority tasks are listed first.

3. **Time of Day**: Tasks specify a scheduled time (HH:MM format, e.g., "09:00"). The `sort_tasks_by_time()` method can order tasks chronologically, though the default schedule prioritizes by priority value rather than time.

- How did you decide which constraints mattered most?

I decided priority matters most by making it the primary sort key in `generate_schedule()` (line 698). This reflects the requirement that critical tasks (feeding, health concerns) should be done regardless of when they're scheduled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler makes a critical tradeoff: **Priority-first scheduling that accepts time conflicts**.

In `generate_schedule()`, tasks are sorted by priority without reordering them to their scheduled times. Conflicts are detected and reported as warnings, but they don't prevent schedule generation. Additionally, in `detect_conflicts()`, the default `strict_mode=False` (line 595) only flags conflicts for tasks on the *same pet*, assuming the owner can work on multiple pets in parallel.

- Why is that tradeoff reasonable for this scenario?

Pet owners often juggle multiple animals simultaneously (e.g., feeding the dog while the cat plays nearby). Preventing high-priority tasks from being scheduled just because of a time conflict could leave pets unfed or unmedicated. Warning the owner about conflicts lets them make deliberate trade-offs: they can adjust times manually, remove lower-priority conflicting tasks, or expand available time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI (Copilot) primarily for design brainstorming during the initial UML phase, and then during implementation for suggesting enhancements to the core classes. The AI helped validate design decisions and suggested improvements like adding the `owner` parameter to Scheduler and implementing capacity validation in `add_task_to_pet()`.

- What kinds of prompts or questions were most helpful?

Questions about validation constraints and feasibility checking were most helpful. Asking "How do I ensure a schedule is feasible?" led to suggestions for capacity validation and constraint checking. Questions about recurring task logic and time conflict detection also produced clear, actionable suggestions.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

**Adding capacity validation to `add_task_to_pet()`**: The AI suggested adding validation that calculates cumulative durations across all pets and raises `ValueError` if adding a task exceeds the owner's budget (lines 728–746). Rather than accepting this immediately, I recognized the core issue: the original design accepted all tasks without checking time constraints, making the system "vulnerable to silently creating infeasible schedules."

- How did you evaluate or verify what the AI suggested?

I tested the validation by attempting to add tasks that together exceed 180 minutes, confirming the error was raised appropriately. I also verified the logic calculated durations correctly by tracing through the implementation: summing pending tasks for the specific pet plus all other pets, then checking if the total would exceed available time.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

My code prioritizes **boundary and constraint validation**:
- Invalid inputs (negative age, empty names, priority outside 1-10 range)
- Capacity constraints (total task duration vs. available time)
- Time format validation (HH:MM format, hours 00-23, minutes 00-59)
- Task status transitions (PENDING → IN_PROGRESS → COMPLETED)
- Recurring task generation (creating next task instances with calculated due dates)
- Conflict detection (overlapping task times)

- Why were these tests important?

These tests prevent invalid state (e.g., infeasible schedules, corrupted data) and ensure the scheduler fails fast with clear error messages rather than producing silently incorrect plans.

**b. Confidence**

- How confident are you that your scheduler works correctly?

**Confidence: Medium-High** for the core design. The class structure is solid and handles most validation. Recurring task logic is well-implemented. However, there are gaps in comprehensive testing—no explicit tests for what happens when adding a recurring task that would exceed capacity, or edge cases around time wraparound.

- What edge cases would you test next if you had more time?

1. Adding a recurring DAILY task right at the time limit—can the next occurrence even be scheduled?
2. Tasks with 0 duration or exactly 1440+ minutes (full day or more)
3. Tasks scheduled at 23:00 for 120 minutes (ends at 01:00 next day)—how should wraparound be handled?
4. Marking a task complete multiple times—does completion_count keep incrementing correctly?
5. Pet/owner relationships: Can a pet's owner change mid-schedule? How does that affect task assignments?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the scheduler logic came together in a clean way. I like that it can sort tasks, filter by status/pet, detect conflicts, and handle recurring tasks after completion. It feels like the app is not just storing data but actually making useful planning decisions.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the scheduling algorithm so it balances both priority and time better instead of mostly priority-first. I would also add more edge-case tests, especially around monthly recurrence and late-night tasks that cross midnight. On the UI side, I would add an easier way to edit or reschedule tasks directly from the schedule table.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

My biggest takeaway is that AI is most helpful when I use it like a coding partner, not a copy-paste answer machine. It helped me move faster, but I still had to verify logic, test edge cases, and make final design choices myself. I also learned that small design decisions early (like class relationships and method responsibilities) make implementation much easier later.
