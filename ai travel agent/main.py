import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, set_tracing_disabled
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from typing_extensions import TypedDict

# Load environment variables
load_dotenv()

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file.")

# Initialize OpenAI provider with Gemini API settings
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)

# Define typed dictionaries for mock data
class FlightInfo(TypedDict):
    airline: str
    departure: str
    arrival: str
    price: int

class HotelInfo(TypedDict):
    name: str
    rating: float
    price: int
    location: str

# Mock data for flights and hotels
MOCK_FLIGHTS: Dict[str, List[FlightInfo]] = {
    "NYC-LON": [
        {"airline": "Delta", "departure": "08:00", "arrival": "20:00", "price": 750},
        {"airline": "British Airways", "departure": "10:30", "arrival": "22:30", "price": 800},
        {"airline": "Virgin Atlantic", "departure": "14:15", "arrival": "02:15", "price": 700},
    ],
    "NYC-PAR": [
        {"airline": "Air France", "departure": "09:00", "arrival": "21:30", "price": 850},
        {"airline": "Delta", "departure": "13:45", "arrival": "02:15", "price": 780},
    ],
    "SFO-TYO": [
        {"airline": "ANA", "departure": "11:00", "arrival": "15:00", "price": 1200},
        {"airline": "United", "departure": "14:30", "arrival": "18:30", "price": 1100},
    ],
    "default": [
        {"airline": "Generic Airlines", "departure": "07:00", "arrival": "10:00", "price": 300},
        {"airline": "Budget Air", "departure": "15:00", "arrival": "18:00", "price": 250},
    ]
}

MOCK_HOTELS: Dict[str, List[HotelInfo]] = {
    "Paris": [
        {"name": "Le Meurice", "rating": 4.8, "price": 450, "location": "City Center"},
        {"name": "Hotel du Louvre", "rating": 4.5, "price": 300, "location": "Near Louvre"},
        {"name": "Ibis Budget", "rating": 3.2, "price": 80, "location": "Suburb"},
    ],
    "London": [
        {"name": "The Ritz", "rating": 4.9, "price": 500, "location": "Piccadilly"},
        {"name": "Premier Inn", "rating": 4.0, "price": 120, "location": "City Center"},
    ],
    "Tokyo": [
        {"name": "Park Hotel Tokyo", "rating": 4.7, "price": 350, "location": "Shiodome"},
        {"name": "APA Hotel", "rating": 3.8, "price": 100, "location": "Shinjuku"},
    ],
    "default": [
        {"name": "Grand Hotel", "rating": 4.5, "price": 200, "location": "City Center"},
        {"name": "Comfort Inn", "rating": 3.5, "price": 90, "location": "Downtown"},
    ]
}

# Define context for the agent
@dataclass
class TravelContext:
    user_id: str
    current_location: Optional[str] = None
    destination: Optional[str] = None
    travel_dates: Optional[Dict[str, str]] = None
    budget: Optional[int] = None

# Define input/output schemas
class GetFlightsInput(BaseModel):
    origin: str
    destination: str
    date: str

class GetFlightsOutput(BaseModel):
    flights: List[FlightInfo]

class SuggestHotelsInput(BaseModel):
    city: str
    check_in: str
    check_out: str
    budget: int

class SuggestHotelsOutput(BaseModel):
    hotels: List[HotelInfo]

# Error handling function for tools
async def tool_error_handler(ctx: RunContextWrapper[TravelContext], error: Exception) -> str:
    return f"Tool failed: {str(error)}"

# Function tools
@function_tool(failure_error_function=tool_error_handler)
async def get_flights(input: GetFlightsInput) -> GetFlightsOutput:
    """Search for available flights between two cities on a specific date.
    
    Args:
        input: Pydantic model with origin, destination, and date
    """
    try:
        route = f"{input.origin.upper()}-{input.destination.upper()}"
        flights = MOCK_FLIGHTS.get(route, MOCK_FLIGHTS["default"])
        
        # Add price variation based on date
        date_obj = datetime.strptime(input.date, "%Y-%m-%d")
        if date_obj.weekday() >= 5:  # Weekend
            flights = [{**f, "price": int(f["price"] * 1.2)} for f in flights]
        
        return GetFlightsOutput(flights=flights)
    except Exception as e:
        raise ValueError(f"Failed to fetch flights: {str(e)}")

