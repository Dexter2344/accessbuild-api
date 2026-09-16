from typing import List


def calculate_accessibility_score(elements: List) -> dict:
    """
    Calculate accessibility score based on labeled vs unlabeled elements.
    
    Scoring logic:
    - Only interactive elements count (buttons, inputs, links, icons)
    - Static text elements don't require labels
    - A label can come from: accessibility label (content-desc) OR visible text
    """
    
    # Interactive element types that MUST have labels
    interactive_types = {"button", "input", "icon", "link", "checkbox", "radio", "toggle", "tab"}
    
    # Count only interactive elements
    interactive = [e for e in elements if e.type.lower() in interactive_types]
    
    total = len(interactive)
    
    if total == 0:
        return {
            "score": "N/A",
            "grade": "No interactive elements found",
            "total": 0,
            "labeled": 0,
            "unlabeled": 0,
            "percentage": 0.0,
            "recommendation": "No interactive elements to audit on this screen."
        }
    
    # Count labeled elements (has accessibility label OR visible text)
    labeled = sum(
        1 for e in interactive 
        if (e.label and e.label.strip()) or (e.text and e.text.strip())
    )
    
    unlabeled = total - labeled
    percentage = round((labeled / total) * 100, 1)
    
    # Determine grade
    if percentage >= 90:
        score = "A"
        recommendation = "Excellent. This screen is accessible to screen reader users."
    elif percentage >= 70:
        score = "B"
        recommendation = "Good. Most elements are labeled. Minor improvements needed."
    elif percentage >= 50:
        score = "C"
        recommendation = "Needs work. Half of interactive elements lack labels. Fix high-traffic screens first."
    elif percentage >= 25:
        score = "D"
        recommendation = "Urgent. Most elements are invisible to screen readers. Immediate fixes required."
    else:
        score = "F"
        recommendation = f"Critical. {unlabeled} out of {total} interactive elements have no labels. Visually impaired users cannot use this screen."
    
    return {
        "score": score,
        "grade": f"{score} — {percentage}% accessible",
        "total": total,
        "labeled": labeled,
        "unlabeled": unlabeled,
        "percentage": percentage,
        "recommendation": recommendation
    }