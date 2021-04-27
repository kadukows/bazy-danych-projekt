from dataclasses import dataclass

@dataclass(frozen=True)
class BogusLessonInstance:
    id: int
    lesson_name: str
    teacher_name: str
    class_name: str
    begin_time: str
    end_time: str

def get_lesson_instances_for_student_id(student_id: int):
    from . import get_db
    cursor = get_db().cursor()
    lesson_instance_tuples = cursor.execute("""
        SELECT lesson_instance.id, lesson.name, teacher.name, class.name, lesson_instance.begin_time, lesson_instance.end_time
        FROM lesson_instance
            INNER JOIN lesson ON lesson_instance.lesson_id = lesson.id
            INNER JOIN teacher ON lesson_instance.teacher_id = teacher.id
            INNER JOIN class ON lesson_instance.class_id = class.id
        WHERE class.id = :student_id
    """, student_id=student_id).fetchall()

    return [BogusLessonInstance(*lesson_instance_tuple) for lesson_instance_tuple in lesson_instance_tuples]
