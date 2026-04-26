# loading all the libraries and frameworks
from dotenv import load_dotenv
load_dotenv()

import os
import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "Error: API key not found"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    print("DEBUG:", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather data')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"

#  searching for weather in a city tavily news tool
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city : str) -> str:
  """Get latest news about the city"""
  response = tavily_client.search(query=f"latest news about {city}", search_depth="advanced")
  return f"Latest news about {city}: {response['results'][0]['title']}"