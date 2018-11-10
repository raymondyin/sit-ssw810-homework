"""
@author: Xi Wei (Raymond) Yin
cwid: 10442986

assignment: Homework 9
date: Oct 28, 2018

url:
https://sit.instructure.com/courses/28343/assignments/118685
"""

import os
import pathlib as p

from collections import defaultdict
from prettytable import PrettyTable
from HW08_dir.HW08XiWei_Yin import parse_lines_from_file


class Repository:
    def __init__(self, school_name):
        """create a new repository for an educational institution"""
        self.name = school_name
        self.instructors = defaultdict(Instructor)  # key: instructor's cwid | value: Instructor
        self.students = defaultdict(Student)  # key: student's cwid | value: Student
        self.grades = defaultdict(list)  # key: student's cwid and/or instructor's cwid | value: [Grade, ..]
        self.majors = defaultdict(Major)  # key: str of dept | value: Major

    def add_instructor(self, cwid, name, dept):
        self.instructors[cwid] = Instructor(cwid, name, dept)

    def add_student(self, cwid, name, major):
        self.students[cwid] = Student(cwid, name, major)

    def add_grade(self, stud_cwid, course, letter_grade, inst_cwid):
        self.grades[stud_cwid].append(Grade(stud_cwid, course, letter_grade, inst_cwid))
        self.grades[inst_cwid].append(Grade(stud_cwid, course, letter_grade, inst_cwid))

    def add_major(self, dept, flag, course):
        self.majors[dept].dept = dept
        if flag == 'R':
            self.majors[dept].required.add(course)
        elif flag == 'E':
            self.majors[dept].electives.add(course)

    def join_data(self):
        for cwid in self.students:
            for grade in self.grades[cwid]:
                if grade.is_complete():
                    self.students[cwid].add_course(grade.course, grade.letter_grade)

        for cwid in self.instructors:
            for grade in self.grades[cwid]:
                if grade.is_teaching(cwid):
                    self.instructors[cwid].add_course(grade.course, grade.stud_cwid)

        for student in self.students.values():
            student.required_remain = self.majors[student.major].required - set(student.completed_courses.keys())
            student.electives_remain = self.majors[student.major].electives - set(student.completed_courses.keys())

    def get_table(self, data_type):
        if data_type == "student":
            return self._get_student_table()
        elif data_type == "instructor":
            return self._get_instructor_table()
        elif data_type == "major":
            return self._get_major_table()
        else:
            return "No such type of table."

    def _get_student_table(self):
        table = PrettyTable(field_names=Student.labels)
        for student in self.students.values():
            table.add_row(student.get_row())
        return table.get_string()

    def _get_instructor_table(self):
        table = PrettyTable(field_names=Instructor.labels)
        # TODO: the table needs to be displayed in sequence of a sorted list by instructor's name (can't figure out
        # how to use sorted() in this case, since the value is Instructor and to refer to its "name" attribute, I need
        # to refer to is as self.instructors[CWID].name which I don't know how to express in "sorted(iterable, key=...)"
        # sorted_list = sorted(self.instructors.items(), key=)
        for instructor in self.instructors.values():
            for row in instructor.get_all_rows():
                table.add_row(row)

        return table.get_string()

    def _get_major_table(self):
        table = PrettyTable(field_names=Major.labels)
        for major in self.majors.values():
            table.add_row((major.dept, major.required, major.electives))

        return table.get_string()


class Student:
    """class Student to hold all of the details of a student, including a defaultdict(str) to store the classes taken
    and the grade where the course is the key and the grade is the value."""

    labels = ["cwid", "Name", "Completed Courses", "Remaining Required", "Remaining Electives"]

    def __init__(self, cwid='0', name="anonymous", major="unknown"):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.completed_courses = defaultdict(str)  # key: course code | value: completed course letter grade
        self.required_remain = set()
        self.electives_remain = set()

    def get_row(self):
        return [self.cwid, self.name, sorted(self.completed_courses.keys()), self.required_remain, self.electives_remain]

    def add_course(self, course, letter_grade):
        self.completed_courses[course] = letter_grade


class Instructor:
    labels = ["cwid", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid='0', name="anonymous", dept="unknown"):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(set)  # key: course name | value: student number

    def get_all_rows(self):
        """ Note: this class function is a generator."""
        for course in self.courses:
            yield self.cwid, self.name, self.dept, course, len(self.courses[course])

    def add_course(self, course, stud_cwid):
        self.courses[course].add(stud_cwid)


class Grade:
    def __init__(self, stud_cwid, course, letter_grade, inst_cwid):
        self.stud_cwid = stud_cwid
        self.course = course
        self.letter_grade = letter_grade
        self.inst_cwid = inst_cwid

    def is_complete(self):
        return self.letter_grade != 'F'

    def is_teaching(self, inst_cwid):
        return self.inst_cwid == inst_cwid


class Major:
    labels = ["Dept", "Required", "Electives"]

    def __init__(self):
        self.dept = ''
        self.required = set()
        self.electives = set()

