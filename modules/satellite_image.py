# modules/satellite_image.py

from bs4 import BeautifulSoup

from utils.get_url import get_content_from_url


async def get_image_url(url):
    content = get_content_from_url(url)
    soup = BeautifulSoup(content, 'lxml')

    img_tag = soup.find('img', class_='img-fluid w-100 in-satellite')

    if img_tag:
        image_url = img_tag.get('src')
        return image_url
    else:
        print("Image tag not found on the page.")
        return None


async def get_maldivian_met_sat_image():
    url = "https://www.meteorology.gov.mv"
    return await get_image_url(url)
