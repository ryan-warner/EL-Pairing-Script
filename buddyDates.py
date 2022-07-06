import csv
from math import comb
from os.path import exists
import random

## Script Options ##
numWeeks = 26
useRecycledPairs = True
useOldPairings = True

## File Information ##
outputFilePath = "Buddy Dates - EL 2023-2024 Spring.csv"
oldPairingsPath = "Buddy Dates - EL 2023-2024 Fall.csv"
emergelingsPath = "roster.csv"
advisorsPath = "advisors.csv"

## Function to gather unique pairs ##
def getNewPair(optionsList, advisorsList, oldPairingsList, allowRecycledPairs):
    allowableException = False
    forceExit = False

    counter = 1
    tempList = [] # Temp list contains the combinations that have been tried
    while counter <= comb(len(optionsList), 2):
        if counter == comb(len(optionsList), 2) and allowRecycledPairs:
            allowableException = True
        elif counter == comb(len(optionsList), 2):
            forceExit = True
               
        pairing = random.sample(optionsList, 2)
        checkMessage = checkPairing(pairing, advisorsList, oldPairingsList, tempList, allowableException)
        if checkMessage == "Match OK":
            return pairing
        elif checkMessage == "Already tried":
            if not allowRecycledPairs and forceExit:
                counter += 1
            else:
                pass
        elif checkMessage == "Advisors may not be matched":
            tempList.append(pairing)
            counter += 1
        elif checkMessage == "Already matched - recycled pairs allowed":
            return pairing
        elif checkMessage == "Already matched":
            tempList.append(pairing)
            counter += 1
    return None

## Function to check if pairing is unique ##
def checkPairing(pairing, advisorsList, oldPairingsList, tempList, allowRecycledPairs):
    reversedPairing = pairing[::-1]
    if (pairing in tempList or reversedPairing in tempList) and not allowRecycledPairs:
        return "Already tried"
    elif pairing[0] in advisorsList and pairing[1] in advisorsList:
        return "Advisors may not be paired"
    elif pairing in oldPairingsList or reversedPairing in oldPairingsList:
        if allowRecycledPairs:
            return "Already matched - recycled pairs allowed"
        else:
            return "Already matched"
    else:
        return "Match OK"

## Function to write weekly pairings to a file ##
def writePairings(pairings, weekNum, writer):
    writer.writerow(["Week " + str(weekNum) + " Pairings"])
    for pair in pairings:
        writer.writerow(pair[0] + pair[1])

## Function to import old pairings from an existing file ##
def getOldPairings():
    oldPairings = []
    with open(oldPairingsPath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        fileContent = list(reader)
        for line in fileContent:
            if len(line) != 0 and line[0] != "" and "Week" not in line[0]:
                oldPairings.append([[line[0]], [line[1]]])
    return oldPairings

## Main Program ##

if not exists(emergelingsPath):
    print("Error: The provided Emergeling roster does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
    exit()

if not exists(advisorsPath):
    print("Error: The provided advisors roster does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
    exit()

with open(emergelingsPath, 'r') as emergelingsInput:
    # read each line of the csv file into an array of names
    reader = csv.reader(emergelingsInput)
    emergelings = list(reader)

with open(advisorsPath, 'r') as advisorsInput:
    # read each line of the csv file into an array of names
    reader = csv.reader(advisorsInput)
    advisors = list(reader)

names = emergelings + advisors
numMembers = len(names)

## Include old.csv in the directory when running if you want to account for old pairings ##
if useOldPairings:
    if exists(oldPairingsPath):
        completePairings = getOldPairings()
    else:
        print("Error: The old pairings provided do not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
        exit()
else:
    completePairings = []

outputFile = open(outputFilePath, 'w')
writer = csv.writer(outputFile)

result = []
counter = 0
currentWeek = 1

## Pairing Loop ##
while currentWeek <= numWeeks:
    while counter < numMembers / 2:
        # get a random pairing from the names array
        pairing = getNewPair(names, advisors, completePairings, useRecycledPairs)
        if pairing is not None:
            result.append(pairing)
            completePairings.append(pairing)
        counter += 1

    writePairings(result, currentWeek, writer)
    if (len(result) == 0):
        writer.writerow(["Maximum combinations reached. Consider allowing recycled pairs."])
    writer.writerow("")
    print("Week " + str(currentWeek) + " pairings complete.")
    currentWeek += 1
    counter = 0
    result = []

outputFile.close()
print("")
print("All done :)")