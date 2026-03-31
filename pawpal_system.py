"""PawPal+ pet care scheduling system — core domain classes."""

from typing import List, Optional


class PetOwner:
    """Represents a pet owner with their daily availability."""

    def __init__(self, name: str, available_time_per_day: int):
        """Initialize a PetOwner with a name and daily time budget in minutes."""
        self.name = name
        self.available_time_per_day = available_time_per_day

    def update_available_time(self, new_time: int):
        """Update the owner's daily available time in minutes."""
        self.available_time_per_day = new_time

    def get_summary(self) -> str:
        """Return a short summary of the owner."""
        return f"{self.name} ({self.available_time_per_day} min/day)"


class Pet:
    """Represents a pet with its basic info and special needs."""

    def __init__(self, name: str, species: str, age: int,  # pylint: disable=too-many-arguments
                 special_needs: str, owner: PetOwner):
        """Initialize a Pet with its profile and owning PetOwner."""
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        self.owner = owner

    def update_info(self, name: Optional[str] = None, species: Optional[str] = None,
                    age: Optional[int] = None, special_needs: Optional[str] = None):
        """Update one or more fields on the pet's profile."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age
        if special_needs is not None:
            self.special_needs = special_needs

    def get_summary(self) -> str:
        """Return a short summary of the pet."""
        return f"{self.name} ({self.species}, age {self.age})"


class Task:
    """Represents a single pet-care task with duration and priority."""

    def __init__(self, name: str, duration: int, priority: int):
        """Initialize a Task with a name, duration in minutes, and priority (1–10)."""
        self.name = name
        self.duration = duration
        self.priority = priority

    def update_task(self, name: Optional[str] = None, duration: Optional[int] = None):
        """Update the task's name and/or duration."""
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration

    def adjust_priority(self, new_priority: int):
        """Set a new priority value (1–10)."""
        self.priority = new_priority

    def estimate_urgency(self) -> str:
        """Return 'high', 'medium', or 'low' based on the task's priority."""
        if self.priority >= 8:
            return "high"
        if self.priority >= 4:
            return "medium"
        return "low"


class Scheduler:
    """Creates a care plan by scheduling tasks for a pet within given constraints."""

    def __init__(self, pet: Pet, constraints: List[str]):
        """Initialize the Scheduler with a target pet and a list of constraint descriptions."""
        self.pet = pet
        self.tasks: List[Task] = []
        self.constraints = constraints

    def add_task(self, task: Task):
        """Add a Task to the scheduler's task list."""
        self.tasks.append(task)

    def generate_schedule(self) -> List[Task]:
        """Return tasks sorted by priority (highest first)."""
        return sorted(self.tasks, key=lambda t: t.priority, reverse=True)
