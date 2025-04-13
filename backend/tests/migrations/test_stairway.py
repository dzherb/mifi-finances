import typing

from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
import pytest

from tests.utils import get_alembic_config


def get_revisions() -> list[Script]:
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    alembic_config = get_alembic_config()

    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(alembic_config)

    # Get & sort migrations, from first to last
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script) -> None:
    upgrade(alembic_config, revision.revision)

    # We need -1 for downgrading first migration (its down_revision is None)
    downgrade(alembic_config, typing.cast(str, revision.down_revision) or '-1')
    upgrade(alembic_config, revision.revision)
