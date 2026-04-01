import streamlit as st

from pawpal_system import Pet, PetOwner, Scheduler, Task, TaskFrequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time per day (minutes)",
    min_value=1,
    max_value=1440,
    value=180,
)

# Session "vault": create owner once, then reuse it across reruns/pages.
if "owner" not in st.session_state:
    st.session_state["owner"] = PetOwner(
        name=owner_name,
        available_time_per_day=int(available_time),
    )

owner = st.session_state["owner"]
if owner.name != owner_name:
    owner.name = owner_name
if owner.available_time_per_day != int(available_time):
    owner.update_available_time(int(available_time))

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler(owner=owner, constraints=[])

scheduler = st.session_state["scheduler"]

st.caption(f"Session owner loaded: {owner.get_summary()}")

st.markdown("### Add a Pet")

pet_col1, pet_col2 = st.columns(2)
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pet_col2:
    pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)
    special_needs = st.text_input("Special needs", value="None")

if st.button("Add pet"):
    try:
        new_pet = Pet(
            name=pet_name,
            species=species,
            age=int(pet_age),
            special_needs=special_needs,
            owner=owner,
        )
        owner.add_pet(new_pet)
        st.success(f"Added pet: {new_pet.get_summary()}")
    except ValueError as exc:
        st.error(str(exc))

all_pets = owner.get_all_pets()
if all_pets:
    st.write("Current pets:")
    st.table([
        {
            "name": pet.name,
            "species": pet.species,
            "age": pet.age,
            "special_needs": pet.special_needs,
        }
        for pet in all_pets
    ])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Schedule a Task")
st.caption("Create a task and attach it to one of your pets.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_description = st.text_input("Task description", value="Daily care task")
task_frequency = st.selectbox(
    "Frequency",
    ["once", "daily", "weekly", "monthly", "as_needed"],
    index=1,
)

pet_names = [pet.name for pet in all_pets]
selected_pet_name = st.selectbox(
    "Assign to pet",
    pet_names if pet_names else ["No pets available"],
)

priority_map = {"low": 3, "medium": 6, "high": 9}
frequency_map = {
    "once": TaskFrequency.ONCE,
    "daily": TaskFrequency.DAILY,
    "weekly": TaskFrequency.WEEKLY,
    "monthly": TaskFrequency.MONTHLY,
    "as_needed": TaskFrequency.AS_NEEDED,
}

if st.button("Add task"):
    if not all_pets:
        st.warning("Add at least one pet before scheduling tasks.")
    else:
        try:
            task = Task(
                name=task_title,
                duration=int(duration),
                priority=priority_map[priority],
                description=task_description,
                frequency=frequency_map[task_frequency],
            )
            scheduler.add_task_to_pet(selected_pet_name, task)
            st.success(f"Added task '{task.name}' to {selected_pet_name}.")
        except ValueError as exc:
            st.error(str(exc))

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([
        {
            "pet": task.pet.name if task.pet else "-",
            "title": task.name,
            "duration_minutes": task.duration,
            "priority": task.priority,
            "frequency": task.frequency.value,
            "status": task.status.value,
        }
        for task in all_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's schedule from your pending tasks.")

if st.button("Generate schedule"):
    try:
        schedule = scheduler.generate_schedule()
        if not schedule:
            st.info("No pending tasks to schedule yet.")
        else:
            st.success("Today's Schedule")
            st.table([
                {
                    "pet": task.pet.name if task.pet else "-",
                    "task": task.name,
                    "duration_minutes": task.duration,
                    "priority": task.priority,
                    "urgency": task.estimate_urgency(),
                }
                for task in schedule
            ])
            st.caption(scheduler.get_daily_summary())
    except ValueError as exc:
        st.error(str(exc))
