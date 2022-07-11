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
def getPair(names, advisors, oldPairings, currentPairings,allowRecycledPairs):
    attemptedMatches = []

    for attempt in range(1, comb(len(names),2)):
        pairing = getPairing(names, attemptedMatches, True)
        if isUnique(pairing, advisors, currentPairings, oldPairings, False):
            return pairing
        elif allowRecycledPairs and attempt == comb(len(names),2):
            pairingOK = False
            while not pairingOK:
                if isUnique(pairing, advisors, currentPairings, oldPairings, True):
                   pairingOK = True
                else:
                    pairing = getPairing(names, attemptedMatches, False)

            return pairing
        elif attempt == comb(len(names), 2):
            return None

## Function to get pairing
def getPairing(names, attemptedPairings, rigidCheck):
    newPairing = False
    while not newPairing:
        pairing = random.sample(names, 2)
        if not rigidCheck:
            return pairing
        reversedPairing = pairing[::-1]
        if pairing in attemptedPairings or reversedPairing in attemptedPairings:
            return pairing

## Function to check if pairing is unique ##
def isUnique(pairing, advisors, currentPairings, oldPairings, basicCheck):
    reversedPairing = pairing[::-1]

    person1 = pairing[0]
    person2 = pairing[1]

    if person1 in currentPairings or person2 in currentPairings:
        return False

    if person1 in advisors and person2 in advisors:
        return False
    
    if basicCheck:
        return True

    for oldPair in oldPairings:
        if pairing == oldPair or reversedPairing == oldPair:
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
                oldPairings.append([[line[0]], [line[1]]])
    return oldPairings

## Main Program ##

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

# Set up old matches
if useOldPairings:
    oldMatches = getOldPairings()
else:
    oldMatches = []

# Loop Variables
result = []
currentWeek = []
tempMatches = []
counter = 0
numMembers = len(names)
expectedPairings = floor(numMembers / 2)

for week in range(1,numWeeks):
    while counter < expectedPairings:
        pairing = getPair(names, advisors, oldMatches, currentWeek, useRecycledPairs)
        if pairing is not None:
            currentWeek.append(pairing)
            tempMatches.append(pairing)
        counter += 1

    result.append(tempMatches)
    print(len(tempMatches))
    tempMatches = []

