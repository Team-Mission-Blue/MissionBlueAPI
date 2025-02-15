"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Mission Blue."""


if __name__ == "__main__":
    main(prog_name="mission-blue")  # pragma: no cover
