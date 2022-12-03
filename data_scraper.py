import requests
import pandas as pd
from bs4 import BeautifulSoup
from pydub import AudioSegment
from urllib.request import urlretrieve
import os
import random
import time


def get_languages() -> list:
    """
    This function gets the list of languages from http://accent.gmu.edu/browse_language.php
    and returns a list of languages
    """
    url = "http://accent.gmu.edu/browse_language.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find(id="maincontent")
    languages = [language.text for language in main_content.find_all("li")]
    return languages


def get_language_urls(language: str) -> dict:
    """
    This function finds all the urls for a given language
    """
    url = f"http://accent.gmu.edu/browse_language.php?function=find&language={language}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find(id="maincontent")
    content = main_content.find(class_="content")
    samples = content.find_all("p")
    result = {}
    for sample in samples:
        result[sample.text.replace(", ", "_")] = "http://accent.gmu.edu/" + sample.find("a")["href"]
    return result


def get_audio(url: str, folder: str, name: str) -> None:
    """
    This function downloads the audio file from a given url
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    audio_url = "http://accent.gmu.edu" + soup.find("source").get("src")
    (audio, headers) = urlretrieve(audio_url)
    audio = AudioSegment.from_mp3(audio)
    if not os.path.exists(f"data/{folder}/"):
        os.makedirs(f"data/{folder}/")
    audio.export(f"data/{folder}/{name}.wav", format="wav")


def download_data():
    if not os.path.exists("data/"):
        os.makedirs("data/")
    languages = get_languages()
    for language in languages:
        if language in ["english", "russian", "german", "dutch", "swedish", "mandarin", "arabic", "spanish"]:
            print(f"Downloading {language}...")
            urls = get_language_urls(language)
            for name, url in urls.items():
                time.sleep(random.randint(1, 5))
                get_audio(url, language, name)


def main():
    download_data()


if __name__ == "__main__":
    main()
