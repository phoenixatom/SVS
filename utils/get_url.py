# utils/get_url.py
import requests


def get_content_from_url(url):
    return requests.get(url).content


def get_json_from_url(url):
    return requests.get(url).json()
