
def check_image_info(images):
    result = {
        "correct_dimensions": True,
        "correct_aspect_ratio": True,
        "properly_sized": True,
        "required_alt_attribute": True,
        "image_details": [],
    }
    for image in images:
        image_details = {
            "src": image.get("src", None),
            "width": image.get("width", None),
            "height": image.get("height", None),
            "alt": image.get("alt", None),
            "is_svg": image.get("src", "").endswith(".svg"),
        }
        if image_details["src"]:
            if image_details["is_svg"]:
                pass
            else:
                if not image_details["width"] or not image_details["height"]:
                    result["correct_dimensions"] = False
                if not image_details["alt"]:
                    result["required_alt_attribute"] = False
                result["image_details"].append(image_details)

    return result


def check_image_aspect_ratio(image):
    width = image.get_property("width")
    height = image.get_property("height")
    natural_width = image.get_property("naturalWidth")
    natural_height = image.get_property("naturalHeight")
    if width / height != natural_width / natural_height:
        return False
    return True


def check_image_viewport_sizing(image):
    style = image.get_property("style")
    if "width: 100%;" in style or "height: 100%;" in style:
        return True
    return False


def check_image_alt_attribute(image):
    alt_text = image.get_property("alt")
    if not alt_text:
        return False
    return True

async def get_image_properties(image_handle, page):
    rendered_size = await image_handle.evaluate("el => [el.offsetWidth, el.offsetHeight]")
    rendered_aspect_ratio = rendered_size[0] / rendered_size[1]

    # Option 1: Using developer tools (might be less efficient)
    intrinsic_size_and_ratio = await page.evaluate(
        """
        const el = document.querySelector("%s")
        const computedStyle = window.getComputedStyle(el)
        return [el.naturalWidth, el.naturalHeight, computedStyle.aspectRatio]
        """ % image_handle.selector
    )

    # Option 2: Download and calculate file size (might not be optimal)
    # image_data = await page.screenshot({clip: image_handle.bounding_box()})
    # file_size = len(image_data)

    # Get current source
    current_source = await image_handle.evaluate("el => el.src")

    return {
        "rendered_size": rendered_size,
        "rendered_aspect_ratio": rendered_aspect_ratio,
        "intrinsic_size_and_ratio": intrinsic_size_and_ratio,
        "file_size": None,  # Replace with Option 2 if needed
        "current_source": current_source,
    }
