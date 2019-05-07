# Finance Calculator

This is a very simple finance calculator example with some production readiness built in. It's purposes solely to demonstrate the features of Heroku.

## How it works

Customers or leads in the market for a Finance product (mortgage, home, loan, car loan) can use the Finance Calculator to get an idea of what their repayments might be like at different interest rates.

For the Bank this is a great opportunity to gather leads for their Finance products. Having the ability to store the data in different ways gives the bank the flexibility to build optimised workflows based on the technology they use to build other services or customer experiences. For example, most modern programming languages use a JSON-based object structure so using MongoDB, which stores documents in JSON format makes the storage and retrieval of data very straight forward. Alternatively, the bank may want an Enterprise-grade PostgreSql, relational, data store for compatability with legacy systems, or for building out a performant data lake, or to use with Heroku Connect and bi-directionally sync data to Salesforce to empower sales processes. Whatever the requirement having the flexibility of multiple storage types is a massive benefit.

So, what's in this code example? There are 2 processes that run in parallel: 

1. `app.py` - A web service and API that exposes the website and `/calculate` endpoint.
2. `lib/consumer.py` - An asynchronous worker that consumers messages from the AMQP message queue and persists loan enquiries to MongoDB and PostgreSql.

There is also a loging addon called Coralogix. It's one of my favourites as it is layed with lots of useful features for gaining deep insights into your logs. Meaning you can easily use application logging as a mechnism for building business intelligence.

## Deploy
### One-click deploy with Heroku button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/travega/finance-calculator)

### Scripted Deploy

First create and app in Heroku:

```bash
heroku create <appname>
```

In the Common Runtinme, Heroku apps are provisioned in the US region by default. So, optionally, you can add the region flag if you'd like to provision the in another region:

```bash
heroku create <appname> --region=eu
```

Then, run the `setup.sh` from the root of the project and pass it 2 parameters:

```bash
./setup.sh <appname>
```

**appname** (required): The name of the app you want to use in Heroku

Before deploying the code to Heroku configure the Heroku Connect mappings using the `connect_config.json` file. You can do this by selecting import in the Heroku Connect Settings menu.

Once deployed you will need to give the worker dynos some resource. On your apps Resources tab click the edit icon beside the dyno's name and increase the dyno count to at least 1, and save.
