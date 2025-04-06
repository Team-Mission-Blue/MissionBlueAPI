<!-- CONTRIBUTING.md is based on the provided in the Red Queen Repo: https://github.com/Qiskit/red-queen/blob/a9f396b16c88cea9c9987cd379526c0624e22323/CONTRIBUTING.md -->

# Contributing

First read the overall project contributing guidelines. These are all
included in the ReadMe file of this repo:

<https://github.com/Team-Mission-Blue/MissionBlueAPI/blob/6d8f8f29bfd135fc6769003ca8d0125980390508/README.md>

## Contributing to Mission Blue API

## Style and lint

Mission Blue uses 2 tools for verify code formatting and lint checking. The
first tool is [black](https://github.com/psf/black) which is a code formatting
tool that will automatically update the code formatting to a consistent style.
The second tool is [ruff](https://github.com/astral-sh/ruff) which is a code linter
which does a deeper analysis of the Python code to find both style issues and
potential bugs and other common issues in Python.

You can check that your local modifications conform to the style rules
by running `nox` which will run `black` and `ruff` to check the local
code formatting and lint. You will need to have [nox](https://github.com/wntrblm/nox)
installed to run this command. You can do this with `pip install -U nox`.

If black returns a code formatting error you can run `nox -s format` to
automatically update the code formatting to conform to the style. However,
if `ruff` returns any error you will have to fix these issues by manually
updating your code.
