# AI Travel Designer Agent

## Overview
The **AI Travel Designer Agent** is a multi-agent system that plans a complete travel experience.  
Built using the **OpenAI Agent SDK + Runner**, it coordinates between:

- **DestinationAgent**
- **BookingAgent**
- **ExploreAgent**

The system suggests destinations, simulates bookings, and recommends attractions and dining options based on user preferences (e.g., mood or interests).

---

## How It Works
The system takes user input (e.g., `"I want a relaxing beach vacation"`) and processes it through a sequence of specialized agents.  
Each agent uses tools to generate relevant travel plans and hands off tasks to the next agent for a seamless experience.

---

## Agents and Their Roles

### 1. DestinationAgent
- **Function:** Suggests travel destinations based on user mood or interests.  
- **Tool Used:** `suggest_destinations()` — Recommends locations (e.g., *Maldives* for relaxation) using mock data or AI-generated suggestions.  
- **Output:** A list of destination options with brief descriptions.  
- **Handoff:** Passes the chosen destination to the **BookingAgent**.

---

### 2. BookingAgent
- **Function:** Simulates travel bookings for flights and hotels.  
- **Tools Used:**  
  - `get_flights()` — Generates mock flight options (e.g., airline, price, duration).  
  - `suggest_hotels()` — Recommends hotels based on destination and budget.  
- **Output:** A travel itinerary with flight and hotel details.  
- **Handoff:** Forwards the itinerary to the **ExploreAgent**.

---

### 3. ExploreAgent
- **Function:** Suggests attractions, activities, and dining options for the destination.  
- **Tool Used:** `suggest_attractions()` — Provides mock data on attractions and restaurants.  
- **Output:** A curated list of activities and dining recommendations.  
- **Handoff:** Returns the final travel plan to the user.

---

## Tools

| Tool | Description |
|------|-------------|
| `suggest_destinations()` | Maps user preferences to suitable destinations (e.g., `"adventure"` → *New Zealand*). |
| `get_flights()` | Simulates flight options with mock data (departure times, prices, airlines). |
| `suggest_hotels()` | Recommends hotels with details like star rating, amenities, and price. |
| `suggest_attractions()` | Generates a list of activities and restaurants tailored to the destination. |

---

## Handoff Logic
The **OpenAI Agent SDK + Runner** manages the handoff process:

1. **DestinationAgent** processes user input and uses `suggest_destinations()` to provide destination options.  
2. User selects a destination → **DestinationAgent** hands off to **BookingAgent** with the destination as context.  
3. **BookingAgent** uses `get_flights()` and `suggest_hotels()` to create an itinerary → passes it to **ExploreAgent**.  
4. **ExploreAgent** uses `suggest_attractions()` to finalize the travel plan and returns it to the user.  
5. If the user changes preferences, the system loops back to the **DestinationAgent**.

---

## Flow Example

**User input:**  
