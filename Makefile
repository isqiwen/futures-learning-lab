.PHONY: check test demo plan
check:
	python3 scripts/validate.py
	python3 -m unittest discover -s tests -v
test:
	python3 -m unittest discover -s tests -v
demo:
	python3 examples/ledger_demo.py
	python3 examples/asof_demo.py
	python3 examples/selection_bias_demo.py
plan:
	python3 scripts/publish.py
