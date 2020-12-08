from base_app import *
from api import api_blueprint
from websocket import socketio


app.register_blueprint(api_blueprint)
socketio.init_app(app)


if __name__ == '__main__':
    app.run(debug=TEST)

