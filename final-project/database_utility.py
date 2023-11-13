import requests
from cs50 import SQL
from helpers import DECORATED_COLLECTION_MAPPING, GRADE_MAPPING


reverse_decorated_collection_mapping = {value : key for key, value in DECORATED_COLLECTION_MAPPING.items()}
reverse_grade_mapping = {value: key for key, value in GRADE_MAPPING.items()}

db = SQL("sqlite:///final-project.db")

# If new warpaints, add them into war_paints list and run the insert_warpaints function.
war_paints = [
    "Park Pigmented", "Sax Waxed", "Yeti Coated", "Croc Dusted", "Macaw Masked", 
    "Piña Polished", "Anodized Aloha", "Bamboo Brushed", "Leopard Printed", 
    "Mannana Peeled", "Tiger Buffed", "Fire Glazed", "Bonk Varnished", 
    "Dream Piped", "Freedom Wrapped", "Bank Rolled", "Clover Camo'd", 
    "Kill Covered", "Pizza Polished", "Bloom Buffed", "Cardboard Boxed", 
    "Merc Stained", "Quack Canvassed", "Star Crossed", "Carpet Bomber Mk.II", 
    "Woodland Warrior Mk.II", "Wrapped Reviver Mk.II", "Forest Fire Mk.II", 
    "Night Owl Mk.II", "Woodsy Widowmaker Mk.II", "Autumn Mk.II", 
    "Plaid Potshotter Mk.II", "Civil Servant Mk.II", "Civic Duty Mk.II", 
    "Bovine Blazemaker Mk.II", "Dead Reckoner Mk.II", "Backwoods Boomstick Mk.II", 
    "Masked Mender Mk.II", "Iron Wood Mk.II", "Macabre Web Mk.II", 
    "Nutcracker Mk.II", "Smalltown Bringdown Mk.II", "Dragon Slayer", 
    "Smissmas Sweater", "Miami Element", "Jazzy", "Mosaic", 
    "Cosmic Calamity", "Hana", "Neo Tokyo", "Uranium", 
    "Alien Tech", "Bomber Soul", "Cabin Fevered", "Damascus and Mahogany", 
    "Dovetailed", "Geometrical Teams", "Hazard Warning", "Polar Surprise", 
    "Electroshocked", "Ghost Town", "Tumor Toasted", "Calavera Canvas", 
    "Spectral Shimmered", "Skull Study", "Haunted Ghosts", "Horror Holiday", 
    "Spirit of Halloween", "Totally Boned", "Winterland Wrapped", "Smissmas Camo", 
    "Smissmas Village", "Frost Ornamented", "Sleighin' Style", "Snow Covered", 
    "Alpine", "Gift Wrapped", "Igloo", "Seriously Snowed", 
    "Spectrum Splattered", "Pumpkin Pied", "Mummified Mimic", "Helldriver", 
    "Sweet Toothed", "Crawlspace Critters", "Raving Dead", "Spider's Cluster", 
    "Candy Coated", "Portal Plastered", "Death Deluxe", "Eyestalker", 
    "Gourdy Green", "Spider Season", "Organ-ically Hellraised", 
    "Starlight Serenity", "Saccharine Striped", "Frosty Delivery", "Cookie Fortress", 
    "Frozen Aurora", "Elfin Enamel", "Smissmas Spycrabs", "Gingerbread Winner", 
    "Peppermint Swirl", "Gifting Mann's Wrapping Paper", "Glacial Glazed", 
    "Snow Globalization", "Snowflake Swirled", "Misfortunate", "Broken Bones", 
    "Party Phantoms", "Necromanced", "Neon-ween", "Polter-Guised", 
    "Swashbuckled", "Kiln and Conquer", "Potent Poison", "Sarsaparilla Sprayed", 
    "Searing Souls", "Simple Spirits", "Skull Cracked", "Sacred Slayer", "Bonzo Gnawed", 
    "Ghoul Blaster", "Metalized Soul", "Pumpkin Plastered", "Chilly Autumn", 
    "Sunriser", "Health and Hell", "Hypergon", 
    "Cream Corned", "Sky Stallion", "Business Class", "Deadly Dragon", 
    "Mechanized Monster", "Steel Brushed", "Warborn", "Bomb Carrier", 
    "Pacific Peacemaker", "Secretly Serviced", "Team Serviced"
]

