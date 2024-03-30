import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def shorten_link(user_url, token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {"long_url": user_url}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(bitlink, token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    params = {"unit": 'month', "units": -1}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()['total_clicks']


def is_bitlink(bitlink, token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Программы сокращает ссылку и показывает перехпды по сокращенным ссылкам')
    parser.add_argument('--link', type=str, help='Введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.link)
    parsed_url = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(parsed_url, token):
            print(count_clicks(parsed_url, token))
        else:
            print(shorten_link(args.link, token))
    except requests.exceptions.HTTPError:
        print("Ошибка, проверьте вашу ссылку")