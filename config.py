params = {
    "iterations": 10000,
    "debugging": False,  # Plays only one game with logging when True
}

player_name_1 = "Skill"
player_name_2 = "Luck"
skill = {
    "wild_color": False,  # Picks the color the player has most of (when has wild/plus 4 card)
    "highest_card": False,  # Picks the highest valued card to play
    "unfavor_wild": False  # If another card besides wild playable, plays it
}

luck = {
    "always_first": False,  # Always goes first
    "lucky_draws":  # Draws a playable card (based on the open card)
    {
            "state": False,  # Off/On
            "luck": 0.2  # Probability this person will automatically draw a playable card
        }
}
