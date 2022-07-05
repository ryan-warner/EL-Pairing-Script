# EL Buddy Date Script
A short script to create random pairs from a given roster. 

Provides options to recycle pairs when no more combinations are possible, as well as to exclude a list of previously generated pairings. 

## Configuration

Edit the options directly in script. Could be turned into CLI arguments, but for ease of use hardcoding will likely be the most intuitive. 

    ## Script Options ##
    numWeeks = 26
    allowRecycledPairs = False
    useOldPairings = True

    ## File Information ##
    outputFilePath = "outputFile.csv"
    oldPairingsPath = "inputFile.csv"
    emergelingsPath = "roster.csv"

It should be possible to locate files outside of the folder where the script is contained, but it's likely easiest to simply place the script in the folder where pairings will be stored. 

## Running

Set the desired options as shown above, and run by calling

    python3 buddyDates.py

From the folder where the script is located. 