# ----- DIRECTORY DEFINITION -----

> SQLite database will be created here
> .env needs to be added to this dir with app settings
> Anything with FLASK_ will be added to app.config
> SECRET_KEY and ENCRYPTION_KEY added by app.
> Needs the following for SQLAlchemy.

    FLASK_SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=False
