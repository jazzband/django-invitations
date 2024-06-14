[![Jazzband](https://jazzband.co/static/img/jazzband.svg)](https://jazzband.co/)

This is a [Jazzband](https://jazzband.co/) project. By contributing you agree to abide by the [Contributor Code of Conduct](https://jazzband.co/about/conduct) and follow the [guidelines](https://jazzband.co/about/guidelines).

# Setting up

`django-invitations` uses [Poetry] to build and package the project.
We recommend that you use it to manage your virtual environment during development as well.
You can install it using [`pipx`][pipx] like this:

    pipx install poetry

Install all dependencies mentioned in `poetry.lock` by running:

    poetry install --with=dev

# Translation files

In order to update the Gettext `.po` files with any changed translatable strings, run:

    poetry run make po

To compile `.mo` files from the `.po` files, run:

    poetry run make mo

# Tests

You can run the tests using [`tox`][tox], like this:

    poetry run tox

There are also tests that check for simple coding issues and stylistic issues.
We use a framework (confusingly) named [pre-commit] to check for these issues.
Run it like this:

    poetry run pre-commit run --all-files

If you would like to run the pre-commit tests automatically before making a Git commit, modify `.git/hooks/pre-commit`.
You can do this in one step by running:

    poetry run pre-commit install

# Documentation

The docs are found under the `docs/` directory. They are in [reStructuredText].
To build the docs into HTML, run:

    cd docs
    make html

Now open `docs/_build/html/index.html` in your browser.

[Poetry]: https://python-poetry.org/
[pipx]: https://pipx.pypa.io/stable/
[tox]: https://tox.wiki/
[pre-commit]: https://pre-commit.com/
[reStructuredText]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
