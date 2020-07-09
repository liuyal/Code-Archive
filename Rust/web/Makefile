SHELL := /bin/bash

DEBUG_ARGS = --debug
RELEASE_ARGS = --release
FRONTEND_ARGS = -p frontend --target wasm32-unknown-unknown

HOST_ARG = --auto-reload --host 192.168.1.73

all: run

SOURCE_CARGO=source ~/.cargo/env

build:
	$(SOURCE_CARGO) && cargo web build $(FRONTEND_ARGS)

run: 
	$(SOURCE_CARGO) && cargo web deploy $(FRONTEND_ARGS) $(RELEASE_ARGS)

