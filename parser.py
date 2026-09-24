import xml.etree.ElementTree as ET
import logging
from typing import List
from models import Element

logger = logging.getLogger(__name__)


def parse_ui_tree(xml_string: str) -> List[Element]:
    elements = []

    try:
        root = ET.fromstring(xml_string)

        for idx, node in enumerate(root.iter("node")):
            node_class = node.get("class", "").lower()
            content_desc = node.get("content-desc", "").strip()
            text = node.get("text", "").strip()
            clickable = node.get("clickable", "false") == "true"
            focusable = node.get("focusable", "false") == "true"

            element_type = classify_element(node_class, clickable, focusable)
            if element_type is None:
                continue

            elements.append(Element(
                id=str(idx),
                type=element_type,
                label=content_desc if content_desc else None,
                text=text if text else None
            ))

        return elements

    except ET.ParseError as e:
        logger.error(f"XML parse error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected parse error: {e}")
        return []


def classify_element(node_class: str, clickable: bool, focusable: bool) -> str:
    if "button" in node_class:
        return "button"
    if "edittext" in node_class or "input" in node_class:
        return "input"
    if "imageview" in node_class or "imagebutton" in node_class:
        return "icon"
    if "tab" in node_class:
        return "tab"
    if "checkbox" in node_class:
        return "checkbox"
    if "radiobutton" in node_class:
        return "radio"
    if "switch" in node_class or "toggle" in node_class:
        return "toggle"
    if clickable or focusable:
        return "button"
    return None