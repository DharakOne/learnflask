from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    edad = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r >' % self.username


@app.route('/user', methods=['POST'])
def user():
    print(request.json)
    new_user=User(
        username=request.json["username"],
        edad=request.json["edad"])
    db.session.add_all([new_user])
    db.session.commit()
    return 'Succes'



@app.route('/')
def hola_mundo():
    return '<h1>Hello World!</h1>'


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
