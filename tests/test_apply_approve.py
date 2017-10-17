import unittest
from app import create_app
from app.models import db, Teacher, Student, Project, Competition, User, Item, Application


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
        item = Item(
            type=1,
            num=6,
            status='ended',
            ddl='2017-12-25',
            requires='happy is just fine'
        )
        db.session.add(item)
        item2 = Item(
            type=0,
            num=6,
            status='pending',
            ddl='2017-12-25',
            requires='emmmmmmmmmc'
        )
        db.session.add(item)
        db.session.add(item2)
        db.session.flush()

        proj = Project(
            id=item.id,
            tea_id='teacher1',
            theme='block chain',
            introduction='bitcoin is a application of block chain'
        )
        db.session.add(proj)
        comp = Competition(
            id=item2.id,
            comp_name='bigchuang',
            publisher_id='student1'
        )
        db.session.add(comp)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_apply_post_successful(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result = self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': '教练我想打篮球'
            }
        )

        result2 = self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 2,
                'content': 'uffffffffffffs'
            }
        )

        self.assertEqual(result.status_code, result2.status_code)
        self.assertTrue('ok' in result.data.decode())

    def test_apply_identity_fault(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        result = self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': '教练我想打篮球'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('permission does not' in result.data.decode())

    def test_duplicate_apply(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result = self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': '教练我想打篮球'
            }
        )

        result2 = self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': 'uffffffffffffs'
            }
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result2.status_code, 500)
        self.assertTrue('duplicate' in result2.data.decode())

    def test_apply_put_successful(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        apply = Application(
            stu_id='student1',
            item_id=1
        )

        db.session.add(apply)
        db.session.flush()

        result = self.client.put(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': '教练我想打篮球'
            }
        )

        self.assertEqual(result.status_code, 200)
        self.assertTrue('ok' in result.data.decode())
        self.assertTrue('教练我想打篮球' in apply.content)

    def test_apply_put_not_found(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result = self.client.put(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': '教练我想打篮球'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('exist' in result.data.decode())

    def test_apply_get_successful(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result0 = self.client.get(
            '/api/apply/1'
        )

        self.client.post(
            '/api/apply',
            data={
                'token': token,
                'item_id': 1,
                'content': 'are you ok'
            }
        )

        result2 = self.client.get(
            '/api/apply/1'
        )

        self.assertTrue('[]' in result0.data.decode())
        self.assertTrue('are you ok' in result2.data.decode())

    def test_apply_delete_successful(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        apply = Application(
            stu_id='student1',
            item_id=1
        )

        db.session.add(apply)
        db.session.flush()
        id = apply.id

        result = self.client.delete(
            '/api/apply/1',
            data={'token': token}
        )

        after_apply = Application.query.get(id)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('ok' in result.data.decode())
        self.assertTrue(after_apply is None)

    def test_approve_successful(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        stu1 = User.query.get('student1')
        token2 = stu1.generate_auth_token()

        apply = Application(
            stu_id='student1',
            item_id='1'
        )
        apply2 = Application(
            stu_id='student2',
            item_id=2
        )
        db.session.add(apply)
        db.session.add(apply2)
        db.session.flush()

        result = self.client.post(
            '/api/approve',
            data={
                'token': token,
                'apply_id': apply.id,
                'result': 1
            }
        )

        result2 = self.client.post(
            '/api/approve',
            data={
                'token': token2,
                'apply_id': apply2.id,
                'result': -1
            }
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(apply.status, 1)
        self.assertEqual(result2.status_code, 200)
        self.assertEqual(apply2.status, -1)

    def test_approve_not_found(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        result = self.client.post(
            '/api/approve',
            data={
                'token': token,
                'apply_id': 100,
                'result': 1
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('exist' in result.data.decode())

    def test_approve_permission_denied(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        apply2 = Application(
            stu_id='student2',
            item_id=2
        )
        db.session.add(apply2)
        db.session.flush()

        result = self.client.post(
            '/api/approve',
            data={
                'token': token,
                'apply_id': apply2.id,
                'result': 1
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(apply2.status, 0)
        self.assertTrue('permission' in result.data.decode())
