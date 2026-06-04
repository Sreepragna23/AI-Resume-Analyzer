import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO
import re
from google import genai
client = genai.Client(
     api_key=st.secrets["GEMINI_API_KEY"]
)
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")
st.caption("Analyze Resume | ATS Score | Missing Skills | Career Suggestions")

job_description = st.text_area(
    "Paste Job Description Here"
)

uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    st.success("✅ Resume Uploaded Successfully!")

    with st.expander("📄 View Resume Text"):
        st.write(text)

    skills_list = [
        "python",
        "java",
        "c programming",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "git",
        "aws",
        "docker",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pandas",
        "numpy",
        "power bi",
        "excel",
        "mysql",
        "spring boot",
        "rest api"
    ]
    # Resume Sections Detection

    st.subheader("📑 Resume Sections Analysis")

    sections = {
        "Education": "education",
        "Projects": "project",
        "Skills": "skill",
        "Internship": "internship",
        "Certifications": "certification"
     }

    for section_name, keyword in sections.items():
        if keyword.lower() in text.lower():
            st.write("✅", section_name)

        else:
            st.write("❌", section_name)
    # Resume Skills
    found_skills = []

    for skill in skills_list:
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
        if re.search(pattern, text.lower()):
            found_skills.append(skill)

    # JD Skills
    jd_skills = []

    for skill in skills_list:
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
        if re.search(pattern, job_description.lower()):
            jd_skills.append(skill)
    # Display Skills
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Resume Skills")

        if found_skills:
            for skill in found_skills:
                st.write("✅", skill)
        else:
            st.write("No skills found")

    with col2:
        st.subheader("💼 JD Skills")

        if jd_skills:
            for skill in jd_skills:
                st.write("📌", skill)
        else:
            st.write("No JD skills found")

    # Match Score
    if len(jd_skills) > 0:

        matched_skills = []

        for skill in found_skills:
            if skill in jd_skills:
                matched_skills.append(skill)

        missing_skills = []

        for skill in jd_skills:
            if skill not in found_skills:
                missing_skills.append(skill)

        score = (len(matched_skills) / len(jd_skills)) * 100
        st.markdown("---")
        st.subheader("📊 ATS Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("ATS Score", f"{score:.0f}%")

        with col2:
            st.metric("Matched Skills", len(matched_skills))

        with col3:
            st.metric("Missing Skills", len(missing_skills))
        st.divider()    

        st.progress(int(score))

        # ATS Result
        if score >= 80:
            st.success("🌟 Excellent Resume Match")
        elif score >= 60:
            st.warning("👍 Good Resume Match")
        else:
            st.error("⚠️ Needs Improvement")
        st.divider()

        if score >= 80:
            st.info("🚀 Your resume is highly ATS friendly.")
        elif score >= 60:
            st.info("📈 Your resume is good but can be improved.")
        else:
            st.info("🛠️ Add more relevant skills to improve ATS score.")    
        st.subheader("⭐ Resume Rating")
        if score >= 90:
            st.success("★★★★★ Excellent")
        elif score >= 75:
            st.success("★★★★☆ Very Good")
        elif score >= 60:
            st.warning("★★★☆☆ Good")
        else:
            st.error("★★☆☆☆ Needs Improvement")   
        st.divider()

        # Pie Chart
        st.subheader("📊 Skills Match Chart")

        labels = ["Matched Skills", "Missing Skills"]
        sizes = [len(matched_skills), len(missing_skills)]

        fig, ax = plt.subplots(figsize=(3, 3))

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%"
        )

        ax.axis("equal")

        st.pyplot(fig, use_container_width=False)

        # Missing Skills
        st.subheader("🚫 Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.error(skill)
        else:
            st.success("🎉 No Missing Skills Found")

        # Suggestions
        st.subheader("💡 Suggestions")

        if missing_skills:
            for skill in missing_skills:
                st.info(f"Learn {skill} to improve ATS score")
        else:
            st.write("✅ Your resume already matches the Job Description well.")
        # Career Roadmap

        st.subheader("🎯 Career Roadmap")

        if missing_skills:
            step = 1
            for skill in missing_skills:
                st.info(f"Step {step} → Learn {skill}")
                step += 1

            st.success(f"Step {step} → Build Projects using these skills")
            step += 1

            st.success(f"Step {step} → Apply for relevant jobs")

        else:
            st.success("🎉 You are ready to apply for this role")    
        # PDF Report Generation
        # AI Feedback

        st.subheader("🤖 AI Feedback")
        feedback = []

        if score >= 80:
            feedback.append("Your resume is highly aligned with the job description.")
        elif score >= 60:
            feedback.append("Your resume matches many requirements but can be improved.")
        else:
            feedback.append("Your resume needs additional skills for this role.")

        if "python" in found_skills:
            feedback.append("Strong Python skills detected.")
        if "java" in found_skills:
            feedback.append("Good Java knowledge identified.")
        if "spring boot" in found_skills:
            feedback.append("Backend development experience detected.")

        if missing_skills:
            feedback.append(
                f"Consider learning: {', '.join(missing_skills)}"
            )
        for item in feedback:
            st.info(item)
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)
        c.drawString(100, 800, "AI Resume Analyzer Report")
        c.drawString(100, 770, f"ATS Score: {score:.0f}%")
        c.drawString(100, 740, "Matched Skills:")
        y = 720
        for skill in matched_skills:
            c.drawString(120, y, f"- {skill}")
            y -= 20

        c.drawString(100, y - 10, "Missing Skills:")
        y -= 30

        for skill in missing_skills:
            c.drawString(120, y, f"- {skill}")
            y -= 20

        c.save()

        pdf_buffer.seek(0)
        # Resume Strength Analysis

        st.subheader("💪 Resume Strength Analysis")
        strengths = []
        if "python" in found_skills:
            strengths.append("Good Python Knowledge")

        if "java" in found_skills:
            strengths.append("Strong Java Skills")

        if "spring boot" in found_skills:
            strengths.append("Backend Development Experience")

        if "mysql" in found_skills:
            strengths.append("Database Knowledge")

        if strengths:
            for item in strengths:
                st.success(item)

