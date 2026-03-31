"""Unit tests for PawPal+ pet care scheduling system."""

import unittest
from pawpal_system import (
    PetOwner,
    Pet,
    Task,
    TaskStatus,
    TaskFrequency,
)


class TestPawPalSystem(unittest.TestCase):
    """Test cases for the PawPal+ system."""

    def setUp(self):
        """Set up test fixtures for each test."""
        self.owner = PetOwner(name="Test Owner", available_time_per_day=180)
        self.pet = Pet(
            name="TestPet",
            species="Dog",
            age=2,
            special_needs="None",
            owner=self.owner,
        )
        self.task = Task(
            name="Test Task",
            duration=30,
            priority=5,
            pet=self.pet,
            description="A test task",
            frequency=TaskFrequency.DAILY,
        )

    def test_task_completion_changes_status(self):
        """Verify that mark_completed() changes task status from PENDING to COMPLETED."""
        # Arrange: task should initially be PENDING
        self.assertEqual(self.task.status, TaskStatus.PENDING)
        self.assertEqual(self.task.completion_count, 0)

        # Act: mark the task as completed
        self.task.mark_completed()

        # Assert: status should be COMPLETED and count should increment
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        self.assertEqual(self.task.completion_count, 1)

    def test_task_addition_increases_pet_count(self):
        """Verify that adding a task to a Pet increases task count."""
        # Arrange: pet should initially have no tasks
        self.assertEqual(len(self.pet.get_tasks()), 0)

        # Act: add the task to the pet
        self.pet.add_task(self.task)

        # Assert: pet should now have one task
        self.assertEqual(len(self.pet.get_tasks()), 1)
        self.assertIn(self.task, self.pet.get_tasks())

    def test_multiple_task_completions_increment_counter(self):
        """Verify that completing a recurring task multiple times increments counter."""
        # Act: mark task completed three times
        self.task.mark_completed()
        self.task.mark_completed()
        self.task.mark_completed()

        # Assert: completion count should be 3
        self.assertEqual(self.task.completion_count, 3)
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)

    def test_adding_multiple_tasks_to_pet(self):
        """Verify that adding multiple tasks increases count correctly."""
        # Arrange: create additional tasks
        task_2 = Task(
            name="Task 2",
            duration=15,
            priority=6,
            pet=self.pet,
            frequency=TaskFrequency.DAILY,
        )
        task_3 = Task(
            name="Task 3",
            duration=20,
            priority=7,
            pet=self.pet,
            frequency=TaskFrequency.WEEKLY,
        )

        # Act: add all tasks
        self.pet.add_task(self.task)
        self.pet.add_task(task_2)
        self.pet.add_task(task_3)

        # Assert: pet should have three tasks
        self.assertEqual(len(self.pet.get_tasks()), 3)


if __name__ == "__main__":
    unittest.main()
