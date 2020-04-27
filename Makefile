SHELL = zsh

run:
	export FLASK_APP=app/application.py
	flask run

install:
	pip install -r requirements.txt
