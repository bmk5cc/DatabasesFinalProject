# DatabasesFinalProject
Note: Project doesn't represent best coding practices due to time constraints

## Set up
Once the project is cloned, create a [virtual environment](https://docs.python.org/3/library/venv.html) within the root folder of the project.
Then run pip install -r requirements.txt

Also add DB_SOCIAL_KEY and DB_SOCIAL_SECRET. You can either ask for mine, or make you own through [google](https://console.developers.google.com/projectselector/apis/library?supportedpurview=project). Then enable the google+ api

If you want to log in to view the add and delete course functionality, modify students/fixtures/db1.json to have your computing id in one of the students.

## Running the server
Install Django and run python manage.py migrate

Then run python manage.py loaddata db1.json

Finally run python manage.py runserver

If you want to view what is inside the database, download sqlite3, then run sqlite3 db.sqlite3
