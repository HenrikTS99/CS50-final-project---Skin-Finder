from cs50 import SQL
from flask import Flask, redirect, render_template, request

from helpers import (create_mp_link, create_bp_link, create_scm_link, create_kit_link, create_collection_dict, 
    create_quicksearch_links, get_skin_data, LINK_TABLE_NAMES, AVAILABLE_WEAR_TIERS, 
    AVAILABLE_GRADE_TIERS, DECORATED_COLLECTION_MAPPING, GRADE_MAPPING, WARPAINT_COLLECTION_MAPPING,
    WARPAINTS_LIST, WEAPON_SKINS_LIST, TF2_WEAPONS
    )

# configure app
app = Flask(__name__)

# configure cs50 library to use SQlite
db = SQL("sqlite:///final-project.db")


@app.route("/")
def index():
    return redirect("/search")


@app.route("/search")
def search():
    return render_template("search.html", warpaints=WARPAINTS_LIST, weapon_skins=WEAPON_SKINS_LIST, weapons=TF2_WEAPONS)


# Grid of all tf2 decorated weapons. Sort after grade or collection.
@app.route("/decorated_weapons")
def display_decorated_weapons():
    decorated_weapons = db.execute("SELECT * FROM decorated_weapons") # declare variable outside function?
    decorated_weapons = sorted(decorated_weapons, key=lambda x: GRADE_MAPPING.get(x['grade']))

    collection_dict = create_collection_dict("decorated_weapons", DECORATED_COLLECTION_MAPPING) # function arguments: table, collection
    page_title = 'decorated Weapons'
    return render_template("all_skins_overview.html", skins=decorated_weapons, collection_dict=collection_dict, page_title = page_title)


# If only a specific decorated weapon skin is selected in URL, show only weapons with those skins. Can only be accessed trough changing URL.
@app.route("/decorated_weapons/<skin>")
def display_decorated_weapons_skins(skin):
    decorated_weapons = db.execute("SELECT * FROM decorated_weapons WHERE skin = ?", skin)
    # if nothing found in database
    if decorated_weapons == []:
        return render_template("error.html", search=skin)

    collection_dict = create_collection_dict("decorated_weapons", DECORATED_COLLECTION_MAPPING)
    
    return render_template("all_decorated_weapons.html", decorated_weapons=decorated_weapons, collection_dict=collection_dict)


# Info/showcase for a speficic decorated weapon. Include links for quickly searching through that weapon on 3 diffrent sites, with 12 diffrent preset filters.
@app.route("/decorated_weapons/<skin>/<weapon>")
def decorated_weapon_info(skin, weapon):
    decorated_weapon_dict = db.execute("SELECT * FROM decorated_weapons WHERE skin = ? AND weapon = ?", skin, weapon)
    # if nothing found in database
    if decorated_weapon_dict == []:
        return render_template("error.html", search=skin+' '+weapon)

    decorated_weapon_dict = decorated_weapon_dict[0]
    link_dict = create_quicksearch_links(decorated_weapon_dict['skin'], decorated_weapon_dict['weapon'])

    return render_template("warpaintInfo.html", warpaint=decorated_weapon_dict, scm_links=link_dict['scm_links'], 
        bp_links=link_dict['bp_links'], mp_links=link_dict['mp_links'], table_names=LINK_TABLE_NAMES, type='decorated weapon')


# Grid of all tf2 warpaints. Sort after grade or collection.
@app.route("/warpaint")
def display_warpaints():
    warpaints = db.execute("SELECT * FROM warpaints")  # declare variable outside function?

    collection_dict = create_collection_dict("warpaints", WARPAINT_COLLECTION_MAPPING)
    warpaints = sorted(warpaints, key=lambda x: GRADE_MAPPING.get(x['grade']))
    page_title = 'Warpaints'
    return render_template("all_skins_overview.html", skins=warpaints, collection_dict = collection_dict, page_title = page_title)


# Info/showcase for a speficic warpaint. Include links for quickly searching through that warpaint on 3 diffrent sites, with 12 diffrent preset filters.
@app.route("/warpaint/<warpaintName>")
def warpaint(warpaintName):
    warpaint_dict = db.execute("SELECT * FROM warpaints WHERE name = ?", warpaintName)
    # if nothing found in database
    if warpaint_dict == []:
        return render_template("error.html", search=warpaintName)

    warpaint_dict=warpaint_dict[0]
    link_dict = create_quicksearch_links(warpaint_dict['name'])

    return render_template("warpaintInfo.html", warpaint=warpaint_dict, scm_links=link_dict['scm_links'], 
        bp_links=link_dict['bp_links'], mp_links=link_dict['mp_links'], table_names=LINK_TABLE_NAMES, type='warpaint')


#handle the search made in the search form
@app.route("/result")
def result():
    weapon_skin = request.args.get("weapon_skin")
    warpaint = request.args.get("warpaint")
    search_text = request.args.get("search_text")
    killstreak = request.args.get("killstreak")
    weapon = request.args.get("weapon")
    print(weapon)
    description = request.args.get("description")

    # Check if a warpaint or skin is selected
    skin_type, skin_texture, warpaint_dict, weapon = get_skin_data(weapon_skin, warpaint, weapon)
    if warpaint_dict == []:
        return render_template("error.html", search=skin_texture)
    print(weapon)

    # Create lists for wear tiers, grade tiers and quality tags
    wear_tiers = [wear for wear in AVAILABLE_WEAR_TIERS if request.args.get(wear)]
    grade_tiers = [grade for grade in AVAILABLE_GRADE_TIERS if request.args.get(grade)]
    quality_tags = [tag for tag in ["strange", "rarity4"] if request.args.get(tag)]

    # Generate links that fit the search made
    scm_link = create_scm_link(skin_texture, search_text, description, killstreak, weapon, wear_tiers, grade_tiers, quality_tags)
    bp_link = create_bp_link(skin_texture, killstreak, weapon, wear_tiers, quality_tags)
    mp_link = create_mp_link(skin_texture, killstreak, weapon, wear_tiers, quality_tags)

    # Creates killstreak kit link if weapon and killstreak is selected in search form. Returns None if not.
    killstreak_kit_link = create_kit_link(weapon, killstreak)

    return render_template("searchResult.html", grade_tiers=grade_tiers, wear_tiers=wear_tiers, 
        bp_link=bp_link, mp_link=mp_link, scm_link=scm_link, kit_link=killstreak_kit_link, 
        quality_tags=quality_tags, warpaint_dict=warpaint_dict, type=skin_type,
        available_grade_tiers=AVAILABLE_GRADE_TIERS, killstreak=killstreak, weapon=weapon,
        warpaint_list=WARPAINTS_LIST, weapon_skin_list=WEAPON_SKINS_LIST, weapons=TF2_WEAPONS)