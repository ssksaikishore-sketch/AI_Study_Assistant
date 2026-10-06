
import streamlit as st
import json
import os
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="Student Attendance System",
    page_icon="📚",
    layout="centered"
)

FILE_NAME = "attendance_records.json"


def load_records():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_records(records):
    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)


def create_pdf(records):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "Student Attendance Report")

    y -= 40

    pdf.setFont("Helvetica", 11)

    # Calculate student analysis
    analysis = {}

    for record in records:
        roll = record["roll"]

        if roll not in analysis:
            analysis[roll] = {
                "name": record["name"],
                "present": 0,
                "absent": 0
            }

        if record["status"] == "✅ Present":
            analysis[roll]["present"] += 1
        else:
            analysis[roll]["absent"] += 1

    for roll, student in analysis.items():

        total = student["present"] + student["absent"]

        percentage = (
            student["present"] / total
        ) * 100

        if y < 100:
            pdf.showPage()
            y = height - 50

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(
            50,
            y,
            f"Student: {student['name']}"
        )

        y -= 20

        pdf.setFont("Helvetica", 11)

        pdf.drawString(
            60,
            y,
            f"Roll Number: {roll}"
        )

        y -= 18

        pdf.drawString(
            60,
            y,
            f"Total Classes: {total}"
        )

        y -= 18

        pdf.drawString(
            60,
            y,
            f"Present: {student['present']}"
        )

        y -= 18

        pdf.drawString(
            60,
            y,
            f"Absent: {student['absent']}"
        )

        y -= 18

        pdf.drawString(
            60,
            y,
            f"Attendance: {percentage:.2f}%"
        )

        y -= 18

        result = (
            "Eligible"
            if percentage >= 75
            else "Shortage"
        )

        pdf.drawString(
            60,
            y,
            f"Status: {result}"
        )

        y -= 35

    # Detailed records
    if y < 150:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        "Attendance Records"
    )

    y -= 25

    pdf.setFont("Helvetica", 10)

    for record in records:

        if y < 50:
            pdf.showPage()
            y = height - 50

        text = (
            f"{record['date']} | "
            f"{record['name']} | "
            f"{record['roll']} | "
            f"{record['status']}"
        )

        pdf.drawString(50, y, text)

        y -= 18

    pdf.save()

    buffer.seek(0)

    return buffer


st.title("📚 Student Attendance Analysis")

st.write(
    "Record and analyze student attendance easily."
)

st.divider()

st.subheader("👨‍🎓 Student Details")

student_name = st.text_input(
    "Student Name",
    placeholder="Enter student name"
)

roll_number = st.text_input(
    "Roll Number",
    placeholder="Enter roll number"
)

attendance_date = st.date_input(
    "Attendance Date",
    value=date.today()
)

st.divider()

st.subheader("📝 Record Attendance")

status = st.radio(
    "Attendance Status",
    ["✅ Present", "❌ Absent"],
    horizontal=True
)

if st.button(
    "💾 Record Attendance",
    use_container_width=True
):

    if not student_name or not roll_number:

        st.warning(
            "Please enter student name and roll number."
        )

    else:

        records = load_records()

        record = {
            "name": student_name,
            "roll": roll_number,
            "date": str(attendance_date),
            "status": status
        }

        records.append(record)

        save_records(records)

        st.success(
            "✅ Attendance recorded successfully!"
        )


records = load_records()


if records:

    st.divider()

    st.subheader("📊 Attendance Analysis")

    analysis = {}

    for record in records:

        roll = record["roll"]
        name = record["name"]

        if roll not in analysis:

            analysis[roll] = {
                "name": name,
                "present": 0,
                "absent": 0
            }

        if record["status"] == "✅ Present":
            analysis[roll]["present"] += 1
        else:
            analysis[roll]["absent"] += 1


    for roll, student in analysis.items():

        total = (
            student["present"]
            + student["absent"]
        )

        percentage = (
            student["present"] / total
        ) * 100

        st.markdown(
            f"### 👨‍🎓 {student['name']}"
        )

        st.write(
            f"**Roll Number:** {roll}"
        )

        st.write(
            f"**Total Classes:** {total}"
        )

        st.write(
            f"**Present:** {student['present']}"
        )

        st.write(
            f"**Absent:** {student['absent']}"
        )

        st.write(
            f"**Attendance:** {percentage:.2f}%"
        )

        if percentage >= 75:

            st.success(
                "🟢 Eligible — Attendance is 75% or above."
            )

        else:

            st.error(
                "🔴 Shortage — Attendance is below 75%."
            )

        st.divider()


    st.subheader("📋 Attendance Records")

    for record in records:

        st.write(
            f"**{record['date']}** — "
            f"{record['name']} "
            f"({record['roll']}) — "
            f"{record['status']}"
        )


    st.divider()

    st.subheader("📄 Attendance Report")

    pdf_file = create_pdf(records)

    st.download_button(
        label="📥 Download Attendance Report as PDF",
        data=pdf_file,
        file_name="Student_Attendance_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:

    st.info(
        "No attendance records yet. "
        "Record attendance above to see the analysis."
    )
