import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("SUNO_BASE_URL")


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    # print("response = ", response)
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    x = get_quota_information()
    print(x)
