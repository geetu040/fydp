#!/bin/bash
export OPENAI_API_KEY=open-api-key
exec gunicorn app.main:app -c gunicorn_conf.py
