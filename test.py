counter = 1
import buddyDates

def runScript():
    buddyDates.main()

while counter <= 10:
    runScript()
    print("Run " + str(counter) + " complete")
    counter += 1