.PHONY=default build run clean test all
mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
build_dir := "$(mkfile_path)build/"

GAME_IMAGE := docker.io/tomastomecek/open-house-2018-game


default: all

build: build/id_rsa.pub
	docker-compose build

run:
	docker-compose up -d

all: build run
# build and run, this is the default; we don't want to build every time we run

clean:
	rm -f $(build_dir)id_rsa{,.pub}
	rmdir $(build_dir)

build/id_rsa.pub build/id_rsa: build/
	ssh-keygen -b 8192 -N "" -t rsa -f $(build_dir)id_rsa

build/:
	mkdir -p $(build_dir)

build-game-image:
	docker build -f ./Dockerfile.game --tag=$(GAME_IMAGE) .

push-game-image: build-game-image
	docker push $(GAME_IMAGE)

