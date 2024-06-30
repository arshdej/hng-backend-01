from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    client_ip = request.client.host
    # Get location based on IP
    ip_info = requests.get(f"http://ip-api.com/json/{client_ip}").json()
    city = ip_info.get("city", "unknown")
    
    temperature = 32

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}"

    return JSONResponse(content={"client_ip": client_ip, "location": city, "greeting": greeting})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
