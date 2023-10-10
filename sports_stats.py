from metaphor_python import Metaphor
import requests
from bs4 import BeautifulSoup

api_key = "0e16c430-9bbb-48c1-a8a9-924715afabec"
metaphor = Metaphor(api_key)
tag = False


# Getting the sport and stat the user wants a link to
user_sport = input("Enter a sport you want stats about: ")
user_stat = input("Enter the stat you want: ")

# The combined search query
search_query = user_sport + " all time " + user_stat + " leaders:"

# Retrieving the search results from metaphor using keyword searching
search_response = metaphor.search(search_query, type="keyword")

# Looping through the search results and getting the url with the string Reference in the Title
# Break out once it's found and stored
for response in search_response.results:
    if "Reference" in response.title:
        url = response.url
        tag = True
        break

# Check if the url was not found
if tag == False:
    print("No reference to this sport or statistic, sorry :(")
    exit()

# Send an HTTP GET request to the URL
request = requests.get(url)

# Check if the request was successful
if request.status_code == 200:

    # Setup site parsing
    soup = BeautifulSoup(request.text, "html.parser")

    # Find the table with player ranking
    table = soup.find("table")

    # Player list initialization
    top_five_players = []

    # Iterate through the table, skipping header
    for row in table.find_all("tr")[1:6]:
        columns = row.find_all("td")

        # Store the player rank, name, and stat
        rank = columns[0].text.strip()
        player = columns[1].text.strip()
        stat = columns[2].text.strip()

        # Add stats to the player list
        top_five_players.append({
            "Rank": rank,
            "Player": player,
            user_stat: stat,
        })

    count = 1

    # Print the list of the top 5 in the given stat
    # The columns may vary per website retrieved, however, the player name and their ranking
    # in the stat will be placed in order from 1-5
    print("\nHere are the top 5 players in history in this stat:")
    for person in top_five_players:
        print(str(count) + f": {person['Rank']}, {person['Player']}, {person[user_stat]}")    
        count += 1  

# Case if request was unsuccessful
else:
    print("Website couldn't be retrieved")