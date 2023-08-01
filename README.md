# vk_bot
test project for implementing dockerized vk_bot


### To run the project, follow these steps:

1. Clone the project from the GitHub repository. You can use the ```git clone``` command and provide the repository URL.

2. Navigate to the project directory using the ```cd``` command.

3. Make sure you have Docker and Docker Compose installed on your machine. If not, follow the instructions to install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

Run the command ```docker-compose up --build``` to start the project. This command will build the Docker container and launch it.

### .env example

```
POSTGRES_DB=patisserie
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST= # название контейнера в локальной сети
DB_PORT=5432

VK_TOKEN=... # необходимо получить в группе вк, где будет функционировать бот
```