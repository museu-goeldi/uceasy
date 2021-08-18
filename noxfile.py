import tempfile

import nox


locations = "src", "tests", "noxfile.py"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.7"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "coverage[toml]", "pytest-cov")
    session.run("pytest", *args)


@nox.session(python="3.8")
def coverage(session):
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python=["3.8", "3.7"])
def mypy(session):
    args = session.posargs or locations
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)
