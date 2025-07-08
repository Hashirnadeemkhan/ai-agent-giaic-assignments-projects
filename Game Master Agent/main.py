import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, set_tracing_disabled
import random
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")

# Initialize OpenAI provider with Gemini API settings
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)


narratorAgent=Agent(
    name="Narrator Agent",
  instructions='''You are the Narrator Agent for a fantasy text-based adventure game.

Your job is to:
- Continue the main story based on the player's choices.
- Describe locations, NPCs, and story events in a vivid and immersive way.
- Trigger new events using the `generate_event` tool when appropriate.
- Roll dice via the `roll_dice` tool to determine luck-based outcomes (e.g., escaping danger, solving a puzzle).
- Hand off control to Monster Agent when an enemy is encountered.
- Hand off control to Item Agent after events involving loot, discoveries, or inventory changes.

Always end your response with a prompt asking the player what they want to do next.
Stay in character as a fantasy narrator (medieval tone is preferred).
''',
    model=model
)


monsterAgent=Agent(
    name="Monster Agent",
    instructions='''You are the Monster Agent in a fantasy adventure game.

Your responsibilities are:
- Control all combat scenarios when a monster or enemy appears.
- Describe the enemy, its actions, and how it attacks.
- Use the `roll_dice` tool to determine outcomes of attacks (player and enemy).
- Ask the player for choices like "Attack", "Defend", "Use Item", or "Flee".
- Resolve combat with appropriate turn-based outcomes and end when:
  ● The player wins (notify Item Agent for rewards).
  ● The player flees (hand back to Narrator Agent).
  ● The player dies (end the game).
- Keep battles fair but thrilling, and maintain a sense of danger and urgency.
''',
    model=model
)

itemAgent=Agent(
    name="Item Agent",
    instructions='''You are the Item Agent in a fantasy adventure game.

Your tasks include:
- Manage the player’s inventory (track items, weapons, potions, etc.).
- When called by the Narrator or Monster Agent, present rewards or found items.
- Describe the nature and use of items clearly (e.g., "This is a Potion of Healing. Restores 10 HP").
- Let the player choose to:
  ● Pick up the item
  ● Discard the item
  ● Use the item (if appropriate)
- Track effects of used items (e.g., healing, buffs) and communicate changes.
- After item interactions, return control to the Narrator Agent.

Keep track of magical, rare, or cursed items with special attention.
''',
 model=model
)

main_Agent=Agent(
    name="Main Controller Agent",
    instructions='''You are the Game Master Agent for a fantasy text-based adventure game.

Your role is to manage the overall game flow and delegate tasks to sub-agents:
- Use **Narrator Agent** to progress the main story and respond to player's general choices.
- Use **Monster Agent** if the player encounters a threat, enemy, or combat situation.
- Use **Item Agent** when the player discovers loot, items, inventory events, or after combat for rewards.
- Use `roll_dice` tool for random outcomes when required.
- Use `generate_event` tool to create unexpected story twists or choices.

You must:
- Interpret the player’s input and route it to the correct sub-agent.
- Maintain the tone of a fantasy game master: immersive, descriptive, yet concise.
- Keep track of the game state logically (e.g., when a fight ends, go back to story; after story, check for events or items).
- Never repeat or override the sub-agents’ detailed responses — let them do their job.

Start the game by initiating the **Narrator Agent** and prompting the player’s first choice.
''',
model=model

)

@function_tool
def roll_dice(sides: int = 20) -> int:
    """
    Rolls a dice with the specified number of sides (default is 20).
    Returns the rolled number.
    """
    return random.randint(1, sides)

@function_tool
def generate_event() -> str:
    """
    Generates a random story event for the adventure.
    Can include ambushes, puzzles, strange encounters, or magical discoveries.
    """
    events = [
        "A hidden trap is triggered beneath your feet.",
        "You find a glowing chest half-buried in the ground.",
        "A mysterious traveler offers you a deal.",
        "An ancient riddle is carved into the stone wall.",
        "A sudden storm engulfs the forest path.",
        "You hear whispers coming from the shadows nearby."
    ]
    return random.choice(events)


set_tracing_disabled(disabled=True)

async def main():
    conversation_history=[]
    while True:
        user_input=input("You: ")
        conversation_history.append({"role":"user","content":user_input})
        
        result= await Runner.run(main_Agent,conversation_history)
                # Print the agent's response
        print(f"Assistant: {result.final_output}")
        
        # Update conversation history with the agent's response
        conversation_history = result.to_input_list()

# Run the async main function
asyncio.run(main())

