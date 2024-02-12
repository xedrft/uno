import os
import pandas as pd
import numpy as np

from src.game import real
import config as conf

def main():

    run = real(
        iterations = conf.params['iterations'],
        comment    = conf.params['logging']
    )

    result = pd.concat([
        pd.Series(run[0], name='winner'),
        pd.Series(run[1], name='games'),
        pd.Series(run[2], name='point_difference')
    ], axis = 1)

    result["win_rate"] = np.where(result["winner"]==conf.player_name_1,1,0)
    result["win_rate"] = result["win_rate"].cumsum()/(result.index+1)


    if not os.path.exists("assets"):
        os.makedirs("assets")

    result.to_csv("assets/results.csv", index=False)

    result['point_difference'] = pd.to_numeric(result['point_difference'], errors='coerce')
    total_point_difference = result['point_difference'].sum()

    with open("assets/results.csv", 'a') as f:
        f.write(f'\nTotal Point Difference,{total_point_difference}')

if __name__ == "__main__":
    main()

    import os
    import pandas as pd
    import numpy as np
    from multiprocessing import Pool, cpu_count

    from src.game import real
    import config as conf


    def simulate_game(iteration):
        return real(iterations=1, comment=conf.params['logging'])


    def main():
        iterations = conf.params['iterations']

        # Use multiprocessing Pool to parallelize simulations
        with Pool(cpu_count()) as pool:
            runs = pool.map(simulate_game, range(iterations))
        winners, games, point_differences = list(), list(), list()
        for i in runs:
            winners.append(i[0])
            games.append(i[1])
            point_differences.append(i[2])

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

        result['point_difference'] = pd.to_numeric(result['point_difference'], errors='coerce')
        total_point_difference = result['point_difference'].sum()

        with open("assets/results.csv", 'a') as f:
            f.write(f'\nTotal Point Difference,{total_point_difference}')


    if __name__ == "__main__":
        main()
