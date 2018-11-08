"""
@author: Xi Wei (Raymond) Yin
cwid: 10442986

assignment: Homework 9
date: Oct 28, 2018

url:
https://sit.instructure.com/courses/28343/assignments/118685
"""

import unittest
import HW09XiWei_Yin as h

# TODO: read below
'''Use your file reader generator from HW08 to read the students, instructors, and grades files into appropriate data 
structures or classes.
Generate warning messages for the user if the input file doesn't exist or doesn't meet the expected format
Handle error conditions gracefully if the file does not exist

Be sure to handle unexpected cases, e.g. a student from the students.txt file who has no grades yet (she might be a 
first semester student).  You can be sure that your testing group (Prof JR) will have some curious test cases to try
 against your solution.
'''


# TODO write the test cases

class TestRepository(unittest.TestCase):

    def test_repository_creation(self):
        new_repo = h.Repository('stevens')
        self.assertEqual(new_repo.name, "stevens")


class TestStudent(unittest.TestCase):
    def test_student_creation(self):
        """ This test function indirectly tested get_row() function. """
        # test creating default mysterious student
        new_stud = h.Student()
        self.assertEqual(new_stud.get_row(), ['0', 'anonymous', []])

        # test creating customized student
        cus_stud = h.Student("8888", "Raymond Yin", "software engineering")
        self.assertEqual(cus_stud.get_row(), ["8888", 'Raymond Yin', []])
        self.assertEqual(cus_stud.major, "software engineering")

    def test_add_course(self):
        # test creating default mysterious student
        new_stud = h.Student()
        self.assertEqual(new_stud.get_row(), ['0', 'anonymous', []])

        # test creating customized student
        cus_stud = h.Student("8888", "Raymond Yin", "software engineering")
        self.assertEqual(cus_stud.get_row(), ["8888", 'Raymond Yin', []])
        self.assertEqual(cus_stud.major, "software engineering")


class TestInstructor(unittest.TestCase):
    def test_instructor_creation(self):
        new_inst = h.Instructor()
        print(list(new_inst.get_all_rows()))
        self.assertEqual(list(new_inst.get_all_rows()), [])
        self.assertEqual(new_inst.name, 'anonymous')


class TestOtherNuances(unittest.TestCase):

    def test_parse_file_exception(self):

        with self.assertRaises(ValueError):
            # file contains content with invalid format
            list(h.parse_lines_from_file(
                "/Users/ramen/PycharmProjects/SSW810/homeworks/HW09_dir/test_files_mock/students.txt", 3, '\t'))

    def test_create_repo_through_files(self):
        dir_path = './test_files_happy_path_short'
        repo = h.Repository("stevens")
        h.process_data_files(repo, dir_path)

        self.assertEqual(repo.students['10103'].get_row(), ['10103', 'Baldwin, C', ['SSW 564', 'SSW 567']])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
