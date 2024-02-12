params = {
    "iterations": 10000,
    "debugging": False, # Plays only one game with logging when True
}

player_name_1 = "Skill"
player_name_2 = "Luck"
skill = {
    "wild_color": False,  # Picks the color the player has most of (when has wild/plus card)
    "highest_card": False  # Picks the highest valued card to play
}

luck = {
    "always_first": False,  # Always goes first
    "lucky_draws": # Whether the player automatically draws a playable card (based on the open card)
        {
            "state": True, # Off/On
            "luck": 0.2 # Percent of times this person will automatically draw a playable card
        }
}
