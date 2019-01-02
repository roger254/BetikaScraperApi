.PHONY: clean system-packages python-packages install scrape run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

system-packages:
	sudo apt install python-pip -y


python-packages:
	pip install -r requirements.txt

install:system-packages python-packages

scrape:
	python manage.py new_games

run:
	python manage.py run

all: clean install scrape run