#! /opt/local/bin/python

import pandas as pd
import numpy as np
import math
import os.path
import time
import sys
import re
import os

# check_report is the function that can be fed a filename and prereqdict
# to print out prereq test results.


# Course prerequisites are defined in one of three ways that handles all cases
# All course names must be in parentheses (sorry!) ans with no spaces
# Requirements are added per examples below as
# Course definitions are inside parentheses
# Definitions of requirements are made by adding a line of the form
# Course name: (definitions),
# The comma is necessary, as are the parentheses
#
# Definitions:
# A single course definition required is simply listed, for example
#       "ME2700"
# A list of multiple required courses is in square brackets, for example
#       ["ME1020", "ME2120"]
# Multiple methods of satisfying the requirement are created by multiple
# lists, each in square brackets.
# For instance, consider a situation where both ME1010 and ME 2120 are
# required for ME 2700. This is listed as
#       "ME2700":(["CHM1210","PHY2400"]),
# On the other hand, if either is sufficient, then they are listed instead as
#       "ME2700":(["CHM1210"],["PHY2400"]),
# Here the code will go through each list to see if is is satisfied.
# In the scenario where prerequisites can be satisfied by a single course or
# Two other courses, they must be definined as two separate lists, even though
# one of the lists is a list of length 1.
# Let's consider a complicated example, ME2120. In that case, the prerequisites
# are (EGR1010 or MTH2310) and ME1040 and PHY2400
# This construc really means that there are two possible solutions,
# EGR1010, ME1040 and PHY2400 or MTH2310, ME1040 and PHY2400
# This is written as:
#       "ME2120":(["EGR1010", "ME1040", "PHY2400"],["MTH2310", "ME1040", "PHY2400"]),

print('capstone design')
print(
    'ME 1040 and ME 3600 and MTH 2320 and PHY 2410 and PHY 2410L and ((ME 3210 and ME 3310 and ME 3360 and ME 4140) or (ME 3760 and ME 4620 (ME 4620 (with concurrency) and ME 4720))')

prereqdict = {"ME1020": ("EGR1010"),
              "ME2120": (["EGR1010", "ME1040", "PHY2400"], ["MTH2310", "ME1040", "PHY2400"]),
              "ME2210": (["ME1020", "ME2120"]),  # Verified Aug-15-2016
              # This is a pre or co requisite. How to code? I think this works now.
              "ME2600": ("ME2700c"),  # Recitation is a co-requisite
              "ME2700": (["CHM1210", "PHY2400"]),
              "ME3120": ("ME1020", "ME2120"),  # Verified Aug-15-2016
              "ME3210": (["EE2010", "ME2210", "ME3120", "ME3350", "MTH2350"]),  # Verified Aug-16-2016
              "ME3310": (["EGR1010", "MTH2310", "ME2120"]),
              "ME3320": (["ME1020", "ME3310"]),  # Verified Aug-16-2016
              "ME3350": (["ME2210", "ME3310"]),  # Verified Aug-16-2016
              "ME3360": (["ME1020", "ME3350", "MTH2350"]),  # Verified Aug-15-2016
              "ME3600": (["EE2010", "EGR3350", "ME2120", "MTH2350"]),
              "ME3750": ("ME2700"),  # Verified Aug-15-2016
              "ME3760": ("ME3750"),  # Verified Aug-15-2016
              "ME4010": (["ME3360", "ME3210"]),  # Verified Aug-15-2016
              "ME4080": (["MTH2350", "ME3210"], ["MTH2530", "ME3210"]),  # Verified Aug-16-2016
              "ME4120": (["MTH2320", "MTH2350", "ME3120"], ["MTH2320", "MTH2330", "MTH2530", "ME3120"]),
              "ME4140": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4150": ("ME4140"),  # Verified Aug-16-2016
              "ME4160": (["ME2020", "ME2210", "ME3120"], ["ME1040", "ME2210", "ME3120"]),
              "ME4180": ("ME2700"),  # Verified Aug-16-2016
              "ME4190": (["MTH2350", "MTH2320", "ME3350"], ["MTH2330", "MTH2530", "MTH2320", "ME3350"]),
              "ME4210": ("ME3210"),  # Verified Aug-16-2016
              "ME4220": ("ME3210"),
              "ME4240": ("ME2210"),  # Verified Aug-16-2016
              "ME4250": ("ME2210"),  # Verified Aug-16-2016
              "ME4260": (["MTH2350"], ["MTH2530"]),
              "ME4330": ("ME3350"),  # Verified Aug-16-2016
              "ME4340": ("ME3360"),  # Verified Aug-16-2016
              "ME4350": ("ME3350"),  # Verified Aug-16-2016
              "ME4360": (["ME3320", "ME3350", "MTH2350"], ["ME3320", "ME3350", "MTH2330"]),
              "ME4430": ("ME3350"),  # Verified Aug-16-2016
              "ME4440": ("ME3350"),  # Verified Aug-16-2016
              "ME4490": ("ME3120"),  # Verified Aug-16-2016
              "ME4520": ("ME3350"),  # Verified Aug-16-2016
              "ME4530": ("ME3310"),  # Verified Aug-16-2016
              "ME4540": ("ME3360"),  # Verified Aug-16-2016
              "ME4550": ("ME3360"),  # Verified Aug-16-2016
              "ME4560": ("ME3350"),  # Verified Aug-16-2016
              "ME4570": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4580": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4590": ("ME3360"),  # Verified Aug-16-2016
              "ME4610": (["ME3360", "3600"]),  # Verified Aug-16-2016
              "ME4620": (["ME2700", "ME3120", "ME3600"]),
              "ME4680": (["CHM1210", "PHY2410"], ["CHM1210", "PHY1120"]),
              "ME4700": (["ME2700", "MTH2320", "MTH2350"]),
              "ME4720": ("ME2700"),  # Verified Aug-16-2016
              "ME4730": ("ME2700"),  # Verified Aug-16-2016
              "ME4740": (["ME2700", "ME3120", "ME4620"]),
              "ME4750": (["ME2600", "ME2700"]),  # Verified Aug-16-2016
              "ME4770": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4820": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4830": ("ME2700"),  # Verified Aug-16-2016
              "ME4840": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4850": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4860": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4870": (["ME2210"], ["BME3212"], ["ISE3212"]),
              "ME4880": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4910": (
              ["ME2020", "EGR3350", "MTH2320", "MTH2350", "PHY2410", "EE2010", "ME2210", "ME2700", "ME3120", "ME3310",
               "ME4620c"]),
              "ME7060": (["ME6120", "ME7100"]),
              "ME7080": (["ME6120", "ME7100"]),
              "ME7120": ("ME6120"),
              "ME7140": (["ME6120", "ME7100"]),
              "ME7160": (["ME6120", "ME7100"]),
              "ME7200": ("ME5120"),
              "ME7210": ("ME6210"),
              "ME7250": ("ME5210"),
              "ME7300": ("ME5350"),
              "ME7330": ("ME5360"),
              "ME7340": ("ME6010"),
              "ME7350": ("ME5360"),
              "ME7390": ("ME7500"),
              "ME7400": ("ME6330"),
              "ME7500": (["ME5320", "ME5750"]),
              "ME7520": (["ME5310", "ME5750"]),
              "ME7550": ("ME7500"),
              "ME7690": ("ME6210"),
              "ME7720": (["ME6720", "ME5750"]),
              "ME7730": ("ME6700"),
              "ME7740": (),
              "ME7750": ("ME6700"),
              "ME7760": ("ME5760"),
              "ME7780": ("ME6730")}

majordict = {"ME4910": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME2700": ['Engineering - IECS', 'Materials Sci + Egr - BSMSE', 'Materials Sci + Egr - IECS',
                        'Materials Sci + Egr - Pre',
                        'Mathematics - BS', 'Mech Engineering - BSME', 'Mech Engineering - IECS',
                        'Mech Engineering - Pre'],
             "ME3120": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3210": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3310": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3320": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3350": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3360": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3600": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3610": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3750": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3760": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3150": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4010": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4080": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4120": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4140": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4150": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4160": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4180": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4190": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4210": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4220": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4240": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4250": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4260": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4330": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4340": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4350": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4360": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4430": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4440": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4490": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4520": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4530": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4540": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4550": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4560": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4570": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4580": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4590": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4610": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4620": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4680": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4700": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4720": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4730": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4740": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4750": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4860": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME3870": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"],
             "ME4880": ["Mech Engineering - BSME", "Materials Sci + Egr - BSMSE"]}

text_output = False



# Hard coded toggling ot text output.
def tprint(string, output = False):
    #print(output)
    if output:
        print(string)

# This co-or-prequisite is hard-coded in passed_class
co_or_preqdict = {"ME2600": ("ME2700")}

def isC(grade):
    answer = grade == 'A' or grade == 'B' or grade == 'C'
    return answer

def isD(grade):
    answer = grade == 'A' or grade == 'B' or grade == 'C' or grade == 'D'
    return answer

def ispass(grade):
    answer = grade == 'A' or grade == 'B' or grade == 'C' or grade == 'D'
    return answer

def isbetterthan(grade_needed, grade_received):
    if grade_needed == 'C':
        answer = isC(grade_received)
    elif grade_needed == 'D':
        answer = isD(grade_received)
    else:
        print("Warning: Grade needed isn't a real grade: {}.".format(grade_needed))
        answer = 3
    return answer

# Check if single course was passed

def passed_class(class_name, classes_taken, course_name):
    '''
    class_name is a string of the course a student must pass to
    complete the prerequisites. If the grade received is not sufficient, this
    function must return a False
    course_name is the course the student is registered for. We are checking
    prerequisites for course_name
    '''

    co_or_preqdict = {"ME2600": ("ME2700")}
    fail_text = ''
    answer = False
    if class_name in classes_taken:
        if class_name is "ME2120" or class_name is "ME3310" or class_name is "ME2700":
            answer = isC(classes_taken[class_name])
        # I hate this hard coding of co-requisite exception. I believe it is
        # now fixed, but this is left in just in case.
        elif course_name is "ME2600" and class_name is "ME2700":
            answer = True
        else:
            answer = isD(classes_taken[class_name])
        # will fall to this if no grade assigned, intercept corequisite
        # exception
        if answer is False:
            if classes_taken[class_name] is 'No grade.':
                # print('Registered but has not completed {}.'.format(class_name))
                fail_text = 'Registered but has not completed {}.\n'.format(
                    class_name)
            else:
                # print('Failed {} with grade of {}'.format(class_name, classes_taken[class_name] ))
                fail_text = 'Failed {} with grade of {}\n.'.format(
                    class_name, classes_taken[class_name])
    elif (class_name[:class_name.find('c')] in classes_taken
          and classes_taken[class_name[:class_name.find('c')]] == '>') or (class_name[:class_name.find('c')]
                                                                           in classes_taken and passed_class(
        class_name[:class_name.find('c')], classes_taken, course_name)[0]):  # corequisite taken earlier and passed?
        answer = True
    else:
        # print('Has not taken {}.'.format(class_name ))
        fail_text = 'Has not taken {}\n.'.format(class_name)
    return answer, fail_text


# Check array of classes to return if all have been passed (sufficiently)


def pass_all(classes, classes_taken, course_name):
    '''
    classes is an array of all classes a student must pass to
    complete the prerequisites. If the grade received is not sufficient in any
    course, this function must return a False
    '''

    answer = True
    for class_name in classes:
        answer, fail_text = passed_class(
            class_name, classes_taken, course_name)
        if not answer:
            answer = False
            # print('Failed {} with grade of {}'.format(class_name, classes_taken[class_name] ))
            break
    return answer


# Check tuple of potential methods to satisfy class to see if any of them work.


def satisfied_requirements(requirements, classes_taken, course_name):
    if type(requirements) is str:
        satisfied = passed_class(requirements, classes_taken, course_name)[0]
    elif type(requirements) is list:
        satisfied = pass_all(requirements, classes_taken, course_name)
    elif type(requirements) is tuple:
        satisfied = False
        for requirement in requirements:
            satisfied = satisfied_requirements(
                requirement, classes_taken, course_name)
            if satisfied is True:
                break
    return satisfied


# Check if students in class meet prerequisites, report on failures


def check_class(course_name, student_list, data, prereqs, no_transfer_data):
    print('=======================================================')
    print('=======================================================')
    print('Start report for:')
    print('Course number {}'.format(course_name))
    print('Section number {}'.format(data["CourseSectionNumber"].iloc[1][:-1]))
    print('Prerequisites are')
    print(prereqs)
    print('=======================================================\n\n')

    email_list = ''
    for student in student_list:
        # print('-------------------------------------------')
        # print('Begin {}'.format(student))
        satisfied = satisfied_requirements(
            prereqs, data["Pre_req_dic"].loc[student], course_name)
        if satisfied is False:
            data.loc[student, "Pre_req_status"] = "Missing prereqs"
            tprint('Begin {}'.format(student))
            if student in no_transfer_data:
                tprint(
                    'No transfer data for {}. ************************'.format(student))

            tprint(student)
            tprint('Section number {}'.format(
                data["CourseSectionNumber"].loc[student][:-1]))

            # print(student)
            tprint('Name: {}'.format(data.loc[student, ["Name"]].values[0]))
            tprint('Email: {}'.format(data.loc[student, ["Email"]].values[0]))
            phone_number = str(data.loc[student, ["PhoneNumber"]].values[0])
            phone_number = '(' + phone_number[:3] + ')' + \
                           phone_number[3:6] + '-' + phone_number[6:]
            tprint('Phone number: {}'.format(phone_number))
            tprint('Program description: {}'.format(
                data.loc[student, ["ProgramDescription"]].values[0]))
            # is "nan":
            if isinstance(data.loc[student, ["PRIMARY_ADVISOR_NAME_LFMI"]].values[0], float):
                tprint('Advisor name: {}\n'.format("No Advisor On Record"))
            else:
                tprint('Advisor name: {}\n'.format(
                    data.loc[student, ["PRIMARY_ADVISOR_NAME_LFMI"]].values[0]))
            tprint(data.loc[student].iloc[6:-1])
            tprint('Has:\n{}'.format(
                data.loc[student, ["Pre_req_dic"]].values[0]))
            # data.loc[student,'Has'] = data.loc[student,["Pre_req_dic"]].values[0]
            tprint('Needs any of the following combinations:')
            allprereqs = ''
            if type(prereqs) is tuple:
                tprint('growing list of prerequisites')
                for idx, set in enumerate(prereqs):
                    allprereqs = allprereqs + set + ', '
                    tprint('idx %', idx)
                    tprint('set %', set)
                    prereqs[idx] = 'and '.join([str(x) for x in prereqs[idx]])
                    tprint(set)
                allprereqs = allprereqs[:-2]
                allprereqs = ', or'.join([str(x) for x in prereqs])
            else:
                tprint(prereqs)
                allprereqs = prereqs
                allprereqs = ', '.join([str(x) for x in allprereqs])
            tprint(allprereqs)
            # Put needs in excel spreadsheet
            # data.loc[student,'Needs'] = allprereqs

            email_list = email_list + ';' + \
                         data.loc[student, ["Email"]].values[0]
            tprint('=====================================================\n\n')
    # print(email_list[1:])
    return data


def read_prereq_report(filename):
    data = pd.read_excel(filename, header=11, index_col=3, skip_footer=1,
                         sheetname="Page1_1", converters={'PhoneNumber': str})
    Course_Name = data["CourseGrade"].iloc[1]
    Course_Name = data["CourseGrade"].iloc[1][:Course_Name.find('-')]

    num_prereqs = 0
    keep_cols = ['Name', 'Email', 'PhoneNumber', 'ProgramDescription',
                 'PRIMARY_ADVISOR_NAME_LFMI', 'CourseSectionNumber']
    base_cols = len(keep_cols)
    for i, c_name in enumerate(data.columns):
        if c_name.find("Requisite") > 0:
            keep_cols.append(c_name)
            num_prereqs = num_prereqs + 1
    num_prereqs = num_prereqs / 2
    data = data[keep_cols]
    lkk = len(keep_cols)
    student_list = data.index

    while not hasattr(student_list[-1], 'encode'):
        student_list = student_list[:-1]
    data = data.loc[student_list, :]
    all_preqs = []
    for student in student_list:
        pre_reqs_taken = {}
        for i in range(base_cols, base_cols + 2 * int(num_prereqs), 2):
            if hasattr(data.loc[student].iloc[i], 'encode'):
                pre_req_class = data.loc[student].iloc[i][
                                0:(data.loc[student].iloc[i].find('-->'))]
                grade_str = data.loc[student].iloc[i + 1]
                if data.loc[student].iloc[i + 1].find(';') == -1:
                    grade = grade_str[-1]
                else:
                    grade = grade_str[
                        data.loc[student].iloc[i + 1].find(';') - 1]
                if grade is '>':
                    grade = "No grade."
                pre_reqs_taken[pre_req_class] = grade
                grade = ''
        all_preqs.append(pre_reqs_taken)
    data['Pre_req_dic'] = all_preqs

    return data, student_list, Course_Name


# Append transfered data to student record
def append_transfer(data, student_list):
    filename = "/Users/jslater/Documents/OneDriveBusiness/OneDrive - Wright State University/Chair-OneDrive/PrereqData/Student_prerequisite_data.xlsx"
    while True:
        try:
            transfer_data = pd.read_excel(filename, index_col=0, skip_footer=1)
            break
        except IOError:
            tprint("Oops!  Cannot find {}".format(filename))
            filename = input("Try using the full path: ")
    tprint('\n\n*****************************************************************************')
    tprint("Transfer prerequisite file last modified: %s" %
          time.ctime(os.path.getmtime(filename)))
    tprint('*****************************************************************************\n\n')

    transfer_data = pd.read_excel(filename, index_col=0, skip_footer=1)
    all_preqs = []
    pre_reqs_taken = {}
    no_transfer_data = []
    for student in student_list:
        pre_reqs_taken = data['Pre_req_dic'].loc[student]
        completed_courses = []
        if student in transfer_data.keys():
            completed_courses = transfer_data[student].loc[
                transfer_data[student] == "Satisfied"].keys()
        else:
            no_transfer_data.append(student)

        grades = ["C"] * len(completed_courses)
        trans_classes = dict(zip(completed_courses, grades))

        if type(pre_reqs_taken) is dict and type(trans_classes) is dict:

            pre_reqs_taken.update(trans_classes)
        elif type(trans_classes) is dict:
            pre_reqs_taken = trans_classes

        all_preqs.append(pre_reqs_taken)
    data['Pre_req_dic'] = all_preqs

    return data, no_transfer_data


def check_majors(major_requirement, data, student_list):
    print('\n\nMajor Checking\n-----------------------------------------\n\n')
    for student in student_list:
        # print(student)
        # print(data)
        # print(data["ProgramDescription"].loc[student])
        if data.loc[student, "ProgramDescription"] not in major_requirement:
            print('{} ({}) major is {}. Must be {}.\n'.format(data["Name"].loc[student], data[
                "Email"].loc[student], data["ProgramDescription"].loc[student], major_requirement))
            data.loc[student, "Major"] = "Wrong major"
        print('That\'s it!')
    return data


def check_report(filename, prereqdict=prereqdict, majordict=majordict):
    data, student_list, course_name = read_prereq_report(filename)
    print(filename)
    file_path =  filename[:filename.rfind('/')+1]
    print(file_path)
    prereqs = prereqdict[course_name]
    data, no_transfer_data = append_transfer(data, student_list)
    data = check_class(course_name, student_list,
                       data, prereqs, no_transfer_data)
    if course_name in majordict:
        data = check_majors(majordict[course_name], data, student_list)
        data = data[data.Major.notnull() and data.Pre_req_status.notnull()]
        cols = data.columns.tolist()
        cols = cols[:1] + cols[-2:] + cols[1:-2]
        data = data[cols]

    else:
        data = data[data.Pre_req_status.notnull()]
        cols = data.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        data = data[cols]

    data = data.sort_values(by=('PRIMARY_ADVISOR_NAME_LFMI'))
    print(data['Email'][0])

    email_list = ''
    for email in data['Email']:
        email_list += email
        email_list += '; '
    email_list = email_list[:-1]
    print(email_list)
    d = {'Name': pd.Series('', index=['E List'])}


    df2 = pd.DataFrame(d)
    original_columns = list(data)
    data = data.append(df2)
    data = data[original_columns]
    #data['Name','E List'] = 'x'
    data.at['E List', 'Name'] = email_list
    #data.iat[18, 0] = 7
    writer = pd.ExcelWriter(file_path + course_name + '_report.xlsx',  engine='xlsxwriter')
    data.to_excel(writer, sheet_name = 'Checks')
    #writer.sheets['Checks'].column_dimensions['Name'].width = 15
    #help(writer.sheets['Checks'].set_column)
    #writer.sheets['Checks'].set_column('Name','Name',15)
    #writer.column_dimensions['Name'].width = 15
    writer.save()
    print(file_path + course_name + '_report.xlsx written.')
    tprint('\a')
    print('end')
    return data


# ! /usr/bin/env python

"Find string in file, show file name, line number, and line"

os.environ['PATH'] = os.path.normpath(
    os.environ['PATH'] + ':opt.local/bin:/usr/texbin:/usr/local/bin:/usr/bin:/bin:')
str2find = sys.argv[-1]

# print(sys.argv[1])

for file in sys.argv:
    # print(file[-2:])
    if ".py" in file:
        # print(file[-2:])
        tprint('\n')
        # print("Ignoring {}".format(file))
    elif "Student_prerequisite_data.xlsx" in file or '~' in file:
        tprint('\n')
    else:
        tprint(file)
        tprint('**************')
        data = check_report(file, prereqdict, majordict)

        # print(data)
