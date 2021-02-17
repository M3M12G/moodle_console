import u_base
import student


class Teacher(u_base.UserBase):
    """Class that defines Teacher's methods"""
    _leading_courses = []
    _rating = []

    def __init__(self, email="unknown", first_name="unknown", surname="unknown", role="teacher", leading_courses=[],
                 rating=[]):
        super(Teacher, self).__init__(email, first_name, surname, role)
        self._leading_courses = leading_courses
        self._rating = rating

    def whois(self):
        super(Teacher, self).whois()
        if len(self._leading_courses) == 0:
            print("Do not have any courses to lead")
        else:
            print("Leading Courses:\n{}".format(self._enrolled_courses))
        if len(self._rating) == 0:
            print("Still did not rated")
            return
        r_sum = 0
        for r in self._rating:
            r_sum = r_sum + r
        avg_rating = r_sum / len(self._rating)
        print("Average rating: {}".format(avg_rating))

    def is_teacher_exists(self):
        db = self.get_db().read_db()
        teachers = db["teachers"]
        for st in teachers:
            if st["email"] == self.get_email():
                return True
                break
        return False

    # used by student to rate teacher
    def rate_teacher(self):
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        rating = int(input("Please, rate student - {} from 1 to 10\n>"))
        if rating < 1 or rating > 10:
            print("There were allowed numbers between 1 to 10")
            return

        users = self.get_db().read_db()
        for t_i in range(len(users["teachers"])):
            if users["teachers"][t_i]["email"] == self.get_email():
                users["teachers"][t_i]["rating"].append(rating)
                break
        self.get_db().write_db(users)
        print("Rating of Teacher completed")

    @staticmethod
    def add_teacher():
        email = input("Please, enter email for new teacher >")
        t = Teacher(email)
        if t.is_teacher_exists():
            print("Teacher with email - {} is already exists. Please, type another email".format(email))
            return
        db = t.get_db().read_db()
        new_teacher = {
            "email": email,
            "first_name": input("Enter first name >"),
            "surname": input("Enter surname >"),
            "role": "teacher",
            "leading_courses": [],
            "rating": []
        }
        db["teachers"].append(new_teacher)
        t.get_db().write_db(db)
        print("New teacher is created")
        registered_t = Teacher(**new_teacher)
        registered_t.whois()
        return

    @staticmethod
    def delete_teacher():
        email = input("Please, enter email of teacher to delete >")
        t = Teacher(email)
        if not t.is_teacher_exists():
            print("Teacher with email - {} is does not exists".format(email))
            return

        db = t.get_db().read_db()
        for t_i in range(len(db["teachers"])):
            if db["teachers"][t_i]["email"] == t.get_email():
                del db["teachers"][t_i]
                break
        t.get_db().write_db(db)
        print("Teacher with email - {} is deleted".format(email))
        return

    @staticmethod
    def get_all_teachers():
        teachers_to_return = []
        users = Teacher.get_db().read_db()
        teachers = users["teachers"]
        for t in teachers:
            teachers_to_return.append(Teacher(**t))
        return teachers_to_return

    @staticmethod
    def print_all_teachers():
        all_t = Teacher.get_all_teachers()
        for t in all_t:
            print(t.whois())
            print("--------------")

    # returns the students of specific course
    def get_students_of_course(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist".format(self.get_email()))
            return
        pass

    # returns the courses name where the teacher is lead
    def get_lead_courses(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        users = self.get_db().read_db()
        for t_i in range(len(users["teachers"])):
            if users["teachers"][t_i]["email"] == self.get_email():
                if len(users["teachers"][t_i]["leading_courses"]) > 0:
                    return users["teachers"][t_i]["leading_courses"]

    def print_my_courses(self):
        # always ensure that the operating teacher is exists in db
        self.get_lead_courses()
        pass

    def mark_student(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        pass

    def add_student_to_course(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        # provide the list of students to enroll them to course
        student.Student.print_all_students()
        pass

    def delete_student_from_course(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        pass

    # used by teacher to rate student
    @staticmethod
    def rate_student_tch_side():
        student_email = input("Please, type the student email to rate >")
        s = student.Student(student_email)
        s.rate_student()


# Test methods to check


'''
COPY AND PASTE test code outside the comments block
Make testing classes, predvaritelno zakommentiv this portion of test code

Teacher.add_teacher()
Teacher.delete_teacher()
Teacher.print_all_teachers()
'''
