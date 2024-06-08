import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face Hub API token
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("Hugging Face API token is missing. Please set it in the .env file.")

# Salesforce BLIP Image Captioning model
model_id = "Salesforce/blip-image-captioning-large"
headers = {
    "Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_caption(image_url):
    payload = {
        "inputs": image_url
    }
    response = requests.post(f"https://api-inference.huggingface.co/models/{model_id}", headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get('generated_text', 'No caption found')
        else:
            return "Unexpected response format"
    else:
        print("Error:", response.text)
        return None

def main():
    image_url = input("Enter the URL of the image: ")
    caption = generate_caption(image_url)
    if caption:
        print("Image Caption:", caption)
    else:
        print("Failed to generate caption.")

if __name__ == "__main__":
    main()
