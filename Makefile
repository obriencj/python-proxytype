# Sorry that this Makefile is a bit of a disaster. Run `make help` to
# see a list of valid targets.


PYTHON ?= $(shell which python3 python 2>/dev/null | head -n1)
PYTHON := $(PYTHON)

TOX ?= $(shell which tox 2>/dev/null | head -n1)
TOX := $(TOX)


PROJECT := $(shell $(PYTHON) ./setup.py --name)
VERSION := $(shell $(PYTHON) ./setup.py --version)

ARCHIVE := $(PROJECT)-$(VERSION).tar.gz


define checkfor
	@if ! which $(1) >/dev/null 2>&1 ; then \
		echo $(1) "is required, but not available" 1>&2 ; \
		exit 1 ; \
	fi
endef


##@ Basic Targets

default: quick-test	## Runs the quick-test target


help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


report-python:
	@echo "Using python" $(PYTHON)
	@$(PYTHON) -VV


##@ Local Build and Install

build: clean-built report-python flake8	## Produces a wheel using the default system python
	@$(TOX) -qe build


install: build	## Installs using the default python for the current user
ifeq ($(UID),"0")
	@$(PYTHON) -B -m pip.__main__ \
		install -IU --no-deps \
		dist/$(PROJECT)-$(VERSION)-py3-none-any.whl
else
	$(PYTHON) -B -m pip.__main__ \
		install -IU --no-deps --user \
		dist/$(PROJECT)-$(VERSION)-py3-none-any.whl
endif


uninstall:	## Uninstalls using the default python for the current user
ifeq ($(UID),"0")
	@$(PYTHON) -B -m pip.__main__ \
		uninstall $(PROJECT)
else
	@$(PYTHON) -B -m pip.__main__ \
		uninstall $(PROJECT)
endif


##@ Cleanup

purge:	clean
	@rm -rf .eggs .tox .mypy_cache


tidy:	## Removes stray eggs and .pyc files
	@rm -rf *.egg-info
	@$(call checkfor,find)
	@find -H . \
		\( -iname '.tox' -o -iname '.eggs' -prune \) -o \
		\( -type d -iname '__pycache__' -exec rm -rf {} + \) -o \
		\( -type f -iname '*.pyc' -exec rm -f {} + \)


clean: tidy	## Removes built content
	@rm -rf build/* dist/*
	@rm -rf bandit.sarif


##@ Testing


test: clean requires-tox	## Launches tox
	@$(TOX) -q


bandit:	requires-tox	## Launches bandit via tox
	@$(TOX) -qe bandit


flake8:	requires-tox	## Launches flake8 via tox
	@$(TOX) -qe flake8


mypy:	requires-tox	## Launches mypy via tox
	@$(TOX) -qe mypy


twine: 	clean-built requires-tox	## Launches twine via tox to check the wheel
	@$(TOX) -qe twine


quick-test: requires-tox flake8 ## Launches nosetest using the default python
	@$(TOX) -qe quicktest


##@ Workflow Features

project:	## project name
	@echo $(PROJECT)

version:	## project version
	@echo $(VERSION)

python:		## detected python executable
	@echo $(PYTHON)


requires-git:
	@$(call checkfor,git)

requires-tox:
	@$(call checkfor,$(TOX))


.PHONY: build clean clean-built default flake8 help mypy project python quick-test report-python requires-git requires-tox test tidy twine version


# The end.
