import unittest
from app import create_app
from app.models import db, Teacher, Student, Project, Competition, User, Item


class TestApi(unittest.TestCase):
    def setUp(self):
        app = create_app('test')
        self.client = app.test_client()
        db.app = app

        db.create_all()

        db.session.add(User(
            openid='teacher1',
            identity=1,
            name='wkm',
            email='wkm@gmail.com'
        ))
        db.session.add(Teacher(
            openid='teacher1',
            p_num='t01'
        ))
        db.session.add(User(
            openid='student1',
            identity=0,
            name='cty',
            email='cty@gmail.com'
        ))
        db.session.add(Student(
            openid='student1',
            s_num='s01'
        ))
        db.session.add(User(
            openid='student2',
            identity=0,
            name='lf',
            email='lf@gmail.com'
        ))
        db.session.add(Student(
            openid='student2',
            s_num='s02'
        ))
        db.session.add(User(
            openid='student3',
            identity=0,
            name='yrb',
            email='yrb@gmail.com'
        ))
        db.session.add(Student(
            openid='student3',
            s_num='s03'
        ))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_wxlogin(self):
        result = self.client.post(
            '/api/wxlogin',
            data=dict(js_code='test')
        )
        self.assertTrue('invalid js code' in result.get_data(as_text=True))

