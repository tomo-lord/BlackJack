import pandas as pd
import random
import matplotlib.pyplot as plt
from blackjack_main_function import BJ_simulator

import pandas as pd
import numpy as np

def BJ_simulation_wrapper(
    trips: int,
    starting_bankroll: int,
    min_table_bet: int,
    games_per_trip: int,
    max_table_bet: int = 10000,
    shoe_size=8,
    games_per_deck=8,
    decision_engine='kelly_and_exceptions'
):
    """
    Simulates multiple Blackjack 'trips', each containing a certain number of games.

    Parameters
    ----------
    trips : int
        Number of trips (or series) to be simulated.
    starting_bankroll : int
        Initial bankroll for each trip.
    min_table_bet : int
        Minimum table bet.
    games_per_trip : int
        Number of games to be played per trip.
    max_table_bet : int, default=10000
        Maximum allowed table bet.
    shoe_size : int, default=8
        Number of decks in the shoe.
    games_per_deck : int, default=8
        Approximate number of games we aim to play per deck (for simulation logic)
    decision_engine: defines the decision engine of player.
        'basic' is neither adjusting bet sizes nor playing True Count exceptions
        'kelly' is adjusting the bet sizes but not playing True Count exceptions
        'kelly_and_exceptions' is both adjusting the bet sizes and playing True Count exceptions

    Returns
    -------
    metadata : pd.DataFrame
        Summary of each trip (total result, final bankroll, ruin statistics, etc.).
    df : pd.DataFrame
        Full record of all games played across all trips.
    """


    all_trips_df_list = []

    # Loop over the number of trips
    for i in range(trips):


        data = BJ_simulator(
            iterations=games_per_trip,
            bankroll=starting_bankroll,
            shoe_size=shoe_size,
            games_per_deck=games_per_deck,
            min_table_bet=min_table_bet,
            max_table_bet=max_table_bet,
            decision_engine=decision_engine
        )

        # Convert the dictionary to a DataFrame
        temp_df = pd.DataFrame(data)

        # Add columns to identify the trip and game number within that trip
        temp_df['series id'] = i
        temp_df['game number'] = range(1, len(temp_df) + 1)

        # Store this trip's DataFrame in the list
        all_trips_df_list.append(temp_df)

     # Concatenate all trips once at the end
    df = pd.concat(all_trips_df_list, ignore_index=True)

    # Now we can do post-processing:

    # 2) Determine if (and when) ruin occurs
    df['ruin'] = df['$account'] <= 0
    # 'ruin game' is the first game number within a series that triggered ruin
    df['ruin game'] = np.where(df['ruin'], df['game number'], np.nan)
    x=1
    # 3) Build a pivot table (or groupby) to get summary by 'series id'
    metadata = pd.pivot_table(
        df,
        values=['$result', '$account', 'ruin game'],
        index=['series id'],
        aggfunc={
            '$result': 'sum',
            '$account': 'last',
            'ruin game': lambda x: np.nan if x.isnull().all() else np.nanmin(x)
        }
    )

    # Rename some columns
    metadata.rename(
        columns={
            '$result': 'trip $ result',
            '$account': '$account'
        },
        inplace=True
    )

    # Move 'series id' out of the index into a column
    metadata.reset_index(inplace=True)

    # Average outcome per game in the trip
    metadata['average hand value'] = metadata['trip $ result'] / games_per_trip

    # Optionally define 'series length' if it makes sense in your model:
    metadata['series length'] = games_per_trip * games_per_deck * shoe_size

    # 4) If 'ruin game' is NaN, ruin did not occur => ruin=0; if not NaN => ruin=1
    try:
        metadata['ruin'] = np.where(metadata['ruin game'].isna(), 0, 1)
    except:
        pass

    # We can keep or drop 'series id' in final summary
    # metadata.drop(columns=['series id'], inplace=True)

    # Add 'starting bankroll' as a column (the same for all trips)
    metadata['starting bankroll'] = starting_bankroll

    # Reorder columns so that 'starting bankroll' is at the front
    # cols = list(metadata.columns)
    # cols.insert(0, cols.pop(cols.index('starting bankroll')))
    # metadata = metadata[cols]

    return metadata, df


if __name__ == '__main__':
    metadata, df = BJ_simulation_wrapper(
        trips = 10,
        starting_bankroll = 10000,
        min_table_bet=100,
        games_per_trip=1000,
        max_table_bet= 1000,
        shoe_size=8,
        games_per_deck=8)
    print(metadata)
    #print(df)