@function_tool(failure_error_function=tool_error_handler)
async def suggest_hotels(input: SuggestHotelsInput) -> SuggestHotelsOutput:
    """Find hotel options in a city within a specified budget.
    
    Args:
        input: Pydantic model with city, check-in, check-out, and budget
    """
    try:
        hotels = MOCK_HOTELS.get(input.city.title(), MOCK_HOTELS["default"])
        filtered_hotels = [h for h in hotels if h["price"] <= input.budget]
        
        if not filtered_hotels:
            filtered_hotels = [min(hotels, key=lambda x: x["price"])]
        
        return SuggestHotelsOutput(hotels=filtered_hotels)
    except Exception as e:
        raise ValueError(f"Failed to suggest hotels: {str(e)}")

# Define specialized agents
destination_agent = Agent[TravelContext](
    name="Destination Agent",
    instructions="""
You are a travel assistant specializing in destination recommendations.

- Suggest 3–5 destinations based on the user's mood (e.g., relaxed, adventurous, romantic) or interests (e.g., beaches, mountains, culture).
- Provide a brief description for each destination and why it fits.
- Ensure diversity in recommendations (mix of international and local options).
- Do not handle bookings or itineraries. Focus only on destination suggestions.
- Use the context to personalize recommendations (e.g., consider user's current_location).
""",
    model=model,
)

booking_agent = Agent[TravelContext](
    name="Booking Agent",
    instructions="""
You are a travel booking assistant handling logistics.

- Use `get_flights()` to fetch flight options from the user's current_location to the destination.
- Use `suggest_hotels()` to provide 2–3 hotel options in the destination city.
- Confirm travel dates and budget with the user before proceeding (use context if available).
- Structure output clearly: flights first, then hotels.
- Do not suggest destinations or attractions. Focus on logistics.
""",
    model=model,
    tools=[get_flights, suggest_hotels],
)

explore_agent = Agent[TravelContext](
    name="Explore Agent",
    instructions="""
You are a travel explorer assistant recommending attractions and experiences.

- Suggest 3–5 attractions, activities, or local food options in the destination.
- Include a mix of popular and unique experiences with brief descriptions.
- Do not provide flight or hotel information. Focus on exploration.
- Use the destination from the context if available.
""",
    model=model,
)

# Main orchestrator agent
main_agent = Agent[TravelContext](
    name="AI Travel Designer Agent",
    instructions="""
You are an AI Travel Designer coordinating the travel planning process.

1. If the user needs help choosing a destination, hand off to the Destination Agent.
2. Once a destination is chosen, hand off to the Booking Agent for flights and hotels.
3. After logistics are confirmed, hand off to the Explore Agent for attractions.
4. Maintain context (user_id, current_location, destination, travel_dates, budget) throughout.
5. Confirm details with the user before proceeding to the next step.
6. Summarize the complete travel plan at the end.

Guidelines:
- Keep responses clear, concise, and organized.
- Use context to personalize the experience.
- Handle errors gracefully and inform the user if issues arise.
""",
    model=model,
    handoffs=[destination_agent, booking_agent, explore_agent],
    tools=[get_flights, suggest_hotels],
)

# Disable tracing for simplicity
set_tracing_disabled(disabled=True)


async def main():
    # Initialize conversation history
    conversation_history = []
    while True:
        # Get user input
        user_input = input("You: ")
        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Run the agent with the updated conversation history
        result = await Runner.run(main_agent, conversation_history)
        
        # Print the agent's response
        print(f"Assistant: {result.final_output}")
        
        # Update conversation history with the agent's response
        conversation_history = result.to_input_list()

# Run the async main function
asyncio.run(main())