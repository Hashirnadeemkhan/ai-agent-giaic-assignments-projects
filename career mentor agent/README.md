Career Mentor Agent README
Overview
The Career Mentor Agent is a multi-agent system designed to guide students through career exploration. It uses the OpenAI Agent SDK + Runner to coordinate between three specialized agents: CareerAgent, SkillAgent, and JobAgent. These agents work together to recommend career paths, provide skill-building plans, and share real-world job roles based on user interests.
How It Works
The system takes user input (e.g., interests like "technology" or "creative arts") and processes it through a sequence of agents with specific roles. The agents use tools to generate relevant outputs and hand off tasks to each other to provide a cohesive career exploration experience.
Agents and Their Roles

CareerAgent:

Function: Suggests career paths based on user interests.
Tool Used: suggest_careers() - Generates a list of career paths tailored to the user's input (e.g., "software engineering" for technology interest).
Output: A list of recommended career fields.
Handoff: Passes the selected career to the SkillAgent for skill recommendations.


SkillAgent:

Function: Provides a skill-building roadmap for the chosen career.
Tool Used: get_career_roadmap() - Generates a detailed plan of skills (e.g., programming, communication) and learning resources (e.g., online courses, certifications).
Output: A structured roadmap with skills and resources.
Handoff: Forwards the roadmap and career choice to the JobAgent for real-world job insights.


JobAgent:

Function: Shares real-world job roles and descriptions for the selected career.
Tool Used: get_job_roles() - Retrieves job titles, responsibilities, and typical employers (mock data for simulation).
Output: A list of job roles with details.
Handoff: Returns the final output to the user or loops back to CareerAgent if the user wants to explore another career.



Tools

suggest_careers(): Maps user interests to career fields using predefined data or AI-generated suggestions.
get_career_roadmap(): Creates a step-by-step skill acquisition plan, including timelines and resources.
get_job_roles(): Provides mock job listings with details like salary ranges, required experience, and company types.

Handoff Logic
The handoff between agents is managed by the OpenAI Agent SDK + Runner:

The CareerAgent processes the initial user input and uses suggest_careers() to generate career options.
Once the user selects a career, the CareerAgent hands off to the SkillAgent with the career choice as context.
The SkillAgent uses get_career_roadmap() and passes the roadmap to the JobAgent.
The JobAgent finalizes the output with get_job_roles() and returns it to the user.
If the user wants to explore another career, the system loops back to the CareerAgent.

Flow Example

User inputs: "I’m interested in technology."
CareerAgent: Suggests "Software Engineering, Data Science, Cybersecurity" using suggest_careers().
User selects "Software Engineering."
SkillAgent: Generates a roadmap (e.g., learn Python, complete a coding bootcamp) using get_career_roadmap().
JobAgent: Shares roles like "Junior Developer, Backend Engineer" with details using get_job_roles().
Output: A complete career guide from exploration to job roles.

Implementation Details

Framework: OpenAI Agent SDK + Runner handles agent coordination and tool execution.
Tools: Implemented as Python functions that return mock or AI-generated data.
Handoff: Managed via the SDK’s runner, which routes tasks between agents based on context and user input.
Scalability: The system can be extended to include more tools (e.g., salary estimator) or agents (e.g., mentorship finder).

Running the Agent

Install dependencies: OpenAI Agent SDK, Python 3.8+.
Run the main script: python career_mentor.py.
Input interests via the console or UI (if implemented).
Follow the prompts to select a career and receive the roadmap and job roles.

