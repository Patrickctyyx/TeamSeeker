from app.models import User, Student, Teacher, Item, Project, Competition, Application, db


def test_model():

    user1 = User(
        openid='1',
        identity=1
    )
    user2 = User(
        openid='2',
        identity=0
    )
    user3 = User(
        openid='3',
        identity=0
    )
    user4 = User(
        openid='4',
        identity=0
    )

    teacher = Teacher(
        openid='1'
    )

    student1 = Student(
        openid='2'
    )
    student2 = Student(
        openid='3'
    )
    student3 = Student(
        openid='4'
    )

    item1 = Item()
    item2 = Item()
    item3 = Item()

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(teacher)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.commit()

    project = Project(
        id=item1.id,
        tea_id=teacher.openid,
        students=[student1, student2]
    )
    db.session.add(project)
    db.session.commit()

    competition1 = Competition(
        id=item2.id,
        publisher_id=student3.openid,
        students=[student2, student3]
    )
    db.session.add(competition1)
    db.session.commit()

    competition2 = Competition(
        id=item3.id,
        publisher_id=student2.openid,
        students=[student2, student1]
    )
    db.session.add(competition2)
    db.session.commit()

    application1 = Application(
        item_id=project.id,
        stu_id=student3.openid
    )

    application2 = Application(
        item_id=competition2.id,
        stu_id=student3.openid
    )

    db.session.add(application1)
    db.session.add(application2)
    db.session.commit()

    print(teacher.projects.all())
    print(student1.projects.all())
    print(student1.competitions.all())
    print(student2.projects.all())
    print(student2.competitions.all())
    print(student3.competitions.all())
    print(project.students)
    print(competition1.students)
    print(competition2.students)
    print(student3.applications)



