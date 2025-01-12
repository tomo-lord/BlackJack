from multiprocessing import Pool
import pandas as pd
from blackjack_main_function import BJ_simulator
import os


def simulate_single_trip(args):
    trip_id, starting_bankroll, min_table_bet, games_per_trip, max_table_bet, shoe_size, games_per_deck, decision_engine = args
    data = BJ_simulator(
        iterations=games_per_trip,
        bankroll=starting_bankroll,
        shoe_size=shoe_size,
        games_per_deck=games_per_deck,
        min_table_bet=min_table_bet,
        max_table_bet=max_table_bet,
        decision_engine=decision_engine,
    )
    temp_df = pd.DataFrame(data)
    temp_df["series id"] = trip_id
    temp_df["game number"] = range(1, len(temp_df) + 1)
    return temp_df


def BJ_simulation_wrapper_parallel(
    trips: int,
    starting_bankroll: int,
    min_table_bet: int,
    games_per_trip: int,
    max_table_bet: int,
    shoe_size=8,
    games_per_deck=8,
    decision_engine="kelly_and_exceptions",
    processes=4,
):
    """multiprocess blackjack simulation."""

    args = [
        (i, starting_bankroll, min_table_bet, games_per_trip, max_table_bet, shoe_size, games_per_deck, decision_engine)
        for i in range(trips)
    ]

    # multiprocesing launch
    with Pool(processes=processes) as pool:
        all_trips_df_list = pool.map(simulate_single_trip, args)


    df = pd.concat(all_trips_df_list, ignore_index=True)


    df["ruin"] = df["$account"] <= 0


    df["ruin game"] = df.apply(
        lambda row: row["game number"] if row["ruin"] else None, axis=1
    )


    metadata = pd.pivot_table(
        df,
        values=["$result", "$account", "ruin game", "game number"],
        index=["series id"],
        aggfunc={
            "$result": "sum",
            "$account": "last",
            "ruin game": lambda x: pd.Series(x).dropna().min() if len(x) > 0 else None,
            "game number": "max",
        },
    )

    metadata.rename(
        columns={
            "$result": "trip $ result",
            "$account": "final bankroll",
            "ruin game": "ruin game",
            "game number": "total games played",
        },
        inplace=True,
    )

    metadata["average hand value"] = metadata["trip $ result"] / metadata["total games played"]
    metadata["ruin"] = metadata["ruin game"].notna().astype(int)
    metadata["starting bankroll"] = starting_bankroll

    metadata.reset_index(inplace=True)

    return metadata, df


if __name__ == "__main__":
    
    metadata, df = BJ_simulation_wrapper_parallel(
        trips=100,
        starting_bankroll=20000,
        min_table_bet=10,
        games_per_trip=2000,
        max_table_bet=500,
        shoe_size=8,
        games_per_deck=8,
        processes=os.cpu_count(),
    )
    metadata.to_csv('meta results.csv', index=False)
    df.to_csv('sim results.csv', index=False)
    print(metadata)
