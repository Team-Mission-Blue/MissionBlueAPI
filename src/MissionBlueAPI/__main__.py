"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Mission Blue API."""


if __name__ == "__main__":
    main(prog_name="MissionBlueAPI")  # pragma: no cover
