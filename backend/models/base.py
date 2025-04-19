from sqlalchemy import MetaData
from sqlmodel import SQLModel

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata = MetaData(naming_convention=naming_convention)

SQLModel.metadata = metadata


class BaseModel(SQLModel):
    pass


def import_all_models() -> None:
    import importlib
    import os

    models_dir = os.path.dirname(__file__).replace('/db', '/models')
    package_name = 'models'

    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'{package_name}.{filename[:-3]}'
            importlib.import_module(module_name)
