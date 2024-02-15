params = {
    "iterations": 100,
    "debugging": False,  # Plays only one game with logs when True
}

player_name_1 = "Skill"
player_name_2 = "Luck"

# These apply to the skill player only
skill = {
    "wild_color": False,  # Picks the color the player has most of (when has wild/plus 4 card)
    "highest_card": False,  # Picks the highest valued card to play
    "disfavor_wild": False,  # If another card besides wild playable, plays it
    "skip_chain": False,  # If one reverse/skip played, keep playing them
    "plus_uno" : False #  Whenever you are able to change the color, change the color
}

# These apply to the luck player only
luck = {
    "always_first": False,  # Always goes first
    "lucky_draws":  # Draws a playable card (based on the open card)
    {
            "state": False,  # Off/On
            "luck": 0.2  # Probability this person will automatically draw a playable card
        },
    "initial_cards": # What cards you start with (lucky_draws does not apply to starting cards)
    {
        "state": False,  # Off/On
        "luck" : 3  # How many out of 7 cards will automatically be an action card
        }
}
sup = [0,1]

