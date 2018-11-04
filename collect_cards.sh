#!/bin/sh

echo "Converting cdb to sql file..."
sqlite3 $1/cards.cdb .dump > $1/cards.sql

echo "Successfully converted cdb to sql file, now collecting card date..."
python yugioh/cards/main.py $1