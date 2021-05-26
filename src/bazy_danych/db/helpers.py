from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BogusLessonInstance:
    lesson_name: str
    teacher_name: str
    class_name: str
    begin_time: datetime
    end_time: datetime
    class_id: int
    lesson_id: int


@dataclass(frozen=True)
class BogusStudent:
    id: int
    name: str
    class_id: int

@dataclass(frozen=True)
class BogusClass:
    id: int
    name: str

@dataclass(frozen=True)
class BogusGrade:
    id: int
    grade: float
    timestamp: datetime
    comment: str

@dataclass(frozen=True)
class BogusLesson:
    id: int
    name: str

def cursor_to_iterable(cursor):
    while True:
        next_result = cursor.fetchone()

        if next_result is None:
            break

        yield next_result


def get_lesson_instances_for_student_id(student_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT lesson_name, teacher_name, class_name, begin_time, end_time, class_id, lesson_id
        FROM lesson_instance_view
            INNER JOIN enrolls ON lesson_instance_view.lesson_id = enrolls.lesson_id
        WHERE enrolls.student_id = :student_id
    """, student_id=student_id)

    return (BogusLessonInstance(*lesson_instance_tuple) for lesson_instance_tuple in cursor_to_iterable(cursor))


def get_lesson_instances_for_teacher_id(teacher_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT lesson_name, teacher_name, class_name, begin_time, end_time, class_id, lesson_id
        FROM lesson_instance_view
        WHERE teacher_id = :teacher_id
    """, teacher_id=teacher_id)

    return (BogusLessonInstance(*lesson_instance_tuple) for lesson_instance_tuple in cursor_to_iterable(cursor))


def get_class_for_id(class_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT id, name
        FROM class
        WHERE id = :class_id
    """, class_id=class_id)

    return BogusClass(*cursor.fetchone())


def get_students_for_class_id(class_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT id, name, class_id
        FROM student
        WHERE
            class_id = :class_id
    """, class_id=class_id)

    return (BogusStudent(*student_tuple) for student_tuple in cursor_to_iterable(cursor))

def get_students_for_lesson_id(lesson_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT student.id, student.name, student.class_id
        FROM student
            INNER JOIN enrolls ON student.id = enrolls.student_id
        WHERE enrolls.lesson_id = :lesson_id
    """, lesson_id=lesson_id)

    return (BogusStudent(*student_tuple) for student_tuple in cursor_to_iterable(cursor))


def get_grades_for_student_for_lesson(student_id: int, lesson_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT id, grade, timestamp, mycomment
        FROM grades
        WHERE
            student_id = :student_id
            AND lesson_id = :lesson_id
    """, lesson_id=lesson_id, student_id=student_id)

    return (BogusGrade(*grade_tuple) for grade_tuple in cursor_to_iterable(cursor))
