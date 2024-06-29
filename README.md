# mdformat-plugin

[![Build Status](https://img.shields.io/github/actions/workflow/status/gaige/mdformat-pelican/tests.yml?branch=main)](https://github.com/gaige/mdformat-pelican/actions)
[![PyPI Version](https://img.shields.io/pypi/v/mdformat_pelican)](https://pypi.org/project/mdformat_pelican/)
![License](https://img.shields.io/pypi/l/mdformat_pelican?color=blue)

An [mdformat](https://github.com/executablebooks/mdformat) plugin for the pelican static site generator.
[Pelican](https://getpelican.com) is a static site generator and uses markdown with a couple of additions,
namely skipping the K:V pairs at the start and the ability to reference:

- tag
- author
- category
- index
- filename
- static
- attach

Note that the `{name}` forms are supported, and the `|name|` forms are converted to the newer form,
as the pipe form has been deprecated.


## Development

This package utilises [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install these development dependencies:

```bash
pip install tox
```

To run the tests:

```bash
tox
```

and with test coverage:

```bash
tox -e py311-cov
```

The easiest way to write tests, is to edit tests/fixtures.md

To run the code formatting and style checks:

```bash
tox -e py311-pre-commit
```

or directly

```bash
pip install pre-commit
pre-commit run --all
```

To run the pre-commit hook test:

```bash
tox -e py311-hook
```

## Publish to PyPi

Either use flit directly:

```bash
pip install flit
flit publish
```

or trigger the GitHub Action job, by creating a release with a tag equal to the version, e.g. `v0.0.1`.
