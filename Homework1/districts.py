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

    #for x in state_lines:
    #    if x["D"] and x["D"] != "H":
    #        print(x["STATE"], " ",x["D"], " ", x["GENERAL %"])
    #        winning_district(x["D"],state_lines)

    #margins = {}
    #for ss in set(x["D"] for x in state_lines if x["D"] and x["D"] != "H"):
    #    margins[ss] = winning_district(ss,state_lines)
    #return margins

    margins = {}
    old_district = -1
    maxper = 0
    second = 0
    for x in state_lines:
        if x["D"] and x["D"] != "H":
            district = int(x["D"].replace(" - FULL TERM","").replace(" - UNEXPIRED TERM",""))
            if district != old_district:
                if old_district != -1:
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
            if x["GENERAL VOTES "] == "Unopposed":
                maxper=100
                second = 0
            old_district = district
    return margins


    #margins = {}
    #for x in state_lines:
    #    if x["D"] != "H":
    #        margins[x["D"].replace(" - FULL TERM", "").replace(" - UNEXPIRED TERM","")] = winning_district(x["D"], state_lines)
    #return margins

    # Complete this function
    #return dict((int(x["D"].replace(" - FULL TERM", "").replace(" - UNEXPIRED TERM", "")), 
        #25) for x in state_lines if x["D"] and x["D"] != "H")
        #winner(x["D"], state_lines)) for x in state_lines if x["D"] and x["D"] != "H")

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

def winning_district(district, state_info):
    maxper = 0;
    second = 0;
    for x in state_info:
        vote_per = x["GENERAL %"].replace(",",".").replace("%","")
        print(vote_per)
        print(x["D"], " ", district)
        if x["D"] == district and vote_per != "":
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



