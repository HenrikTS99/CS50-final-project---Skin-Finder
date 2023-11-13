from cs50 import SQL
from flask import render_template

db = SQL("sqlite:///final-project.db")

# Names for all the links in quicksearch link table. The categories is for setting the correct css color for the diffrent names.
LINK_TABLE_NAMES = [
    {'name': 'All', 'category': 'decorated'},
    {'name': 'Factory New', 'category': 'decorated'},
    {'name': 'Minimal Wear', 'category': 'decorated'},
    {'name': 'Field Tested', 'category': 'decorated'},
    {'name': 'Well Worn', 'category': 'decorated'},
    {'name': 'Battle Scarred', 'category': 'decorated'},
    {'name': 'All Strange', 'category': 'strange'},
    {'name': 'Strange Factory New', 'category': 'strange'},
    {'name': 'Strange Minimal Wear', 'category': 'strange'},
    {'name': 'Strange Field Tested', 'category': 'strange'},
    {'name': 'Strange Well Worn', 'category': 'strange'},
    {'name': 'Strange Battle Scarred', 'category': 'strange'}
    ]
    
TF2_WEAPONS = sorted([ # Weapons that can have warpaints applied to them.
    "Air Strike", "Amputator", "Back Scratcher", "Bazaar Bargain",
    "Black Box", "Brass Beast", "Claidheamh Mòr", "Crusader's Crossbow",
    "Degreaser", "Detonator", "Disciplinary Action", "Dragon's Fury",
    "Family Business", "Flame Thrower", "Grenade Launcher", "Holy Mackerel",
    "Iron Bomber", "Jag", "Knife", "Loch-n-Load", "Loose Cannon",
    "Medi Gun", "Minigun", "Panic Attack", "Persian Persuader", "Powerjack",
    "Rescue Ranger", "Revolver", "Scotsman's Skullcutter", "Scorch Shot",
    "Shahanshah", "Shortstop", "Shotgun", "SMG", "Sniper Rifle", "Soda Popper",
    "Stickybomb Launcher", "Tomislav", "Ubersaw", "Winger", "Scattergun", "Rocket Launcher", "Wrench"
])


WARPAINTS_LIST = db.execute("SELECT name FROM warpaints") # returns a list of dicts (name:value)
WARPAINTS_LIST = sorted([value for dict in WARPAINTS_LIST for value in dict.values()])

WEAPON_SKINS_LIST = db.execute("SELECT skin, weapon FROM decorated_weapons")
WEAPON_SKINS_LIST = sorted(WEAPON_SKINS_LIST, key=lambda x: x['skin'])

WEAR_MAPPING = {'FactoryNew': 1, 'MinimalWear' : 2, 'FieldTested' : 3, 'WellWorn' : 4, 'BattleScared' : 5}
AVAILABLE_WEAR_TIERS = list(WEAR_MAPPING)

GRADE_MAPPING = {'Elite': 1, 'Assassin': 2, 'Commando': 3, 'Mercenary': 4, 'Freelance': 5, 'Civilian': 6}
AVAILABLE_GRADE_TIERS = list(GRADE_MAPPING)

# collection mapping nums is for when adding into database
DECORATED_COLLECTION_MAPPING = {'The Teufort Collection': 1, 'The Craftsmann Collection': 2, 'The Concealed Killer Collection': 3, 'The Powerhouse Collection': 4,
 'The Harvest Collection': 5, "The Gentlemanne's Collection": 6, 'The Pyroland Collection': 7, 'The Warbird Collection': 8}

WARPAINT_COLLECTION_MAPPING = {
    "Jungle Jackpot Collection": 1,
    "Infernal Reward Collection": 2,
    "Decorated War Hero Collection": 3,
    "Contract Campaigner Collection": 4,
    "Saxton Select Collection": 5,
    "Mann Co. Events Collection": 6,
    "Winter 2017 Collection": 7,
    "Scream Fortress X Collection": 8,
    "Winter 2019 Collection": 9,
    "Scream Fortress XII Collection": 10,
    "Winter 2020 Collection": 11,
    "Scream Fortress XIII Collection": 12,
    "Scream Fortress XIV Collection": 13,
    "Summer 2023 Collection": 14
}

