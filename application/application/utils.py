import os
from os.path import abspath, dirname
import requests

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured


def get_env(var_name, default_value=None, is_bool=False):
    try:
        value = os.environ.get(var_name)
        if value is None or len(value) == 0:
            return default_value
        if is_bool:
            return str(value).lower() == 'true'
        return value
    except KeyError:
        error_msg = "set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


def create_file(file_name: str, content: str):
    dir_path = os.path.dirname(file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_name, mode='w') as f:
        f.write(content)


def notify_slack(message: str, channel_name: str, blocks=""):
    slack_token = get_env('SLACK_TOKEN')
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': "Bearer {}".format(slack_token),
    }
    json = {
        'token': slack_token,
        'channel': channel_name,
        'text': message,
        'blocks': str(blocks) if len(blocks) > 0 else None
    }

    requests.post(url=url, headers=headers, json=json)


if os.environ.get('ENV_LOADED') == None:
    # initialize environment variables only once

    os.environ.setdefault('ENV_LOADED', '1')

    # in production you can keep the .env in another location
    dotenv_path = '/home/user/.env'
    dotenv_path = dotenv_path if os.path.exists(dotenv_path) else dirname(abspath(__file__)) + '/.env'

    load_dotenv(dotenv_path)
