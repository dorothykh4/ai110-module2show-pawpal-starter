"""PawPal+ pet care scheduling system — core domain classes."""

from typing import List, Optional, Dict
from enum import Enum


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
    ):
        """Initialize Task with name, duration, priority, pet, frequency."""
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

        self.name = name
        self.duration = duration
        self.priority = priority
        self.pet = pet
        self.description = description
        self.frequency = frequency
        self.status: TaskStatus = TaskStatus.PENDING
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

    def mark_completed(self):
        """Mark the task as completed and increment completion count."""
        self.status = TaskStatus.COMPLETED
        self.completion_count += 1

    def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = TaskStatus.IN_PROGRESS

    def mark_pending(self):
        """Mark the task as pending."""
        self.status = TaskStatus.PENDING

    def is_recurring(self) -> bool:
        """Return True if the task recurs (not a one-time task)."""
        return self.frequency != TaskFrequency.ONCE

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
            f"{self.frequency.value}{pet_name}, status: {self.status.value}"
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

    def generate_schedule(
        self, pet_name: Optional[str] = None
    ) -> List[Task]:
        """Generate a prioritized schedule, sorted by priority."""
        if pet_name:
            tasks = self.get_tasks_by_pet(pet_name, TaskStatus.PENDING)
        else:
            tasks = self.get_all_tasks(TaskStatus.PENDING)

        if not tasks:
            return []

        # Validate feasibility for the owner's time constraints
        total_duration = sum(task.duration for task in tasks)
        if total_duration > self.owner.available_time_per_day:
            raise ValueError(
                f"Cannot generate schedule. Total duration "
                f"({total_duration} min) exceeds available time "
                f"({self.owner.available_time_per_day} min)."
            )

        # Return tasks sorted by priority (highest first)
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

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

    def complete_task(self, task: Task):
        """Mark a task as completed."""
        if not isinstance(task, Task):
            raise ValueError("Task must be a Task instance.")
        task.mark_completed()

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
