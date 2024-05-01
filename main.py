import requests   #import requests module to handle api
import random   #import random module to give random choice


print('Question loading.')

total_data = []
best_chars_data = []

# use SWAPI the Star Wars Api to get data on all characters from the people endpoint found in SWAPI documents
endpoint = 'https://swapi.dev/api/people/'
response = requests.get(endpoint)
data = response.json()

total_data = total_data + data['results']

# While data['next'] isn't empty, add character's name, movies and starship data to char_data
while data['next'] is not None:
    response = requests.get(data['next'])
    data = response.json()
    total_data = total_data + data['results']

print("Please enter three of your favourite Star Wars Characters to find out more about their ships. Please select Chewbacca as one of the characters as he is of course the best. If you would like a character to be selected for you, please enter 'random'.")
a = input("First character's full name: ")
b = input("Second character's full name: ")
c = input("Third character's full name: ")
# chose to do seperate inputs rather than split bc there are spaces between names and user may not use commas

#put input results in a list
best_chars = [a.title(), b.title(), c.title()] #use title to match format of API data

def replaceRandomCharacter():
    #if input is random, replace with a random name from API data
    for i in range(len(best_chars)):
        if best_chars[i] == 'Random' or best_chars[i] == "'Random'":
          random_char = random.choice(total_data)
          best_chars[i] = random_char['name']
    return best_chars

def getCharacterData():
    #check for names that match the API people data
    for i in range(len(total_data)):
     for char in best_chars:
            if char == total_data[i]['name']:
             best_chars_data.append(total_data[i])
    return best_chars_data

def getShipData():
#get data for star ships and add ship name and speed to char data
    for i in range(len(best_chars_data)):
     best_chars_data[i].update({'ship_data': {}})
     if len(best_chars_data[i]['starships']) > 0:
           for x in range(len(best_chars_data[i]['starships'])):
               endpoint_2 = best_chars_data[i]['starships'][x]
               response_2 = requests.get(endpoint_2)
               starship_data = response_2.json()
               best_chars_data[i]['ship_data'][starship_data['name']] = starship_data['max_atmosphering_speed']
    return best_chars_data



#check Chewbacca is in list, if true then run the program
if 'Chewbacca' in best_chars:
    #update best_chars to replace random characters
    replaceRandomCharacter()
    #update best_chars_data with matching character info and ship data
    getCharacterData()
    getShipData()

    #use updated best_chars_data to print message
    for i in range(len(best_chars_data)):       #for each character user selected
        name = best_chars_data[i]['name']
        if len(best_chars_data[i]['starships']) > 0:   #if there is data for star ships print this message
           max_speed = max(best_chars_data[i]['ship_data'].values())     #find maximum speed of startships piloted
           fastest_ship = max(best_chars_data[i]['ship_data'], key=best_chars_data[i]['ship_data'].get)   #find name of fastest starship
           total_ships = len(best_chars_data[i]['starships'])
           ship_names = ", ".join(best_chars_data[i]['ship_data'].keys())
           msg = (f"{name} has piloted {total_ships} starships: {ship_names}. The fastest ship they have piloted is the {fastest_ship} at max atmosphering speed of {max_speed} kilometers per hour.")
           print(msg)
        else:    #if no data for starships then print this message
           msg = (f"{name} is not a pilot.")
           print(msg)
        with open('Star_Wars_Pilots.txt', 'a') as file:      #save results in a text file, use 'a' to add new result each time
            file.write(msg + '\n')    #log message
else: print('Chewbacca is not one of the three characters you have chosen. Please try again and select Chewbacca as a character.')
