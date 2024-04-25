# feature_toggle_project

###### How to setup project ######

1. Clone this code in your local machine
2. Create logs folder by the name - "logs" in main project folder
3. All log files will be saved in this logs folder.
4. Setup virtual environment for this project
5. Before doing any code activate this virtual env.
6. Go to main project directory run command - pip install -r requirements.txt, it will install all the listed dependencies required to the project.
7. run command - python manage.py collectstatic. This command will copy all static files in static/ folder
8. create mysql database on local machine as per configuration in config.settings
9. Use .env file for database configuration with your own credentials
    path = config/.env
    # Add VAriables in .env file
        DEBUG=FALSE
        DB_NAME=""
        DB_USER=""
        DB_PASSWORD=""
        DB_HOST=""
        DB_PORT=""
10. run command - python manage.py migrate
11. run command - python manage.py createsuperuser = this will create an admin account to access Django admin
12. run command - python manage.py runserver
13. run command to test unittes cases - python manage.py test
    NOTE: 12 unittest cases added 

NOTE: logs are not added in the code for now but its a good practice to use logs 