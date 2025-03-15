import json
import subprocess
import time

# உங்கள் Gemini API விசையை இங்கே உள்ளிடவும்
API_KEY = ""


def get_saraamsam(text):
    """curl கட்டளையைப் பயன்படுத்தி ஜெமினி API இலிருந்து தமிழ் சாராம்சத்தைப் பெறுகிறது."""
    try:
        command = [
            "curl",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}",
            "-H", "Content-Type: application/json",
            "-X", "POST",
            "-d", json.dumps({
                "contents": [{"parts": [{"text": f"கொடுக்கப்பட்ட உரைக்கு 512 எழுத்துகளுக்குள் தமிழ் சாராம்சம் வழங்கவும்: {text}"}]}]
            })
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        data = response["candidates"][0]["content"]["parts"][0]["text"].strip()
        print('Response '+data)
        return data
    except Exception as e:
        print(f"API பிழை: {e}")
        return None


def process_stories(stories):
    """ஒவ்வொரு கதைக்கும் சாராம்சத்தைப் பெற்று JSON தரவில் சேர்க்கிறது."""
    for story in stories:
        meaning = story.get("meaning", "")
        if meaning:
            saraamsam = get_saraamsam(meaning)
            if saraamsam:
                story["conclusion"] = saraamsam
            time.sleep(1)  # API அழைப்புகளுக்கு இடையில் தாமதம்
    return stories


# உங்கள் JSON தரவை ஏற்றவும் (உங்கள் பாதையை மாற்றவும்)
with open("completed/purananooru.json", "r") as f:
    stories = json.load(f)

# சாராம்சத்தைப் பெற்று JSON தரவைப் புதுப்பிக்கவும்
updated_stories = process_stories(stories)

# புதுப்பிக்கப்பட்ட JSON தரவைச் சேமிக்கவும் (உங்கள் பாதையை மாற்றவும்)
with open("updated_stories.json", "w") as f:
    json.dump(updated_stories, f, ensure_ascii=False, indent=4)

print("முடிந்தது! முடிவுகள் 'updated_stories.json' இல் சேமிக்கப்பட்டுள்ளன.")
