#! /bin/bash

heroku addons:create heroku-postgresql:standard-0 --app $1
heroku addons:create mongolab:sandbox --app $1
heroku addons:create coralogix:startup --app $1
heroku addons:create cloudamqp:lemur --app $1
heroku config -s --app $1 > .env