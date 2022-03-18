NAME=jaggerbean
PACKAGE=iss-data
TAG=1.0
PYTEST=test_data.py

run: kill clean build run


images:
	docker images | grep ${PACKAGE}

ps:
	docker ps -a | grep ${PACKAGE}

kill:
	- docker stop ${PACKAGE}

clean:
	- docker rm ${PACKAGE}

build:
	docker build -t ${NAME}/${PACKAGE}:${TAG} .

run:
	docker run --name "${PACKAGE}" -p 5002:5000 ${NAME}/${PACKAGE}:${TAG}

push:
	docker login docker.io
	docker push ${NAME}/${PACKAGE}:${TAG}
