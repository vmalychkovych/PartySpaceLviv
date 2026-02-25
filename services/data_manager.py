import json
import os


def get_promotion_text():
    """Get promotion text from JSON file."""
    try:
        with open('../data/text.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get the promotion text, return empty string if not found
        return data.get("action", {}).get("text", "")

    except FileNotFoundError:
        # Return empty string if file doesn't exist
        return ""
    except json.JSONDecodeError:
        # Handle invalid JSON
        print("Error: Invalid JSON format in text.json")
        return ""
    except Exception as e:
        # Handle any other errors
        print(f"Error reading promotion text: {e}")
        return ""


def update_promotion_text(text: str) -> bool:
    """
    Update promotion text in JSON file.
    Returns True if successful, False otherwise.
    """
    try:
        # Check if file exists
        if os.path.exists('../data/text.json'):
            with open('../data/text.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # Create default structure if file doesn't exist
            data = {"action": {}}

        # Update the text
        if "action" not in data:
            data["action"] = {}
        data["action"]["text"] = text

        # Write back to file
        with open('../data/text.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"Error updating promotion text: {e}")
        return False