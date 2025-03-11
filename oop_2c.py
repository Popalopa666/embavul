from datetime import datetime, timedelta
from dbm import error

class DeadlineError(Exception):
    def __init__(self, message="You are late"):
        self.message = message
        super().__init__(self.message)

class Person:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

class Homework:
    def __init__(self, text, days):
        self.text = text
        self.deadline = timedelta(days=days)
        self.created = datetime.now()

    def is_active(self):
        return datetime.now() < self.created + self.deadline

class Teacher(Person):
    homework_done = {}

    @staticmethod
    def create_homework(text, days):
        return Homework(text, days)

    @classmethod
    def check_homework(cls, homework_result):
        if len(homework_result.solution) > 5:
            if homework_result.homework not in cls.homework_done:
                cls.homework_done[homework_result.homework] = set()
            cls.homework_done[homework_result.homework].add(homework_result)
            return True
        else:
            return False

    @classmethod
    def reset_results(cls, homework=None):
        if homework:
            if homework in cls.homework_done:
                del cls.homework_done[homework]
        else:
            cls.homework_done.clear()

class Student(Person):

    def do_homework(self, homework, solution):
        if homework.is_active():
            return HomeworkResult(homework, self, solution)
        else:
            raise DeadlineError("You are late")

class HomeworkResult:
    def __init__(self, homework, author, solution):
        if not isinstance(homework, Homework):
            raise ValueError("Неверный классовый объект.")

        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = datetime.now()




opp_teacher = Teacher('Daniil', 'Shadrin')
advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

lazy_student = Student('Roman', 'Petrov')
good_student = Student('Lev', 'Sokolov')

oop_hw = opp_teacher.create_homework('Learn OOP', 1)
docs_hw = opp_teacher.create_homework('Read docs', 5)

result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
result_3 = lazy_student.do_homework(docs_hw, 'done')
try:
    result_4 = HomeworkResult(good_student, "fff", "Solution")
except Exception:
    print('There was an exception here')
opp_teacher.check_homework(result_1)
temp_1 = opp_teacher.homework_done

advanced_python_teacher.check_homework(result_1)
temp_2 = Teacher.homework_done
assert temp_1 == temp_2

opp_teacher.check_homework(result_2)
opp_teacher.check_homework(result_3)

print(Teacher.homework_done[oop_hw])
print(Teacher.homework_done[docs_hw])
Teacher.reset_results()