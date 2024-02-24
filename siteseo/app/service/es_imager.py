
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
            "width": int(image.get("width", 0)),
            "height": int(image.get("height", 0)),
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
