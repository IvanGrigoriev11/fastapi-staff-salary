## Employee service 
    This service provides information about users' salaries and the date of the next raise based on private access for each user.

## Setting up

**NOTE**: The instruction below is shown for MacOS.

1. Clone the repository to your local machine.
1. Navigate to the project directory: `cd <repo_root>`.
1. Install Poetry from the [Official page - Poetry](https://python-poetry.org/docs/#installation).
1. Install the project dependencies using Poetry: `poetry install`.
1. Activate poetry environment by `poetry shell`.


## Configure environment variables for running service

The service relies on the environment variable called `JWT_SECRET_KEY` which is neccessary for encoding/decoding token required for JWT based authentication. 

1. Set `JWT_SECRET_KEY` environment variable by writing in the terminal `openssl rand -hex 64`. Put the result in your profile (e.g. `open ~/.zshrc`).
   1. `export JWT_SECRET_KEY=<your value>`.

## Launching tests

1. `cd <repo_root>`.
1. Do `poetry run pytest .`.


## Creating a docker image 

1. Build the docker image with `docker build --tag employee_service .`. 


## Running the dockerized service locally

1. Run the image by `docker run -dit -p 8000:8000 -e JWT_SECRET_KEY=$JWT_SECRET_KEY --name employee_service employee_service`. It will launch the container in the testing mode. This mode has 2 preconfigured users than can be used in the steps below.
1. Check the container is active by `docker ps`.
1. Open `Postman`. If you don't have Postman installed, do `curl -LJO "https://dl.pstmn.io/download/latest/osx"`.
1. Form `POST` request to `http://0.0.0.0:8000/login` address. Use a preconfigured user:
{
    "username": "user1",
    "password": "password1"
} 
The response will contain an access token in the `access_token` field. 
1. Form `GET` request to `http://0.0.0.0:8000/users/salary` address by first adding `access_token` value from the response above to the `Authorization` tab in Postman. Receive response with the particular user's `salary` and `salary_increase_date`.
1. Stop the docker container by `docker stop <container_id>`.
1. Remove the docker container from your local machine by `docker rm <container_id>`.
