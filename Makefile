SHELL := /bin/bash

CONTAINER_NAME = versioner

.PHONY: help
help: ## View help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the container to run our commands within a container
	docker build -t $(CONTAINER_NAME) -f ./Dockerfile .

.PHONY: commitlint
commitlint: build ## Verify that commits conform to our standard
	docker run \
		$(CONTAINER_NAME) \
		npm run commitlint

.PHONY: version
version: build commitlint ## Update our changelog
	docker run \
		--mount type=bind,src=`pwd`/.git,dst=/src/.git -w /src \
		--mount type=bind,src=`pwd`/package.json,dst=/src/package.json -w /src \
		--mount type=bind,src=`pwd`/CHANGELOG.md,dst=/src/CHANGELOG.md -w /src \
		$(CONTAINER_NAME) \
		npm run version

.PHONY: unreleased
unreleased: build commitlint ## View unreleased changes
	docker run \
		--mount type=bind,src=`pwd`/.git,dst=/src/.git,readonly -w /src \
		--mount type=bind,src=`pwd`/package.json,dst=/src/package.json,readonly -w /src \
		--mount type=bind,src=`pwd`/CHANGELOG.md,dst=/src/CHANGELOG.md,readonly -w /src \
		$(CONTAINER_NAME) \
		npm run unreleased
