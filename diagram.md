```mermaid
classDiagram
    class PetOwner {
        +String name
        +int available_time_per_day
        +update_available_time()
    }

    class Pet {
        +String name
        +String species
        +int age
        +String special_needs
        +PetOwner owner
        +update_info()
    }

    class Task {
        +String name
        +int duration
        +int priority
        +update_task()
        +adjust_priority()
        +estimate_urgency()
    }

    class Scheduler {
        +List tasks
        +Pet pet
        +List constraints
        +generate_schedule()
        +add_task()
    }

    PetOwner --> Pet : owns
    Pet --> Task : requires
    Scheduler --> Pet : manages
    Scheduler --> Task : schedules
