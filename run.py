import time
import pandas as pd
import numpy as np
import os
from multiprocessing import Pool, cpu_count
from src.game import real
import config as conf
import json

def alter_skill(value, key):
    with open("config.json", "r+") as config:
        content = json.load(config)
        content["skill"][key] = value
        config.seek(0)
        json.dump(content, config, indent=4)
        config.truncate()

def alter_luck(value, key):
    with open("config.json", "r+") as config:
        content = json.load(config)
        content["luck"][key] = value
        config.seek(0)
        json.dump(content, config, indent=4)
        config.truncate()

def alteralter(value, key, key1):
    with open("config.json", "r+") as config:
        content = json.load(config)
        content["luck"][key][key1] = value
        config.seek(0)
        json.dump(content, config, indent=4)
        config.truncate()


with open('config.json', 'r') as file:
    data = json.load(file)

debugging = data["params"]["debugging"]
iterations = data["params"]["iterations"]

# if debugging:

#     def main():

#         run = real(
#             iterations=1,
#             comment=debugging
#         )

#         result = pd.concat([
#             pd.Series(run[0], name='winner'),
#             pd.Series(run[1], name='games'),
#             pd.Series(run[2], name='point_difference')
#         ], axis=1)

#         result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
#         result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)


#         if not os.path.exists("assets"):
#             os.makedirs("assets")

#         result.to_csv("assets/results.csv", index=False)
    
#     if __name__ == "__main__":
#         main()


    
# else:
def simulate_game(iteration):
    return real(iterations=1, comment=debugging)


def main():
    with open('config.json', 'r') as file:
        data = json.load(file)

    iterations = data["params"]["iterations"]
    skill = data["skill"]
    luck = data["luck"]

    timer_start = time.time()

    with Pool(cpu_count()) as pool:
        runs = pool.map(simulate_game, range(iterations))

    winners, games, point_differences, count, playable, total = zip(*runs)
    count = sum(count)

    timer_end = time.time()
    timer_dur = timer_end - timer_start
    print(
        f'Execution lasted {round(timer_dur / 60, 2)} minutes ({round(count / timer_dur, 2)} games per second, '
        f'{round(iterations / timer_dur, 2)} iterations per second)')

    result = pd.DataFrame({
        'winner': winners,
        'games': games,
        'point_difference': point_differences,
        'playable_draws' : playable,
        'total_draws' : total
    })

    result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
    result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)

    result["points_difference_per_game"] = pd.Series([sum(result["point_difference"][:i + 1]) / (i + 1) for i in result.index])

    result["chance_of_playable_draw"] = pd.Series([sum(result["playable_draws"][:i + 1]) / sum(result["total_draws"][:i + 1]) for i in result.index])

    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    

    name = []
    for key in skill:
        if skill[key]:
            name.append("1")
        else:
            name.append("0")

    for key in luck:
        if isinstance(luck[key], int) and luck[key]:
            name.append("1")
        elif isinstance(luck[key], dict) and luck[key]["state"]:
            name.append(f"1-{luck[key]["luck"]}")
        else:
            name.append("0")



    result.to_csv(f"assets/{"_".join(name)}.csv", index=False, mode='w')
    
if __name__ == "__main__":
    main()
    for param in conf.skill:
        alter_skill(1, param)
        main()
        alter_skill(0, param)
    alter_luck(1, "always_first")
    main()
    alter_luck(0, "always_first")
    alteralter(1, "lucky_draws", "state")
    for value in [round(0.05 * i, 2) for i in range(1,11)]:
        alteralter(value, "lucky_draws", "luck")
        main()
    alteralter(0, "lucky_draws", "state")
    alteralter(1, "initial_cards", "state") 
    for value in range(1,8):
        alteralter(value, "initial_cards", "luck") 
        main()
    alteralter(0, "initial_cards", "state") 

