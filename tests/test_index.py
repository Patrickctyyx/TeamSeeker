import uuid
import random
import unittest
from app import create_app
from app.models import db, Teacher, Student, Project, Competition, User, Item, Application
from pypinyin import lazy_pinyin


try:
    from utils.fake_name import get_name
except Exception:
    from .utils.fake_name import get_name


def generate_fake_user():
    dep = [
        ['信息科学与技术学院', '计算机科学系'],
        ['公共管理与应急管理学院', '行政管理系'],
        ['经济学院', '经济学系']
    ]
    for i in range(15):
        name = get_name()
        openid = str(uuid.uuid4())
        identity = 0
        cur_dep = dep[random.randint(0, 2)]

        if i == 0 or i % 5 == 0:
            identity = 1

        db.session.add(User(
            openid=openid,
            identity=identity,
            name=name,
            email=''.join(lazy_pinyin(name)) + '@email.com',
            wx_id=''.join(lazy_pinyin(name)),
            university='暨南大学',
            college=cur_dep[0],
            department=cur_dep[1],
            introduction=cur_dep[0] + '/' + cur_dep[1]
        ))

        if identity:
            db.session.add(Teacher(
                openid=openid,
                p_num='T000' + '%03d' % i
            ))
        else:
            db.session.add(Student(
                openid=openid,
                s_num='S000' + '%03d' % i,
                level='college',
                enter_year=2015
            ))
    db.session.commit()


def generate_fake_item_and_application():
    students = Student.query.all()
    teachers = Teacher.query.all()
    status_list = ['pending', 'processing', 'ended']
    theme_list = ['人工智能', '大数据', '区块链', 'Web 安全', '深度学习']
    comp_list = [
        '港澳台侨学生创新创业大赛',
        '大学生创新创业大赛',
        '挑战杯',
        '赢在创新'
    ]

    for teacher in teachers:
        num = random.randint(3, 8)
        item = Item(
            type=1,
            num=num,
            current_num=0,
            status=random.choice(status_list),
            requires='不限'
        )
        db.session.add(item)
        db.session.flush()
        theme = random.choice(theme_list)
        proj = Project(
            id=item.id,
            tea_id=teacher.openid,
            theme=theme,
            introduction=theme
        )
        for _ in range(random.randint(0, num)):
            i = random.randint(0, len(students) - 1)
            proj.students.append(students[i])
            item.current_num += 1
        db.session.add(proj)

    i = 0
    for student in students:
        i += 1
        if i % 2 == 0:
            continue
        num = random.randint(3, 8)
        item = Item(
            type=0,
            num=num,
            current_num=0,
            status=random.choice(status_list),
            requires='不限'
        )
        db.session.add(item)
        db.session.flush()
        comp = Competition(
            id=item.id,
            comp_name=random.choice(comp_list),
            publisher_id=student.openid
        )
        for _ in range(random.randint(0, num)):
            i = random.randint(0, len(students) - 1)
            comp.students.append(students[i])
            item.current_num += 1
        db.session.add(comp)

    db.session.commit()

    items = Item.query.all()
    for item in items:
        for _ in range(random.randint(0, len(students) - 1)):
            i = random.randint(0, len(students) - 1)
            if item.type == 1:
                if item.project and students[i] in item.project.students:
                    continue
            elif item.type == 0:
                if item.competition and students[i] in item.competition.students:
                    continue
            apply = Application.query.filter_by(
                stu_id=students[i].openid,
                item_id=item.id
            ).first()
            if apply:
                continue
            apply = Application(
                stu_id=students[i].openid,
                item_id=item.id,
                content='我想一起组队',
                status=random.choice([-1, 0, 1])
            )
            if item.apply_count:
                item.apply_count += 1
            else:
                item.apply_count = 1
            db.session.add(apply)

    db.session.commit()


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()
        generate_fake_user()
        generate_fake_item_and_application()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        result = self.client.get(
            '/api/index'
        )

        with open('index_output.txt', 'w') as f:
            f.write(result.data.decode())

        self.assertEqual(result.status_code, 200)

    def test_published(self):
        users = User.query.all()
        with open('published_output.txt', 'w') as f:
            f.write('')

        for user in users:
            result = self.client.get(
                '/api/published',
                data={'publisher_id': user.openid}
            )

            with open('published_output.txt', 'a') as f:
                f.write(str(user.identity) + '\n')
                f.write(user.openid + '\n')
                f.write(result.data.decode() + '\n')

            self.assertEqual(result.status_code, 200)

    def test_sent_application(self):
        users = User.query.all()

        with open('sent_application_output.txt', 'w') as f:
            f.write('')

        for user in users:
            if user.identity == 1:
                continue
            token = user.generate_auth_token()

            result = self.client.get(
                '/api/sent',
                data={'token': token}
            )

            with open('sent_application_output.txt', 'a') as f:
                f.write(user.openid + '\n')
                f.write(result.data.decode() + '\n')

            self.assertEqual(result.status_code, 200)

    def test_received_application(self):
        users = User.query.all()

        with open('received_application_output.txt', 'w') as f:
            f.write('')

        for user in users:
            token = user.generate_auth_token()

            result = self.client.get(
                '/api/received',
                data={'token': token}
            )

            with open('received_application_output.txt', 'a') as f:
                f.write(user.openid + '\n')
                f.write(result.data.decode() + '\n')

            self.assertEqual(result.status_code, 200)


