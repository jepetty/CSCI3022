import csv
from csv import DictReader

def main():
	JessSolution()
	print("\n")
	JordanSolution()

def CleanRow(data):
	newData = data.replace(".","")
	newData = newData.replace("[", "")
	newData = newData.replace(",", "")
	newData = newData.replace("]", "")
	newData = newData.replace("%","")
	return int(newData)


def JessSolution():
    with open('2012pres.csv', newline = '\n') as csvfile:
	    reader = csv.reader(csvfile, delimiter=';')
	    reader.__next__()
	    votes = 0
	    newVotes = 0
	    otherVotes = 0
	    maxDiff = 0
	    maxState = ""
	    currState = ""
	    newState = False
	    topCand = 0
	    for row in reader:
	    	votes = votes + CleanRow(row[10])
	    	if newState == True:
	    		newState = False
	    		newDiff = topCand - CleanRow(row[10])
	    		if newDiff > maxDiff:
	    			maxDiff = newDiff
	    			maxState = currState
	    	if (currState != row[3] and row[8] != "Total State Votes:"):
	    		currState = row[3]
	    		newState = True
	    		topCand = CleanRow(row[10])
	    		otherVotes = otherVotes + CleanRow(row[10])
	    	elif row[8] == "Total State Votes:":
	    		newVotes = newVotes + CleanRow(row[10])
	    	elif row[8] != "Total State Votes:":
	    		otherVotes = otherVotes + CleanRow(row[10])


	    votes = votes/2
	    print("Total votes: ", votes)
	    print("Total with new votes: ", newVotes)
	    print("Other votes: ", otherVotes)
	    print("Max Difference: ", maxDiff, " in state: ", maxState)


# from csv import DictReader
def JordanSolution():
	votes = list(DictReader(open("2012pres.csv", 'r'), delimiter=";"))
	total_votes = sum(int(x["TOTAL VOTES #"].replace(".",""))
		for x in votes if x["TOTAL VOTES #"])
	print("Jordan's total votes: ", total_votes)

	margins = {}
	for ss in set(x["STATE"] for x in votes):
		margins[ss] = winner(votes, ss)[1] - second(votes, ss)[1]
	num_margin = argmax(margins)



if __name__ == "__main__":
	main()

#total state votes = rows[8]
#vote count = rows[10]