def get_best_combination(pair_players_df, msp_limit=10, hero_limit=5):
    edges = []
    for _, pair_player in pair_players_df.iterrows():
        edges.append({
            's': pair_player['player1'],
            't': pair_player['player2'],
            'weight': pair_player['winrate']
        })

    edges = sorted(edges, key=lambda x: -x['weight'])

    dsu = {}

    def parent(s):
        if s not in dsu:
            dsu[s] = {
                'parent': -1,
                'cluster_size': 1
            }
            return s
        if dsu[s]['parent'] == -1:
            return s
        p = parent(dsu[s]['parent'])
        dsu[s]['parent'] = p
        return p

    def merge(s, t):
        s = parent(s)
        t = parent(t)
        if s == t:
            return s
        dsu[t]['parent'] = s
        dsu[s]['cluster_size'] += dsu[t]['cluster_size']
        return s

    cluster_id = -1

    for edge in edges:
        id = merge(edge['s'], edge['t'])
        if dsu[id]['cluster_size'] >= msp_limit:
            cluster_id = id
            break

    heroes = []
    for hero_id in dsu.keys():
        if parent(hero_id) == cluster_id:
            heroes.append(hero_id)

    # print(heroes)

    def get_weight(id1, id2):
        for edge in edges:
            if edge['s'] == id1 and edge['t'] == id2:
                return edge['weight']
        return 0

    visited = [False for x in heroes]

    def calculate_score():
        sum = 0
        for i in range(len(heroes)):
            for j in range(len(heroes)):
                if i == j:
                    continue
                if visited[i] and visited[j]:
                    sum += get_weight(heroes[i], heroes[j])
        return sum

    get_best_combination.best_combination = []
    get_best_combination.best_score = -1

    def dfs(p, cnt):
        if cnt == hero_limit:
            score = calculate_score()
            if score > get_best_combination.best_score:
                get_best_combination.best_score = score
                get_best_combination.best_combination = []
                for i in range(len(heroes)):
                    if visited[i]:
                        get_best_combination.best_combination.append(heroes[i])
            return
        if p >= len(heroes):
            return
        visited[p] = True
        dfs(p + 1, cnt + 1)
        visited[p] = False
        dfs(p + 1, cnt)

    dfs(0, 0)

    # print(best_combination)
    # print(best_score)
    return get_best_combination.best_combination
