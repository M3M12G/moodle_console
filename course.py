import db


class Course(object):
    _file = db.DB("db/courses.json")
    _course_name = None
    _teacher = None
    _total_place = None
    _students = []

    def __init__(self, course_name="unknown", teacher="unknown", total_place=0, students=[]):
        self._course_name = course_name
        self._teacher = teacher
        self._total_place = total_place
        self._students = students

    # representing method of Course class
    def course_info(self):
        """
            would be invoked by object of Course
            prints details of Course
        """
        print("Course name: {}".format(self._course_name))
        print("Lead teacher: {}".format(self._teacher))

        if len(self._students) == 0:
            print("Course does not enrolled by any student")
        else:
            print("Enrolled: {}/{}".format(len(self._students), self._total_place))

    def get_teacher(self):
        return self._teacher

    def set_new_teacher(self, teacher_email):
        self._teacher = teacher_email

    def extend_limited_places(self):
        self._total_place + 1

    def get_total_place(self):
        return self._total_place

    def get_students_list(self):
        return self._students

    # adding new course to json file
    @staticmethod
    def add():
        """
            writes to json file Course object structure
        """
        prev_courses = Course._file.read_db()
        course_name = input("Please, type course name >")
        # check course for uniqueness/ instantiating blank class with one attribute
        c = Course(course_name)
        if c.is_course_exists():
            print("{} is already exists".format(course_name))
            return

        prev_courses["courses"].append({
            "course_name": course_name,
            "teacher": input("Please, type teacher's email >"),
            "total_place": int(input("Please, type total enrolled number >")),
            "students": []
        })
        Course._file.write_db(prev_courses)
        print("New course - {} is added".format(course_name))
        return

    @staticmethod
    def delete():
        """
            deletes from json file provided course name with its sub-records
        """
        Course.print_all_crs()
        course_name = input("Please, type course name >")
        c = Course(course_name)
        if c.is_course_exists():
            db = Course._file.read_db()
            for crs_i in range(len(db["courses"])):
                if db["courses"][crs_i]["course_name"] == course_name:
                    del db["courses"][crs_i]
                    break
            Course._file.write_db(db)
            print("{} course is deleted".format(course_name))
        else:
            print("Failed. {} course does not exist".format(course_name))

    def is_course_exists(self):
        """
            checks whether invoking Course object is exists in json file
        """
        db = Course._file.read_db()
        courses = db["courses"]
        for crs in courses:
            if crs["course_name"] == self._course_name:
                return True
                break
        return False

    @staticmethod
    def get_courses():
        """returns all courses mapped to Course class"""
        courses = []
        courses_recs = Course._file.read_db()
        for course in courses_recs["courses"]:
            courses.append(Course(**course))
        return courses

    @staticmethod
    def print_all_crs():
        """
            prints all courses
        """
        all = Course.get_courses()
        print("All courses")
        for c in all:
            c.course_info()
            print("----------")

    @staticmethod
    def print_all_free_courses():
        """
            prints all courses, where the number of students does
            not exceed the number of limited places of course
        """
        all = Course.get_courses()
        print("All free courses")
        for c in all:
            if len(c._students) >= c._total_place:
                continue
            c.course_info()
            print("----------")

    def get_course(self):
        """
            returns records from json file mapped to
            Course class object
        """
        db = Course._file.read_db()
        courses = db["courses"]
        for crs in courses:
            if crs["course_name"] == self._course_name:
                return Course(**crs)
                break

    def get_list_of_students(self):
        """
            returns the list of students
        """
        return self._students

    def update_course(self):
        """
            just provide course_name and new teacher id/or if it is not needed just type
            prev teacher email and provide extension number of limited places into blank
            Course instance
        """
        # ensure that updating course is exists
        if self.is_course_exists():
            db = Course._file.read_db()
            for crs_i in range(len(db["courses"])):
                if db["courses"][crs_i]["course_name"] == self._course_name:

                    # ensuring that user does not provided less number of limited places
                    if db["courses"][crs_i]["total_place"] > self._total_place:
                        print("{} course's limited places number must be more than {}".format(
                            self._course_name,
                            db["courses"][crs_i]["total_place"]
                        ))
                        return

                    db["courses"][crs_i]["teacher"] = self._teacher
                    db["courses"][crs_i]["total_place"] = self._total_place
                    break
        self._file.write_db(db)
        print("The course - {} is updated".format(self._course_name))
        return self.get_course().course_info()

    def enroll_student(self, student_email):
        """
            would be invoked by Teacher/Admin/Student, where Course would
            record students email to students list of course
        """
        # check if course exists
        if not self.is_course_exists():
            print("The given course not found")
            return

        if self.is_student_enrolled(student_email):
            print("The course is not exists or/ and student {} is already enrolled".format(student_email))
            return
        else:
            db = self._file.read_db()
            for crs_i in range(len(db["courses"])):
                if db["courses"][crs_i]["course_name"] == self._course_name:
                    db["courses"][crs_i]["students"].append(student_email)
                    break
            self._file.write_db(db)
            print("The new student is enrolled to course: {}".format(self._course_name))

    # used by teachers or admins to detach student from course
    def unenroll_student(self, student_email):
        """
            would be invoked by Teacher/Admin/Student, where Course would
            delete email record of student from students list of course
        """
        # check if course exists
        if not self.is_course_exists():
            print("The given course not found")
            return

        if self.is_student_enrolled(student_email):
            db = self._file.read_db()
            for crs_i in range(len(db["courses"])):
                if db["courses"][crs_i]["course_name"] == self._course_name:
                    if student_email in db["courses"][crs_i]["students"]:
                        db["courses"][crs_i]["students"].remove(student_email)
                        break
            self._file.write_db(db)
            print("The student with email : {} is unenrolled from {} course".format(student_email, self._course_name))
        else:
            print("No matching student found by email : {}".format(student_email))

    def is_student_enrolled(self, student_email):
        """
            checks whether student is in students list of course
        """
        if not self.is_course_exists():
            print("Course with name - {} does not exist".format(self._course_name))
            return
        course = self.get_course()
        for s in course._students:
            if s == student_email:
                return True
                break
        return False

    def is_teacher_leads(self, teacher_email):
        """
            checks whether teacher leads course or not
        """
        if not self.is_course_exists():
            print("Course with name - {} does not exist".format(self._course_name))
            return
        course = self.get_course()
        if teacher_email == course._teacher:
            return True
        return False


# Testing code
# to test, just unwrap code from comments

# Course.add()

'''
crs = Course("Test")
c = crs.get_course()
c.set_new_teacher("admin")
c.extend_limited_places()
c.update_course()
'''

# c = Course("Python")
# print((c.is_teacher_leads("sh_a"))

# Course.print_all_free_courses()

# crs = Course("Python")

# Course.delete()

# Course.print_all_crs()

# c = Course("Python")
# c.enroll_student("st_ebwt")
# c.unenroll_student("st_ebwt")
