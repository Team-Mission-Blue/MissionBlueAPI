import nox


@nox.session
def tests(session: nox.Session) -> None:
    # session.install("pytest")
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