def handle_string_input_and_set_path(string_input=''):
    """ (the following code is from homework 8 with modification) Prompt to get user's directory string input to set
    current path; exceptions are handled. Input string 'default' will change the working directory to current directory
    of the running Python script. """

    while True:
        try:
            # handle string nuances
            if string_input == '':
                string_input = input("Please enter a directory path or keyword 'default': ")
            path = "./test_files_happy_path" if string_input == 'default' else string_input

            if not os.path.isdir(path):
                raise FileNotFoundError("No such directory")

            os.chdir(path)  # set current directory as working director
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as e:
            print(str(e))
            break
        # except Exception:
        #     print("Something else went wrong, please try again.")
        else:
            return os.getcwd()


def process_data_files(repo, path):
    """ Populate data of students, instructors and grades from text data files within current give path, recursively."""

    # retrieve all file path beforehand
    student_file_path = ''
    instructor_file_path = ''
    grade_file_path = ''
    major_file_path = ''

    for file_path in p.Path(path).rglob("*.txt"):
        path_str = str(file_path)
        # print(path_str.find("students.txt"))
        if path_str.find("students.txt") != -1:
            student_file_path = path_str
        if path_str.find("instructors.txt") != -1:
            instructor_file_path = path_str
        if path_str.find("grades.txt") != -1:
            grade_file_path = path_str
        if path_str.find("majors.txt") != -1:
            major_file_path = path_str

    try:
        for stud_cwid, name, major in parse_lines_from_file(student_file_path, 3, '\t'):
            repo.add_student(stud_cwid, name, major)

        for inst_cwid, name, dept in parse_lines_from_file(instructor_file_path, 3, '\t'):
            repo.add_instructor(inst_cwid, name, dept)

        for stud_cwid, course, grade, inst_cwid in parse_lines_from_file(grade_file_path, 4, '\t'):
            repo.add_grade(stud_cwid, course, grade, inst_cwid)

        for dept, flag, course in parse_lines_from_file(major_file_path, 3, '\t'):
            repo.add_major(dept, flag, course)

    # I understand that I can omit this try/except block if I want to have the program terminated by the ValueError
    # raised from "parse_lines_from_file()" function. I just have this structure for future refactoring in case the
    # requirement is changed to something like "handling invalid date without interrupting the program".
    except ValueError as e:
        print(e)
        raise ValueError
    except FileNotFoundError as e:
        print(e)
        raise FileNotFoundError

    repo.join_data()


def create_a_univ(name, path):
    # program setup
    curr_dir_path = handle_string_input_and_set_path(path)  # the parameter can be customized
    repo = Repository(name)
    process_data_files(repo, curr_dir_path)
    return repo


def display_univ_data(repo):
    # getting results
    print("Student Summary")
    print(repo.get_table("student"))
    print("Instructor Summary")
    print(repo.get_table("instructor"))


def main():
    """ Main program logic for this assignment."""

    # TODO: implement and test an interactive sequence of prompt so the testers can keep adding multiple universities.
    # (Please forget it for now, as I really don't have time to test and finish this part. I also don't think it is the
    # main point of this assignment.)

    # # Since 'Your solution should definitely allow me to represent multiple universities easily without replicating
    # # code in the main() routine.' Here you go (it's like creating command line UI):
    # univ_dict = {}
    #
    # while True:
    #     try:
    #         print("I've heard you don't want to replicate code in main() routine yet you want to represent multiple",
    #               "universities? :)")
    #         univ_name = input("Then please enter the name of a university that you want to create:")
    #         univ_path = input("Ok now please enter the path of the folder that contains the data files:")
    #     except ValueError as e:
    #         print("Ops, something went wrong:", e, "Please try again.")
    #         continue
    #     else:
    #         if univ_dict.get(univ_name) is not None:
    #             print("There's already a university with the same name, please try something else.")
    #             continue
    #         else:
    #             univ_dict[univ_name] = create_a_univ(univ_name, univ_path)  # create a new university
    #             option = ''
    #             while True:
    #                 option = input("Are you done? (enter 'y' to move on/ 'n' to add another university:")
    #                 if option == 'y' or 'n':
    #                     break
    #                 else:
    #                     continue
    #             if option == 'y':
    #                 break
    #             elif option == 'n':
    #                 continue
    #
    # while True:
    #     print("Phew... okay now which university's data do you want to check?")
    #     univ_name = input("Please enter a legit name: (i'm so tired of checking all the non-happy path cases I
    #     + " swear to god! Q_Q")
    #     if univ_dict.get(univ_name) is None:
    #         print("There's no such university. Please try again.\n")
    #         continue
    #     else:
    #         display_univ_data(univ_dict[univ_name])
    #         option = ''
    #         while True:
    #             option = input("Are you done? (enter 'y' to move on/ 'n' to add another university:")
    #             if option == 'y' or 'n':
    #                 break
    #             else:
    #                 continue
    #         if option == 'y':
    #             print("OMG thank you!")
    #             break
    #         elif option == 'n':
    #             print("wut?! alright you asked for it")
    #             continue

    # the following is for a smoke test
    # program setup
    curr_dir_path = handle_string_input_and_set_path("default")  # the parameter can be customized
    stevens_repo = Repository("Stevens Institute of Technology")
    process_data_files(stevens_repo, curr_dir_path)
    # getting results
    print("Major Summary")
    print(stevens_repo.get_table("major"))
    print("Student Summary")
    print(stevens_repo.get_table("student"))
    print("Instructor Summary")
    print(stevens_repo.get_table("instructor"))


if __name__ == '__main__':
    main()
