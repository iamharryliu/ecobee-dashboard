from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from flaskApp import create_app, db

app = create_app()
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command("runserver", Server(port=8000))
manager.add_command("db", MigrateCommand)
from flaskApp.models import *

if __name__ == "__main__":
    manager.run()
