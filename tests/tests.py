import unittest
from app import create_app
from app.models import db, Teacher, Student, Project, Competition, User, Item
from app.errors import InvalidJSCode


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

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
            s_num='s01',
            level='college',
            enter_year='2015'
        ))
        db.session.add(User(
            openid='student2',
            identity=0,
            name='lf',
            email='lf@gmail.com'
        ))
        db.session.add(Student(
            openid='student2',
            s_num='s02',
            level='college',
            enter_year='2015'
        ))
        db.session.add(User(
            openid='student3',
            identity=0,
            name='yrb',
            email='yrb@gmail.com'
        ))
        db.session.add(Student(
            openid='student3',
            s_num='s03',
            level='college',
            enter_year='2015'
        ))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_wxlogin(self):

        result = self.client.post(
            '/api/wxlogin',
            data=dict(js_code='test')
        )

        self.assertTrue('invalid js code' in result.data.decode())

    def test_student_post_success(self):
        s4 = User(openid='student4')
        db.session.add(s4)
        db.session.commit()

        token = s4.generate_auth_token()

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 0,
                'name': 'wlz',
                'email': 'wlz@gmail.com',
                'university': 'jnu',
                'college': 'economy',
                'department': 'accounting',
                's_num': 's04',
                'level': 'college',
                'enter_year': '2015'
            }
        )

        self.assertEqual(result.status_code, 200)
        s4_dtl = Student.query.get('student4')
        self.assertEqual(s4_dtl.s_num, 's04')

    def test_teacher_post_success(self):
        t2 = User(openid='teacher2')
        db.session.add(t2)
        db.session.commit()

        token = t2.generate_auth_token()

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 1,
                'name': 'wlf',
                'email': 'wlf@gmail.com',
                'university': 'jnu',
                'college': 'ist',
                'department': 'ns',
                'p_num': 't02'
            }
        )

        self.assertEqual(result.status_code, 200)
        t2_dtl = Teacher.query.get('teacher2')
        self.assertEqual(t2_dtl.p_num, 't02')

    def test_teacher_post_lackinfo(self):
        t2 = User(openid='teacher2')
        db.session.add(t2)
        db.session.commit()

        token = t2.generate_auth_token()

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 1,
                'name': 'wlf',
                'email': 'wlf@gmail.com',
                'university': 'jnu',
                'college': 'ist',
                'department': 'ns'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('lack of' in result.data.decode())

    def test_student_post_lackinfo(self):
        s4 = User(openid='student4')
        db.session.add(s4)
        db.session.commit()

        token = s4.generate_auth_token()

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 0,
                'name': 'wlz',
                'email': 'wlz@gmail.com',
                'university': 'jnu',
                'college': 'economy',
                'department': 'accounting',
                's_num': 's04',
                'level': 'college'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('lack of' in result.data.decode())

    def test_auth_post_invalid_token(self):
        s4 = User(openid='student4')
        db.session.add(s4)
        db.session.commit()

        token = 'invalid token'

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 0,
                'name': 'wlz',
                'email': 'wlz@gmail.com',
                'university': 'jnu',
                'college': 'economy',
                'department': 'accounting',
                's_num': 's04',
                'level': 'college',
                'enter_year': '2015'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('invalid token' in result.data.decode())

    def test_student_post_duplicate(self):
        s4 = User(openid='student4')
        db.session.add(s4)
        db.session.commit()

        token = s4.generate_auth_token()

        result = self.client.post(
            '/api/auth',
            data={
                'token': token,
                'identity': 0,
                'name': 'wlz',
                'email': 'cty@gmail.com',
                'university': 'jnu',
                'college': 'economy',
                'department': 'accounting',
                's_num': 's03',
                'level': 'college',
                'enter_year': '2015'
            }
        )

        s5 = User(openid='student5')
        db.session.add(s5)
        db.session.commit()

        self.assertEqual(result.status_code, 500)
        self.assertTrue('duplicate' in result.data.decode())

    def test_student_get_info(self):
        result = self.client.get(
            '/api/auth/student1'
        )

        self.assertEqual(result.status_code, 200)
        self.assertTrue('cty' in result.data.decode())

    def test_student_get_not_found(self):
        result = self.client.get(
            '/api/auth/studentA'
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('not exist' in result.data.decode())

    def test_student_put_duplicate(self):
        s1 = User.query.get('student1')

        token = s1.generate_auth_token()

        result = self.client.put(
            '/api/auth',
            data={
                'token': token,
                'email': 'lf@gmail.com',
                'university': 'jnu',
                'college': 'economy',
                'department': 'accounting',
                'level': 'college',
                'enter_year': '2015'
            }
        )

        s5 = User(openid='student5')
        db.session.add(s5)
        db.session.commit()

        print(result.data.decode())
        self.assertEqual(result.status_code, 500)
        self.assertTrue('duplicate' in result.data.decode())
