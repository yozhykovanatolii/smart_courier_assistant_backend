import httpx
from config import settings
from exceptions.external_service_exception import OptimizationRouteException

class OpenRouteClient:
    def __init__(self):
        self.__api_key = settings.openroute_api_key
    
    async def optimize_route(self, jobs: list[dict], courier_coordinates: list[float]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openrouteservice.org/optimization",
                headers={
                    "Authorization": f'{self.__api_key}',
                    "Content-Type": "application/json",
                },
                json={
                    "jobs": jobs,
                    "vehicles": [
                        {
                            "id": 1,
                            "start": courier_coordinates,
                            "profile": "driving-car",
                        }
                    ],
                },
            )
        if response.status_code != 200:
            raise OptimizationRouteException()
        
        data = response.json()
        return data['routes'][0]['steps']
    
    
    async def get_route_polyne(self, coordinates: list[list[float]]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openrouteservice.org/v2/directions/driving-car/geojson",
                headers={
                    "Authorization": f'{self.__api_key}',
                    "Content-Type": "application/json",
                },
                json={'coordinates': coordinates},
            ) 
        data = response.json()
        return data['features'][0]['geometry']['coordinates']