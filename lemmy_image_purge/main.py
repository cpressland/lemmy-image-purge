"""Main module for Lemmy Image Purge app."""
import warnings

import requests
from pendulum import now
from sqlalchemy import create_engine, delete, exc, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from lemmy_image_purge.settings import logger, settings


class Purge:
    """Main Class for Lemmy Image Purge app."""

    def __init__(self, community: str, domain: str, days: int) -> None:
        """Initialize the Purge class.

        Args:
            community (str): The full path of the community to purge, example: 'https://lemmy.world/c/lemmyshitpost'
            domain (str): The domain of *your* lemmy, example: 'devops.pizza'
            days (int): The number of days to purge.
        """
        self.community = community
        self.domain = domain
        self.days = days

        self.engine = create_engine(settings.database_url)
        self.database = automap_base()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            self.database.prepare(autoload_with=self.engine)
        self.table_post = self.database.classes.post
        self.table_community = self.database.classes.community

    def _lookup(self) -> list:
        """Access the Lemmy Database and lookup images to purge."""
        query = (
            select(self.table_post.id, self.table_post.thumbnail_url)
            .join(self.table_community)
            .where(self.table_community.actor_id == self.community)
            .where(self.table_post.thumbnail_url.like("%" + self.domain + "%"))
            .where(self.table_post.published > now().subtract(days=7))
        )
        with Session(self.engine) as session:
            return session.execute(query).all()

    def _purge_pictrs(self, url: str) -> None:
        """Call Pict-rs API, purge image."""
        logger.info(f"Attempting to purge: {url}")
        filename = url.split("/")[-1]
        headers = {"X-Api-Token": settings.pictrs_api_key}
        params = {"alias": filename}
        requests.post(
            settings.pictrs_url + "/internal/purge",
            params=params,
            headers=headers,
            timeout=10,
        )
        logger.info(f"Purged {filename} from Pict-rs.")

    def _purge_lemmy(self, post_id: int) -> None:
        logger.info(f"Attempting to delete post {post_id} from the database.")
        query = delete(self.table_post).where(self.table_post.id == post_id)
        with Session(self.engine) as session:
            session.execute(query)
            session.commit()
        logger.info(f"Deleted Post: {post_id} from the database.")

    def cli(self) -> None:
        """Entrypoint for the CLI to purge images.

        Call the _lookup() function to get a list of images to purge,
        then call the _purge_pictrs() function to purge the image from pictrs,
        then call the _purge_lemmy() function to delete the post from the database.
        """
        lookup = self._lookup()
        for image in lookup:
            post_id = image[0]
            url = image[1]
            self._purge_pictrs(url)
            self._purge_lemmy(post_id)
