Game Master Agent (Fantasy Adventure Game) README

Overview

The Game Master Agent is a multi-agent system that runs a text-based fantasy adventure game. Built with the OpenAI Agent SDK + Runner, it coordinates between NarratorAgent, MonsterAgent, and ItemAgent to narrate a story, handle combat, and manage inventory based on player choices.

How It Works

The system guides the player through a fantasy adventure, responding to their choices (e.g., "explore cave" or "fight monster"). Agents use tools to generate story events, resolve combat, and manage rewards, with handoffs ensuring dynamic gameplay.

Agents and Their Roles





NarratorAgent:





Function: Progresses the story based on player choices.



Tool Used: generate_event() - Creates story events (e.g., "You find a hidden treasure" or "A dragon appears").



Output: Narrative text describing the current game state.



Hល: If the choice leads to combat, hands off to MonsterAgent; if it involves items, hands off to ItemAgent.



MonsterAgent:





Function: Manages combat phases.





Tool Used: roll_dice() - Determines combat outcomes (e.g., hit/miss, damage).



Output: Combat results (e.g., "You defeated the goblin").



Handoff: Returns to NarratorAgent for story continuation or ItemAgent for loot.





ItemAgent:





Function: Manages player inventory and rewards.



Tool Used: generate_item() - Generates random or context-based items (e.g., "Magic Sword").



Output: Updated inventory list.



Handoff: Returns to NarratorAgent for next story event.

Tools





generate_event(): Creates dynamic story events based on player choices and game state.



roll_dice(): Simulates dice rolls for combat or chance events (e.g., 1-20 scale).



generate_item(): Adds items to inventory or rewards after events.

Handoff Logic

The OpenAI Agent SDK + Runner manages dynamic handoffs:





The NarratorAgent uses generate_event() to advance the story based on player input.



If the event involves combat, it hands off to MonsterAgent, which uses roll_dice() to resolve the fight.



If the event involves items or rewards, it hands off to ItemAgent to update inventory with generate_item().



After combat or item updates, control returns to NarratorAgent for the next story event.



The system loops based on player choices, ensuring varied gameplay.

Flow Example





Player inputs: "Enter the dark forest."



NarratorAgent: Generates event, "A wild boar charges at you!" using generate_event().



MonsterAgent: Uses roll_dice() to resolve combat (e.g., "You hit the boar for 10 damage").



ItemAgent: Awards loot, e.g., "Boar’s Tusk added to inventory" using generate_item().



NarratorAgent: Continues story, "The forest grows darker ahead."



Output: A continuous narrative with combat and inventory updates.

Implementation Details





Framework: OpenAI Agent SDK + Runner for agent coordination and tool execution.



Tools: Python functions for event generation, dice rolling, and item management.



Handoff: SDK runner manages context-aware transitions between agents.



Flexibility: Can add more agents (e.g., NPC dialogue agent) or tools (e.g., map generator).

Running the Agent





Install dependencies: OpenAI Agent SDK, Python 3.8+.



Run the script: python game_master.py.



Input choices via console or UI.



Follow the narrative, engage in combat, and collect items.