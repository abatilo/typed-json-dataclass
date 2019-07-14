SHELL := /bin/bash

CONTAINER_NAME = versioner
SYNCER_NAME = syncer

.PHONY: help
help: ## View help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the container to run our commands within a container
	docker build -t $(CONTAINER_NAME) -f ./Dockerfile .

.PHONY: build_syncer
build_syncer: ## Build the container that keeps our versions in sync
	docker build -t $(SYNCER_NAME) -f ./actions/version_syncer/Dockerfile \
		./actions/version_syncer/

.PHONY: commitlint
commitlint: build ## Verify that commits conform to our standard
	docker run \
		$(CONTAINER_NAME) \
		npm run commitlint

.PHONY: bump
bump: build commitlint ## Update our changelog
	docker run \
		--mount type=bind,src=`pwd`/.git,dst=/src/.git -w /src \
		--mount type=bind,src=`pwd`/package.json,dst=/src/package.json -w /src \
		--mount type=bind,src=`pwd`/package-lock.json,dst=/src/package-lock.json -w /src \
		--mount type=bind,src=`pwd`/CHANGELOG.md,dst=/src/CHANGELOG.md -w /src \
		$(CONTAINER_NAME) \
		npm run version

.PHONY: sync
sync: build_syncer ## Sync versions between package.json and pyproject.toml
	docker run \
		--mount type=bind,src=`pwd`/package.json,dst=/package.json \
		--mount type=bind,src=`pwd`/pyproject.toml,dst=/pyproject.toml \
		$(SYNCER_NAME) /package.json /pyproject.toml
	git add pyproject.toml
	git commit -m "chore: sync package.json version to pyproject.toml version"

.PHONY: version ## Update versions for packages
version: bump sync

.PHONY: unreleased
unreleased: build commitlint ## View unreleased changes
	docker run \
		--mount type=bind,src=`pwd`/.git,dst=/src/.git,readonly -w /src \
		--mount type=bind,src=`pwd`/package.json,dst=/src/package.json,readonly -w /src \
		--mount type=bind,src=`pwd`/package-lock.json,dst=/src/package-lock.json,readonly -w /src \
		--mount type=bind,src=`pwd`/CHANGELOG.md,dst=/src/CHANGELOG.md,readonly -w /src \
		$(CONTAINER_NAME) \
		npm run unreleased
