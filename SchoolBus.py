'''
@author: Linh Vo
@purpose: This program takes input from users for school start time and stop number 
then calculates the pricing and the arrival and departure time of the school bus to a specified location
'''

TOTAL_TRIP_LENGTH = 45  # in minutes
STOP_TRAVEL_LENGTH = 3  # in minutes
STOP_WAIT_TIME = 2  # in minutes
BASE_COST = 1  # in dollar
INTERVAL = 4  # in minutes
EXTRA_COST = .15  # in dollar

# get input from user
schoolStartHour = input('Please enter the hour when school starts: ')
schoolStartMin = input('Please enter the minute when school starts: ')
stopNumber = input('Please enter your stop number: ')

# convert school start time to minutes
schoolStartTime = eval(schoolStartHour) * 60 + eval(schoolStartMin)

# calculate arrival time for input stop
firstStopArrivalTime = schoolStartTime - TOTAL_TRIP_LENGTH
userStopArrivalTime = firstStopArrivalTime + \
    ((eval(stopNumber) - 1) * (STOP_WAIT_TIME + STOP_TRAVEL_LENGTH))
userStopArrivalHour = userStopArrivalTime // 60
userStopArrivalMin = userStopArrivalTime % 60

# calculate leave time for input stop
userStopLeaveTime = userStopArrivalTime + 2
userStopLeaveHour = userStopLeaveTime // 60
userStopLeaveMin = userStopLeaveTime % 60

# calculate length of trip in minutes
lengthOfTrip = schoolStartTime - userStopLeaveTime

# calculate ticket cost for the trip
totalCost = BASE_COST + EXTRA_COST * (lengthOfTrip // 4)

# print out results
print('The bus will be at stop number ', stopNumber, ' between ', userStopArrivalHour,
      ':', str(userStopArrivalMin).zfill(2), ' and ', userStopLeaveHour,
      ':', str(userStopLeaveMin).zfill(2), sep='')
print('The length of the trip from stop number',
      stopNumber, 'is', lengthOfTrip, 'minutes')
print('The cost of the ticket from stop number ',
      stopNumber, ' is $', totalCost, sep='')
