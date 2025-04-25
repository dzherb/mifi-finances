from pathlib import Path

from alembic.command import revision
from alembic.config import Config
import paracelsus.cli  # type: ignore
from paracelsus.cli import ColumnSorts, Formats, get_graph_string, inject


def inject_mermaid_schema_to_readme() -> None:
    from models.base import import_all_models

    readme_path = Path(__file__).parent.parent.parent / 'README.md'

    # monkey patch to adjust types in the graph
    paracelsus.cli.get_graph_string = _get_graph_string

    import_all_models()

    inject(
        file=readme_path,
        base_class_path='models.base:BaseModel',
        column_sort=ColumnSorts.preserve,
        format=Formats.mermaid,
        replace_begin_tag='<!-- BEGIN_DB_SCHEMA_DOCS -->',
        replace_end_tag='<!-- END_DB_SCHEMA_DOCS -->',
    )


def _get_graph_string(*args, **kwargs) -> str:  # type: ignore
    return _clean_sqlalchemy_types(get_graph_string(*args, **kwargs))


def _clean_sqlalchemy_types(mmd_graph: str) -> str:
    # mermaid doesn't except commas and spaces in types,
    # so we have to update things like NUMERIC(12, 5) to NUMERIC(12_5)
    return mmd_graph.replace(', ', '_')


def make_migrations() -> None:
    """Creates a new Alembic migration revision
    and updates the schema diagram in README.md."""
    revision(
        config=Config(Path(__file__).parent.parent / 'alembic.ini'),
        message=input('Revision message: '),
        autogenerate=True,
    )
    inject_mermaid_schema_to_readme()


if __name__ == '__main__':
    make_migrations()
