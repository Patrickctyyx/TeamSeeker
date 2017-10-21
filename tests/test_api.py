import unittest
from app import create_app
from app.models import db, Teacher, Student, Project, Competition, User, Item


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
            email='wkm@gmail.com',
            wx_id='teacher1'
        ))
        db.session.add(Teacher(
            openid='teacher1',
            p_num='t01'
        ))
        db.session.add(User(
            openid='student1',
            identity=0,
            name='cty',
            email='cty@gmail.com',
            wx_id='student1'
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
            email='lf@gmail.com',
            wx_id='student2'
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
            email='yrb@gmail.com',
            wx_id='student3'
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

        u = User.query.get(s4.openid)

        self.assertEqual(result.status_code, 500)
        self.assertTrue('duplicate' in result.data.decode())
        self.assertEqual(u.name, None)

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

        s5 = User(openid='student5', email='test@email.com')
        db.session.add(s5)

        s6 = User(openid='student6', email='test2@email.com')
        db.session.add(s6)
        db.session.commit()

        print(result.data.decode())
        self.assertEqual(result.status_code, 500)
        self.assertTrue('duplicate' in result.data.decode())

    def test_student_post_item_success(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 0,
                'status': 'pending',
                'requires': 'handsome',
                'comp_name': 'bigchuanghahaha'
            }
        )

        comp = Competition.query.filter_by(comp_name='bigchuanghahaha').first()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(stu1.openid, comp.publisher_id)

    def test_student_post_item_duplicate(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        item = Item(
            type=0,
            requires='handsome'
        )
        db.session.add(item)
        db.session.flush()

        item_dtl = Competition(
            id=item.id,
            publisher_id=stu1.openid
        )
        db.session.add(item_dtl)
        db.session.commit()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 0,
                'status': 'pending',
                'requires': 'handsome',
                'comp_name': 'bigchuanghahaha'
            }
        )

        comp = Competition.query.filter_by(comp_name='bigchuanghahaha').first()

        self.assertEqual(result.status_code, 500)
        self.assertEqual(comp, None)

    def test_student_post_permission_not_match(self):
        stu1 = User.query.get('student1')
        token = stu1.generate_auth_token()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 1,
                'status': 'pending',
                'requires': 'handsome'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('permission does not match' in result.data.decode())

    def test_teacher_post_item_success(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 1,
                'status': 'processing',
                'requires': 'handsome as well',
                'theme': 'block chain',
                'introduction': 'bitcoin is a application of block chain'
            }
        )

        proj = Project.query.filter_by(tea_id=tea1.openid).first()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(proj.theme, 'block chain')

    def test_teacher_post_item_duplicate(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        item = Item(
            type=1,
            requires='handsome as well'
        )
        db.session.add(item)
        db.session.flush()

        item_dtl = Project(
            id=item.id,
            tea_id=tea1.openid
        )
        db.session.add(item_dtl)
        db.session.commit()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 1,
                'status': 'pending',
                'requires': 'handsome as well',
                'theme': 'block chain',
                'introduction': 'bitcoin is a application of block chain'
            }
        )

        comp = Project.query.filter_by(theme='block chain').first()

        self.assertEqual(result.status_code, 500)
        self.assertEqual(comp, None)

    def test_teacher_post_permission_not_match(self):
        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        result = self.client.post(
            '/api/create',
            data={
                'token': token,
                'type': 0,
                'status': 'pending',
                'requires': 'handsome'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('permission does not match' in result.data.decode())

    def test_item_get_success(self):
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

        result = self.client.get(
            '/api/create/' + str(item.id)
        )
        result2 = self.client.get(
            '/api/create/' + str(item2.id)
        )

        self.assertTrue('bitcoin is a application of block chain' in result.data.decode())
        self.assertTrue('bigchuang' in result2.data.decode())

    def test_item_get_lackinfo(self):
        result = self.client.get(
            '/api/create'
        )

        self.assertTrue('lack of' in result.data.decode())

    def test_item_get_not_found(self):
        result = self.client.get(
            '/api/create/666'
        )

        self.assertTrue('not exist' in result.data.decode())

    def test_project_put_successful(self):
        item = Item(
            type=1,
            num=6,
            status='ended',
            ddl='2017-12-25',
            requires='happy is just fine'
        )
        db.session.add(item)
        db.session.flush()

        proj = Project(
            id=item.id,
            tea_id='teacher1',
            theme='block chain',
            introduction='bitcoin is a application of block chain'
        )
        db.session.add(proj)
        db.session.commit()

        tea1 = User.query.get('teacher1')
        token = tea1.generate_auth_token()

        result = self.client.put(
            '/api/create',
            data={
                'token': token,
                'id': item.id,
                'num': 5,
                'status': 'processing',
                'ddl': '2018-1-1',
                'requires': 'handsome',
                'theme': 'ai',
                'introduction': 'artificial intelligence'
            }
        )

        the_proj = Item.query.get(item.id)
        proj_find = Project.query.get(item.id)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(the_proj.num, 5)
        self.assertTrue(the_proj.status, 'processing')
        self.assertEqual(proj_find.theme, 'ai')

    def test_item_put_permission_not_match(self):
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

        stu2 = User.query.get('student2')
        token = stu2.generate_auth_token()

        result = self.client.put(
            '/api/create',
            data={
                'token': token,
                'id': item.id,
                'num': 5,
                'status': 'processing',
                'ddl': '2018-1-1',
                'requires': 'handsome',
                'theme': 'ai',
                'introduction': 'artificial intelligence'

            }
        )

        result2 = self.client.put(
            '/api/create',
            data={
                'token': token,
                'id': item2.id,
                'num': 5,
                'status': 'processing',
                'ddl': '2018-1-1',
                'requires': 'handsome',
                'comp_name': 'smallchuang'
            }
        )

        self.assertEqual(result.status_code, 500)
        self.assertTrue('permission does not match' in result.data.decode())
        self.assertEqual(result2.status_code, 500)
        self.assertTrue('permission does not match' in result2.data.decode())
        self.assertFalse(item.num is 5)
        self.assertFalse(item2.status is 'processing')

    def test_item_delete_successful(self):
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

        stu = User.query.get('student1')
        token = stu.generate_auth_token()

        tea1 = User.query.get('teacher1')
        token2 = tea1.generate_auth_token()

        result = self.client.delete(
            '/api/create/' + str(item.id),
            data={
                'token': token2
            }
        )

        result2 = self.client.delete(
            '/api/create/' + str(item2.id),
            data={
                'token': token
            }
        )
        print(result.data.decode())

        self.assertEqual(result.status_code, result2.status_code)
        self.assertTrue('ok' in result.data.decode())
