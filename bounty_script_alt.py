import csv
import json

last_index = -1
csv_filename = 'poker_alt.csv'
with open(csv_filename, newline='') as csvfile:
    table_reader = csv.reader(csvfile)
    for row in table_reader:
        if row[0] != "AVG-Stack":   #we use this to confirm the last index (or play date) in the table, 
                                    #if the value is zero, this coloumn (and any following) wasn't played yet.
            continue

        for i in range(len(row)):
            if row[i] == "0":
                last_index = i
                break


person_look_up = {}

rows_to_ignore = ["Datum", "Runde" ,"AVG-Stack", "Start-Stack", "Netto-Gewinne", "Platzierungen", "Anzahl Buy-Ins", "Rebuy-Stacks"]

list_of_averages = []

with open(csv_filename, newline='') as csvfile:
    table_reader = csv.reader(csvfile)
    for row in table_reader: #iterating through the non important rows
        if row[0] == "":
            continue
        
        if row[0] == "Netto-Gewinne":
            #print("Break") #just a check for debug reasons
            break #we advance to the main loop


    for row in table_reader: #main loop
        if row[0] == "":
            continue
        
        if row[0] == "Platzierungen":
            #print("Break") #just a check for debug reasons
            break #we are done with the main cycle

        if row[0] in rows_to_ignore:
            continue
        

        playername = row[0]
        person_look_up[playername] = {
            "three_round_avg":0,
        }
        count = 0
        for index in range(last_index-1,0,-1):
            if count == 3: 
                break
            if row[index] == "":
                continue
            #else
            #print(row[index])
            if row[index] == "n.t." or row[index] == "n. t.":
                continue
            person_look_up[playername][count]= int(row[index])
            count+=1
        person_look_up[playername]["count"] = count # how many times this person joined us to play, in case its less than 3

        if count > 0:
            average = sum(person_look_up[playername][c] for c in range(count)) / count
            person_look_up[playername]["three_round_avg"] = average
            list_of_averages.append(average)

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
