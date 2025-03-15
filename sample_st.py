import os
import time
import requests
import bs4
import json
import traceback

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


def dump_error(story):
    with open("error.log", "a") as log:
        log.write(f"{time.ctime()} - {story}\n")
        log.write(traceback.format_exc())


def save_as_json(file, dictionary_list):
    directory = os.getcwd() + "/scraped"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{file}.json", "w") as outfile:
        # ensure_ascii=False to support Tamil string
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


def scrape_content(stories: list):
    for index, story in enumerate(stories):
        print(f"Scraping story: {story['story_category']} {index+1}...")
        try:
            req = requests.get(story["url"], headers)
            soup = bs4.BeautifulSoup(req.content, "html.parser")
            post_container = soup.find("div", "print-div")
            text_elements = []
            if post_container:
                color_blue_span = post_container.find("span", class_="color-blue")
                if color_blue_span:
                    cleaned_text = color_blue_span.text.replace("\r", "").replace("                ", "\n").strip()
                    story["information"] = cleaned_text
                table = post_container.find("table")
                if table:
                  poem_text = ""
                  rows = table.find_all("tr")
                  for row in rows:
                    strong_tag = row.find("strong")
                    if strong_tag:
                      poem_text += strong_tag.text + "\n"
                      cleaned_poem = poem_text.replace("\r", "").replace("                ", "\n").strip()
                  story["poem"] = cleaned_poem.strip() # Remove trailing newline.

            for element in post_container:
                if not isinstance(element, bs4.Tag):
                    line = element.strip()
                    if not len(line) == 0:
                        text_elements.append(line)
            content = " ".join(text_elements)
            story["meaning"] = content
            save_as_json(story["story_category"], stories)
        except Exception:
            dump_error(f"{story['story_category']} {index+1}")
        time.sleep(10)


def load_json(file):
    with open(file, "r") as infile:
        file_contents = json.load(infile)
        return file_contents


def run_scrapper():
    path = os.getcwd() + "/stories"
    directory = os.listdir(path)
    for index, file in enumerate(directory):
        stories_file = load_json(f"{path}/{file}")
        scrape_content(stories_file)


run_scrapper()
