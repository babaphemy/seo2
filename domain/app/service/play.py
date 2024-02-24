from playwright.sync_api import sync_playwright
def handle_friendly_url(url: str) -> dict:
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        all_links = page.query_selector_all("a")
        non_friendly = {"friendly": True, "link_details": []}
        for link in all_links:
            link_details = {
                "href": link.get_attribute("href"),
                "text": link.inner_text().strip(),
                "rel": link.get_attribute("rel"),
                "target": link.get_attribute("target"),
                "title": link.get_attribute("title"),
            }
            txt = link.inner_text().strip()
            # link has descriptive text
            if not link_details["text"]:
                non_friendly["friend"] = False
            if txt.lower() in [
                "click here",
                "more",
                "read more"
            ]:
                non_friendly["friend"] = False
            if len(txt) > 60:
                non_friendly["friend"] = False
        result["non_friendly_links"] = non_friendly
    return result


