# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 20:18:25 2021

@author: Mayuko
"""


from .base import *
import dj_database_url
from socket import gethostname

hostname = gethostname()

db_from_env = dj_database_url.config()

DATABASES = {
    'default': dj_database_url.config()
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'hgdgvhsyb',
    'API_KEY': '486584728357188',
    'API_SECRET': '1EkhtDKOjzMLb4PDaj8x4mfrnho'
}
