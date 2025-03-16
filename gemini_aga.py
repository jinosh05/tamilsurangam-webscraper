import os
import time
import requests
import json

GEMINI_API_KEY = ''

headers = {'Content-Type': 'application/json'}


def get_gemini_response(prompt, max_retries=3, retry_delay=5):
    """Fetch response from Gemini API with retries."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "")
            elif response.status_code == 429:
                print(
                    f"Rate limited (429). Retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries}).")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(
                f"Request exception: {e}. Retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries}).")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

    print(f"Failed to get response after {max_retries} attempts.")
    return None


def save_as_json(filename, dictionary_list):
    """Save data to JSON file after each API call."""
    directory = os.path.join(os.getcwd(), "scraped")
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{filename}.json")
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


def process_json(data, save_file="updated_stories"):
    """Process JSON and save data after each API response."""
    updated_data = []

    for index, item in enumerate(data, start=1):
        print(
            f"Processing {index}/{len(data)}: {item['story_id']} - {item['story_title']}")
        prompt = (
            f"Provide song info in this format:\n"
            f"பாடலின் விவரங்கள்:\n"
            f"திணை:\n"
            f"துறை:\n"
            f"பாடியவர்:\n"
            f"பாடப்பட்டவர்:\n"
            f"For: '{item.get('information', '')}', title: '{item['story_title']}' in Tamil. Just give me output."
        )

        item['song_info'] = get_gemini_response(prompt)
        updated_data.append(item)

        # Save progress after each API call
        save_as_json(save_file, updated_data)

        time.sleep(3)  # Avoid exceeding API rate limits

    print(f"Processing completed. Data saved to 'scraped/{save_file}.json'.")
    return updated_data


# Load your JSON data
file_path = "scraped/agananooru.json"

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {file_path}")
    exit()

# Process and save updated JSON
process_json(json_data, save_file="updated_stories")
