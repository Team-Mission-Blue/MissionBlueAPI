import nox


@nox.session
def all(session: nox.Session) -> None:
    """Run all sessions in sequence: format, lint, tests."""
    session.notify("format")
    session.notify("lint")
    session.notify("tests")


@nox.session
def tests(session: nox.Session) -> None:
    session.install("-r", "requirements.txt")
    session.run(
        "coverage",
        "run",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "*_test.py",
    )
    session.run("coverage", "report", "--fail-under=90")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", "--fix")


@nox.session
def format(session: nox.Session) -> None:
    session.install("black")
    session.run("black", ".")
