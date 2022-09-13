.PHONY: check outdated dump image prod-image build up down ps start stop logs shell test

test = 0 # set test = 1 to run the tests in containers
cache = 1 # set cache = 0 to disable the docker build cache

REPOSITORY = gledi/rates
TAG = develop
SVC = api
SHELL = bash

ifeq ($(test), 1)
	TAG = testing
	SVC = testapi
	BUILD_ARGS = --build-arg ENVIRONMENT=test
	COMPOSE_FILE = --file docker-compose.testing.yml
endif

ifeq ($(cache), 0)
	NO_CACHE = --no-cache
endif


check:
	@echo "REPOSITORY =" $(REPOSITORY)
	@echo "TAG =" $(TAG)
	@echo "SVC =" $(SVC)
	@echo "SHELL =" $(SHELL)
	@echo "BUILD_ARGS =" $(BUILD_ARGS)
	@echo "COMPOSE_FILE =" $(COMPOSE_FILE)
	@echo "NO_CACHE =" $(NO_CACHE)

outdated:
	@poetry show --outdated

dump:
	@poetry export --without-hashes --without-urls -o requirements/base.txt
	@poetry export --without-hashes --without-urls --with=test -o requirements/test.txt
	@poetry export --without-hashes --without-urls --with=migrations -o requirements/migrations.txt
	@poetry export --without-hashes --without-urls --with=prod --with=migrations --with=test --with=dev -o requirements/dev.txt
	@poetry export --without-hashes --without-urls --with=prod -o requirements/prod.txt

image:
	docker build --tag $(REPOSITORY):$(TAG) --file ./containers/Dockerfile $(BUILD_ARGS) $(NO_CACHE) .

prod-image:
	docker build --tag $(REPOSITORY):latest --tag $(REPOSITORY):production --file ./containers/Dockerfile.production $(NO_CACHE) .

build:
	docker compose $(COMPOSE_FILE) build $(BUILD_ARGS) $(NO_CACHE)

up: build
	docker compose $(COMPOSE_FILE) up -d

down:
	docker compose $(COMPOSE_FILE) down --remove-orphans --rmi local --volumes

ps:
	docker compose $(COMPOSE_FILE) ps

start:
	docker compose $(COMPOSE_FILE) start $(SVC)

stop:
	docker compose $(COMPOSE_FILE) stop $(SVC)

logs:
	docker compose $(COMPOSE_FILE) logs -f $(SVC)

shell:
	docker compose $(COMPOSE_FILE) exec $(SVC) $(SHELL)

test:
	docker compose --file docker-compose.testing.yml run --rm testapi python -m pytest -v .
	docker compose --file docker-compose.testing.yml down --remove-orphans --rmi local --volumes
