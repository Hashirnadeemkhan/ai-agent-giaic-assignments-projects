AI Travel Designer Agent README

Overview

The AI Travel Designer Agent is a multi-agent system that plans a complete travel experience. Built using the OpenAI Agent SDK + Runner, it coordinates between DestinationAgent, BookingAgent, and ExploreAgent to suggest destinations, simulate bookings, and recommend attractions and dining options based on user preferences (e.g., mood or interests).

How It Works

The system takes user input (e.g., "I want a relaxing beach vacation") and processes it through a sequence of specialized agents. Each agent uses tools to generate relevant travel plans and hands off tasks to the next agent for a seamless experience.

Agents and Their Roles





DestinationAgent:





Function: Suggests travel destinations based on user mood or interests.



Tool Used: suggest_destinations() - Recommends locations (e.g., Maldives for relaxation) using mock data or AI-generated suggestions.



Output: A list of destination options with brief descriptions.



Handoff: Passes the chosen destination to the BookingAgent.



BookingAgent:





Function: Simulates travel bookings for flights and hotels.



Tools Used:





get_flights(): Generates mock flight options (e.g., airline, price, duration).



suggest_hotels(): Recommends hotels based on destination and budget.



Output: A travel itinerary with flight and hotel details.



Handoff: Forwards the itinerary to the ExploreAgent.



ExploreAgent:





Function: Suggests attractions, activities, and dining options for the destination.



Tool Used: suggest_attractions() - Provides mock data onterestinations() - Provides a list of attractions and restaurants.



Output: A curated list of activities and dining recommendations.



Handoff: Returns the final travel plan to the user.

Tools





suggest_destinations(): Maps user preferences to suitable destinations (e.g., "adventure" → New Zealand).



get_flights(): Simulates flight options with mock data (e.g., departure times, prices).



suggest_hotels(): Recommends hotels with details like star rating and amenities.



suggest_attractions(): Generates a list of activities and restaurants tailored to the destination.

Handoff Logic

The OpenAI Agent SDK + Runner manages the handoff process:





The DestinationAgent processes user input and uses suggest_destinations() to provide destination options.



User selects a destination, and the DestinationAgent hands off to the BookingAgent with the destination as context.



The BookingAgent uses get_flights() and suggest_hotels() to create an itinerary, then passes it to the ExploreAgent.



The ExploreAgent uses suggest_attractions() to finalize the travel plan and returns it to the user.



If the user changes preferences, the system loops back to the DestinationAgent.

Flow Example





User inputs: "I want a relaxing beach vacation."



DestinationAgent: Suggests "Maldives, Bali, Seychelles" using suggest_destinations().



User selects "Maldives."



BookingAgent: Provides mock flight options (e.g., "Emirates, $1200, 8h") and hotel options (e.g., "5-star resort, $300/night") using get_flights() and suggest_hotels().



ExploreAgent: Recommends activities (e.g., snorkeling, spa day) and restaurants using suggest_attractions().



Output: A complete travel plan with destinations, bookings, and activities.

Implementation Details





Framework: OpenAI Agent SDK + Runner for agent coordination and tool execution.



Tools: Python functions returning mock data for flights, hotels, and attractions.



Handoff: Managed by the SDK’s runner, ensuring context is preserved across agents.



Extensibility: Can integrate real APIs (e.g., Expedia, TripAdvisor) for live data.

Running the Agent





Install dependencies: OpenAI Agent SDK, Python 3.8+.



Run the script: python travel_designer.py.



Input travel preferences via console or UI.



Follow prompts to select a destination and receive the full travel plan.