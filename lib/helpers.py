# lib/helpers.py
from models.__init__ import CURSOR, CONN
from models.show import Show
from models.network import Network




def shows_loop(network): 
    shows = network.shows() 
    if shows:
      print("\nShows")
      print("***************")
      for i, show in enumerate(shows, start=1):
            print(f"{i}.{show.name} ({show.genre})\n ")  
      print("\n***************\n ")
    else:
      print(f"  No shows found on {network.name}.")
    return shows



def exit_program():
    print("Goodbye!")
    exit()


    
def list_shows():
    shows = Show.get_all()
    return shows    

def create_show(network, network_id):
    name = input("Enter the show name: ")
    genre = input("Enter the show genre: ")
    network_id = network_id
    try:
        show = Show.create(name, genre, network_id)
        print(f'Success: {show.name} was added to the network')
    except Exception as exc:
        print("Error creating show: ", exc) 

    
def delete_show(network, show_index):
    shows = network.shows()  # Assuming network has a shows() method
    if 0 <= show_index < len(shows):
        show = shows[show_index]
        show.delete()  # Assuming show object has a delete method
        print("\n***************\n ")
        print(f'Show {show.name} was deleted')
        print("\n***************\n ")
    else:
        print("Invalid selection. Please try again.")


def create_network():
    name = input("Enter the network name: ")
    location = input("Enter the network location: ")

    try:
        network = Network.create(name, location)
        print(f"Network created: {network.name}")
        list_networks()
    except Exception as exc:
        print("Error creating network: ", exc)
    else:   
        print(f" Enter 'B' to go back to Main Menu or 'A' to add first show to {network.name}")
        menu_choice = input("> ")
        if menu_choice in ("B", "b"):
            return  # Exit to main menu
        else:
            create_show(network.id)


def list_networks():
    networks = Network.get_all()
    print("\n   Networks \n ") 
    print("***************\n ")
    for i, network in enumerate(networks, start=1):
        print(f"{i}.{network.name} ") 
    print("\n***************\n ")
    return networks


def network_details(network):
  """Displays details of a specific network and their shows (if any)"""
  if network:
    print(f"\nNetwork: {network.name}") 
  else:
    print(f"Network with ID {network} not found.") 

def network_loop(network):
    network_deleted = False
    shows = network.shows() 
    while True:
      print("\n  Options:")      
      print(" Enter 'B' to go back to Main Menu")
      if not network_deleted:  # Don't show 'Add Show' if deleted
        print(" Enter 'A' to Add Show")
        print(" Enter 'D' to delete network")
        print(" Enter show number to delete show")
        shows_loop(network)
      sub_choice = input("Enter your choice: ")
      if sub_choice in ("A", "a"):
        create_show(network, network.id) 
        # Code to add a show (call a separate function or implement logic here)
        #break  # Exit sub-menu after adding a show - CHANGE THIS TO CALL main_menu
      elif sub_choice in ("B", "b"):
        #break  # Exit sub-menu loop (back to main menu)
         return
      elif sub_choice in ("D", "d"):                
        #networks = [n for n in networks if n.id != network.id]  # Update the networks list 
        #loop through network shows and delete them first - otherwise the shows get stranded with no network - for show in network.shows
        for show in network.shows():
           show.delete()
        network.delete_network()
        network_deleted = True
        print("\n***************\n ")
        print(f"{network.name} network was successfully deleted")
      elif sub_choice not in ("A", "a", "B", "b", "D", "d"):
        try:
            show_index = int(sub_choice) - 1  # Adjust for 0-based indexing
            if 0 <= show_index < len(shows):
                delete_show(network, show_index)  # Pass network and show index
            else:
                print("Invalid show number. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number or a valid option.")
      else:
        print("Invalid choice. Please enter 1 or 2.")

  


   
