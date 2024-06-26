"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Fleaky."""


if __name__ == "__main__":
    main(prog_name="fleaky")  # pragma: no cover
