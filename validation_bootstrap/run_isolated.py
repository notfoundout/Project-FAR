"""Run ``python -m far_validation`` without letting the checkout shadow the standard library.

``python -m far_validation`` puts the working directory first on ``sys.path``, so a candidate's
top-level ``json.py`` (or ``ast.py``, ``subprocess.py``) replaced the standard-library module
inside the validator itself. For example, it could register an exit hook that turns a failing
weakening check into exit status 0.

Run this file as ``python -I -X pycache_prefix=<dir> validation_bootstrap/run_isolated.py ARGS``:

- ``-I`` drops the script directory and user site-packages from ``sys.path`` and ignores
  ``PYTHON*`` variables;
- the checkout is then appended after the standard library and site-packages, so only
  ``far_validation`` itself resolves from it;
- ``pycache_prefix`` makes Python ignore bytecode committed under ``__pycache__``.

This protects the validator only while no candidate code has run in the same job; afterwards, any
step can be replaced through ``GITHUB_PATH`` or ``GITHUB_ENV``.
"""
import os
import runpy
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
runpy.run_module("far_validation", run_name="__main__", alter_sys=True)
