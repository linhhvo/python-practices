"""
@author: Linh Vo
@purpose: This program composes and displays a summary of the purchase data from the past week for a coffee shop then provides answers for questions regarding peak for each day of the week.
"""

import datetime
import orderlog

ORDERS = orderlog.orderlst
ORDERS.pop(0)  # Remove column header of order list

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

OPEN_TIME = 6 * 60
CLOSE_TIME = 22 * 60


# Function to convert time string to minutes


def toMin(timeString):
    """
    Parameters:
    timeString - a string of format 'HH:MM:SS', where HH is hour, MM is minute, SS is second.
    Returns a single integer corresponding to the time specified by
    the parameter, converted to minutes.
    """
    h, m, s = timeString.split(":")
    minutes = int(h) * 60 + int(m) + int(s) // 60
    return minutes


# Function to produce a string label with begin-end times of an interval


def labelString(intervalIndex, openingTime, intervalLength):
    """
    Parameters:
    intevalIndex - a single integer, 0-based.
    openingTime - a single integer, constant defined as OPEN_TIME.
    intervalLength - a single integer, in minutes.
    Returns a string defining the start and end time of the interval.
    """

    # Calculate start and end time of the interval
    startTime = openingTime + (intervalLength * intervalIndex)
    endTime = startTime + intervalLength - 1

    # Create start and end time strings
    startTimeString = str(startTime // 60) + ":" + str(startTime % 60).zfill(2)
    endTimeString = str(endTime // 60) + ":" + str(endTime % 60).zfill(2)

    # Combine string
    timeString = startTimeString + "-" + endTimeString
    return timeString


# Function to create the order summary matrix


def composeWeeklyOrdersMatrix(intervalLength=60):
    """
    Parameters:
    intervalLength - a single integer default to 60, in minutes.
    Returns a two-dimensional list populated with summarized order information.
    """

    # Calculate the number of time intevals
    intervalCount = (CLOSE_TIME - OPEN_TIME) // intervalLength
    # Create 2 dimensional list
    matrix = []
    for i in range(len(DAYS_OF_WEEK)):
        matrix.append([])
        for j in range(intervalCount):
            matrix[i].append(0)
    # Get data from order list
    for order in ORDERS:
        y, m, d = order[0].split("-")
        orderDay = datetime.datetime(int(y), int(m), int(d)).weekday()
        orderMinute = toMin(order[1])
        orderInterval = (orderMinute - OPEN_TIME) // intervalLength
        # Add data to oder summary matrix
        matrix[orderDay][orderInterval] += 1
    return matrix


# Function to display the content of the matrix


def printOrderSummaryMatrix(orderMatrix, intervalLength):
    """
    Parameters:
    orderMatrix - a two-dimensional list of integers.
                intervalLength - a single integer, in minutes.
    Print order summary display.
    """

    # Create string for all time intervals
    timeIntervals = ""
    intervalCount = (CLOSE_TIME - OPEN_TIME) // intervalLength
    for i in range(intervalCount):
        timeIntervals += labelString(i, OPEN_TIME, intervalLength).rjust(11) + "|"

    # Summary length to use for displaying dashes
    stringLength = len("DAY\\TIME".ljust(9) + "|" + timeIntervals)

    print("\nWEEKLY ORDER SUMMARY\n")
    print("DAY\\TIME".ljust(9) + "|" + timeIntervals)  # Column header
    print("-" * stringLength)
    # Format and print order summary matrix
    for x in range(len(DAYS_OF_WEEK)):
        orders = ""
        for order in orderMatrix[x]:
            orders += str(order).rjust(12)
        print(DAYS_OF_WEEK[x].ljust(9) + orders)
    print("-" * stringLength)


# Main function to start the program flow, read user input, call other functions


def main():
    intervalInput = ""
    while not intervalInput.isdigit():
        intervalInput = input("\nPlease specify the length of the time interval in minutes: ")

    intervalInput = eval(intervalInput)
    # Display order summary
    orderMatrix = composeWeeklyOrdersMatrix(intervalInput)
    printOrderSummaryMatrix(orderMatrix, intervalInput)

    dayInput = "day"
    # If user doesn't press Enter, run this loop body
    while dayInput != "":
        # If user enters an invalid day of week, ask for input again
        while dayInput not in DAYS_OF_WEEK and dayInput != "":
            dayInput = input("\nEnter day to see peak interval, or press Enter to stop: ").capitalize()
        # If user presses Enter, exit the loop
        if dayInput == "":
            break

        dayIndex = DAYS_OF_WEEK.index(dayInput)
        # Get and print the highest number of orders and its time interval
        peakAmount = max(orderMatrix[dayIndex])
        peakInterval = orderMatrix[dayIndex].index(peakAmount)
        peakIntervalString = labelString(peakInterval, OPEN_TIME, intervalInput)

        if peakAmount > 0:
            print(f"{peakIntervalString}, {peakAmount} orders")
        else:
            print("There are no orders on this day.")

        dayInput = input("\nEnter day to see peak interval, or press Enter to stop: ").capitalize()

    # End the program when user presses Enter
    print("Bye!")


main()