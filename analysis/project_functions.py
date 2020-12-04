import json

import pandas as pd
import seaborn as sns


def generate_players(matches_df):
    # Generate players from matches
    players = []
    for _, match in matches_df.iterrows():
        game_players = match['players']
        for player in game_players:
            player['win'] = match['radiant_win'] ^ player['isRadiant']
            players.append(player)

    # Create player dataframe and clean it
    players_df = (
        pd.DataFrame(players)
        .dropna()
        .rename(columns={
            'gold_per_min': 'gpm',
            'xp_per_min': 'xpm',
        })
        .drop(columns=['player_slot', 'item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'isRadiant'])
        .reset_index(drop=True)
    )

    return players_df


def generate_pair_players(matches_df):
    pair_players = []
    for _, match in matches_df.iterrows():
        game_players = match['players']
        for player1 in game_players:
            for player2 in game_players:
                if player1['hero_id'] == player2['hero_id'] or player1['isRadiant'] != player2['isRadiant']:
                    continue
                pair_player = {
                    'player1': player1['hero_id'],
                    'player2': player2['hero_id'],
                    'win': match['radiant_win'] ^ player1['isRadiant']
                }
                pair_players.append(pair_player)

    pair_players_df = (
        pd.DataFrame(pair_players)
        .dropna()
        .groupby(['player1', 'player2'])
        .agg(['mean', 'count'])
        .reset_index()
        .sort_values(by=[('win', 'mean')])
    )

    pair_players_df = pair_players_df[pair_players_df['win']['count'] > 100]
    pair_players_df['count'] = pair_players_df['win']['count']
    pair_players_df['winrate'] = pair_players_df['win']['mean']
    pair_players_df = pair_players_df.drop(columns=['win'])

    return pair_players_df


def load_and_process(url_or_path_to_json_file):
    # load and clean matches
    matches = []
    with open(url_or_path_to_json_file) as f:
        for line in f.readlines():
            matches.append(json.loads(line))

    matches_df = (
        pd.DataFrame(matches)
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

    players_df = generate_players(matches_df)
    pair_players_df = generate_pair_players(matches_df)

    # Remove players from matches as we don't need it anymore
    matches_df = matches_df.drop(columns=['players', ])

    return matches_df, players_df, pair_players_df


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
    data = players_df.groupby('hero_id').mean().sort_values('win')[-5:]['win'] * 100
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


def player_synergy_heatmap(pair_players_df):
    players = pair_players_df[pair_players_df['winrate'] > 0.63]['player1'].values
    data2d = (
        pair_players_df[pair_players_df['player1'].isin(players) & pair_players_df['player2'].isin(players)]
        .pivot_table(index='player1', columns='player2')['winrate']
    )
    plot = sns.heatmap(data2d, cmap=sns.color_palette("coolwarm", as_cmap=True))
    return plot


def process_and_save_data(url_or_path_to_json_file="../data/raw/matches.json"):
    matches_df, players_df, pair_players_df = load_and_process(url_or_path_to_json_file)

    matches_df.to_csv(path_or_buf='../data/processed/matches.csv', index=False)
    players_df.to_csv(path_or_buf='../data/processed/players.csv', index=False)
    pair_players_df.to_csv(path_or_buf='../data/processed/pair_players.csv', index=False)


def load_processed_data():
    matches_df = pd.read_csv('../data/processed/matches.csv').dropna()
    players_df = pd.read_csv('../data/processed/players.csv').dropna()
    pair_players_df = pd.read_csv('../data/processed/pair_players.csv').dropna()

    return matches_df, players_df, pair_players_df


def graph_generator():
    pair_players_df = pd.read_csv('data/processed/pair_players.csv').dropna()

    players = pair_players_df[pair_players_df['winrate'] > 0.63]['player1'].unique()

    for i in players:
        print(int(i))
    for _, row in pair_players_df[pair_players_df['player1'].isin(players) & pair_players_df['player2'].isin(players)].iterrows():
        if row['winrate'] > 0.6 and row['player1'] < row['player2']:
            print("{} {} {:.2f}%".format(int(row['player1']), int(row['player2']), row['winrate']*100))


def final_graph_generator():
    pair_players_df = pd.read_csv('data/processed/pair_players.csv').dropna()
    players = [97.0, 74.0, 114.0, 87.0, 95.0]

    for i in players:
        print(int(i))
    for _, row in pair_players_df[pair_players_df['player1'].isin(players) & pair_players_df['player2'].isin(players)].iterrows():
        if row['player1'] < row['player2']:
            print("{} {} {:.2f}%".format(int(row['player1']), int(row['player2']), row['winrate']*100))
