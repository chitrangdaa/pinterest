from flask_migrate import Migrate

from pinterest import create_app, db, socketio

app = create_app()
migrate = Migrate(app, db)
socketio.run(app, debug=True)
