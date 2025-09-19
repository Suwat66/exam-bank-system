#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# --- เพิ่มคำสั่งนี้เข้าไป ---
python manage.py create_initial_user