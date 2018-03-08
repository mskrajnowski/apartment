# -*- coding: utf-8 -*-

import os

from apartment.crawler.shub import environment


# Convert scrapinghub ENV_* settings to environment variables,
# so we can use them to build settings
environment.load_env()

if environment.is_shub():
    # TODO: shub frontier backend
    pass
else:
    BACKEND = 'frontera.contrib.backends.sqlalchemy.FIFO'
    SQLALCHEMYBACKEND_ENGINE = 'sqlite:///frontier.db'

MAX_REQUESTS = 2000
MAX_NEXT_REQUESTS = 10
DELAY_ON_EMPTY = 0.0
