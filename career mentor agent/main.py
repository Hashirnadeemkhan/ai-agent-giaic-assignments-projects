import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, set_tracing_disabled

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

# Initialize OpenAI provider with Gemini API settings
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)

# Define the career roadmap tool
@function_tool
def get_career_roadmap(name: str, career_field: str) -> str:
    """
    Tool to generate a skill roadmap for a given career field.
    Args:
        name (str): The user's name.
        career_field (str): The career field (e.g., 'Software Engineering').
    Returns:
        str: A formatted string with the career roadmap.
    """
    return f"Career roadmap for {name} in {career_field}: Start with foundational skills (e.g., Python, basic algorithms), progress to intermediate projects (e.g., small AI models), and specialize in advanced topics (e.g., deep learning, cloud deployment)."

# Define CareerAgent
career_agent = Agent(
    name="CareerAgent",
    instructions="""
You are CareerAgent, an intelligent career guidance assistant. Suggest 3–5 career fields based on the user's interests, personality, educational background, and passions. Ask clarifying questions if needed, then provide short, insightful reasons for each recommendation. Focus on long-term success and personal satisfaction, tailoring responses to the user’s unique profile. Be practical, motivational, and forward-looking.
""",
    model=model,
    tools=[get_career_roadmap]
)

# Define SkillAgent
skill_agent = Agent(
    name="SkillAgent",
    instructions="""
You are SkillAgent, a personalized skill-development strategist. Create clear, actionable skill-building roadmaps for users aiming to grow in a specific field. Divide the plan into beginner, intermediate, and advanced phases. Suggest tools, platforms, and learning resources for each phase. Recommend real-world projects and timelines based on the user’s knowledge level, time availability, and learning preferences.
""",
    model=model,
    tools=[get_career_roadmap]
)

# Define JobAgent
job_agent = Agent(
    name="JobAgent",
    instructions="""
You are JobAgent, a smart job-matching advisor. Suggest 3–5 real-world job roles and entry-level positions that fit the user's current skills, goals, and educational background (e.g., recent graduate). For each role, provide:
- **Title**: The job title.
- **Description**: A brief overview of the role.
- **Key Responsibilities**: Main tasks the role involves.
- **Required Skills**: Essential skills or qualifications.
- **Industries**: Common industries hiring for this role.
Focus on relevant, realistic, and achievable roles, especially for users with little professional experience but strong practical skills or project work. For AI/ML roles, prioritize entry-level positions suitable for recent graduates.
""",
    model=model,
    tools=[get_career_roadmap]
)

# Define TriageAgent
triage_agent = Agent(
    name="TriageAgent",
    instructions="""
You are TriageAgent, the central coordinator that routes user queries to the most appropriate specialized agent:

1. **CareerAgent**: For users exploring career paths based on interests, personality, or background (e.g., "What career should I choose?").
2. **SkillAgent**: For users seeking a skill-building roadmap in a specific field (e.g., "How do I become a data scientist?").
3. **JobAgent**: For users asking about job roles or positions matching their skills or goals (e.g., "What jobs can I get in AI?").

Analyze the user’s query and conversation history to identify intent. If the query explicitly mentions job roles, positions, or employment opportunities, route to JobAgent. If unclear, ask one short clarifying question. Be concise, practical, and user-focused with a motivational tone. Log which agent is selected for debugging.
""",
    model=model,
    tools=[get_career_roadmap],
    handoffs=[career_agent, skill_agent, job_agent],
)

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

# Initialize conversation history
conversation_history = []

def print_welcome_message():
    print("\n=== Career Guidance Assistant ===")
    print("Hello! I'm here to help with career planning, skill development, or job matching.")
    print("Type your query below, or type 'exit' to quit.")
    print("================================\n")

def format_history_for_context():
    """Format conversation history for passing to the agent."""
    if not conversation_history:
        return ""
    return "\n".join([f"User: {entry['user']}\nAgent: {entry['agent']}" for entry in conversation_history])

def main():
    print_welcome_message()
    
    while True:
        # Get user input
        query = input("Enter your query (or 'exit' to quit): ").strip()
        
        if query.lower() == 'exit':
            print("Goodbye! Best of luck on your career journey!")
            break
        
        if not query:
            print("Please enter a valid query.")
            continue
        
        # Append user query to history
        conversation_history.append({"user": query, "agent": None})
        
        # Prepare context with history (limit to last 3 for focus)
        context = format_history_for_context()
        full_query = f"{context}\n\nCurrent Query: {query}" if context else query
        
        try:
            # Run the query through TriageAgent
            result = Runner.run_sync(
                starting_agent=triage_agent,
                input=full_query,
            )
            
            # Get the final output
            response = result.final_output or "Sorry, I couldn't generate a response. Let me provide some default AI/ML job roles for a recent graduate:\n" + fallback_ai_ml_jobs()
            
            # Update the latest history entry with the agent's response
            conversation_history[-1]["agent"] = response
            
            # Print the response
            print("\nAssistant:", response, "\n")
            
            # Keep history manageable (last 3 interactions)
            if len(conversation_history) > 3:
                conversation_history.pop(0)
                
        except Exception as e:
            print(f"\nError processing query: {str(e)}")
            print("Please try again or check your API key and connection.\n")


if __name__ == "__main__":
    main()