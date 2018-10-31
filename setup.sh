#! /bin/bash

heroku create $1 --region=eu --team $2
heroku addons:create heroku-postgresql:standard-0
heroku addons:create mongolab:sandbox
heroku addons:create coralogix:startup
heroku addons:create cloudamqp:lemur
heroku config -s > .env