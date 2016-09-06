from collections import defaultdict
from csv import DictReader, DictWriter
import heapq

kHEADER = ["STATE", "DISTRICT", "MARGIN"]

def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """
    #for x in state_lines:
        #if x["D"] != "H" and x["STATE"] == "Louisiana":
            #print("DISTRICT: ", x["D"]," PRIMARY %: ", x["PRIMARY %"], " RUNOFF %: ", x["RUNOFF %"], " GENERAL %: ", x["GENERAL %"], " GE RUNOFF ELECTION % (LA): ",
                #x["GE RUNOFF ELECTION % (LA)"], " COMBINED % (CT, NY, SC): ", x["COMBINED % (CT, NY, SC)"])
            #print(x["D"], " ",x["TOTAL VOTES"], " ", x["GENERAL VOTES "])
            #print(x["D"], " ", float(x["GENERAL %"].replace(",",".").replace("%","")))

    # Complete this function
    return dict((int(x["D"].replace(" - FULL TERM", "").replace(" - UNEXPIRED TERM", "")), 
        winner(x["D"].replace(" - FULL TERM","").replace(" - UNEXPIRED TERM",""), state_lines))
        #winner(x["D"].replace(" - FULL TERM","").replace(" - UNEXPIRED TERM",""),x["GENERAL %"].replace(",",".").replace("%",""))) 
        for x in state_lines if x["D"] and x["D"] != "H")

def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """
    return set((x["STATE"]) for x in lines if x["STATE"])


def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """

    for ii in lines:
        if ii["STATE"] == state:
            yield ii

def winner(district, state_info):
    maxper = 0;
    second = 0;
    for x in state_info:
        vote_per = x["GENERAL %"].replace(",",".").replace("%","")
        if x["D"].replace(" - FULL TERM","").replace(" - UNEXPIRED TERM","") == district and vote_per != "":
            #print(x["GENERAL %"].replace(",",".").replace("%",""))
            #votes = x["GENERAL %"].replace(",",".").replace("%","")
            #votes = float(x["GENERAL %"].replace(",",".").replace("%",""))
            if float(vote_per) > maxper:
                second = maxper
                maxper = float(vote_per)
            elif float(vote_per) < maxper and float(vote_per) > second:
                second = float(vote_per)
    return (maxper - second)

    #if vote_percentage == "":
        #print(district, " ", vote_percentage)
    #return vote_percentage["GENERAL %"]

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    for state in all_states(lines):
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            #print(state, " ", ii, " ", margins[ii])
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})



