import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from app.service import es_imager
from app.util import utils

def get_page_info(url):
    result_dict = {}
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")

    result_dict["title"] = soup.title.text.strip()

    headings = soup.find_all("h1")
    result_dict["h1s"] = [heading.text.strip() for heading in headings]

    meta_description = soup.find("meta", attrs={"name": "description"})
    result_dict["meta_description"] = meta_description["content"] if meta_description else None

    return result_dict

def handle_friendly_url(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")

    non_friendly = {"friendly": True, "link_details": []}

    for link in soup.find_all("a"):
        link_details = {
            "href": link.get("href"),
            "text": link.text.strip(),
            "rel": link.get("rel"),
            "target": link.get("target"),
            "title": link.get("title"),
        }

        # Check if link is descriptive even if text is empty
        if not link_details["text"]:
            # Check if title exists and has content
            if link_details["title"]:
                link_details["text"] = link_details["title"].strip()
            else:
                non_friendly["friendly"] = False

        # Check for common non-descriptive text (modify as needed)
        if link_details["text"].lower() in [
            "click here",
            "more",
            "read more",
        ]:
            non_friendly["friendly"] = False

        # Check for excessively long text (modify threshold as needed)
        if len(link_details["text"]) > 60:
            non_friendly["friendly"] = False

        non_friendly["link_details"].append(link_details)

    return non_friendly

def image_check(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    result = {"friendly": True, "link_details": []}

    soup = BeautifulSoup(response.content, "html.parser")
    if utils.is_javascript:
        chrome_options = Options()
        driver = webdriver.Chrome(executable_path="/chromedriver/chromedriver")
    all_img = soup.find_all("img")
    print(soup)

    image_info = es_imager.check_image_info(all_img)
    result["images"] = image_info
    return result




