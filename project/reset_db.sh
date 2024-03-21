#!/bin/bash

# Delete the SQLite database file
rm db.sqlite3

# Run migrations
python manage.py migrate

# Start the Django shell and execute the insert_data.py script
echo "from data_creation import insert_data; insert_data.run()" | python manage.py shell

