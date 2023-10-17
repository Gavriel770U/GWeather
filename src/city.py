import requests

def get_city_name() -> str:
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        city = data.get('city', 'Unknown')
        return city
    except Exception as e:
        return "Unknown"