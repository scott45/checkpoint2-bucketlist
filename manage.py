#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.v1 import models
from app import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)

if __name__ == '__main__':
    manager.run()
