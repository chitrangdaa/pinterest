from flask_migrate import Migrate

from pinterest import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
