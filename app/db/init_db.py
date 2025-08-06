import logging

from app.db.session import engine
from app.db.base import Base

# Import all the models, so that they are registered on the metadata.
# Otherwise, 'create_all' will not see them and will not create the tables.
from app.models.user import User
from app.models.notification import Notification
from app.models.meal import Meal  # Import the Meal model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")


if __name__ == "__main__":
    init_db()