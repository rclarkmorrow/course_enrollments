from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app
from database.models import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
