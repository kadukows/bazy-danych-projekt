from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BogusLessonInstance:
    lesson_name: str
    teacher_name: str
    class_name: str
    begin_time: datetime
    end_time: datetime


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
        SELECT lesson_name, teacher_name, class_name, begin_time, end_time
        FROM lesson_instance_view
            INNER JOIN enrolls ON lesson_instance_view.lesson_id = enrolls.lesson_id
        WHERE enrolls.student_id = :student_id
    """, student_id=student_id)

    return (BogusLessonInstance(*lesson_instance_tuple) for lesson_instance_tuple in cursor_to_iterable(cursor))


def get_lesson_instances_for_teacher_id(teacher_id: int):
    from . import get_db
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT lesson_name, teacher_name, class_name, begin_time, end_time
        FROM lesson_instance_view
        WHERE teacher_id = :teacher_id
    """, teacher_id=teacher_id)

    return (BogusLessonInstance(*lesson_instance_tuple) for lesson_instance_tuple in cursor_to_iterable(cursor))
