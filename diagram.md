```mermaid
classDiagram
    class TaskFrequency {
        <<enumeration>>
        ONCE
        DAILY
        WEEKLY
        MONTHLY
        AS_NEEDED
    }

    class TaskStatus {
        <<enumeration>>
        PENDING
        IN_PROGRESS
        COMPLETED
    }

    class PetOwner {
        +str name
        +int available_time_per_day
        +Dict[str, Pet] pets
        +add_pet(pet)
        +remove_pet(pet_name)
        +get_pet(pet_name)
        +get_all_pets()
        +get_all_tasks()
        +update_available_time(new_time)
        +get_summary()
    }

    class Pet {
        +str name
        +str species
        +int age
        +str special_needs
        +PetOwner owner
        +List[Task] tasks
        +add_task(task)
        +remove_task(task)
        +get_tasks(status)
        +get_pending_tasks()
        +get_completed_tasks()
        +update_info(name, species, age, special_needs)
        +get_summary()
    }

    class Task {
        +str name
        +int duration
        +int priority
        +Pet pet
        +str description
        +TaskFrequency frequency
        +TaskStatus status
        +str time
        +date due_date
        +int completion_count
        +update_task(name, duration, description, frequency)
        +adjust_priority(new_priority)
        +mark_completed() Optional~Task~
        +mark_in_progress()
        +mark_pending()
        +is_recurring()
        +estimate_urgency()
        +get_summary()
    }

    class Scheduler {
        +PetOwner owner
        +List constraints
        +List[str] last_conflicts
        +get_all_tasks(status)
        +get_tasks_by_pet(pet_name, status)
        +get_high_priority_tasks(priority_threshold)
        +get_recurring_tasks()
        +sort_tasks_by_time(tasks)
        +filter_tasks(status, pet_name)
        +detect_conflicts(tasks, strict_mode)
        +generate_schedule(pet_name)
        +get_schedule_warnings()
        +validate_schedule(pet_name)
        +add_task_to_pet(pet_name, task)
        +remove_task_from_pet(pet_name, task)
        +complete_task(task)
        +get_daily_summary()
    }

    PetOwner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Task "0..*" --> "0..1" Pet : assigned_to
    Scheduler "1" --> "1" PetOwner : manages
    Scheduler ..> Task : sorts/filters/conflict-checks
    Task --> TaskFrequency
    Task --> TaskStatus

