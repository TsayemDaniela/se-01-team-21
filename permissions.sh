#!/bin/bash


chmod 644 scripts/.htaccess
find ./ -iname "*.html" -exec chmod --verbose 644  {} \;
find ./ -iname "*.css" -exec chmod --verbose 644  {} \;
find ./ -iname "*.py" -exec chmod --verbose 755  {} \;
find ./ -iname "*.png" -exec chmod --verbose 644  {} \;
find ./ -iname "*.jpeg" -exec chmod --verbose 644  {} \;
find ./ -iname "*.jpg" -exec chmod --verbose 644  {} \;
find ./ -iname "*.py" -exec chmod --verbose 755 {} \;
find ./ -iname "*.js" -exec chmod --verbose 755 {} \;
find ./ -iname "*.jinja" -exec chmod --verbose 755 {} \;

find img -type d -exec  chmod --verbose 755 {} \;




# find views -type d -exec  chmod --verbose u+rw,g+rw,o+rw {} \;