# creates a marketplace.tf link according to the search parameters. 
# Args default to '' incase a arg is not included in function call. Cant default to 'None' because that can go into the search params.
def create_mp_link(warpaint='', killstreak='', weapon='', wear_tiers='', quality_tags=''):
    wear_filter, quality_filter,  = '', ''
    
    # change blank space with '+' for proper URL encoding.
    warpaint, killstreak, weapon = process_variables(warpaint, killstreak, weapon)

    if len(wear_tiers) == 1:
        wear_filter = f'&swear={WEAR_MAPPING[wear_tiers[0]]}'

    if 'rarity4' in quality_tags:
        quality_filter = f'&squality=5'
    
    if 'strange' in quality_tags:
        quality_filter += f'&sstrange=1'

    # A URL for marketplace.tf based on the provided parameters.
    link = f'https://marketplace.tf/browse/tf2?sterm={killstreak}+{warpaint}+{weapon}{wear_filter}{quality_filter}&ssortfield=min_price&ssortdir=1'
    return link


# creates a backpack.tf link according to the search parameters. 
# Args default to '' incase a arg is not included in function call. Cant default to 'None' because that can go into the search params.
def create_bp_link(warpaint='', killstreak='', weapon='', wear_tiers='', quality_tags=''):
    # For converting the search grade to the correct filter in backpack.tf searches.
    killstreak_mapping = {'Killstreak': 1, 'Specialized Killstreak' : 2, 'Professional Killstreak' : 3}
    quality_mapping = {'strange': 11, 'rarity4' : 5}
    warpaint_filter, killstreak_filter, weapon_filter, wear_filter, quality_filter,  = '', '', '', '', ''

    #create search filters
    if warpaint:
        warpaint = warpaint.replace(' ', '+')
        warpaint_filter = f'&texture_name={warpaint}'
    
    if killstreak in killstreak_mapping:
        killstreak_filter = f'&killstreak_tier={killstreak_mapping[killstreak]}'
    
    if weapon:
        weapon = weapon.replace(' ', '+')
        weapon_filter = f'&item={weapon}'

    for idx, wear in enumerate(wear_tiers):
        if wear in WEAR_MAPPING:
            if idx == 0:
                wear_filter = f'&wear_tier={WEAR_MAPPING[wear]}'
            else:
                wear_filter +=f'%2C{WEAR_MAPPING[wear]}'

    for idx, quality in enumerate(quality_tags):
        if quality in quality_mapping:
            if idx == 0:
                quality_filter = f'&quality={quality_mapping[quality]}'
            else:
                quality_filter +=f'%2C{quality_mapping[quality]}'
    
    # A URL for backpack.tf based on the provided parameters.
    link = f'https://backpack.tf/classifieds?{weapon_filter}{killstreak_filter}{warpaint_filter}{wear_filter}{quality_filter}'
    return link    


# Creates a steam community market link according to the search parameters. 
# Args default to '' incase a arg is not included in function call. Cant default to 'None' because that can go into the search params.
def create_scm_link(warpaint='', search_text='', description='', killstreak='', weapon='', wear_tiers='', grade_tiers='', quality_tags=''):
    # For converting the search grade to the correct filter in steam community market searches.
    grade_rarity_mapping = {'Elite': 'Ancient', 'Assassin': 'Legendary', 'Commando': 'Mythical', 'Mercenary': 'Rare', 'Freelance': 'Uncommon', 'Civilian': 'Common'}
    tier_filter, quality_filter, grade_filter = '', '', ''

    # change blank space with '+' for proper URL encoding.
    warpaint, search_text, weapon, killstreak = process_variables(warpaint, search_text, weapon, killstreak)

    #create search filters
    if description:
        desc = '&descriptions=1'
    else:
        desc = ''
    if quality_tags:
        for tag in quality_tags:
            quality_filter += f'&category_440_Quality%5B%5D=tag_{tag}'
    if grade_tiers:
        for grade in grade_tiers:
            grade_filter += f'&category_440_Rarity%5B%5D=tag_Rarity_{grade_rarity_mapping[grade]}'
    if wear_tiers:
        for wear in wear_tiers:
            tier_filter += f'&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_{wear}'

    # A URL for the Steam Community Market search based on the provided parameters.
    link = (f"https://steamcommunity.com/market/search?q={warpaint}+{search_text}+{killstreak}+{weapon}{desc}"
        f"&category_440_Collection[0]=any&category_440_Type[0]=any"
        f"{tier_filter}{grade_filter}{quality_filter}#p1_price_asc")
    return link


