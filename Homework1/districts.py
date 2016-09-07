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
    margins = {}
    old_district = -1
    maxper = 0
    second = 0
    for x in state_lines:
        #if x["STATE"] == "New Jersey":
        #    print(x, "\n")
        if x["D"] and x["D"] != "H":
            if " - UNEXPIRED TERM" not in x["D"]:
                district = int(x["D"].replace(" - FULL TERM",""))
                if district != old_district:
                    if old_district != -1:
                        if maxper == 0 or second == 0:
                            maxper = 100
                        if x["STATE"] == "New Jersey":
                            print("updating: ", old_district, " ", maxper-second)
                        margins[old_district] = maxper - second
                    vote_per = x["GENERAL %"].replace(",",".").replace("%","")
                    if vote_per != "":
                        maxper = float(vote_per)
                    else:
                        maxper = 0
                    second = 0
                else:
                    vote_per = x["GENERAL %"].replace(",",".").replace("%","")
                    if (vote_per != ""):
                        if float(vote_per) > maxper:
                            second = maxper
                            maxper = float(vote_per)
                        elif float(vote_per) < maxper and float(vote_per) > second:
                            second = float(vote_per)
            #if x["GENERAL VOTES "] == "Unopposed":
            #    maxper=100
            #    second = 0
                old_district = district

    if maxper == 0 or second == 0:
        maxper = 100
    margins[old_district] = maxper - second
    return margins

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

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    for state in all_states(lines):
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})



