import pprint
from tournament import *

tournament_list = []

def addTournament():
    showTournaments()
    print()
    name = raw_input("Enter the name of the tournament you would like to add, or enter 'quit' to quit: ")

    if name == "quit":
        return
    
    registerTournament(name)

def deleteMatches():
    choice = input("'1' to delete all matches, '2' to delete from particular tournament ('0' to quit): ")

    if choice == 1:
        print("\tDelete all matches")
        deleteAllMatches()
        print("\tDeletion successful!")
    elif choice == 2:
        tournament_name = selectTournament()
        if len(tournament_name) == 0:
            return
        print("\tDeleting matches from tournament '{}'".format(tournament_name)) 
        deleteMatchesFromTournament(tournament_name)
        print("\tDeletion successful!")
    else:
        return

def addPlayerToDB():
    name = raw_input("Enter the name of the player you wish to add, or 'quit' to quit: ")
    
    if name == "quit":
        return

    print("\tAdding player {} to database".format(name))
    registerPlayer(choice)
    print("\tPlayer successfully added!")

    choice = input("'1' to register player for tournament, '2' to return to menu: ")

    if choice == 1:
        tournament_name = raw_input("Enter the name of the tournament you wish to register to player for: ")
        registerPlayerForTournament(name, tournament_name):

def playerStandingsForTournament():
    return

def reportMatchForTournament():
    return

def swissPairingsForTournament():
    return

def runAllTests():
    return

def selectTournament():
    showTournaments()
    choice = input("\nChoose the number of the tournament you wish to choose, or '0' to quit: ")

    if choice == 0:
        return ""

    return tournament_list[choice-1]

def showTournaments():
    print("\nShowing all tournaments:")
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT tournament_name FROM tournaments")
    tournaments = c.fetchall()
    if len(tournaments) == 0:
        print("\tNo tournaments registered")
    else:
        global tournament_list
        for i, tournament in enumerate(tournaments, start=1):
            tournament_list.append(tournament[0])
            print("\t{}. {}".format(i, tournament[0]))
    DB.close()

def list_options():
    print('-' * 60)
    print("Options:")
    print("\t1. Add a tournament to the database")
    print("\t2. Delete matches from a particular tournament")
    print("\t3. Delete all player records")
    print("\t4. Count the number of players")
    print("\t5. Register player name")
    print("\t6. Show player standings for a tournament")
    print("\t7. Report a match result for a particular tournament")
    print("\t8. Automatically generate Swiss pairings")
    print("\t9. Run all tests")

def main():
    print("Alan Gou's SQL Tournament driver")
    choice = -1

    while choice != 0: 
        list_options()
        choice = input("\nEnter number of command ('0' to quit): ")

        if choice == 1:
            addTournament()
        elif choice == 2:
            deleteMatches()
        elif choice == 3:
            deletePlayers()
        elif choice == 4:
            countPlayers()
        elif choice == 5:
            addPlayerToDB()
        elif choice == 6:
            playerStandingsForTournament()
        elif choice == 7:
            reportMatchForTournament()
        elif choice == 8:
            swissPairingsForTournament()
        elif choice == 9:
            runAllTests()
        
if __name__ == "__main__":
    main()
