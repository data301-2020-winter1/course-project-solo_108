import pandas as pd
import seaborn as sns


def load_and_process(url_or_path_to_json_file):

    # load and clean matches
    matches_df = (
        pd.read_json(url_or_path_to_json_file, lines=True)
        .dropna()
        .rename(columns={
            'radiant_score': 'radiant_kills',
            'dire_score': 'dire_kills',
        })
        .drop(columns=['match_id'])
        .reset_index(drop=True)
    )

    # Convert radiant_win to boolean type
    matches_df['radiant_win'] = matches_df['radiant_win'].apply(lambda x: True if x == 1 else False)

    # Generate players from matches
    players = []
    for _, match in matches_df.iterrows():
        game_players = match['players']
        for player in game_players:
            player['win'] = match['radiant_win'] ^ player['isRadiant']
            players.append(player)

    # Remove players from matches as we don't need it anymore
    matches_df = matches_df.drop(columns=['players', ])

    # Create player dataframe and clean it
    players_df = (
        pd.DataFrame(players).
        dropna().
        rename(columns={
            'gold_per_min': 'gpm',
            'xp_per_min': 'xpm',
        }).
        drop(columns=['player_slot', 'item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'isRadiant']).
        reset_index(drop=True)
    )

    return matches_df, players_df


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
    plot = sns.displot(matches_df, x='radiant_kills')
    plot.set(xlabel='Radiant Kills (#)', ylabel='Number of matches')

    return plot


def winrate_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('win')[-5:]['win']*100
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Win Rate')
    return plot


def kills_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('kills')[-5:]['kills']
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Number of Kills')
    return plot


def assists_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('assists')[-5:]['assists']
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Number of Assists')
    return plot


def deaths_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('deaths')[:5]['deaths']
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Number of Deaths')
    return plot


def gpm_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('gpm')[-5:]['gpm']
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Gold per Minute')
    return plot


def xpm_plot(players_df):
    data = players_df.groupby('hero_id').mean().sort_values('xpm')[-5:]['xpm']
    plot = sns.barplot(x=data.index, y=data)
    plot.set(xlabel='Hero id', ylabel='Average Experience per Minute')
    return plot
