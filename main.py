"""PawPal+ main script demonstrating pet care scheduling."""

from pawpal_system import (
    PetOwner,
    Pet,
    Task,
    Scheduler,
    TaskFrequency,
    TaskStatus,
)


def main():
    """Create a sample schedule and display today's tasks."""
    print("=" * 60)
    print("PawPal+ Pet Care Scheduling System")
    print("=" * 60)
    print()

    # Create an owner
    owner = PetOwner(name="Sarah", available_time_per_day=180)
    print(f"Owner Created: {owner.get_summary()}")
    print()

    # Create pets
    luna = Pet(
        name="Luna",
        species="Dog",
        age=3,
        special_needs="Needs regular walks",
        owner=owner,
    )
    owner.add_pet(luna)

    whiskers = Pet(
        name="Whiskers",
        species="Cat",
        age=2,
        special_needs="Sensitive stomach",
        owner=owner,
    )
    owner.add_pet(whiskers)

    tiger = Pet(
        name="Tiger",
        species="Parrot",
        age=5,
        special_needs="Needs mental stimulation",
        owner=owner,
    )
    owner.add_pet(tiger)

    print("Pets Created:")
    for pet in owner.get_all_pets():
        print(f"  - {pet.get_summary()}")
    print()

    # Create tasks for Luna (dog)
    task_1 = Task(
        name="Morning Walk",
        duration=30,
        priority=9,
        pet=luna,
        description="Walk around the park",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Luna").add_task(task_1)

    task_2 = Task(
        name="Feeding",
        duration=10,
        priority=10,
        pet=luna,
        description="Breakfast and dinner",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Luna").add_task(task_2)

    task_3 = Task(
        name="Playtime",
        duration=20,
        priority=8,
        pet=luna,
        description="Fetch and tug",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Luna").add_task(task_3)

    # Create tasks for Whiskers (cat)
    task_4 = Task(
        name="Feeding",
        duration=5,
        priority=10,
        pet=whiskers,
        description="Special cat food",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Whiskers").add_task(task_4)

    task_5 = Task(
        name="Litter Box Cleaning",
        duration=15,
        priority=8,
        pet=whiskers,
        description="Clean and refill litter",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Whiskers").add_task(task_5)

    task_6 = Task(
        name="Interactive Playtime",
        duration=15,
        priority=7,
        pet=whiskers,
        description="Play with laser pointer",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Whiskers").add_task(task_6)

    # Create tasks for Tiger (parrot)
    task_7 = Task(
        name="Feeding",
        duration=10,
        priority=10,
        pet=tiger,
        description="Seed and fruit mix",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Tiger").add_task(task_7)

    task_8 = Task(
        name="Training Session",
        duration=20,
        priority=8,
        pet=tiger,
        description="Teach new tricks",
        frequency=TaskFrequency.DAILY,
    )
    owner.get_pet("Tiger").add_task(task_8)

    print("Tasks Created:")
    for pet in owner.get_all_pets():
        print(f"\n{pet.name}:")
        for task in pet.get_tasks():
            print(f"  - {task.get_summary()}")

    print("\n" + "=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)
    print()

    # Create scheduler and generate schedule
    constraints = [
        "Complete high-priority tasks first",
        "Feeding tasks non-negotiable",
    ]
    scheduler = Scheduler(owner=owner, constraints=constraints)

    # Display all tasks organized by pet
    for pet in owner.get_all_pets():
        pet_tasks = scheduler.get_tasks_by_pet(pet.name)
        print(f"{pet.name.upper()} - Tasks ({len(pet_tasks)}):")
        scheduled = scheduler.generate_schedule(pet.name)
        for i, task in enumerate(scheduled, 1):
            print(
                f"  {i}. {task.name} ({task.duration} min) "
                f"- Priority: {task.priority}/10 - {task.estimate_urgency()}"
            )
        print()

    # Display daily summary
    print(scheduler.get_daily_summary())
    print()

    # Mark a task as completed to show status tracking
    print("=" * 60)
    print("Task Status Update")
    print("=" * 60)
    task_1.mark_completed()
    print(f"Marked '{task_1.name}' as completed (Count: {task_1.completion_count})")
    print()

    # Show updated schedule summary
    print(scheduler.get_daily_summary())


if __name__ == "__main__":
    main()
