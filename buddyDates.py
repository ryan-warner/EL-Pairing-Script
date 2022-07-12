import csv
from math import comb, floor
from os.path import exists
import random

## Script Options ##
numWeeks = 26
useRecycledPairs = False
useOldPairings = False

## File Information ##
outputFilePath = "Buddy Dates - EL 2023-2024 Spring.csv"
oldPairingsPath = "Buddy Dates - EL 2023-2024 Fall.csv"
emergelingsPath = "roster.csv"
advisorsPath = "advisors.csv"

## Function to gather unique pairs ##
def getPair(funcNames, funcAdvisors, oldPairings, currentPairings, allowRecycledPairs):
    attemptedMatches = []

    for attempt in range(1, comb(len(funcNames),2) + 1):
        pairing = getPairing(funcNames, attemptedMatches, True)
        attemptedMatches.append(pairing)
        if isUnique(pairing, funcAdvisors, currentPairings, oldPairings, False):
            return pairing
        elif allowRecycledPairs and attempt == comb(len(funcNames),2):
            pairingOK = False
            funcAttemptCounter = 0
            while not pairingOK:
                if isUnique(pairing, funcAdvisors, currentPairings, oldPairings, True):
                   pairingOK = True
                else:
                    pairing = getPairing(funcNames, attemptedMatches, False)
                    funcAttemptCounter += 1
                if funcAttemptCounter > 5000:
                    return -1
            return pairing
        elif attempt == comb(len(funcNames), 2):
            return None

## Function to get pairing
def getPairing(funcNames, attemptedPairings, rigidCheck):
    newPairing = False
    while not newPairing:
        pairing = random.sample(funcNames, 2)
        reversedPairing = pairing[::-1]
        if not rigidCheck:
            newPairing = True
        elif pairing not in attemptedPairings or reversedPairing not in attemptedPairings:
            newPairing = True

    return pairing

## Function to check if pairing is unique ##
def isUnique(funcPairing, funcAdvisors, currentPairings, oldPairings, basicCheck):
    reversedPairing = funcPairing[::-1]

    person1 = funcPairing[0]
    person2 = funcPairing[1]

    for tempPairing in currentPairings:
        if person1 in tempPairing or person2 in tempPairing:
            return False

    if person1 in funcAdvisors and person2 in funcAdvisors:
        return False
    
    if basicCheck:
        return True

    for oldPair in oldPairings:
        if funcPairing == oldPair or reversedPairing == oldPair:
            return False
    return True

## Function to write weekly pairings to a file ##
def writePairings(pairings, weekNum, writer):
    writer.writerow(["Week " + str(weekNum) + " Pairings"])
    for pair in pairings:
        writer.writerow(pair[0] + pair[1])

## Function to import old pairings from an existing file ##
def getOldPairings():
    if not exists(oldPairingsPath):
        print("Error: The provided pairings file does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
        exit()
    else:
        print("Old pairings found. Importing...")

    oldPairings = []
    with open(oldPairingsPath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        fileContent = list(reader)
        for line in fileContent:
            if len(line) != 0 and line[0] != "" and "Week" not in line[0]:
                oldPairings.append([[line[0]],[line[1]]])
    return oldPairings

## Main Program ##

def run():
    # Get Emergeling Data
    if not exists(emergelingsPath):
            print("Error: The provided Emergeling roster does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
            exit()
    else:
        print("Emergeling roster found.")

    with open(emergelingsPath, 'r') as emergelingsInput:
        # read each line of the csv file into an array of names
        reader = csv.reader(emergelingsInput)
        emergelings = list(reader)
        print("Emergeling roster loaded.")

    # Get Advisor Data
    if not exists(advisorsPath):
        print("Error: The provided advisors roster does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
        exit()
    else:
        print("Advisors roster found.")

    with open(advisorsPath, 'r') as advisorsInput:
        # read each line of the csv file into an array of names
        reader = csv.reader(advisorsInput)
        advisors = list(reader)
        print("Advisors roster loaded.")

    names = emergelings + advisors
    print("")

    # Set up old matches
    if useOldPairings:
        oldMatches = getOldPairings()
    else:
        oldMatches = []

    # Loop Variables
    result = []
    currentWeek = []
    counter = 1
    numMembers = len(names)
    numExpectedPairings = floor(numMembers / 2)
    pairsPossible = comb(len(names), 2) - comb(len(advisors), 2) - len(oldMatches)
    #pairsRemaining = comb(len(names), 2) - comb(len(advisors), 2) - len(oldMatches)
    expectedWeek = floor(pairsPossible / numExpectedPairings) + 1
    remainder = pairsPossible % numExpectedPairings
    attemptCounter = 0
    weekInd = 0

    while weekInd < numWeeks:
        escape = False
        while counter <= numExpectedPairings and not escape:
            pairing = getPair(names, advisors, oldMatches, currentWeek, useRecycledPairs)
            attemptCounter += 1
            if pairing is not None:
                currentWeek.append(pairing)
            counter += 1
            
            if pairing == -1:
                print("Error: Unable to generate a valid pairing. Trying again...")
                print("")
                return False

            if attemptCounter > 5000:
                print("Error: Unable to generate a valid pairing. Trying again...")
                print("")
                return False

            if counter > numExpectedPairings and useRecycledPairs and len(currentWeek) < numExpectedPairings:
                currentWeek = []
                counter = 1
            elif counter > numExpectedPairings and weekInd + 1 < expectedWeek and len(currentWeek) < numExpectedPairings:
                currentWeek = []
                counter = 1
            elif counter > numExpectedPairings and weekInd + 1 == expectedWeek and remainder != 0 and len(currentWeek) < remainder:
                currentWeek = []
                counter = 1

            if counter > numExpectedPairings:
                attemptCounter = 0
                escape = True

        result.append(currentWeek)
        oldMatches.extend(currentWeek)
        currentWeek = []
        counter = 1
        weekInd += 1
        print("Week " + str(weekInd) + " complete.")
    
    outputFile = open(outputFilePath, 'w')
    writer = csv.writer(outputFile)

    weekCounter = 1
    for weeklyPairing in result:
        writePairings(weeklyPairing, weekCounter, writer)
        if (len(weeklyPairing) == 0):
            writer.writerow(["Maximum combinations reached. Consider allowing recycled pairs."])
        writer.writerow("")
        weekCounter += 1

    outputFile.close()
    print("")
    print("All done :)")
    return True

## For use in testing (test.py) ##
## def main():
##     finished = False
##     while not finished:
##         finished = run()

## If testing, comment this block out ##
finished = False
while not finished:
    finished = run()