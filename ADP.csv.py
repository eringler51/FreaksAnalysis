import pandas as pd

class ADP():
    def __init__(self):
        super(ADP, self).__init__()

    def load_df(self, filename):
        temp_adp = pd.read_csv(filename)
        cols = temp_adp.columns
        adp = temp_adp.loc[:, ["ADP", "Players + Rookies (390)"]]
        adp.columns = ['adp', 'player']
        adp = clean_adp(adp)
        self.df = adp

    def clean_adp(self, df):
        positions, teams = [], []

        for index in df.index:
            current = df['player'].iloc[index]
            elements = current.split(' ')
            player = elements[0] + ' ' + elements[1]
            if len(elements) < 4:
                teams.append('FA')
                positions.append(elements[2])
            else:
                teams.append(elements[2])
                positions.append(elements[3])
            df['player'].iloc[index] = player

        df['team'] = teams
        df['pos'] = positions
        df['pos'] = df.pos.astype('category')
        return df
