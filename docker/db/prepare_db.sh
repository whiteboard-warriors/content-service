#!/bin/sh
set -e

/opt/src/db/start_postgres.sh

echo 'Creating Schema'
python3 /opt/src/init_db.py

/opt/src/db/stop_postgres.sh
