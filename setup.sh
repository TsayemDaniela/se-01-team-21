#!/bin/sh
interpreter='python3';
$interpreter -m venv venv .;
. venv/bin/activate ;
$interpreter -m pip install -e .;
export FLASK_APP=flaskr;
export FLASK_ENV=development;
echo "setting up database, please enter mysql root password";
mysql -u root -p < SE.sql;
echo "creating test database, please enter mysql root password";
mysql -u root -p < test_db_creation_script.sql;
FILE=./flaskr/userconfig.json;
if ! test -f "$FILE"; then
    echo "creating sample userconfig.json file in flaskr/ directory";
    echo "{
  \"user\": \"dev\",
  \"password\": \"12345\",
  \"host\": \"localhost\",
  \"database\": \"SEG21\",
  \"port\": \"3306\"
}" > "$FILE";
fi;
flask run;
