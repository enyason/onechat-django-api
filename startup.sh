#!/bin/bash

gunicorn --bind 0.0.0.0:8000 onechat_api.asgi:application -k uvicorn.workers.UvicornWorker --access-logfile '-' --error-logfile '-'