import csv
import json

last_index = -1
csv_filename = 'Poker_BB.csv'


with open(csv_filename, newline='') as csvfile:
    table_reader = csv.reader(csvfile)
    for row in table_reader:
        if row[0] != "Stakes":   #we use this to confirm the last index (or play date) in the table, 
                                    #if the value is zero, this coloumn (and any following) wasn't played yet.
            continue

        for i in range(len(row)):
            if row[i] == "":
                last_index = i
                break

person_look_up = {}

rows_to_ignore = ["Datum", "Runde" ,"AVG-Stack", "Start-Stack", "Netto-Gewinne", "Platzierungen", "Anzahl Buy-Ins", "Rebuy-Stacks"]
#this is from the old script, as of right now, not needed anymore.
list_of_averages = []

"""
Here a loop to recognize who played at all, and in which rounds did they. We memorize that by indexes
"""
with open(csv_filename, newline='') as csvfile:
    table_reader = csv.reader(csvfile)
    for row in table_reader: #iterating through the non important rows
        if row[0] == "":
            continue
        
        if row[0] == "in":
            
            break #we advance to the main loop

    for row in table_reader: #main loop
        if row[0] == "":
            continue
        
        if row[0] == "out":
            break #we are done with the first cylce

        if row[0] in rows_to_ignore:
            continue
        playername = row[0]
        person_look_up[playername] = {
            "three_round_avg" : 0,
            "when_played_indexes" : [],
            "count" : 0 
        }
        count = 0
        when_played_indexes = []
        for index in range(last_index-1,0,-1):
            if count == 3: 
                break
            if\
            row[index] == "" or \
            row[index] == "0":
                continue
            count+=1
            when_played_indexes.append(index)

        
        person_look_up[playername]["when_played_indexes"]= when_played_indexes
        person_look_up[playername]["count"]= len(when_played_indexes)



"""
With our Lookup initialized we open the file a second time, to calculate the averages from each player's last rounds. First we fast-forward to everything coming after the "gewinn" line.
Then we access the values at the memorized indexes.
"""

with open(csv_filename, newline='') as csvfile:
    table_reader = csv.reader(csvfile)
    for row in table_reader: #iterating through the non important rows
        if row[0] == "":
            continue
        
        if row[0] == "gewinn":
            
            break #we advance to the main loop


    for row in table_reader: #main loop
        if row[0] == "":
            continue
        
        if row[0] == "": #the first empty line indicates the programm being finished    
            break #we are done with the main cycle

        if row[0] in rows_to_ignore:
            continue
        

        playername = row[0]
        count = person_look_up[playername]["count"]
        if count > 0:
            when_played_indexes = person_look_up[playername]["when_played_indexes"]
            average = sum(int(row[c]) for c in when_played_indexes) / count
            person_look_up[playername]["three_round_avg"] = average
            list_of_averages.append(average)

"""
Having calculated the averages, we build a reverse lookup for fast access after sorting, then sort, then print out the sorted rankings.
"""

reverse_dict = { person_look_up[playername]["three_round_avg"]:[] for playername in person_look_up.keys()  }


for playername in person_look_up.keys():
    if person_look_up[playername]["count"] > 0:
        reverse_dict[person_look_up[playername]["three_round_avg"]].append(playername) #now checks if a listed player has joined us at all
    
list_of_averages = list (set (list_of_averages)) # removes duplicates
list_of_averages.sort(reverse=True)


placement = 1

with open('bounties.txt',"w") as bountyfile:
    for average in list_of_averages:
        for person in reverse_dict[average]:
            person_string = person+ " "*(20-len(person))
            
            print(f"{placement:3}. {person_string} | {int(average):5}") #formating
            print(f"{placement:3}. {person_string} | {int(average):5}", file= bountyfile )

        
        placement += len(reverse_dict[average])
