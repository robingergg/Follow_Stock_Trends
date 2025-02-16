# Example project for dmlab

## Description

This is an example project for dmlab. It is a simple API that allows you to get stock data from the Alpha Vantage API.
In this README I will guide you through the steps to run the project.
Now we will not care about setting up the repository with native way, but only with Docker to make it more simple.


NOTE: For more information on why I chose these technologies, please refer to decision.log - (root/decision.log).
NOTE: This project was developed in WSL 2 on Windows 11 - Ubuntu 24.04.1 LTS.
Recommended usage is only with the use of Docker on Linux or Linux like systems.


## Technologies used

- FastAPI
- PostgreSQL
- Docker
- Python
- React, JS, HTML, CSS


## Prerequisites

- Docker: 
- API key for Alpha Vantage - go to https://www.alphavantage.co/ and click on "Get free API key" button
- PostgreSQL database
- Postgres database config set up - .env file


### Install Docker and Dcoker Compose if not yet installed

`sudo apt-get update`
`sudo apt-get install docker.io -y`

If using WSL you might need to start Docker daemon manually:
`sudo service docker start`

In modern Docker versions, docker compose is now a built-in plugin, but it needs to be installed separately:
`sudo apt-get install docker-compose-plugin -y`

Double check the installed version:
`docker compose version`

You shall see sometihing like this:
- Docker Compose version <x.xx.x>


### Clone the repository

 `git clone https://github.com/robingergg/Follow_Stock_Trends.git`

 Go into the repository

 `cd Follow_Stock_Trends`


### Environment setup

 Create an .env File


#### Database Configuration

ALPHAVANTAGE_API_KEY=<your_alpha_vantage_api_key>
DB_USERNAME=<postgres_username>
DB_PASSWORD=<postgres_password>
DB_NAME=<database_name>
DB_PORT=<database_port>
DB_HOST=<IP_address>


### Start PostgreSQL

`sudo systemctl start postgresql`


### Create the database manually

`sudo -u postgres psql CREATE DATABASE <database_name>;`

Quite from psql:

`\q`


### Build & Run the Application

`docker-compose up --build`

This will:

- Build and start the FastAPI backend
- Build and serve the React frontend
- Connect to PostgreSQL (if configured in Docker)


### Access the Application

Available endpoints:
- FastAPI: http://localhost:8000
- React: http://localhost:3000


#### Access app using curl/ CLI

Open your browser and navigate to:

After successfull build, you should be able to query the API/data at: localhost:8000
Example call: `curl -X GET "http://localhost:8000/stock/IBM?time_series=monthly&use_mock=true"`

This query will return the monthly returns for IBM stock using the mock data.
If mock is set to false, the API will query the Alpha Vantage API for the specified data.


#### Access app using react

Open your browser and navigate to:

- React: http://localhost:3000

Start using the app.