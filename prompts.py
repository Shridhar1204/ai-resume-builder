resume_prompt = """
Create a ONE-PAGE professional resume.

RULES:
- Use ALL CAPS for section headings
- Use bullet points (•)
- Keep language concise and professional
- No filler text

STRUCTURE:

NAME
Target Role

PROFESSIONAL SUMMARY
• 2–3 strong summary lines

SKILLS
• Grouped bullet points

PROJECTS
Project Name
• What was built
• Technologies used
• Outcome

EXPERIENCE
(Job Title – Company – Duration) OR Fresher
• Key responsibilities or achievements

EDUCATION
• Degree – Institution – Year

INPUT DATA:
Name: {name}
Target Role: {role}
Education: {education}
Skills: {skills}
Projects: {projects}
Experience: {experience}
"""
