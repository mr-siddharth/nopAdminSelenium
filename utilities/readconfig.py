from configparser import RawConfigParser

parser = RawConfigParser()
parser.read(".\\configurations\\config.ini")


def get_base_url():
    return parser.get('common', 'base_url')


def get_admin_email():
    return parser.get('common', 'admin_email')


def get_admin_password():
    return parser.get('common', 'admin_password')