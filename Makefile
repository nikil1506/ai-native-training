.PHONY: doctor test docs coverage gateway
doctor:    ## confirm your key/model works and the starters are present
	python scripts/doctor.py
test:
	python -m unittest discover tests
docs:      ## regenerate docs/programme from the HTML guide
	python scripts/html_to_docs.py
coverage:  ## check the repo covers everything the guide names
	python scripts/check_coverage.py
gateway:   ## shared gateway with per-participant caps + usage dashboard
	python -m gateway
