from flask_migrate import Migrate

from pinterest import create_app, db, socketio

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    socketio.run(app, debug=True)
