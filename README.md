# Bounties-API
[![CircleCI](https://circleci.com/gh/Bounties-Network/BountiesAPI.svg?style=svg)](https://circleci.com/gh/Bounties-Network/BountiesAPI) [![codecov](https://codecov.io/gh/Bounties-Network/BountiesAPI/branch/master/graph/badge.svg)](https://codecov.io/gh/Bounties-Network/BountiesAPI)

[Deployed Production API - Mainnet Contract](https://api.bounties.network)

[Deployed Staging API - Rinkeby Contract great for testing](https://staging.api.bounties.network)

## Setup
[Download Docker stable version](https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac)
```
docker volume create --name redis_bounties
docker volume create --name psql_bounties
docker-compose up
```
Locally, you will now be syncing directly from the contract. You may access the api at:

http://locahost:8000

The API will automatically restart if you make code changes. To turn off the services, run `docker-compose down`. Keep in mind, the volumes make it so your DB and redis cache will be in the same state if you start the services again with `docker-compose up`. If you would like to wipe out your databases and start again, then run:
```
docker-compose down
docker volume rm redis_bounties
docker volume rm psql_bounties
docker volume create --name redis_bounties
docker volume create --name psql_bounties
docker-compose up
```
If you add additional packages to a package.json or to the requirements.txt file, you'll need to rebuild the individual service.  To rebuild all services, you may run:
```
docker-compose down
docker-compose build
docker-compose up
```
By default, the sync will connect to mainNet. To change to a rinkeby sync or other, you will need to adjust the eth_network key in the [environment file](https://github.com/Bounties-Network/BountiesAPI/blob/master/.env). As an example, it can be changed to `eth_network=rinkeby`.

## API Schema and Documentation
Visit the [production](api.bounties.network/) or staging [endpoint](https://staging.api.bounties.network/). Both default to the swagger documentation ui. The local version also serves the documentation.

## Architecture

![Architecture Diagram](https://s3.amazonaws.com/bountiespublic/BountiesDiagram2.png)

The **frontend or client** can be any third party service or collaborator that integrates with the [standard bounties ethereum contract](https://github.com/Bounties-Network/StandardBounties).  This API works as a caching and storage layer for what is input into the standard bounties contract. Due to storage costs, the contract puts the majority of the data into IPFS. To understand further, read the documentation on the [standard bounties contract](https://github.com/Bounties-Network/StandardBounties/blob/master/docs/documentation.md).

The [**contract subscriber**](https://github.com/Bounties-Network/BountiesAPI/tree/master/contract_subscriber) listens for events from the contract. In the case a resync is occurring, it will listen to all historical events, starting from the genesis block. In order for the subscriber to know what it has already accessed, the redis cache stores a currentBlock key. Additionally, the redis cache stores the hashes for all transactions that have already been evaluated and stored to the db. The contract subscriber will ignore transactions that have already been written, and will not search through blocks prior to the currentBlock key. When the subscriber picks up on a new event, it looks up the original transaction via web3 and passes the event data along with the original contract function inputs to SQS.  An SQS fifo queue is used. This means we will never have duplication on keys and all events will be handled in the order they come through.

The [**bounties subscriber**](https://github.com/Bounties-Network/BountiesAPI/blob/master/bounties_api/std_bounties/management/commands/bounties_subscriber.py) listens to events that have been passed into SQS by the contract subscriber.  The bounties subscriber uses the data from the event, the inputs to the original contract function, and the IPFS stored data to write the appropriate values to the DB via django.

The [**bounties api**](https://github.com/Bounties-Network/BountiesAPI) is a django API that serves the data that has been written by the bounties subscriber and other running jobs.

[**sql_jobs**](https://github.com/Bounties-Network/BountiesAPI/tree/master/sql_jobs) are scheduled jobs to help enrich the data. [category_ranks.sql](https://github.com/Bounties-Network/BountiesAPI/blob/master/sql_jobs/hourly/category_ranks.sql) produces a table that ranks the most commonly used categories and converges duplicated names.

Other Jobs include:
 - [track_bounty_expirations.py](https://github.com/Bounties-Network/BountiesAPI/blob/master/bounties_api/std_bounties/management/commands/track_bounty_expirations.py).
 - [get_token_values.py](https://github.com/Bounties-Network/BountiesAPI/blob/master/bounties_api/std_bounties/management/commands/get_token_values.py). This syncs with coinmarketcap every 5 minutes and updates pricing on each of the bounties in USD.
