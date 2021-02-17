import u_base
import teacher
import course


class Student(u_base.UserBase):
    """Class that defines Student's class"""
    _enrolled_courses = []
    _marks = {}
    _rating = []

    def __init__(self, email="unknown", first_name="unknown", surname="unknown", role="student", enrolled_courses=[],
                 marks=[], rating=[]):
        super(Student, self).__init__(email, first_name, surname, role)
        self._enrolled_courses = enrolled_courses
        self._marks = marks
        self._rating = rating

    def whois(self):
        super(Student, self).whois()
        if len(self._enrolled_courses) == 0:
            print("Does not enrolled to any course")
            return
        print("Enrolled Courses:\n{}".format(self._enrolled_courses))

        if len(self._rating) == 0:
            print("Any teacher did not rated you")
            return
        sum = 0
        for r in self._rating:
            sum = sum + r
        avg_rating = sum / len(self._rating)
        print("Average rating: {}".format(avg_rating))

    @staticmethod
    def get_students():
        students_to_return = []
        users = Student.get_db().read_db()
        students = users["students"]
        for st in students:
            students_to_return.append(Student(**st))
        return students_to_return

    @staticmethod
    def add_student():
        email = input("Please, enter email for new student >")
        s = Student(email)
        if s.is_student_exist():
            print("Student with email - {} is already exists. Please, provide another email".format(email))
            return

        db = s.get_db().read_db()

        student = {"email": email,
                   "first_name": input("Enter first name >"),
                   "surname": input("Enter surname >"),
                   "role": "student",
                   "enrolled_courses": [],
                   "marks": [],
                   "rating": []
                   }
        db["students"].append(student)
        s.get_db().write_db(db)
        print("New student is created")
        registered = Student(**student)
        registered.whois()

    @staticmethod
    def delete_student():
        email = input("Please, enter email of student >")
        s = Student(email)
        if not s.is_student_exist():
            print("Student with email - {} is does not exists".format(email))
            return

        db = s.get_db().read_db()
        for st_i in range(len(db["students"])):
            if db["students"][st_i]["email"] == s.get_email():
                del db["students"][st_i]
                break
        s.get_db().write_db(db)
        print("Student with email - {} is deleted".format(email))

    @staticmethod
    def print_all_students():
        all = Student.get_students()
        for st in all:
            print(st.whois())
            print("--------------")

    # just provide email of student into Student instance
    def get_my_marks(self):
        if self.is_student_exist():
            users = self.get_db().read_db()
            students = users["students"]
            for st in students:
                if st["email"] == self.get_email():
                    print("Subject - Mark")
                    for crs in st["marks"]:
                        c, m = list(crs.keys()), list(crs.values())
                        print("{} - {}".format(c, m))
                        print("-------")
                    break
        else:
            print("No student found for email - {}".format(self.get_email()))

    # returns mark of exact course
    def get_my_marks_for(self):
        if not self.is_student_exist():
            print("No student found for email - {}".format(self.get_email()))
            return

        self.print_my_courses()
        course_name = input("Please, type name of subject in order to get marks list >")
        if not self.is_enrolled(course_name):
            print("Student with email - {} is not enrolled to this course".format(self.get_email()))
            return
        users = self.get_db().read_db()
        students = users["students"]
        for st in students:
            print("Subject - Mark")
            for crs in st["marks"]:
                c, m = list(crs.keys()), list(crs.values())
                if c == course_name:
                    print("{} - {}".format(c, m))
                    break

    # is used by teacher to rate student
    def rate_student(self):
        if self.is_student_exist():
            rating = int(input("Please, rate student - {} from 1 to 10\n>"))
            if rating < 1 or rating > 10:
                print("There were allowed numbers between 1 to 10")
                return

            users = self.get_db().read_db()
            for st_i in range(len(users["students"])):
                if users["students"][st_i]["email"] == self.get_email():
                    users["students"][st_i]["rating"].append(rating)
                    break
            self.get_db().write_db(users)
            print("Rating completed")
        else:
            print("No student found for email - {}".format(self.get_email()))

    # check if the user is exist in json file to avoid app crash
    def is_student_exist(self):
        db = self.get_db().read_db()
        students = db["students"]
        for st in students:
            if st["email"] == self.get_email():
                return True
                break
        return False

    # returns the list of courses enrolled by student
    def get_my_courses(self):
        if not self.is_student_exist():
            print("Student with email - {} does not exist".format(self.get_email()))
            return
        users = self.get_db().read_db()
        for st_i in range(len(users["students"])):
            if users["students"][st_i]["email"] == self.get_email():
                if len(users["students"][st_i]["enrolled_courses"]) > 0:
                    return users["students"][st_i]["enrolled_courses"]
                    break

    # used to print all enrolled courses by the student
    def print_my_courses(self):
        courses = self.get_my_courses()
        if courses is None:
            print("You did not enrolled to any course")
            return

        print("My courses:\n|Course name|")
        for crs in courses:
            print(crs)

    # used by admin
    # checks wheter student have this in his/her
    # enrolled courses list
    # also checks from courses side
    def is_enrolled(self, course_name):
        check = 0
        # firstly checking inside users json file
        # inside from student's attribute
        users = self.get_db().read_db()
        for st_i in range(len(users["students"])):
            if users["students"][st_i]["email"] == self.get_email():
                if course_name in users["students"][st_i]["enrolled_courses"]:
                    check = check + 1
                break
        c = course.Course(course_name)
        if c.is_student_enrolled(self.get_email()):
            check = check + 1
        if check == 2:
            return True
        else:
            return False

    # used to enroll student to course by themselves
    def enroll_me_to_course(self):
        courses = course.Course.get_courses()
        if len(courses) == 0:
            print("No courses added. Please, check later")
            return
        # printing all free courses for student
        course.Course.print_all_free_courses()
        course_name = input("Please, type course name to enroll >")

        crs = course.Course(course_name)
        crs.enroll_student(self.get_email())

        users = self.get_db().read_db()
        for st_i in range(len(users["students"])):
            if users["students"][st_i]["email"] == self.get_email():
                if course_name in users["students"][st_i]["enrolled_courses"]:
                    print("You have already enrolled to course {}".format(course_name))
                    return
                users["students"][st_i]["enrolled_courses"].append(course_name)
                break
        self.get_db().write_db(users)
        print("You have joined to the course - {}".format(course_name))

    # unenrolls student from the course
    def unenroll_me_from_course(self):
        if not self.is_student_exist():
            print("Student with email - {} does not exist".format(self.get_email()))
            return

        my_courses = self.get_my_courses()
        for c in my_courses:
            print(c)
        course_name = input("Please, type the name of course from you want to unenroll >")

        c = course.Course(course_name)
        c.unenroll_student(self.get_email())

        target_st = self.get_db().read_db()
        for st_i in range(len(target_st["students"])):
            if target_st["students"][st_i]["email"] == self.get_email():
                target_st["students"][st_i]["enrolled_courses"].remove(course_name)
                # mechanism to erasing marks of unenrolled course from users db
                if len(target_st["students"][st_i]["marks"]) > 0:
                    for m_s in range(len(target_st["students"][st_i]["marks"])):
                        if list(target_st["students"][st_i]["marks"][m_s].keys())[0] == course_name:
                            target_st["students"][st_i]["marks"].remove(target_st["students"][st_i]["marks"][m_s])
                            break
        self.get_db().write_db(target_st)
        print("You've unenrolled from the course - {}".format(course_name))

    # used by students to rate teacher
    @staticmethod
    def rate_teacher_st_side():
        teacher_email = input("Please, provide the email of teacher to rate >")
        t = teacher.Teacher(teacher_email)
        t.rate_teacher()

    @staticmethod
    def print_teachers():
        teacher.Teacher.print_all_teachers()
