import streamlit as st
import json
import os
from datetime import date, timedelta

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="centered"
)

FILE_NAME = "study_plan.json"


# Save plan
def save_plan(plan):
    with open(FILE_NAME, "w") as file:
        json.dump(plan, file, indent=4)


# Load saved plan
def load_plan():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return None


st.title("📚 Smart Study Planner")
st.write("Plan your studies and save your progress.")

st.divider()

# Load existing plan
saved_plan = load_plan()

if saved_plan:
    st.success("💾 A saved study plan was found!")

    st.subheader("📋 Saved Plan")

    st.write(f"**Student:** {saved_plan['name']}")
    st.write(f"**Exam Date:** {saved_plan['exam_date']}")
    st.write(f"**Daily Study Hours:** {saved_plan['hours']} hours")

    st.write("### 📚 Subjects")

    for subject in saved_plan["subjects"]:
        st.write(f"• {subject}")

    st.divider()

# Create new plan
st.subheader("👨‍🎓 Create / Update Your Plan")

name = st.text_input(
    "Your name",
    placeholder="Enter your name"
)

hours = st.number_input(
    "Study hours per day",
    min_value=1,
    max_value=12,
    value=3
)

subject_count = st.number_input(
    "Number of subjects",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

for i in range(subject_count):
    subject = st.text_input(
        f"Subject {i + 1}",
        placeholder="Example: Mathematics"
    )

    if subject:
        subjects.append(subject)

exam_date = st.date_input(
    "Exam date",
    min_value=date.today(),
    value=date.today() + timedelta(days=30)
)

st.divider()

if st.button("💾 Save Study Plan", use_container_width=True):

    if not name:
        st.warning("Please enter your name.")

    elif len(subjects) == 0:
        st.warning("Please enter at least one subject.")

    else:

        plan = {
            "name": name,
            "hours": hours,
            "subjects": subjects,
            "exam_date": str(exam_date)
        }

        save_plan(plan)

        st.success("✅ Your study plan has been saved permanently!")

st.divider()

# Study schedule
if saved_plan:

    st.subheader("📅 Your Study Schedule")

    exam = date.fromisoformat(saved_plan["exam_date"])
    days_left = (exam - date.today()).days

    if days_left < 0:
        days_left = 0

    st.info(f"⏳ {days_left} days remaining until your exam.")

    for day in range(min(days_left, 7)):

        study_day = date.today() + timedelta(days=day)

        st.markdown(
            f"### Day {day + 1} — {study_day.strftime('%d %B')}"
        )

        for subject in saved_plan["subjects"]:

            study_time = saved_plan["hours"] / len(
                saved_plan["subjects"]
            )

            st.checkbox(
                f"Study {subject} — {study_time:.1f} hours",
                key=f"{day}_{subject}"
            )