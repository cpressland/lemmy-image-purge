"""Builds the CLI for Lemmy Image Purge."""

import click


@click.group()
def cli() -> None:
    """CLI for Lemmy Image Purge."""


@cli.command(name="purge", context_settings={"max_content_width": 300})
@click.option(
    "--community",
    "-c",
    required=True,
    help="The full path of the community to purge, example: 'https://lemmy.world/c/lemmyshitpost'",
)
@click.option(
    "--domain",
    "-d",
    required=True,
    help="The domain of *your* lemmy, example: 'devops.pizza'",
)
@click.option("--days", "-t", required=True, help="The number of days to purge.")
def _purge(community: str, domain: str, days: int) -> None:
    """Purges images from a Lemmy instance."""
    from lemmy_image_purge.main import Purge

    purge = Purge(community, domain, days)
    purge.cli()


@cli.command(name="version")
def _version() -> str:
    """Get the version of Lemmy Image Purge."""
    import pkg_resources

    click.echo(pkg_resources.get_distribution("lemmy-image-purge").version)


if __name__ == "__main__":
    cli()
