SHELL := /bin/bash

DEBUG_ARGS = --debug
RELEASE_ARGS = --release

BUILD_TEST_ARGS = -p test

all: run

SOURCE_CARGO=source ~/.cargo/env


build:
	$(SOURCE_CARGO) && cargo build $(BUILD_TEST_ARGS)


run: build
	$(SOURCE_CARGO) && cargo run $(BUILD_TEST_ARGS)

