.PHONY: img build up down ps start stop logs shell test-build test

RATES_IMAGE_REPOSITORY=gledi/rates
export RATES_IMAGE_REPOSITORY

RATES_IMAGE_TAG=develop
export RATES_IMAGE_TAG

SVC=api
export SVC

IMG_SHELL=bash
export IMG_SHELL


img:
	docker build --tag $(RATES_IMAGE_REPOSITORY):$(RATES_IMAGE_TAG) --file ./containers/Dockerfile .

build:
	docker compose build

up: build
	docker compose up -d

down:
	docker compose down --remove-orphans --rmi local --volumes

ps:
	docker compose ps

start:
	docker compose start $(SVC)

stop:
	docker compose stop $(SVC)

logs:
	docker compose logs -f $(SVC)

shell:
	docker compose exec $(SVC) $(IMG_SHELL)

test-build:
	docker compose --file docker-compose.testing.yml build

test: test-build
	docker compose --file docker-compose.testing.yml up -d
