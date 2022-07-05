import csv
from math import comb
from os.path import exists
import random

## Script Options ##
numWeeks = 26
allowRecycledPairs = False
useOldPairings = True

## File Information ##
outputFilePath = "Buddy Dates - EL 2023-2024 Spring.csv"
oldPairingsPath = "Buddy Dates - EL 2023-2024 Fall.csv"
emergelingsPath = "roster.csv"

## Function to gather unique pairs ##
def getNewPair(optionsList, oldPairingsList, allowRecycledPairs):
    foundNewPair = False
    counter = 1
    tempList = []
    while not foundNewPair and counter <= comb(len(optionsList), 2):
        newCombination = False
        pairing = None
        reversedPairing = None
        allowableException = False
        while not newCombination:
            pairing = random.sample(optionsList, 2)
            reversedPairing = pairing[::-1]
            if pairing not in tempList and reversedPairing not in tempList:
                newCombination = True
            elif counter == comb(len(optionsList), 2) and allowRecycledPairs:
                pairing = random.sample(optionsList, 2)
                reversedPairing = pairing[::-1]
                allowableException = True

        if (pairing not in oldPairingsList and reversedPairing not in oldPairingsList) or allowableException:
            foundNewPair = True
            return pairing
        else:
            tempList.append(pairing)
            counter += 1
    return None

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
    print("Error: The provided roster does not exist. Please double check that the file is in the same directory as this script, and that you have provided the correct name.")
    exit()

with open(emergelingsPath, 'r') as inputFile:
    # read each line of the csv file into an array of names
    reader = csv.reader(inputFile)
    names = list(reader)
    numEmergelings = len(names)

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
    while counter < numEmergelings / 2:
        # get a random pairing from the names array
        pairing = getNewPair(names, completePairings, allowRecycledPairs)
        if pairing is not None:
            result.append(pairing)
            completePairings.append(pairing)
        counter += 1

    writePairings(result, currentWeek, writer)
    if (len(result) == 0):
        writer.writerow(["Maximum combinations reached. Consider allowing recycled pairs."])
    writer.writerow("")
    currentWeek += 1
    counter = 0
    result = []

outputFile.close()
print("All done :)")