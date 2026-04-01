"""PawPal+ pet care scheduling system — core domain classes."""

from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime, timedelta


class TaskFrequency(Enum):
    """Frequency options for recurring tasks."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


class TaskStatus(Enum):
    """Status options for task completion."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PetOwner:
    """Represents a pet owner managing multiple pets and care tasks."""

    def __init__(self, name: str, available_time_per_day: int):
        """Initialize a PetOwner with name and daily time budget."""
        if not name or not isinstance(name, str):
            raise ValueError("Owner name must be a non-empty string.")
        if available_time_per_day < 0:
            raise ValueError("Available time per day cannot be negative.")
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.pets: Dict[str, 'Pet'] = {}  # pet_name -> Pet instance

    def add_pet(self, pet: 'Pet'):
        """Add a pet to the owner's collection."""
        if not isinstance(pet, Pet):
            raise ValueError("Pet must be a Pet instance.")
        if pet.name in self.pets:
            raise ValueError(
                f"Pet '{pet.name}' already registered to this owner."
            )
        self.pets[pet.name] = pet

    def remove_pet(self, pet_name: str):
        """Remove a pet from the owner's collection."""
        if pet_name not in self.pets:
            raise ValueError(
                f"Pet '{pet_name}' not found in collection."
            )
        del self.pets[pet_name]

    def get_pet(self, pet_name: str) -> Optional['Pet']:
        """Get a pet by name."""
        return self.pets.get(pet_name)

    def get_all_pets(self) -> List['Pet']:
        """Return a list of all pets owned by this owner."""
        return list(self.pets.values())

    def get_all_tasks(self) -> List['Task']:
        """Return a consolidated list of all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets.values():
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_available_time(self, new_time: int):
        """Update the owner's daily available time in minutes."""
        if new_time < 0:
            raise ValueError("Available time per day cannot be negative.")
        self.available_time_per_day = new_time

    def get_summary(self) -> str:
        """Return a short summary of the owner."""
        pet_count = len(self.pets)
        plural = 's' if pet_count != 1 else ''
        return (
            f"{self.name} ({self.available_time_per_day} min/day, "
            f"{pet_count} pet{plural})"
        )


class Pet:
    """Represents a pet with basic info, special needs, and care tasks."""

    def __init__(
        self,
        name: str,
        species: str,
        age: int,
        special_needs: str,
        owner: PetOwner,
    ):  # pylint: disable=too-many-arguments
        """Initialize a Pet with its profile and owning PetOwner."""
        if not name or not isinstance(name, str):
            raise ValueError("Pet name must be a non-empty string.")
        if not species or not isinstance(species, str):
            raise ValueError("Species must be a non-empty string.")
        if age < 0:
            raise ValueError("Pet age cannot be negative.")
        if not isinstance(owner, PetOwner):
            raise ValueError("Owner must be a PetOwner instance.")
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        self.owner = owner
        self.tasks: List['Task'] = []  # List of tasks for this pet

    def add_task(self, task: 'Task'):
        """Add a task to this pet's task list."""
        if not isinstance(task, Task):
            raise ValueError("Task must be a Task instance.")
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self  # Link task back to pet

    def remove_task(self, task: 'Task'):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self, status: Optional[TaskStatus] = None) -> List['Task']:
        """Return all tasks for this pet, optionally filtered by status."""
        if status is None:
            return self.tasks.copy()
        return [t for t in self.tasks if t.status == status]

    def get_pending_tasks(self) -> List['Task']:
        """Return all pending tasks for this pet."""
        return self.get_tasks(TaskStatus.PENDING)

    def get_completed_tasks(self) -> List['Task']:
        """Return all completed tasks for this pet."""
        return self.get_tasks(TaskStatus.COMPLETED)

    def update_info(
        self,
        name: Optional[str] = None,
        species: Optional[str] = None,
        age: Optional[int] = None,
        special_needs: Optional[str] = None,
    ):
        """Update one or more fields on the pet's profile."""
        if name is not None:
            if not isinstance(name, str) or not name:
                raise ValueError("Pet name must be a non-empty string.")
            self.name = name
        if species is not None:
            if not isinstance(species, str) or not species:
                raise ValueError("Species must be a non-empty string.")
            self.species = species
        if age is not None:
            if age < 0:
                raise ValueError("Pet age cannot be negative.")
            self.age = age
        if special_needs is not None:
            self.special_needs = special_needs

    def get_summary(self) -> str:
        """Return a short summary of the pet."""
        task_count = len(self.tasks)
        plural = 's' if task_count != 1 else ''
        return (
            f"{self.name} ({self.species}, age {self.age}) - "
            f"{task_count} task{plural}"
        )


