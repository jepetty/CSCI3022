# Jessica Petty
# CSCI 3022
# Homework 1
# September 8, 2016

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
    top_cand = ""
    win_flag = False
    for x in state_lines:
        if x["D"] and x["D"] != "H":
            if " - UNEXPIRED TERM" not in x["D"]:
                district = int(x["D"].replace(" - FULL TERM",""))
                if x["GE WINNER INDICATOR"] == "W":
                    win_flag = True
                if district != old_district:
                    if old_district != -1:
                        if maxper != 0 and second != 0:
                            margins[old_district] = maxper - second
                        elif second == 0 and maxper == 100:
                            margins[old_district] = 100
                        elif win_flag == True:
                            margins[old_district] = maxper
                            win_flag = False
                    vote_per = x["GENERAL %"].replace(",",".").replace("%","")
                    if vote_per != "":
                        maxper = float(vote_per)
                        top_cand = x["CANDIDATE NAME"]
                    else:
                        maxper = 0
                    second = 0
                else:
                    vote_per = x["GENERAL %"].replace(",",".").replace("%","")
                    if (vote_per != ""):
                        if float(vote_per) > maxper:
                            second = maxper
                            maxper = float(vote_per)
                            top_cand = x["CANDIDATE NAME"]
                        elif float(vote_per) < maxper and float(vote_per) > second:
                            if x["CANDIDATE NAME"] != top_cand:
                                second = float(vote_per)
                old_district = district

    if maxper == 0 or second == 0:
        maxper = 100
    else:
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



