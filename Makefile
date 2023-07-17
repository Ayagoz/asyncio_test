NAME?=app

CODE_ROOT?=src/

.PHONY:  build stop run-dev attach exec

build:
	docker build \
	-t $(NAME) .

stop:
	-docker stop $(NAME)
	-docker rm $(NAME)

exec:
	docker exec -it $(NAME) bash

attach:
	docker attach $(NAME)

run-dev:
	docker run --rm -it \
		--net=host \
		--ipc=host \
		-v $(shell pwd):/workdir \
		--name=$(NAME) \
		$(NAME) \
		bash

run-app:
	docker run --rm -it \
		--net=host \
		--ipc=host \
		-v $(shell pwd):/workdir \
		--name=$(NAME) \
		$(NAME) \
		python3 /workdir/src/app.py

run-prometheus:
	docker run -p 9090:9090 \
			--net host \
			-v $(shell pwd)/prometheus.yaml:/etc/prometheus/prometheus.yml \
			prom/prometheus
