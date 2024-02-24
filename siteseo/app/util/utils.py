from bs4 import BeautifulSoup
def is_javascript(html_content: str) -> bool:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find(id='js-loaded')