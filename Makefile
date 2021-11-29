update_requirements:
	pip freeze | grep -v 0.0.0 > requirements.txt

server-logs:
	docker logs -f delivery_service

debug:
	docker attach delivery_service

runserver:
	docker-compose up --build -d

stopserver:
	docker-compose down
