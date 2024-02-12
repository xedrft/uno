import os
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import time
from src.game import real
import config as conf


def simulate_game(iteration):
    return real(iterations=1, comment=conf.params['logging'])


def main():
    iterations = conf.params['iterations']

    timer_start = time.time()

    with Pool(cpu_count()) as pool:
        runs = pool.map(simulate_game, range(iterations))

    winners, games, point_differences, count = zip(*runs)
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
            f'\nTotal Point Difference: {total_point_difference}'
            f'\nPoint Difference Per Game: {total_point_difference / iterations}')


if __name__ == "__main__":
    main()