weapon_skins_list = [
    "Airwolf", "Spruce Deuce", "American Pastoral", "Antique Annihilator", "Aqua Marine", "Autumn", "Backcountry Blaster", "Backwoods Boomstick",
    "Balloonicorn", "Barn Burner", "Black Dahlia", "Blue Mew", "Bogtrotter", "Boneyard", "Bovine Blazemaker",
    "Brain Candy", "Brick House", "Butcher Bird", "Carpet Bomber", "Civic Duty", "Civil Servant", "Citizen Pain",
    "Coffin Nail", "Corsair", "Country Crusher", "Current Event", "Dead Reckoner", "Dressed to Kill", "Earth, Sky and Fire",
    "Flash Fryer", "Flower Power", "Forest Fire", "Hickory Hole-Puncher", "High Roller's", "Homemade Heater", "Iron Wood",
    "King of the Jungle", "Killer Bee", "Lumber From Down Under", "Low Profile", "Macabre Web", "Masked Mender", "Mister Cuddles",
    "Night Owl", "Night Terror", "Nutcracker", "Old Country", "Plaid Potshotter", "Psychedelic Slugger",
    "Purple Range", "Rainbow", "Red Bear", "Red Rock Roscoe", "Reclaimed Reanimator", "Rooftop Wrangler", "Rustic Ruiner",
    "Sand Cannon", "Sandstone Special", "Sudden Flurry", "Sweet Dream", "Tartan Torpedo", "Team Sprayer", "Thunderbolt",
    "Top Shelf", "Torqued to Hell", "Treadplate Tormenter", "Turbocharged", "War Room", "Warhawk", "Wildwood", "Woodland Warrior",
    "Woodsy Widowmaker", "Liquid Asset", "Shell Shocker", "Pink Elephant", "Spark of Life", "Lightning Rod", "Local Hero", "Mayor Revolver", "Smalltown Bringdown", 
    "Shot in the Dark", "Blasted Bombardier", "Wrapped Reviver", "Pumpkin Patch", "Stabbed to Hell", "Shot to Hell", "Blitzkrieg"
]

# function for inserting warpaints and skins into databases, with name, image, wear, collection, never used while app is running
def insert_warpaints(warpaints):
    for warpaint in warpaints:
        name = warpaint
        if db.execute("SELECT * FROM warpaints WHERE name = ?", name) != []:
            print(name, 'is already in database.')
        else:
            api_url = f'https://api.steamapis.com/image/item/440/{name}%20War%20Paint%20(Factory%20New)'
            response = requests.get(api_url)

            if response.status_code == 200:
                img_url = response.url
            else:
                print('Failed to fetch the image', 404, name)

            print(f'Grade for {name}: 1=elite, 2=assassin, 3=commando, 4=mercenary, 5=freelance, 6=civilian')
            
            while True:
                grade_input = int(input('grade num: '))
                if grade_input in reverse_grade_mapping:
                    grade = reverse_grade_mapping[grade_input]
                    confirmation = input(f'is {grade} correct for {name}? (y/n)')
                    if confirmation == 'y':
                        print(name, img_url, grade)
                        db.execute("INSERT INTO warpaints (name, image_url, grade) VALUES (?, ?, ?)", name, img_url, grade)
                        break
                    else:
                        print('please select correct grade')
                else:
                    print('please select accurate grade number')


def insert_decorated_weapons(skins):
    for skin in skins:
        while True:
            name = skin
            weapon = input(f'input weapon that has {name} as a skin: ')
            if weapon == 'break':
                break
            if db.execute("SELECT * FROM decorated_weapons WHERE skin = ? AND weapon = ?", name, weapon) != []:
                print(name, weapon, 'is already in database.')
            else:
                api_url = f"https://api.steamapis.com/image/item/440/{name}%20{weapon}%20(Factory%20New)"
                response = requests.get(api_url)

                if response.status_code == 200:
                    img_url = response.url
                    print("img sucsess")
                else:
                    print('Failed to fetch the image', 404, name)

                print(f'Grade for {name} {weapon}: 1=elite, 2=assassin, 3=commando, 4=mercenary, 5=freelance, 6=civilian')
                
                while True:
                    grade_input = int(input('grade num: '))
                    if grade_input in reverse_grade_mapping:
                        grade = reverse_grade_mapping[grade_input]
                        confirmation = input(f'is {grade} correct for {name} {weapon}? (y/n)')
                        if confirmation == 'y':
                            while True:
                                print(f"Collection for {name} {weapon}:")
                                for key, value in reverse_decorated_collection_mapping.items():
                                    print(f"{key}={value}")
                                collection_input = int(input('collection num: '))
                                if collection_input in reverse_decorated_collection_mapping:
                                    collection = reverse_decorated_collection_mapping[collection_input]
                                    confirmation_collection = input(f'is {collection} correct for {name} {weapon}? (y/n)')
                                    if confirmation_collection == 'y':
                                        db.execute("INSERT INTO decorated_weapons (skin, weapon, image_url, grade, collection) VALUES (?, ?, ?, ?, ?)", name, weapon, img_url, grade, collection)
                                        
                                        break
                                    else:
                                        print('please select correct collection')
                                else:
                                    print('please select accurate collection number')
                            break
                        else:
                            print('please select correct grade')
                    else:
                        print('please select accurate grade number')
            more_weapon_skins = input(f"is there more weapons with {name} as a skin? (y/n)")
            if more_weapon_skins != 'y':
                break

#insert_warpaints(war_paints)
#insert_decorated_weapons(weapon_skins_list)