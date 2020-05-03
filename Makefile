SHELL = zsh

run:
	export FLASK_APP=app/application.py
	flask run

install:
	pip install -r requirements.txt

backend:
	docker kill backend || true
	docker rm backend || true
	docker run --name backend -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mariadb