# Changes blank space with '+' for proper URL encoding to all variables passed to function. Returns a list with all the processed args
def process_variables(*args):
    processed_args = []
    for arg in args:
        if arg:
            processed_arg = arg.replace(' ', '+')
        else:
            processed_arg = ''
        processed_args.append(processed_arg)

    return processed_args


# Get skin texture, skin data of that texture and skin type. Weapon type if skin type is a weapon skin.
def get_skin_data(weapon_skin, warpaint, current_weapon):
    weapon = current_weapon

    if weapon_skin:
        skin_type = 'decorated weapon'
        weapon_skin_parts = weapon_skin.split('|')

        if len(weapon_skin_parts) != 2:
            return render_template("error.html", search=weapon_skin)

        skin_texture, weapon = weapon_skin_parts
        skin_data = db.execute("SELECT * FROM decorated_weapons WHERE skin = ? AND weapon = ?", skin_texture, weapon)
    elif warpaint:
        skin_type = 'warpaint'
        skin_texture = warpaint
        skin_data = db.execute("SELECT * FROM warpaints WHERE name = ?", warpaint)
    if not (weapon_skin or warpaint):
        skin_texture = None
        skin_data = None
        skin_type = None
        
    if skin_data:
        skin_data=skin_data[0]

    return skin_type, skin_texture, skin_data, weapon


# creates 12 links for each of the 3 sites. links created are for every wear tier + any wear, and the same links in strange. for specific weapon skins/warpaints
def create_quicksearch_links(warpaint, weapon=''):
    scm_links, bp_links, mp_links = [], [], []

    QUALITY_TAG_NONE = ''
    QUALITY_TAG_STRANGE = 'strange'
    # Loops trough twice, second time adding a strange filter to the links.
    for quality_tag in [QUALITY_TAG_NONE, QUALITY_TAG_STRANGE]:

        scm_links.append(create_scm_link(warpaint=warpaint, weapon=weapon, wear_tiers=AVAILABLE_WEAR_TIERS, quality_tags=[quality_tag]))
        bp_links.append(create_bp_link(warpaint=warpaint, weapon=weapon, wear_tiers=AVAILABLE_WEAR_TIERS, quality_tags=[quality_tag]))
        mp_links.append(create_mp_link(warpaint=warpaint, weapon=weapon, wear_tiers=AVAILABLE_WEAR_TIERS, quality_tags=[quality_tag]))

        for wear in AVAILABLE_WEAR_TIERS:
            scm_links.append(create_scm_link(warpaint=warpaint, weapon=weapon, wear_tiers=[wear], quality_tags=[quality_tag]))
            bp_links.append(create_bp_link(warpaint=warpaint, weapon=weapon, wear_tiers=[wear], quality_tags=[quality_tag]))
            mp_links.append(create_mp_link(warpaint=warpaint, weapon=weapon, wear_tiers=[wear], quality_tags=[quality_tag]))
    
    #creates a dict where each key is a list of all the links needed for that site, in correct order.
    link_dict = {'scm_links' : scm_links, 'bp_links' : bp_links, 'mp_links' : mp_links}
    return link_dict


# creates killstreak kit link if weapon and killstreak is selected in search form.
def create_kit_link(weapon, killstreak):
    if weapon and killstreak:
        killstreak = killstreak.replace(' ', '%20')
        weapon = weapon.replace(' ', '%20')
        return f'https://steamcommunity.com/market/listings/440/{killstreak}%20{weapon}%20Kit'
    else:
        return None
    

# creates a dict where each key is a collection name, and the corresponding value is a list of items belonging to that collection, sorted by grade.
def create_collection_dict(table, collection_mapping):
    collection_dict = {}
    for collection in collection_mapping:
        collection_dict[collection] = db.execute("SELECT * FROM ? WHERE collection = ?", table, collection)
    for key, value in collection_dict.items():
        collection_dict[key] = sorted(value, key=lambda x: GRADE_MAPPING.get(x['grade'], float('inf')))
    return collection_dict