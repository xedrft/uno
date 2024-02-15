import time
import pandas as pd
import numpy as np
import os
from multiprocessing import Pool, cpu_count
from src.game import real
import config as conf


if conf.params["debugging"]:

    def main():

        run = real(
            iterations=1,
            comment=conf.params['debugging']
        )

        result = pd.concat([
            pd.Series(run[0], name='winner'),
            pd.Series(run[1], name='games'),
            pd.Series(run[2], name='point_difference')
        ], axis=1)

        result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
        result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)


        if not os.path.exists("assets"):
            os.makedirs("assets")

        result.to_csv("assets/results.csv", index=False)
    
    if __name__ == "__main__":
        main()


    
else:
    def simulate_game(iteration):
        return real(iterations=1, comment=conf.params['debugging'])


    def main():
        iterations = conf.params['iterations']

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
        for key in conf.skill:
            if conf.skill[key]:
                name.append("1")
            else:
                name.append("0")

        for key in conf.luck:
            if isinstance(conf.luck[key], bool) and conf.luck[key]:
                name.append("1")
            elif isinstance(conf.luck[key], dict) and conf.luck[key]["state"]:
                name.append(f"1-{conf.luck[key]["luck"]}")
            else:
                name.append("0")



        result.to_csv(f"assets/{"_".join(name)}.csv", index=False, mode='w')
        
    if __name__ == "__main__":
        main()
        for param in conf.skill:
            conf.skill[param] = True
            main()
            conf.skill[param] = False
        conf.luck["always_first"] = True
        main()
        conf.luck["always_first"] = False
        conf.luck["lucky_draws"]["state"] = True
        for value in [round(0.05 * i, 2) for i in range(1,11)]:
            conf.luck["lucky_draws"]["luck"] = value
            main()
        conf.luck["lucky_draws"]["state"] = False
        conf.luck["initial_cards"]["state"] = True 
        for value in range(1,8):
            conf.luck["initial_cards"]["luck"] = value
            main()
        conf.luck["initial_cards"] = False

