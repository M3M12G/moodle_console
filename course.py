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
        print("Course name: {}".format(self._course_name))
        print("Lead teacher: {}".format(self._teacher))

        if len(self._students) == 0:
            print("Course does not enrolled by any student")
        else:
            print("Enrolled: {}/{}".format(len(self._students), self._total_place))

    # adding new course to json file
    @staticmethod
    def add():
        prev_courses = Course._file.read_db()
        course_name = input("Please, type course name >")
        # check course for uniqueness/ instantiating blank class with one attribute
        c = Course(course_name)
        if c.is_course_exists():
            print("{} is already exists".format(course_name))
            return

        prev_courses["courses"].append({
            "course_name": course_name,
            "teacher": input("Please, type teacher's id >"),
            "total_place": int(input("Please, type total enrolled number >")),
            "students": []
        })
        Course._file.write_db(prev_courses)
        print("New course - {} is added".format(course_name))
        return

    # deleting course
    @staticmethod
    def delete():
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
        db = Course._file.read_db()
        courses = db["courses"]
        for crs in courses:
            if crs["course_name"] == self._course_name:
                return True
                break
        return False

    # returns all courses mapped to Course class
    @staticmethod
    def get_courses():
        courses = []
        courses_recs = Course._file.read_db()
        for course in courses_recs["courses"]:
            courses.append(Course(**course))
        return courses

    @staticmethod
    def print_all_crs():
        all = Course.get_courses()
        print("All courses")
        for c in all:
            c.course_info()
            print("----------")

    @staticmethod
    def print_all_free_courses():
        all = Course.get_courses()
        print("All free courses")
        for c in all:
            if len(c._students) >= c._total_place:
                continue
            c.course_info()
            print("----------")

    # returns single Course object
    def get_course(self):
        db = Course._file.read_db()
        courses = db["courses"]
        for crs in courses:
            if crs["course_name"] == self._course_name:
                return Course(**crs)
                break

    # just provide course_name and new teacher id/or if it is not needed just type prev teacher id
    # and provide extension number of limited places into blank Course instance
    def update_course(self):
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

    # used by teachers or admins to attach student to course
    def enroll_student(self, student_email):
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
                        print(db["courses"][crs_i]["students"])
                        break
            self._file.write_db(db)
            print("The student with email : {} is unenrolled from {} course".format(student_email, self._course_name))
        else:
            print("No matching student found by email : {}".format(student_email))

    def is_student_enrolled(self, student_email):
        if not self.is_course_exists():
            print("Course with name - {} does not exist".format(self._course_name))
            return
        course = self.get_course()
        for s in course._students:
            if s == student_email:
                return True
                break
        return False


# c = Course("Test", "prev_teacher",20)
# c.update_course()

# Course.add()

#c = Course("Thwt")
# all = Course.get_courses()

# Course.print_all_free_courses()

# crs = Course("Python")
# print(crs.get_course().course_info())

# Course.delete()

# Course.print_all_crs()

# c = Course("Python")
#c.enroll_student("st_ebwt")
# c.unenroll_student("st_ebwt")
