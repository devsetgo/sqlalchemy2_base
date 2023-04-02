# -*- coding: utf-8 -*-
"""
Configuration of Gunicorn to serve application utilizing Uvicorn
gunicorn config reference:
https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
"""

import multiprocessing

from service.settings import config_settings

# ip and port to bind
bind = "0.0.0.0:5000"
timeout = 120
# define number of workers by cores times two plus one
# edit if you want to set a specific/limited amount of workers

if config_settings.workers == 0 or config_settings.workers is None:
    workers = multiprocessing.cpu_count() * 2 + 1
else:
    workers = config_settings.workers

# set worker class to uvicorn
worker_class = "uvicorn.workers.uvicornworker"
# worker_class = "uvicorn.workers.UvicornH11Worker"

# Increase maximum request body size to 100MB
client_max_body_size = 100 * 1024 * 1024

# loglevel - the granularity of log output
# a string of "debug", "info", "warning", "error", "critical"
loglevel = str(config_settings.loguru_logging_level.lower())

# Optimize startup time by preloading the application code
preload_app = True

"""
A dictionary containing headers and values that the front-end proxy
 uses to indicate HTTPS requests.
These tell Gunicorn to set wsgi.url_scheme to https,
 so your application can tell that the request is secure.
"""
# secure_scheme_headers = {
#     "X-FORWARDED-PROTOCOL": "ssl",
#     "X-FORWARDED-PROTO": "https",
#     "X-FORWARDED-SSL": "on",
# }
# # ips that are allowed to forward
# FORWARDED_ALLOW_IPS = "127.0.0.1", "0.0.0.0"
