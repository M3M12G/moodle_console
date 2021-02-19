import db
import course


class UserBase(object):
    """Base class that defines attributes and general methods for all user roles"""
    _file = db.DB("db/users.json")

    def __init__(self, email, first_name, surname, role):
        self._email = email
        self._first_name = first_name
        self._surname = surname
        self._role = role

    @staticmethod
    def get_db():
        return UserBase._file

    # used for printing users details. depending on role
    # representation printing may differ
    def whois(self):
        """
        prints details of User object that is invoked this method
        depending on specific role, the method implementation
        may differ because of additional fields for that roles
        """
        print("Role: {}\nEmail: {}\nFirst Name: {}\nSurname: {}".format(
            self._role,
            self._email,
            self._first_name,
            self._surname
        ))

    # returns user's email, used as an id
    def get_email(self):
        return self._email


# --------------------------------------------------------------------- #

# ROLE - STUDENT. IT'S CLASS AND METHODS

class Student(UserBase):
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
            print("Did not rated by any teacher")
            return
        sum = 0
        for r in self._rating:
            sum = sum + r
        avg_rating = sum / len(self._rating)
        print("Average rating: {}".format(avg_rating))

    @staticmethod
    def get_students():
        """returns mapped instances of Student class with records from json file"""
        students_to_return = []
        users = Student.get_db().read_db()
        students = users["students"]
        for st in students:
            students_to_return.append(Student(**st))
        return students_to_return

    @staticmethod
    def add_student():
        """
            writes to json file the records of provided student
            in structure of Student class
        """
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
        """
            deletes the records of specified student from json file
        """
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

    def get_my_marks(self):
        """
        returns list of marks provided student, where records is stored as "Course : Mark" is stored as
        dict object in json file
        """
        if self.is_student_exist():
            users = self.get_db().read_db()
            students = users["students"]
            for st in students:
                if st["email"] == self.get_email():
                    print("Grades")
                    for crs in st["marks"]:
                        print("Course: {}".format(crs["course_name"]))
                        print("Teacher: {}".format(crs["teacher"]))
                        print("Mark: {}".format(crs["mark"]))
                        print("-------")
                    break
        else:
            print("No student found for email - {}".format(self.get_email()))

    # returns mark of exact course
    def get_my_marks_for(self):
        """
        prints student's marks for provided course
        for this, student must be:
            enrolled to course(course name must be in enrolled_courses list,
                               on courses json file, student's email must be
                               in Course's students' list)
        """
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
            print("Grades")
            for crs in st["marks"]:
                if crs["course_name"] == course_name:
                    print("Course: {}".format(crs["course_name"]))
                    print("Teacher: {}".format(crs["teacher"]))
                    print("Mark: {}".format(crs["mark"]))
                    print("-------")
                    break

    def rate_student(self):
        """
        is invoked by teacher to rate student
        """
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

    def is_student_exist(self):
        """
           check if the user is exist in json file to avoid app crash
        """
        db = self.get_db().read_db()
        students = db["students"]
        for st in students:
            if st["email"] == self.get_email():
                return True
                break
        return False

    def get_my_courses(self):
        """
            returns the list of courses enrolled by student
        """
        if not self.is_student_exist():
            print("Student with email - {} does not exist".format(self.get_email()))
            return
        users = self.get_db().read_db()
        for st_i in range(len(users["students"])):
            if users["students"][st_i]["email"] == self.get_email():
                if len(users["students"][st_i]["enrolled_courses"]) > 0:
                    return users["students"][st_i]["enrolled_courses"]
                    break

    def print_my_courses(self):
        """
            used to print all enrolled courses by the student
        """
        courses = self.get_my_courses()
        if courses is None:
            print("You did not enrolled to any course")
            return

        print("My courses:\n|Course name|")
        for crs in courses:
            print(crs)

    def is_enrolled(self, course_name):
        """
            used by admin
            checks wheter student have this in his/her
            enrolled courses list
            also checks from courses side
        """
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

    def enroll_me_to_course(self):
        """
            used to enroll student to course by themselves
            invokes Course's enroll student method
        """
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

    def unenroll_me_from_course(self):
        """
            used to unenroll student from course by students
            invokes unenroll_student method
        """
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
    def rate_teacher_as_student():
        """
            used by student to rate teacher
            invokes Teacher's rate_teacher method
        """
        teacher_email = input("Please, provide the email of teacher to rate >")
        t = Teacher(teacher_email)
        t.rate_teacher()

    @staticmethod
    def print_teachers():
        """
            prints list of teachers by invoking through Teacher class
        """
        Teacher.print_all_teachers()


