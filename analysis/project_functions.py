import pandas as pd
import seaborn as sns


def load_and_process(url_or_path_to_json_file):
    matched_df = (
        pd.read_json(url_or_path_to_json_file, lines=True)
            .dropna()
            .rename(columns={
            'radiant_score': 'radiant_kills',
            'dire_score': 'dire_kills',
        })
    )

    matched_df['radiant_win'] = matched_df['radiant_win'].apply(lambda x: True if x == 1 else False)

    players = []
    for game_players in matched_df['players']:
        for player in game_players:
            players.append(player)

    players_df = pd.DataFrame(players)

    return matched_df, players_df


def duration_plot(matches_df):
    plot = (
        sns.displot(matches_df, x='duration')
        .set(xlabel='Match Duration (s)', ylabel='Number of matches')
    )
    return plot


def first_blood_time_plot(matches_df):
    plot = (
        sns.displot(matches_df, x='first_blood_time')
        .set(xlabel='First Blood Time (s)', ylabel='Number of matches')
    )
    return plot


def radiant_kills_plot(matches_df):
    plot = (
        sns.displot(matches_df, x='radiant_kills')
        .set(xlabel='Radiant Kills (#)', ylabel='Number of matches')
    )
    return plot
