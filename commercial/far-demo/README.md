# FAR hosted demo

The hosted demo is an optional commercial component, not a dependency of the
canonical Project FAR research package. Its runtime and test dependencies are
declared in this directory's `pyproject.toml`.

Run its tests in the component environment:

```bash
python -m pip install -e commercial/far-decision-integrity -e commercial/far-demo
python -m pytest -q commercial/far-demo/tests
```

When repository-wide pytest discovery runs without the optional demo
dependencies, the demo test modules skip at collection with an explicit reason.
They must not fail import collection or be treated as executed component tests.
The canonical repository health suite continues to discover `tests/` through
`tools/run_tests.py`; it does not claim to execute this optional component.