# --------------------------------------------------------------------- #

# ROLE - TEACHER. IT'S CLASS AND METHODS

class Teacher(UserBase):
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
            print("Leading Courses:\n{}".format(self._leading_courses))
        if len(self._rating) == 0:
            print("Still did not rated")
            return
        r_sum = 0
        for r in self._rating:
            r_sum = r_sum + r
        avg_rating = r_sum / len(self._rating)
        print("Average rating: {}".format(avg_rating))

    def is_teacher_exists(self):
        db_conn = self.get_db().read_db()
        teachers = db_conn["teachers"]
        for st in teachers:
            if st["email"] == self.get_email():
                return True
                break
        return False

    def rate_teacher(self):
        """
            used by student to rate teacher
        """
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist".format(self.get_email()))
            return
        rating = int(input("Please, rate teacher - {} from 1 to 10\n>".format(self.get_email())))
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
        """
            writes the records of Teacher to json file
        """
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
        """
            erases the records of Teacher from json file
        """
        email = input("Please, enter email of teacher to delete >")
        t = Teacher(email)
        if not t.is_teacher_exists():
            print("Teacher with email - {} is does not exists".format(email))
            return

        # before deletion of teacher, there should be saved the courses that before leaded by the teacher
        teachers_courses = []

        db_t = t.get_db().read_db()
        for t_i in range(len(db_t["teachers"])):
            if db_t["teachers"][t_i]["email"] == t.get_email():
                teachers_courses = db_t["teachers"][t_i]["leading_courses"]
                del db_t["teachers"][t_i]
                break
        t.get_db().write_db(db_t)

        # using the list of courses that leaded by deleted teacher, by default,
        # that courses' teacher's value would be reassigned to admins email
        # this will give opportunity for admin to update those courses after
        # some time

        for crs_name in teachers_courses:
            c = course.Course(crs_name)
            crs_to_upd = c.get_course()
            crs_to_upd.set_new_teacher("root@admin")
            crs_to_upd.extend_limited_places()
            crs_to_upd.update_course()

        print("Teacher with email - {} is deleted".format(email))
        return

    @staticmethod
    def get_all_teachers():
        """
            method returns the list of mapped objects of Teacher class
            with the records in json file
        """
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

    def get_students_of_course(self):
        """
            prints the list of students of specific course
        """
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist".format(self.get_email()))
            return
        # checking whether teacher has courses to lead
        if self.get_lead_courses() is None:
            print("You do not have any courses to lead")
            return
        # if yes, print
        self.print_my_courses()
        course_name = input("Please, type the course name >")
        c = course.Course(course_name)
        # 1 check whether teacher leads course
        if not c.is_teacher_leads(self.get_email()):
            print("You do not lead the course - {}".format(course_name))
            return
        students = c.get_course().get_list_of_students()
        if students is None:
            print("Course is not enrolled by any student")
            return
        print("{} students: ".format(course_name))
        for s in students:
            print(s)
        return course_name

    def get_lead_courses(self):
        """
            returns the courses name where the teacher is lead
        """
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        users = self.get_db().read_db()
        for t_i in range(len(users["teachers"])):
            if users["teachers"][t_i]["email"] == self.get_email():
                if len(users["teachers"][t_i]["leading_courses"]) > 0:
                    return users["teachers"][t_i]["leading_courses"]
        return None

    def print_my_courses(self):
        my_courses = self.get_lead_courses()
        if my_courses is None:
            print("You do not have any courses to lead")
            return
        print("Leading courses <")
        for crs in my_courses:
            print(crs)

    # does not implemented yet
    def mark_student(self):
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist".format(self.get_email()))
            return
        course_name = self.get_students_of_course()
        student_email = input("Please, type the email of student to mark >")
        s = Student(student_email)
        # 2 check whether student is enrolled to course
        if not s.is_enrolled(course_name):
            print("The student with email - {} does not enrolled to course - {}".format(student_email, course_name))
            return
        db_st = Student.get_db().read_db()
        for st_i in range(len(db_st["students"])):
            if db_st["students"][st_i]["email"] == student_email:
                for crs_m in range(len(db_st["students"][st_i]["marks"])):
                    if db_st["students"][st_i]["marks"][crs_m]["course_name"] == course_name:
                        print("Course: {}".format(db_st["students"][st_i]["marks"][crs_m]["course_name"]))
                        print("Teacher: {}".format(db_st["students"][st_i]["marks"][crs_m]["teacher"]))
                        print("Mark: {}".format(db_st["students"][st_i]["marks"][crs_m]["mark"]))
                        print("-------")

                        mark = input("Please, type mark for student - {} >".format(student_email))
                        db_st["students"][st_i]["marks"][crs_m]["mark"] = mark
                        break
        Student.get_db().write_db(db_st)
        print("Student with email - {} is marked for course - {}".format(student_email, course_name))

    def add_student_to_course(self):
        """
        invoked by teacher
        writes to 2 json files records of student's email
        """
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return

        # checking whether teacher has courses to lead
        if self.get_lead_courses() is None:
            print("You do not have any courses to lead")
            return
        # if yes, print
        self.print_my_courses()
        course_name = input("Please, type the course name >")
        c = course.Course(course_name)
        # 1 check whether teacher leads course
        if not c.is_teacher_leads(self.get_email()):
            print("You do not lead the course - {}".format(course_name))
            return

        print("Here is the list of all students")
        # provide the list of students to enroll them to course
        Student.print_all_students()
        student_email = input("Please, type student email to enroll him/her to course - {} >".format(course_name))
        s = Student(student_email)
        if not s.is_student_exist():
            print("Student with email - {} does not exists".format(student_email))
            return

        # if student does not enrolled to course, then enroll him/her
        if not s.is_enrolled(course_name):
            c.enroll_student(student_email)

            users = Student.get_db().read_db()
            for st_i in range(len(users["students"])):
                if users["students"][st_i]["email"] == student_email:
                    if course_name in users["students"][st_i]["enrolled_courses"]:
                        print("Student - {} enrolled to course {}".format(student_email, course_name))
                        return
                    users["students"][st_i]["enrolled_courses"].append(course_name)
                    break
            Student.get_db().write_db(users)
            print("Student - {} have joined to the course - {}".format(student_email, course_name))
        else:
            print("Student with email - {} is already enrolled to course".format(course_name))

    def delete_student_from_course(self):
        """
        deleting student from course, that invokes Student's method
        unenroll_me_from_course
        """
        # always ensure that the operating teacher is exists in db
        if not self.is_teacher_exists():
            print("Teacher with email - {} does not exist")
            return
        course_name = self.get_students_of_course()
        student_email = input("Please, type the email of student to delete from course >")
        s = Student(student_email)
        # 2 check whether student is enrolled to course
        if not s.is_enrolled(course_name):
            print("The student with email - {} does not enrolled to course - {}".format(student_email, course_name))
            return
        c = course.Course(course_name)
        # deleting from courses json file
        c.unenroll_student(s.get_email())

        # deleting student details about course from users json file
        db_st = Student.get_db().read_db()
        for st_i in range(len(db_st["students"])):
            if db_st["students"][st_i]["email"] == s.get_email():
                # removing course name from student's enrolled courses list
                db_st["students"][st_i]["enrolled_courses"].remove(course_name)
                # mechanism to erasing marks of unenrolled course from users db
                if len(db_st["students"][st_i]["marks"]) > 0:
                    for m_s in range(len(db_st["students"][st_i]["marks"])):
                        if db_st["students"][st_i]["marks"][m_s]["course_name"] == course_name:
                            db_st["students"][st_i]["marks"].remove(db_st["students"][st_i]["marks"][m_s])
                            break
        Student.get_db().write_db(db_st)
        print("Student with email - {} is deleted from course - {}".format(student_email, course_name))

    @staticmethod
    def rate_student_as_teacher():
        """used by teacher to rate student, which invokes Student's method"""
        student_email = input("Please, type the student email to rate >")
        s = Student(student_email)
        s.rate_student()


# Test methods to check
'''
COPY AND PASTE test code outside the comments block
Make testing classes, predvaritelno zakommentiv this portion of test code

t = Teacher("mmg@maga")
t.print_my_courses()
t.get_students_of_course()
# Teacher.add_teacher() # add teacher with email mmg@maga
# t = Teacher("mmg@maga")
# t.get_students_of_course()
# t.mark_student()
# t.add_student_to_course()
# t.delete_student_from_course()
# t.delete_teacher()
# t = Teacher("teach@com")
# t.rate_student_as_teacher()
Teacher.print_all_teachers()
'''
