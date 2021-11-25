import os
import configurations.config as config


def get_base_url():
    return config.settings["base_url"]


def get_admin_email():
    return os.environ.get('NOP_ADMIN_EMAIL')


def get_admin_password():
    return os.environ.get('NOP_ADMIN_PASSWORD')
