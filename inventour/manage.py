def deploy():
    """RUN DEPLOYMENT TASKS"""
    from my-app import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from models import User


    app = create_app()
    app.app_context().push()

    # create database and tables
    db.create_all()

    # migrate database to latest revision
    stamp()
    migrate()
    upgrade()


deploy()