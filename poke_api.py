import requests
import image_lib
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    #pokemon = search_pokemon_entries('squirtle')
    #get_pokemon_names()
    download_pokemon_artwork('pikachu', r'c:\users\dell\desktop')
    #pass

def search_pokemon_entries(poke_entry):
    """Searches the PokeAPI for information on a Pokemon

    Args:
        poke_entry (str): The name or PokeDex number of a Pokemon

    Returns:
        dict: A dictionary with information on the Pokemon
    """
    # Clean the search term
    poke_entry = str(poke_entry).strip().lower()

    # Send a GET request for a pokemon that matches the name or ID
    print(f'Getting information for {poke_entry}...', end='')
    resp_msg = requests.get(POKE_API_URL + poke_entry)

    # Check whether the request was successful
    if resp_msg.ok:
        print('success')
        return resp_msg.json()
    else:
        print("failure")
        print(f"Response code: {resp_msg.status_code} ({resp_msg.reason})")
        print(f"Error: {resp_msg.text}")

def get_pokemon_names(offset=0, limit=100000):
    """Gets a list of all Pokemon names from the Pokemon API

    Args:
        offset (int, optional): The index of the first Pokemon to start from. Defaults to 0.
        limit (int, optional): The total amount of Pokemon names to get. Defaults to 100000.

    Returns:
        list: List of Pokemon names, if successful. None if unsuccessful.
    """
    # Define query parameters
    query_params = {
        "limit" : limit,
        "offset" : offset
    }

    # Send a GET request for pokemon names
    print(f'Getting list of Pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL, params=query_params)

    # Check whether the request was successful
    if resp_msg.ok:
        print('success')
        resp_dict = resp_msg.json()
        # Pull out the names from the response message
        pokemon_names = [p['name'] for p in resp_dict['results']]
        return pokemon_names
    else:
        print("failure")
        print(f"Response code: {resp_msg.status_code} ({resp_msg.reason})")
        print(f"Error: {resp_msg.text}")
        return

def download_pokemon_artwork(pokemon_name, folder_path):
    """Downloads the art for the Pokemon and saves it to the folder path

    Args:
        pokemon_name (str): Name of Pokemon to download artwork
        folder_path (str): Path of the folder to save artwork

    Returns:
        str: File Path of saved artwork, if successful. False if unsuccessful.
    """
    # Verify Pokemon info search was successful
    poke_info = search_pokemon_entries(pokemon_name)
    if poke_info is None:
        return False

    # Pull out the official artwork from the poke_info
    poke_image_url = poke_info['sprites']['other']['official-artwork']['front_default']

    # Download the official art and then check if successful
    image_data = image_lib.download_image(poke_image_url)
    if image_data is None:
        return False

    # Determine the path at which to save the image file
    image_ext = poke_image_url.split('.')[-1]
    file_name = f'{poke_info["name"]}.{image_ext}'
    file_path = os.path.join(folder_path, file_name)

    # Save downloaded image file to folder path
    if image_lib.save_image_file(image_data, file_path):
        return file_path
    
    return False

if __name__ == "__main__":
    main()