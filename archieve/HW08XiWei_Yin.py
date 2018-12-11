"""
@author: Xi Wei (Raymond) Yin
CWID: 10442986

assignment: Homework 8
date: Oct 24, 2018

url:
https://sit.instructure.com/courses/28343/assignments/118684
"""

import datetime as d
import unittest
import os
import pathlib as p
import re
from prettytable import PrettyTable


# Part 1
def calculate_date(date_str, num_of_days):
    """Part 1.1 and 1.2"""
    return d.datetime.strptime(date_str, "%b %d, %Y") + d.timedelta(days=num_of_days)


def calculate_date_delta(date1, date2):
    """Part 1.3"""
    return abs(d.datetime.strptime(date1, "%b %d, %Y") - d.datetime.strptime(date2, "%b %d, %Y"))


# Part 2
def parse_lines_from_file(file_name, num_of_field, separator=',', has_header=False):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        raise FileNotFoundError
    else:
        with file as f:
            line_number = 0
            if has_header:
                line_number += 1
                f.readline()
            for line in f:
                if line != "\n":
                    fields = tuple(field.strip() for field in line.split(separator))
                line_number += 1
                if len(fields) != num_of_field:
                    raise ValueError("ValueError: " + file_name + " has " + str(len(fields)) + " fields on line " +
                                     str(line_number) + " but expected " + str(num_of_field))
                yield fields


class TestPart2(unittest.TestCase):
    def test_parse_lines_from_file(self):
        with self.assertRaises(FileNotFoundError):
            next(parse_lines_from_file("hahaha!!", 1))

        with self.assertRaises(ValueError):
            next(parse_lines_from_file("part2test.txt", 1, "|"))

        # test skipping header
        self.assertEqual(next(parse_lines_from_file("part2test2.txt", 3, has_header=True)),
                         ('data', 'something', 'something else'))

        # test for loop iteration over generator call
        actual = []
        expected = [['data', 'something', 'something else'], ['apple', 'peach', 'banana']]
        for a, b, c in parse_lines_from_file("part2test2.txt", 3, has_header=True):
            actual.append([a, b, c])

        self.assertEqual(actual, expected)


# Part 3
def parse_files(dir_path):
    # handle directory string IO
    try:
        if not os.path.isdir(dir_path):
            raise FileNotFoundError("No such directory")
        os.chdir(dir_path)
    except FileNotFoundError as e:
        print(str(e) + " as '" + dir_path + "'")
    else:
        # gather all python files within current give path recursively
        curr_dir = os.getcwd()

        for file_path in p.Path(curr_dir).rglob("*.py"):
            try:
                file_path_str = str(file_path)
                file = open(file_path_str, 'r')
            except FileNotFoundError as e:
                print(e.strerror + " as '" + file_path_str + "'")
            else:
                with file as f:
                    class_num, func_num, line_num, char_num = 0, 0, 0, 0
                    lines = f.read().split("\n")
                    class_num = len([line for line in lines if line.find("class", 0) == 0])

                    pattern = re.compile(r"^\s+def\s.+\([a-zA-Z0-9_]*\):")
                    func_num = len([line for line in lines if line.find("def", 0) == 0 or re.match(pattern, line)])
                    line_num = len(lines)
                    char_num = len(''.join(lines)) + line_num - 1
                    yield file_path_str, class_num, func_num, line_num, char_num


if __name__ == "__main__":
    # print("1.1 What is the date three days after Feb 27, 2000?")
    # print(calculate_date("Feb 27, 2000", 3))
    # print("1.2 What is the date three days after Feb 27, 2017?")
    # print(calculate_date("Feb 27, 2017", 3))
    #
    # print("1.3 How many days passed between Jan 1, 2017 and Oct 31, 2017?")
    # print(calculate_date_delta("Jan 1, 2017", "Oct 31, 2017"))
    #
    # unittest.main(exit=False, verbosity=2)

    # f = FileScanner()
    # f.gather_files("./test_dir")
    # FileScanner().gather_files("./test_dir")
    # FileScanner().gather_files("./thaha")
    # print(list(parse_files("./test_dir")))

    tb = PrettyTable()
    tb.field_names = ["File Name", "Classes", "Functions", "Lines", "Characters"]
    for file_path_str, class_num, func_num, line_num, char_num in parse_files("./test_dir"):
        tb.add_row([file_path_str, class_num, func_num, line_num, char_num])
    print(tb.get_string())
