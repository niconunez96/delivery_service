create_migrations:
	python ./project/manage.py db init
	python ./project/manage.py db migrate

run_migrations:
	python ./project/manage.py db stamp head
	python ./project/manage.py db upgrade

update_requirements:
	pip freeze | grep -v 0.0.0 > requirements.txt

server-logs:
	docker logs -f book-app

debug:
	docker attach book-app

runserver:
	docker-compose up --build -d

stopserver:
	docker-compose down

db-client:
	docker exec -it mysql-db mysql -u dev_user -p1234
