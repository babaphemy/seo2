from playwright.sync_api import sync_playwright
from siteseo.app.service import es_imager
def handle_friendly_url(url: str) -> dict:
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        images = page.query_selector_all("img")
        image_info = es_imager.check_image_info(images)
        result["images"] = image_info
    return result
async def check_image(url: str) -> dict:
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, wait_until="load")
        images = page.query_selector_all("img")
        image_info = []


        for image in images:
            rendered_size = await image.evaluate("el => [el.offsetWidth, el.offsetHeight]")
            rendered_aspect_ratio = rendered_size[0] / rendered_size[1]  
            intrinsic_aspect_ratio_and_size = await page.evaluate(
                """
const el = document.querySelector("%s")
const computedStyles = window.getComputedStyle(el)
return [el.naturalWidth, el.naturalHeight, computedStyle.aspectRatio]
""" % image.selector
            )
            image_details = {
                "src": image.get_attribute("src"),
                "alt": image.get_attribute("alt"),
                "width": image.get_attribute("width"),
                "height": image.get_attribute("height"),
                "intrinsic": intrinsic_aspect_ratio 
            }
            image_info.append(image_details)
    

        print(images)
        result["images"] = image_info
    return result


