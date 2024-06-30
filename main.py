from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
PORT = int(os.getenv("PORT", 8000))

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    client_ip = request.client.host
    
    try:
        # Get location based on IP
        ip_info = requests.get(f"http://ip-api.com/json/{client_ip}").json()
        if ip_info.get("status") != "success":
            raise ValueError("Failed to get location data")
        city = ip_info.get("city", "unknown")
        
        # Get weather information
        weather_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}")
        weather_data = weather_response.json()
        if "error" in weather_data:
            raise ValueError("Failed to get weather data")
        temperature = weather_data["current"]["temp_c"]
        
        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}"
        return JSONResponse(content={"client_ip": client_ip, "location": city, "greeting": greeting})
    
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail="External API request failed")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
