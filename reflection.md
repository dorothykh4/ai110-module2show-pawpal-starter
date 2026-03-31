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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
