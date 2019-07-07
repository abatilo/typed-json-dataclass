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
