# se-01-team-21
SE Sprint 01, Team 21
## INTRO
    this project is set up using a loosely coupled connection of : mysql and flask. Authentication is carried out exclusively by application logic, and by maintaining the active session-id's in the mysql database. Source code can be found in the
    *flaskr* directory. Html is found in the flaskr/templates directory, and images/js/css is found in the flask/static directory


## DOCUMENTATION
    api documentation can be found in the following link: https://app.swaggerhub.com/apis-docs/osobiehl/group-21/1.0.0
    it is also present as a `documentation.yaml` file in docs/ directory. feel free to expand on that yaml file for further implementations.
    An EER diagram can also be found in the docs/ directory
## SOCKET-IO
    This is an experimental portion of the project, it is shown in the __init__.py file, it can be safely discarded for now as it does not implement anything functional



## SETUP
    if everything is perfect, running the script setup.sh may install all required python dependencies. However, in case this does not work, do the following:
    python -m venv venv .;
    . venv/bin/activate ;

    afterwards, install the dependencies in the root directory using pip:
    python -m pip install -e .;

    then, create the databases and tables used for mysql from the given files
    mysql -u root -p < SE.sql;
    mysql -u root -p < test_db_creation_script.sql;

    finally, modify your authentication string in the userconfig.json file in flaskr/userconfig.json (this file is created by the bash script)

    now, you can run the server
    export FLASK_APP=flaskr;
    export FLASK_ENV=development;
    flask run;

## TESTING
    run npm test inside the tests/ directory to run some testcases. Future implementations will use cookies and other goodies for a more complete coverage, but I suffered enough just getting this to work : ^ )
## CHANGELOG
    * Created a landing page with links to a signup and login page (not functional)
    * implemented API endpoints for instructor authentication by returning a cookie (look at documentation for examples)
    * implemented API endpoints for an instructor to create a dummy game that creates passwords for 4 players
    * implemented API endpoints that allow players to send the password as a one-time secret, becoming authenticated and receiving a cookie (again, look at documentation for examples and setup)
    * implemented views that allow further functions to check for instructor authentication and instructor ownership of a game
    * implemented a delete_game dummy method that deletes an active game instance provided the instructor created the game (look at documentation)
    * configured SQL database with player sessions, instructor sessions, and a `game` instance containing most of the static parameters of a game (This is by no means functional yet, but it works as a proof of concept)