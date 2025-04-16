from sqlmodel import SQLModel


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