# Resume Weaknesses

        st.subheader("⚠️ Areas to Improve")

        if missing_skills:
            for skill in missing_skills:
                st.warning(f"Missing Skill: {skill}")
        else:
            st.success("No major weaknesses found")

# Recommended Roles

        st.subheader("🤖 Recommended Roles")

        recommended_roles = []

        if "python" in found_skills:
            recommended_roles.append("Python Developer")

        if "java" in found_skills:
            recommended_roles.append("Java Developer")

        if "spring boot" in found_skills:
            recommended_roles.append("Backend Developer")

        if "html" in found_skills and "css" in found_skills:
            recommended_roles.append("Frontend Developer")

        if "sql" in found_skills or "mysql" in found_skills:
            recommended_roles.append("Database Developer")

        for role in recommended_roles:
            st.success(role)

        st.divider()
        st.subheader("🧠 AI Resume Summary")
        prompt = f"""
        Analyze this resume.

        Resume:
        {text}

        Job Description:
        {job_description}

        Provide:
        1. Resume Summary
        2. Strengths
        3. Weaknesses
        4. Improvement Suggestions
        """

        with st.spinner("🧠 Generating AI Resume Summary..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
        )

        st.success(response.text)
        st.subheader("🎤 AI Interview Questions")

        question_prompt = f"""
        Based on this resume and job description,
        generate 10 interview questions.

        Resume:
        {text}

        Job Description:
        {job_description}

        Questions should cover:
        - Technical Skills
        - Projects
        - Problem Solving
        - HR Questions
        """

        with st.spinner("🎤 Generating Interview Questions..."):
            questions_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=question_prompt
                )

        st.write(questions_response.text)


        st.download_button(
            label="📄 Download ATS Report",
            data=pdf_buffer,
            file_name="ATS_Report.pdf",
            mime="application/pdf"
        )    