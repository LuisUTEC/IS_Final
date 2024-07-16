from flask import Flask
from routes import app as routes_blueprint
from database import db

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