class Task:
    """Represents a pet-care task with duration, priority, frequency."""

    def __init__(
        self,
        name: str,
        duration: int,
        priority: int,
        pet: Optional[Pet] = None,
        description: str = "",
        frequency: TaskFrequency = TaskFrequency.ONCE,
        time: str = "09:00",
        due_date=None,
    ):
        """Initialize Task with name, duration, priority, pet, frequency, time, and due_date."""
        if not name or not isinstance(name, str):
            raise ValueError("Task name must be a non-empty string.")
        if duration <= 0:
            raise ValueError("Task duration must be positive.")
        if not 1 <= priority <= 10:
            raise ValueError("Priority must be between 1 and 10.")
        if pet is not None and not isinstance(pet, Pet):
            raise ValueError("Pet must be a Pet instance.")
        if not isinstance(frequency, TaskFrequency):
            raise ValueError("Frequency must be a TaskFrequency enum.")
        if not self._validate_time_format(time):
            raise ValueError("Time must be in HH:MM format (00:00 to 23:59).")

        self.name = name
        self.duration = duration
        self.priority = priority
        self.pet = pet
        self.description = description
        self.frequency = frequency
        self.status: TaskStatus = TaskStatus.PENDING
        self.time = time
        self.due_date = due_date if due_date is not None else datetime.now().date()
        # Track how many times this task has been completed
        self.completion_count = 0

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        description: Optional[str] = None,
        frequency: Optional[TaskFrequency] = None,
    ):
        """Update the task's name, duration, description, and/or frequency."""
        if name is not None:
            if not isinstance(name, str) or not name:
                raise ValueError("Task name must be a non-empty string.")
            self.name = name
        if duration is not None:
            if duration <= 0:
                raise ValueError("Task duration must be positive.")
            self.duration = duration
        if description is not None:
            self.description = description
        if frequency is not None:
            if not isinstance(frequency, TaskFrequency):
                raise ValueError("Frequency must be a TaskFrequency enum.")
            self.frequency = frequency

    def adjust_priority(self, new_priority: int):
        """Set a new priority value (1–10)."""
        if not 1 <= new_priority <= 10:
            raise ValueError("Priority must be between 1 and 10.")
        self.priority = new_priority

    def mark_completed(self) -> Optional['Task']:
        """
        Mark the task as completed and create next recurring task instance if applicable.

        This method implements automatic recurring task generation. Upon completion,
        recurring tasks (DAILY, WEEKLY, MONTHLY, AS_NEEDED) trigger the creation of
        a new Task instance with the calculated next due date.

        Recurrence calculation:
            - DAILY: next_due_date = current_due_date + 1 day
            - WEEKLY: next_due_date = current_due_date + 7 days
            - MONTHLY: next_due_date = current_due_date + 30 days
            - AS_NEEDED: next_due_date = today (manual scheduling)
            - ONCE: No next task created

        The new task instance inherits all properties from the original:
            - Same name, duration, priority, pet, description, time, frequency
            - Status reset to PENDING
            - Completion count reset to 0
            - New due_date based on frequency

        Return:
            Task: Newly created Task instance for recurring tasks.
            None: For one-time tasks (frequency == ONCE).

        Side effects:
            - Updates self.status to COMPLETED
            - Increments self.completion_count
            - Adds new task to pet.tasks if pet is assigned
        """
        self.status = TaskStatus.COMPLETED
        self.completion_count += 1

        # Handle recurring tasks
        if not self.is_recurring():
            return None

        # Calculate next due date based on frequency
        if self.frequency == TaskFrequency.DAILY:
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == TaskFrequency.WEEKLY:
            next_due_date = self.due_date + timedelta(days=7)
        elif self.frequency == TaskFrequency.MONTHLY:
            next_due_date = self.due_date + timedelta(days=30)
        elif self.frequency == TaskFrequency.AS_NEEDED:
            next_due_date = datetime.now().date()
        else:
            return None

        # Create new task instance for next occurrence
        next_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            pet=self.pet,
            description=self.description,
            frequency=self.frequency,
            time=self.time,
            due_date=next_due_date,
        )

        # Add the new task to the pet if assigned
        if self.pet:
            self.pet.add_task(next_task)

        return next_task

    def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = TaskStatus.IN_PROGRESS

    def mark_pending(self):
        """Mark the task as pending."""
        self.status = TaskStatus.PENDING

    def is_recurring(self) -> bool:
        """Return True if the task recurs (not a one-time task)."""
        return self.frequency != TaskFrequency.ONCE

    @staticmethod
    def _validate_time_format(time: str) -> bool:
        """
        Validate that a time string is in HH:MM format and within valid range.

        Args:
            time: Time string to validate (e.g., "09:00", "23:59")

        Returns:
            True if time is valid HH:MM format with hours 00-23 and minutes 00-59.
            False otherwise.

        Examples:
            >>> Task._validate_time_format("09:30")
            True
            >>> Task._validate_time_format("25:00")  # Invalid hour
            False
            >>> Task._validate_time_format("9:30")   # Missing leading zero
            False
        """
        if not isinstance(time, str) or len(time) != 5 or time[2] != ':':
            return False
        try:
            hours, minutes = time.split(':')
            h = int(hours)
            m = int(minutes)
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    @staticmethod
    def _time_to_minutes(time: str) -> int:
        """
        Convert HH:MM format time string to total minutes since midnight.

        Used for efficient time comparisons and overlap detection. Converts
        time-of-day to a single integer value (0-1440 minutes).

        Args:
            time: Time string in HH:MM format (e.g., "09:30")

        Returns:
            Integer minutes since midnight (0-1440).

        Examples:
            >>> Task._time_to_minutes("09:00")
            540
            >>> Task._time_to_minutes("09:30")
            570
            >>> Task._time_to_minutes("23:59")
            1439
        """
        hours, minutes = time.split(':')
        return int(hours) * 60 + int(minutes)

    def estimate_urgency(self) -> str:
        """Return 'high', 'medium', or 'low' based on the task's priority."""
        if self.priority >= 8:
            return "high"
        if self.priority >= 4:
            return "medium"
        return "low"

    def get_summary(self) -> str:
        """Return a summary of the task."""
        pet_name = f" ({self.pet.name})" if self.pet else ""
        return (
            f"{self.name} - {self.duration}min, priority {self.priority}, "
            f"{self.frequency.value}{pet_name}, status: {self.status.value}, "
            f"due: {self.due_date}"
        )


