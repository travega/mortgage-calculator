# Mortgage Calculator

This is a very simple mortgage calculator with some production readiness built in.

## Deploy
### One-click deploy with Heroku button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/travega/mortgage-calculator)

### Scripted Deploy

First create and app in Heroku:

```bash
heroku create <appname>
```

Then, run the `setup.sh` from the root of the project and pass it 2 parameters:

```bash
./setup.sh [appname]
```

**appname** (required): The name of the app you want to use in Heroku

Note: the app is created by default in the **US region**.%