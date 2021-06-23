run-db:
	sudo docker-compose up -d \
		db \
		adminer

run-app:
	sudo docker-compose up \
		db \
		adminer \
		redis \
		backend \
		frontend

run-test:
	sudo docker-compose run --rm backend_test

lint:
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r ./test_task
	black ./test_task
	isort ./test_task