class Scheduler:
    """Orchestration engine that manages tasks across multiple pets."""

    def __init__(self, owner: PetOwner, constraints: List[str]):
        """Initialize the Scheduler with an owner and constraints."""
        if not isinstance(owner, PetOwner):
            raise ValueError("Owner must be a PetOwner instance.")
        if not isinstance(constraints, list):
            raise ValueError("Constraints must be a list.")
        self.owner = owner
        self.constraints = constraints
        self.last_conflicts: List[str] = []  # Store conflicts from last schedule

    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Retrieve all tasks from pets, optionally filtered by status."""
        all_tasks = self.owner.get_all_tasks()
        if status is None:
            return all_tasks
        return [t for t in all_tasks if t.status == status]

    def get_tasks_by_pet(
        self, pet_name: str, status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """Retrieve tasks for a specific pet, optionally filtered by status."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"Pet '{pet_name}' not found.")
        return pet.get_tasks(status)

    def get_high_priority_tasks(
        self, priority_threshold: int = 8
    ) -> List[Task]:
        """Return tasks with priority >= threshold, sorted descending."""
        all_tasks = self.get_all_tasks(TaskStatus.PENDING)
        high_priority = [
            t for t in all_tasks if t.priority >= priority_threshold
        ]
        return sorted(high_priority, key=lambda t: t.priority, reverse=True)

    def get_recurring_tasks(self) -> List[Task]:
        """Return all recurring tasks."""
        all_tasks = self.get_all_tasks(TaskStatus.PENDING)
        return [t for t in all_tasks if t.is_recurring()]

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by scheduled time in ascending chronological order.

        Converts each task's time attribute (HH:MM format) to total minutes
        since midnight, then sorts using Python's sorted() function with a
        lambda key. This provides O(n log n) time complexity for scheduling.

        Args:
            tasks: List of Task objects to sort

        Returns:
            New list of tasks sorted by time (earliest to latest).
            Original list is not modified.

        Examples:
            >>> tasks = [task_at_09_00, task_at_08_00, task_at_14_00]
            >>> sorted_tasks = scheduler.sort_tasks_by_time(tasks)
            >>> [t.time for t in sorted_tasks]
            ['08:00', '09:00', '14:00']
        """
        return sorted(
            tasks,
            key=lambda t: Task._time_to_minutes(t.time)
        )

    def filter_tasks(
        self,
        status: Optional[TaskStatus] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """
        Filter tasks by completion status and/or pet name.

        Flexible filtering method that retrieves tasks based on one or both
        criteria. Supports filtering by task status (PENDING, COMPLETED,
        IN_PROGRESS) and/or by pet assignment. Can be called with:
            - No arguments: returns all tasks across all pets
            - Only status: returns all tasks with that status
            - Only pet_name: returns all tasks for that pet (any status)
            - Both: returns tasks for that pet with that status

        Args:
            status: TaskStatus enum to filter by. Options:
                - TaskStatus.PENDING: incomplete tasks
                - TaskStatus.IN_PROGRESS: tasks being worked on
                - TaskStatus.COMPLETED: finished tasks
                - None: all statuses (default)
            pet_name: Pet name to filter by. Performs exact string match.
                - If provided, only tasks assigned to this pet are returned.
                - None: tasks from all pets (default)

        Returns:
            List[Task]: Tasks matching the filter criteria (empty list if none found).

        Raises:
            ValueError: If pet_name is provided but the pet does not exist.

        Examples:
            >>> # Get all pending tasks
            >>> pending = scheduler.filter_tasks(status=TaskStatus.PENDING)

            >>> # Get all tasks for Max
            >>> max_tasks = scheduler.filter_tasks(pet_name="Max")

            >>> # Get completed tasks for Max
            >>> completed = scheduler.filter_tasks(
            ...     status=TaskStatus.COMPLETED, pet_name="Max"
            ... )

            >>> # Get all tasks (any status, any pet)
            >>> all_tasks = scheduler.filter_tasks()
        """
        if pet_name:
            pet = self.owner.get_pet(pet_name)
            if pet is None:
                raise ValueError(f"Pet '{pet_name}' not found.")
            tasks = pet.get_tasks(status)
        else:
            tasks = self.get_all_tasks(status)

        return tasks

    def detect_conflicts(
        self, tasks: List[Task], strict_mode: bool = False
    ) -> List[str]:
        """
        Detect time conflicts among tasks using interval overlap algorithm.

        Implements a lightweight O(n²) conflict detection strategy that checks
        all task pairs for scheduling conflicts. Two tasks conflict if their
        time windows overlap, where each window spans from start_time to
        (start_time + duration).

        Overlap detection algorithm:
            Two tasks A and B overlap if:
                start_A < end_B  AND  start_B < end_A
            Where:
                end_time = start_time_in_minutes + duration_in_minutes

        This method is designed to be non-blocking: conflicts are identified
        and returned as warning messages, but scheduling continues. This
        allows the owner to make deliberate scheduling decisions.

        Args:
            tasks: List of Task objects to analyze for conflicts

            strict_mode: Conflict detection scope (default False)
                - False: Detect conflicts only for tasks assigned to the same pet.
                    Lower-severity warnings ("Same Pet - HIGH"). Assumes owner
                    can work on multiple pets in parallel (permissive mode).
                - True: Detect conflicts for ANY overlapping times, regardless
                    of pet assignment. Assumes owner can only do one task at a
                    time (strict mode for human time constraints).

        Returns:
            List[str]: Warning messages describing each detected conflict.
                Empty list if no conflicts found.

                Each message contains:
                    - Conflict type (Same Pet | Different Pets)
                    - Severity level (HIGH for same pet, MEDIUM otherwise)
                    - Task names and assigned pets
                    - Time windows for each task (HH:MM-HH:MM format)
                    - Duration in minutes
                    - Overlap duration in minutes

        Examples:
            >>> task1 = Task("Walk", 30, 9, pet=dog, time="09:00")
            >>> task2 = Task("Play", 20, 8, pet=dog, time="09:15")
            >>> conflicts = scheduler.detect_conflicts([task1, task2])
            >>> len(conflicts)
            1
            >>> print(conflicts[0])
            [CONFLICT - Same Pet - HIGH]
              Task 1: 'Walk' (Max) at 09:00-09:30 (30min)
              Task 2: 'Play' (Max) at 09:15-09:35 (20min)
              Overlap: 15 minutes

        Time complexity:
            O(n²) where n = number of tasks. For typical daily schedules
            (10-30 tasks), this is negligible. Called once per schedule generation.
        """
        conflicts = []

        for i, task_a in enumerate(tasks):
            for task_b in tasks[i + 1:]:
                # Skip if not same pet and not in strict mode
                if not strict_mode and task_a.pet != task_b.pet:
                    continue

                # Calculate time windows in minutes
                start_a = Task._time_to_minutes(task_a.time)
                end_a = start_a + task_a.duration

                start_b = Task._time_to_minutes(task_b.time)
                end_b = start_b + task_b.duration

                # Check for overlap
                if start_a < end_b and start_b < end_a:
                    # Calculate overlap duration
                    overlap_start = max(start_a, start_b)
                    overlap_end = min(end_a, end_b)
                    overlap_minutes = overlap_end - overlap_start

                    # Format times
                    time_a_str = f"{task_a.time}-{self._minutes_to_time(end_a)}"
                    time_b_str = f"{task_b.time}-{self._minutes_to_time(end_b)}"

                    # Build conflict message
                    pet_a = task_a.pet.name if task_a.pet else "Unassigned"
                    pet_b = task_b.pet.name if task_b.pet else "Unassigned"
                    same_pet = pet_a == pet_b

                    conflict_type = "Same Pet" if same_pet else "Different Pets"
                    severity = "HIGH" if same_pet else "MEDIUM"

                    message = (
                        f"[CONFLICT - {conflict_type} - {severity}]\n"
                        f"  Task 1: '{task_a.name}' ({pet_a})"
                        f" at {time_a_str} ({task_a.duration}min)\n"
                        f"  Task 2: '{task_b.name}' ({pet_b})"
                        f" at {time_b_str} ({task_b.duration}min)\n"
                        f"  Overlap: {overlap_minutes} minutes"
                    )
                    conflicts.append(message)

        return conflicts

    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """
        Convert total minutes since midnight to HH:MM format time string.

        Inverse operation of _time_to_minutes(). Converts an integer representing
        minutes since midnight (0-1440) back to a readable HH:MM time string.

        Handles wraparound: If minutes >= 1440 (one full day), uses modulo
        arithmetic to normalize back to the 0-1440 range.

        Args:
            minutes: Total minutes since midnight (0-1440).
                - 0 = 00:00 (midnight)
                - 540 = 09:00 (9 AM)
                - 1080 = 18:00 (6 PM)
                - 1439 = 23:59

        Returns:
            str: Time in HH:MM format with zero-padded hours and minutes.

        Examples:
            >>> Scheduler._minutes_to_time(0)
            '00:00'
            >>> Scheduler._minutes_to_time(540)
            '09:00'
            >>> Scheduler._minutes_to_time(570)
            '09:30'
            >>> Scheduler._minutes_to_time(1080)
            '18:00'
            >>> Scheduler._minutes_to_time(1439)
            '23:59'
            >>> Scheduler._minutes_to_time(1500)  # Wraparound
            '00:00'
        """
        minutes = minutes % 1440  # Wrap around after midnight
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def generate_schedule(
        self, pet_name: Optional[str] = None
    ) -> List[Task]:
        """
        Generate a prioritized schedule, sorted by priority.

        Also detects and stores any time conflicts for later retrieval.
        Conflicts are detected but do NOT prevent schedule generation.
        """
        if pet_name:
            tasks = self.get_tasks_by_pet(pet_name, TaskStatus.PENDING)
        else:
            tasks = self.get_all_tasks(TaskStatus.PENDING)

        if not tasks:
            self.last_conflicts = []
            return []

        # Validate feasibility for the owner's time constraints
        total_duration = sum(task.duration for task in tasks)
        if total_duration > self.owner.available_time_per_day:
            raise ValueError(
                f"Cannot generate schedule. Total duration "
                f"({total_duration} min) exceeds available time "
                f"({self.owner.available_time_per_day} min)."
            )

        # Detect conflicts
        self.last_conflicts = self.detect_conflicts(tasks, strict_mode=False)

        # Return tasks sorted by priority (highest first)
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def get_schedule_warnings(self) -> List[str]:
        """
        Return conflict warnings detected from the last schedule generation.

        Returns:
            List of warning messages (empty if no conflicts).
        """
        return self.last_conflicts

    def validate_schedule(self, pet_name: Optional[str] = None) -> bool:
        """Check if schedule is feasible within owner's constraints."""
        if pet_name:
            tasks = self.get_tasks_by_pet(pet_name, TaskStatus.PENDING)
        else:
            tasks = self.get_all_tasks(TaskStatus.PENDING)

        total_duration = sum(task.duration for task in tasks)
        return total_duration <= self.owner.available_time_per_day

    def add_task_to_pet(self, pet_name: str, task: Task):
        """Add a task to a specific pet, with capacity validation."""
        if not isinstance(task, Task):
            raise ValueError("Task must be a Task instance.")

        pet = self.owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"Pet '{pet_name}' not found.")

        # Check if adding this task would exceed owner's available time
        pet_tasks_duration = sum(
            t.duration for t in pet.get_tasks(TaskStatus.PENDING)
        )
        other_pets_tasks_duration = sum(
            sum(t.duration for t in p.get_tasks(TaskStatus.PENDING))
            for p in self.owner.get_all_pets()
            if p.name != pet_name
        )
        total_if_added = (
            pet_tasks_duration + other_pets_tasks_duration + task.duration
        )

        if total_if_added > self.owner.available_time_per_day:
            raise ValueError(
                f"Cannot add task '{task.name}' ({task.duration} min). "
                f"Total would be {total_if_added} min, exceeding available "
                f"time ({self.owner.available_time_per_day} min)."
            )

        task.pet = pet
        pet.add_task(task)

    def remove_task_from_pet(self, pet_name: str, task: Task):
        """Remove a task from a specific pet."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"Pet '{pet_name}' not found.")
        pet.remove_task(task)

    def complete_task(self, task: Task) -> Optional[Task]:
        """
        Mark a task as completed.

        For recurring tasks, a new Task instance is automatically created for
        the next occurrence with the calculated due date.

        Returns:
            The newly created Task for recurring tasks, or None for ONCE tasks.

        Raises:
            ValueError: If task is not a Task instance.
        """
        if not isinstance(task, Task):
            raise ValueError("Task must be a Task instance.")
        return task.mark_completed()

    def get_daily_summary(self) -> str:
        """Return summary of daily tasks and time utilization."""
        all_pets = self.owner.get_all_pets()
        pending_tasks = self.get_all_tasks(TaskStatus.PENDING)
        total_pending_duration = sum(t.duration for t in pending_tasks)
        remaining_time = (
            self.owner.available_time_per_day - total_pending_duration
        )

        pet_names = ', '.join(p.name for p in all_pets) if all_pets else 'None'
        summary_lines = [
            f"=== Daily Schedule Summary for {self.owner.name} ===",
            f"Pets: {pet_names}",
            f"Total Pending Tasks: {len(pending_tasks)}",
            f"Time Used: {total_pending_duration}/"
            f"{self.owner.available_time_per_day} minutes",
            f"Time Remaining: {remaining_time} minutes",
        ]
        return "\n".join(summary_lines)
