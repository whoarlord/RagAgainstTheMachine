
RUN=uv run
PYTHON=python -m

run:
	$(RUN) $(PYTHON)

install:
	uv sync