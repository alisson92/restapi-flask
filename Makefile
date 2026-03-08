APP = restapi

test:
	@flake8 . --exclude .venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

down:
	@docker compose down

heroku:
	@heroku container:login
	@heroku container:push -a devops-restapi web
	@heroku container:release -a devops-restapi web