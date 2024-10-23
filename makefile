################################################################################
# Variables
################################################################################

##==============================================================================
# Directories
SRC_D     = pymind
TST_D     = tests
ENV_DIR   = .venv

##==============================================================================
# File Paths
ifeq ($(shell uname -s), "Windows_NT")
BIN     = $(ENV_DIR)/Scripts
else
BIN     = $(ENV_DIR)/bin
endif
PYTHON  = python

##==============================================================================
# Makefile configuration
.PHONY: all setup install update run debug clean test help doc

################################################################################
# Recipes
################################################################################

##==============================================================================
#
all: setup update run ## Default action

##==============================================================================
#
.ONESHELL:
test: setup ## Run unit tests
	source $(BIN)/activate
	$(PYTHON) -m unittest discover -s $(TST_D) -p "test_*.py"

##==============================================================================
#
.ONESHELL:
setup: ## Set up the project
	$(PYTHON) -m venv $(ENV_DIR)
	ls $(BIN)
	source $(BIN)/activate
	@pip install --upgrade pip
	@pip install .

##==============================================================================
#
.ONESHELL:
update: ## Update the virtual environment packages
	@source $(BIN)/activate
	@pip install --upgrade pip
	@pip install .

##==============================================================================
#
.ONESHELL:
run: ## Execute the program
	make setup
	source $(BIN)/activate
	$(PYTHON) pymind

##==============================================================================
#
doc: ## Generate SIG documentation
	doxygen Doxyfile

##==============================================================================
#
debug: ## Enable the debugger (requires `pudb`)
	@source $(BIN)/activate  && \
	cd $(SRC_D)              && \
	python -m pudb main.py

##==============================================================================
#
clean: ## Cleanup the project
	rm -rfv $(ENV_DIR)

##==============================================================================
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## Auto-generated help menu
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	sort                                                | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
