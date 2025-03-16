import requests
import json
import os

# Replace with your actual Gemini API key
GEMINI_API_KEY = ''


def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        # print(response.json()['candidates'][0]['content']['parts'][0]['text'])
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def process_json(data):
    updated_data = []
    for item in data:
        story_id = item['story_id']
        story_category = item['story_category']
        story_title = item['story_title']
        url = item['url']
        information = item['information']
        poem = item['poem']
        print(f"Processing {story_id}")
        sample = " பாடலின் விவரங்கள்:\nதிணை: பாலை (காதல் மற்றும் பிரிவு)\nதுறை: தோழி கவலையில் உணர்ச்சி நிலை\nபாடியவர்: மாமூலனார்\nபாடப்பட்டவர்: பிரிவிடை ஆற்றாளாய தலைமகள் தோழி"
        prompt = f"Information: {information} and title is {story_title} Sample for Information format is {sample}. Only provide data"
        gemini_response = get_gemini_response(prompt)
        item['song_info'] = gemini_response
        updated_data.append(item)
    return updated_data


# Load your JSON data from a local file
# Replace with the actual path to your JSON file
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

updated_json = process_json(json_data)
with open("updated_stories.json", "w") as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)
