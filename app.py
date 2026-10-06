import streamlit as st
import json
import os
from datetime import date, timedelta, time

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="centered"
)

FILE_NAME = "study_plan.json"


def save_plan(plan):
    with open(FILE_NAME, "w") as file:
        json.dump(plan, file, indent=4)


def load_plan():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return None


st.title("📚 Smart Study Planner")
st.write("Create a personalized study schedule with study timings.")

st.divider()

saved_plan = load_plan()

# -----------------------------
# Student Details
# -----------------------------

st.subheader("👨‍🎓 Student Details")

name = st.text_input(
    "Your name",
    placeholder="Enter your name"
)

hours = st.number_input(
    "Total study hours per day",
    min_value=1,
    max_value=12,
    value=4
)

exam_date = st.date_input(
    "Exam date",
    min_value=date.today(),
    value=date.today() + timedelta(days=30)
)

st.divider()

# -----------------------------
# Subjects
# -----------------------------

st.subheader("📚 Subjects")

subject_count = st.number_input(
    "Number of subjects",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

for i in range(subject_count):

    st.markdown(f"### Subject {i + 1}")

    subject_name = st.text_input(
        "Subject name",
        key=f"subject_{i}",
        placeholder="Example: Mathematics"
    )

    col1, col2 = st.columns(2)

    with col1:
        session = st.selectbox(
            "Study session",
            [
                "🌅 Morning",
                "☀️ Afternoon",
                "🌆 Evening",
                "🌙 Night"
            ],
            key=f"session_{i}"
        )

    with col2:
        study_time = st.time_input(
            "Study time",
            value=time(7, 0),
            key=f"time_{i}"
        )

    if subject_name:
        subjects.append({
            "name": subject_name,
            "session": session,
            "time": study_time.strftime("%I:%M %p")
        })

    st.divider()


# -----------------------------
# Save Plan
# -----------------------------

if st.button("💾 Save Study Plan", use_container_width=True):

    if not name:
        st.warning("Please enter your name.")

    elif len(subjects) == 0:
        st.warning("Please enter at least one subject.")

    else:

        plan = {
            "name": name,
            "hours": hours,
            "exam_date": str(exam_date),
            "subjects": subjects
        }

        save_plan(plan)

        st.success("✅ Study plan saved successfully!")


# -----------------------------
# Display Saved Plan
# -----------------------------

saved_plan = load_plan()

if saved_plan:

    st.divider()

    st.subheader("📋 Your Saved Study Plan")

    st.write(f"**Student:** {saved_plan['name']}")
    st.write(f"**Exam Date:** {saved_plan['exam_date']}")
    st.write(
        f"**Daily Study Hours:** {saved_plan['hours']} hours"
    )

    st.subheader("🕐 Study Timings")

    for subject in saved_plan["subjects"]:

        st.markdown(
            f"### 📖 {subject['name']}"
        )

        st.write(
            f"**{subject['session']}** — "
            f"**{subject['time']}**"
        )

    st.divider()

    # -----------------------------
    # Exam Countdown
    # -----------------------------

    exam = date.fromisoformat(
        saved_plan["exam_date"]
    )

    days_left = (exam - date.today()).days

    if days_left < 0:
        days_left = 0

    st.subheader("⏳ Exam Countdown")

    st.info(
        f"**{days_left} days remaining** until your exam."
    )

    # -----------------------------
    # Weekly Schedule
    # -----------------------------

    st.subheader("📅 Study Schedule")

    for day in range(min(days_left, 7)):

        study_day = date.today() + timedelta(days=day)

        st.markdown(
            f"### Day {day + 1} — "
            f"{study_day.strftime('%d %B %Y')}"
        )

        for subject in saved_plan["subjects"]:

            st.checkbox(
                f"{subject['time']} — "
                f"{subject['name']} "
                f"({subject['session']})",
                key=f"task_{day}_{subject['name']}"
            )
