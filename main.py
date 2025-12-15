import streamlit as st
import pandas as pd

grades = {
    "A+" : 10, "A":10, "A-":9, "B":8,"B-":7,"C":6, "C-":5,"D":4, "F": 0, "FS": 0, "I": 0
}

st.set_page_config("CGPA/SGPA Calculator", page_icon="🎓",layout="centered")

st.markdown(
    """
    <h1 style="text-align:center;">🎓 CGPA/SGPA Calculator</h1>
    <p style="text-align:center; color:gray;">
    Enter course credits and grades to compute your SGPA
    </p>
    """,
    unsafe_allow_html=True
)
st.divider()

if "last_sgpa" not in st.session_state:
    st.session_state["last_sgpa"] = None

if "courses" not in st.session_state:
    st.session_state["courses"] = []

if "graded_courses_taken" not in st.session_state:
    st.session_state["graded_courses_taken"] = None

if "dep" not in st.session_state:
    st.session_state["dep"] = None

if "sem" not in st.session_state:
    st.session_state["sem"] = None

courses = st.number_input("Number of Graded Courses Taken :", min_value=1, step = 1)
con1, con2 = st.columns(2)
with con1:
    dep = st.selectbox("Enter your Department :", ["CSE", "AIDS", "ECE", "EE", "ME", "MSME", "MT"])
with con2:
    sem = st.selectbox("Semester Completed :",[1,2,3,4,5,6,7,8])

if (not dep) or (not sem):
    st.error("Please fill the Required Columns")

with st.form("sgpa_form"):
    course_data = []
    for i in range(courses):
        st.subheader(f"Course {i+1}")
        c1, c2 = st.columns(2)
        with c1:
            credit = st.number_input("Credits", min_value=0.5, step=0.5, key=f"credit_{i}")
        with c2:
            grade = st.selectbox( "Grade", options=list(grades.keys()), key=f"grade_{i}")
        course_data.append((credit, grade))
    submitted = st.form_submit_button("📊 Calculate SGPA")

if submitted:
    global sgpa
    total_credits = 0
    weighted_sum = 0
    for credit, grade in course_data:
        total_credits += credit
        weighted_sum += credit * grades[grade]
    sgpa = round(weighted_sum / total_credits, 2)

    st.session_state["graded_courses_taken"] = courses
    st.session_state["dep"] = dep
    st.session_state["sem"] = sem

    st.session_state["last_sgpa"] = sgpa
    st.session_state["courses"] = course_data

    st.success(f"🎯 **SGPA Obtained: {sgpa}**")

if st.session_state["last_sgpa"] is not None:
    st.divider()
    st.subheader("📁 Saved Result")

    user_data = { 
        "Department": st.session_state["dep"], 
        "Semester": st.session_state["sem"],
        "Graded Courses Taken": st.session_state["graded_courses_taken"],
        "SGPA Obtained": st.session_state["last_sgpa"],
    }

    st.dataframe(pd.DataFrame([user_data]), use_container_width=True)

    df = pd.DataFrame(
        st.session_state["courses"],
        columns=["Credits", "Grade"]
    )
    st.dataframe(df, use_container_width=True)

# sum, total_credits = 0,0

# for i in range(courses):
#     st.write(f"Course {i+1} :")
#     col1, col2 = st.columns(2)
#     with col1:
#         credit = st.number_input("Enter Credits :",min_value=0.5, step = 0.5,icon =":material/credit_card_clock:", key= f"credit_course{i}")
#     with col2:
#         grade = st.text_input("Enter Grade Obtained :",icon =":material/leaderboard:", key= f"grade_course{i}")
#     if not grade:
#         st.error("Enter the Grade to move further...")
#     else:
#         if grade in ["F", "FS", "I"]:
#             sum += 0
#         elif grade in grades:
#             sum += float(credit)*grades[grade]
#         else:
#             sum += 0
#             credit = 0
#         total_credits += float(credit)
#         st.write(sum/total_credits)
# st.header(f"SGPA Obtained : {sum/total_credits}")
    


