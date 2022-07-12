counter = 1
import buddyDates
import sys, os

## Uncomment main method in buddyDates.py to test ##
def runScript():
    blockPrint()
    buddyDates.main()
    enablePrint()

# Disable Printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Printing
def enablePrint():
    sys.stdout = sys.__stdout__

while counter <= 100:
    runScript()
    print("Run " + str(counter) + " complete")
    counter += 1