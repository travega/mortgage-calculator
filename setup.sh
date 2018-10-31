#! /bin/bash

heroku addons:create heroku-postgresql:hobby-basic --app $1
heroku pg:wait

heroku addons:create mongolab:sandbox --app $1
heroku pg:wait

heroku addons:create coralogix:startup --app $1
heroku pg:wait

heroku addons:create cloudamqp:lemur --app $1
heroku pg:wait

heroku config:add QUEUE_NAME="load_enquiries"
heroku pg:wait

heroku config -s --app $1 > .env