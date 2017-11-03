import pytumblr
import yaml
import os
from tower.interactive_console import new_oauth


def get_tumblr_client():
    yaml_path = os.path.join(os.path.expanduser('~'), '.tumblr')

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    return pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )
