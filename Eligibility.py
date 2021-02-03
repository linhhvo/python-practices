"""
@author: Linh Vo
@purpose: This program estimates number of students eligible for a program certificate.
"""

import os

# Function to get program name and course details from one file
def processOneProgramFile(filePath):
    """
    Parameters:
    filePath - a string providing the path to a file.
    Returns a tuple consisting of the program name and the dictionary that have course numbers as keys and course description as values.
    """
    courseDict = {}
    programName = ""

    with open(filePath, "r") as fileName:
        # Get program name from the first line of the file
        programName = fileName.readline()[:-1]
        # Get course number and course name from each line in the file
        for line in fileName:
            courseNum = line.split()[0]
            courseName = " ".join(line.split()[1:])
            courseDict[courseNum] = courseName

    return programName, courseDict


# Function to combine individual program data from all program files
def processProgramFiles(folderName):
    """
    Parameters:
    folderName - a string providing the path to a folder that contains program files.
    Returns a dictionary in which the program name is used for key and program course dictionary is the value.
    """
    programDict = {}
    # Iterate through and process 5 program files
    for numb in range(1, 6):
        fileName = "program" + str(numb) + ".txt"
        filePath = os.path.join(os.getcwd(), folderName, fileName)
        program, courses = processOneProgramFile(filePath)
        programDict[program] = courses

    return programDict


# Function to combine course enrollments data from class files
def processClassFiles(folderName):
    """
    Parameters:
    folderName - a string providing the path to a folder that contains class list files.
    Returns a dictionary in which the key is course number and value is a set of student login for students who have taken or are currently taking the course.
    """
    classStudentDict = {}

    folderPath = os.path.join(os.getcwd(), folderName)
    filesList = os.listdir(folderPath)

    for file in filesList:
        if "program" not in file:  # Exclude program files
            filePath = os.path.join(folderPath, file)
            with open(filePath, "r") as fileName:
                studentSet = set()
                # Get course number from the first line of the file
                courseNumb = fileName.readline()[:-1]
                # Check if course number already exists as a key in the dictionary, add student to its value
                if courseNumb in classStudentDict.keys():
                    for line in fileName:
                        student = line.split()[0]
                        classStudentDict[courseNumb].add(student)
                # If course number is not in the dictionary, add a new entry
                else:
                    for line in fileName:
                        student = line.split()[0]
                        studentSet.add(student)
                        classStudentDict[courseNumb] = studentSet

    return classStudentDict


# Function to get a list of all students that ever took a class
def allStudents(classStudentDict):
    """
    Parameters:
    classStudentDict - a dictionary that contains course numbers and their corresponding students.
    Returns a set of students that ever took a class.
    """
    # Get sets of students from all courses
    students = classStudentDict.values()
    allStudents = set()

    for studentSet in students:
        allStudents = allStudents.union(studentSet)

    return allStudents


# Function to find students eligible for a program certificate
def eligibleStudents(programName, programDict, classStudentDict, allStudents):
    """
    Parameters:
    programName - a string for the name of a program certificate.
    programDict - a dictionary in which the program name is used for key and program course dictionary is the value.
    classStudentDict - a dictionary in which the key is course number and value is a set of student login for students who have taken or are currently taking the course.
    allStudents - a set of students that ever took a class.
    Returns a sorted list of students who would be eligible for the certificate in the programName.
    """

    requiredCourses = programDict[programName].keys()
    eligibleStudents = allStudents

    # Get all students attending/attended in each required course
    for course in requiredCourses:
        programClass = "c" + course  # to match with class numbers
        classStudents = classStudentDict.get(programClass)
        # Find students that take all required courses in the program
        eligibleStudents = eligibleStudents.intersection(classStudents)

    return sorted(eligibleStudents)


def main():
    folderName = input("Please enter the name of the subfolder with files: ")
    programName = input("Enter program name or press enter to stop: ").upper()

    # Continue to ask for input if user doesn't press Enter
    while programName != "":
        # Get required courses for each program
        programDict = processProgramFiles(folderName)
        # Check if program name is valid
        if programName in programDict:
            # Get the list of eligible students
            classStudentDict = processClassFiles(folderName)
            students = allStudents(classStudentDict)
            eligibles = eligibleStudents(
                programName, programDict, classStudentDict, students
            )
            # Print the number of eligible students and list of students
            print(
                str(len(eligibles)),
                "students are eligible for degree in",
                programName,
            )
            for student in eligibles:
                print(student)

        programName = input("Enter program name or press enter to stop: ").upper()
    # End program when user presses Enter
    print("Bye!")


main()
