import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

db = SQLAlchemy()


projects = db.Table('proj_stu',
                    db.Column('proj_id', db.Integer, db.ForeignKey('project.id')),
                    db.Column('stu_id', db.Integer, db.ForeignKey('student.openid'))
                    )

competitions = db.Table('comp_stu',
                        db.Column('stu_id', db.Integer, db.ForeignKey('student.openid')),
                        db.Column('comp_id', db.Integer, db.ForeignKey('competition.id'))
                        )


class User(db.Model):

    openid = db.Column(db.String(32), primary_key=True)
    # identity == 1 => teacher, == 0 => student
    identity = db.Column(db.Integer)
    name = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    university = db.Column(db.String(32))
    college = db.Column(db.String(32))
    department = db.Column(db.String(32))
    introduction = db.Column(db.Text)

    teacher = db.relationship(
        'Teacher',
        backref='user',
        uselist=False
    )

    student = db.relationship(
        'Student',
        backref='user',
        uselist=False
    )

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'openid': self.openid})

    @staticmethod
    def verify_auth_token(token):
        if not token:
            return None

        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['openid'])
        return user


class Teacher(db.Model):

    openid = db.Column(db.String(32), db.ForeignKey('user.openid'), primary_key=True)
    p_num = db.Column(db.String(32), unique=True)
    projects = db.relationship(
        'Project',
        backref='teacher',
        lazy='dynamic'
    )


class Student(db.Model):

    openid = db.Column(db.String(32), db.ForeignKey('user.openid'), primary_key=True)
    s_num = db.Column(db.String(32), unique=True)
    level = db.Column(db.Enum('college', 'master', 'doctor'))
    enter_year = db.Column(db.String(8))
    applications = db.relationship(
        'Application',
        backref='student',
        lazy='dynamic'
    )


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # type == 1 => project, == 0 => competition
    type = db.Column(db.Integer)
    # 项目人数
    num = db.Column(db.Integer)
    current_num = db.Column(db.Integer)
    status = db.Column(db.Enum('pending', 'processing', 'ended'))
    ddl = db.Column(db.String(64))
    requires = db.Column(db.Text)
    cred_at = db.Column(db.DateTime, default=datetime.datetime.now)

    project = db.relationship(
        'Project',
        backref='item',
        uselist=False
    )

    competition = db.relationship(
        'Competition',
        backref='item',
        uselist=False
    )

    applications = db.relationship(
        'Application',
        backref='item',
        lazy='dynamic'
    )


class Project(db.Model):

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    tea_id = db.Column(db.Integer, db.ForeignKey('teacher.openid'))
    theme = db.Column(db.String(32))
    introduction = db.Column(db.Text)
    students = db.relationship(
        'Student',
        secondary=projects,
        backref=db.backref('projects', lazy='dynamic')
    )


class Competition(db.Model):

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    comp_name = db.Column(db.String(32))
    publisher_id = db.Column(db.String(32))
    students = db.relationship(
        'Student',
        secondary=competitions,
        backref=db.backref('competitions', lazy='dynamic')
    )


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.ForeignKey('student.openid'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    content = db.Column(db.Text)
    cred_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # status == 1 => proved == 0 => not dealt with == -1 => rejected
    status = db.Column(db.Integer, default=0)




