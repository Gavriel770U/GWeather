import python_weather
import asyncio
import os

async def get_weather(city: str):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        
        return weather.current

async def get_current_forecast(city: str):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

        for forecast in weather.forecasts:
            for hourly in forecast.hourly:
                print(f' --> {hourly!r}')
            return forecast

# test only:
        
if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(get_weather('Lod'))   
    asyncio.run(get_current_forecast('Lod'))
    