.DEFAULT_GOAL := all

COMPOSE=docker-compose $(COMPOSE_OPTS)


# target: help - display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: up-db - Starts db
up-db:
	$(COMPOSE) up -d book-rating-db

# target: up-api - Starts api
up-api:
	$(COMPOSE) up -d book-rating-api

#Starts all apps
start: up-db up-api

# target: all
up-all:
	$(COMPOSE) up --build -d

# target: stop - Stop all apps
down:
	$(COMPOSE) stop

stop: down

# target: build - Builds docker images
build-no-cache:
	$(COMPOSE) build --no-cache

# target: bash - Runs /bin/bash in App container for development
bash:
	$(COMPOSE) exec api bash


migrate:
	$(COMPOSE) exec api bash -c "alembic upgrade head"

# target: bash - Runs /bin/bash python tests
test:
	$(COMPOSE) exec api bash -c "coverage run -m pytest -v"
	$(COMPOSE) exec api bash -c "coverage report"


drop-db:
	$(COMPOSE) exec db psql -U postgres -c "DROP DATABASE IF EXISTS book_db;"

create-db:
	$(COMPOSE) exec db psql -U postgres -c "CREATE DATABASE book_db OWNER postgres;"
	$(COMPOSE) exec db psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE book_db TO postgres;"
	$(COMPOSE) exec db psql -U postgres -c "ALTER USER postgres CREATEDB;"

# target: clean - Stops and removes all containers
clean:
	$(COMPOSE) down -v

# target: logs - Shows logs for db and app
logs-all:
	$(COMPOSE) logs --follow

logs-api:
	$(COMPOSE) logs -f api

logs-db:
	$(COMPOSE) logs -f db