from bs4 import BeautifulSoup
import requests
def is_javascript(html_content: str) -> bool:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find(id='js-loaded')
def get_geolocation():
    # Use a geolocation service to determine the approximate location
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    location = (
        data.get("city", "Unknown City")
        + ", "
        + data.get("region", "Unknown Region")
        + ", "
        + data.get("country", "Unknown Country")
    )
    return location