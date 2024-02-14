import time
import pandas as pd
import numpy as np
import os
from multiprocessing import Pool, cpu_count
from src.game import real
import config as conf

if conf.params["debugging"]:git

    def main():

        run = real(
            iterations=1,
            comment=conf.params['debugging']
        )

        result = pd.concat([
            pd.Series(run[0], name='winner'),
            pd.Series(run[1], name='games'),
            pd.Series(run[2], name='point_difference')  # Corrected column name
        ], axis=1)

        result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
        result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)

        total_point_difference = result['point_difference'].sum()

        if not os.path.exists("assets"):
            os.makedirs("assets")

        result.to_csv("assets/results.csv", index=False)

        with open("assets/results.csv", 'a') as f:
            f.write(
                f'\nTotal Point Difference, {total_point_difference}'
                f'\nPoint Difference Per Game, {total_point_difference}')


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
            'point_difference': point_differences
        })

        result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
        result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)

        if not os.path.exists("assets"):
            os.makedirs("assets")

        result.to_csv("assets/results.csv", index=False, mode='w')

        total_point_difference = result['point_difference'].sum()

        with open("assets/results.csv", 'a') as f:
            f.write(
                f'\nTotal Point Difference, {total_point_difference}'
                f'\nPoint Difference Per Game, {total_point_difference / iterations}'
                f'\nChance of Playable Card, {sum(playable)/sum(total)}')


    if __name__ == "__main__":
        main()
