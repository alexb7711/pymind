################################################################################
# Variables
################################################################################

##==============================================================================
# Directories
SRC_D     = src
TST_D     = tests
ENV_DIR   = .venv

##==============================================================================
# File Paths

ifeq ("$(OS)", "Windows_NT")
BIN     = $(ENV_DIR)/Scripts
else
BIN     = $(ENV_DIR)/bin
endif
PYTHON  = python

################################################################################
# Recipes
################################################################################

##==============================================================================
#
.SILENT:
.PHONY: all
all: setup run ## Default action

##==============================================================================
#
.SILENT:
.PHONY: install
install: uv-check ## Install pymind locally
	uv tool install -e .

##==============================================================================
#
.SILENT:
.PHONY: uninstall
uninstall: uv-check ## Uninstall pymind
	uv tool uninstall pymind

##==============================================================================
#
.ONESHELL:
.SILENT:
.PHONY: setup
test: setup ## Run unit tests
	. "$(BIN)/activate"
	$(PYTHON) -m unittest discover -s $(TST_D) -p "test_*.py"
	coverage run --source=. -m unittest discover -s $(TST_D) -p "test_*.py"
	coverage report

##==============================================================================
#
.ONESHELL:
.SILENT:
.PHONY: setup
setup: uv-check ## Set up the project
	uv sync

##==============================================================================
#
.ONESHELL:
.SILENT:
.PHONY: run
run: uv-check ## Execute the program
	uv run src/pymind

##==============================================================================
#
.ONESHELL:
.SILENT:
.PHONY: doc
doc: upgrade ## Generate documentation
	#@doxygen Doxyfile
	pymind -f -i ./docs -o ./html

##==============================================================================
#
.SILENT:
.PHONY: clean
clean: ## Cleanup the project
	rm -rfv $(ENV_DIR)

##==============================================================================
#
.SILENT:
.PHONY: uv-check
uv-check: ## Ensure `uv` is installed
	 if ! command -v uv 
	 then
		 echo "*** 'uv' is not installed" 
		 exit 1
	 fi

##==============================================================================
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.ONESHELL:
.SILENT:
.PHONY: clean
help:  ## Auto-generated help menu
	grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	sort                                               | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

