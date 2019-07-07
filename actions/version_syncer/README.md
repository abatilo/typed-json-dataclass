# version_syncer

Since we're using
[standard-version](https://github.com/conventional-changelog/standard-version) for
controlling our versioning, we run into the problem that standard-version only supports
working with a package.json file by default. We could try to write a plugin, but the
easier option for now is to simply take whatever version gets put into package.json, and
the copy it into the pyproject.toml, so that when we publish the library, we set the
correct version for PyPI.
