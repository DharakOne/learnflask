from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r users %r>' % (self.name, self.users)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r >' % self.username

   


@app.route('/')
def hola_mundo():
    return '<h1>Hello World!</h1>'


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
