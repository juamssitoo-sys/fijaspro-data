# Metadata and coverage reports

Only coverage metadata, provenance manifests, and validation reports belong here by default.
Do not place third-party match/player datasets here until their license and upstream terms permit local storage and redistribution.

Run the NBA catalog audit locally:
`pip install -r requirements.txt && python scripts/coverage_audit.py`

The audit reads the public catalog metadata and stores only a coverage report; it does not copy game/player rows.
