resume_prompt = """
Create an ATS-friendly resume for a student.

Name: {name}
Target Role: {role}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Generate:
1. Professional Summary
2. Skills (bulleted)
3. Project Descriptions
4. Experience (if applicable)
5. Short Cover Letter
6. Portfolio About Me section
"""
