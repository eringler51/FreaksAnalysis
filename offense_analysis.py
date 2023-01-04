import pandas as pd
import statistics

# 32-33 roster spots available
# 4 QBs
# 4 TEs
# 8-9 threshold WRs ~
# 15-17 RBs

def main():
      offense_avgs, flex_rates, flex1_rates = get_finals()

def get_finals():
      offense_2022, flex_2022 = median_avg_offense(2022)
      rb_flex_rate_2022, wr_flex_rate_2022, te_flex_rate_2022 = flex_distribution(flex_2022)
      rb_flex1_rate_2022, wr_flex1_rate_2022, te_flex1_rate_2022 = flex_distribution(flex_2022.iloc[0:32])

      offense_2021, flex_2021 = median_avg_offense(2021)
      rb_flex_rate_2021, wr_flex_rate_2021, te_flex_rate_2021 = flex_distribution(flex_2021)
      rb_flex1_rate_2021, wr_flex1_rate_2021, te_flex1_rate_2021 = flex_distribution(flex_2021.iloc[0:32])

      offense_2020, flex_2020 = median_avg_offense(2020)
      rb_flex_rate_2020, wr_flex_rate_2020, te_flex_rate_2020 = flex_distribution(flex_2020)
      rb_flex1_rate_2020, wr_flex1_rate_2020, te_flex1_rate_2020 = flex_distribution(flex_2020.iloc[0:32])

      offense_avg = avg_dfs(offense_2022,offense_2021,offense_2020)

      rb_flex_rate_avg = avg_flex_rates(rb_flex_rate_2020,rb_flex_rate_2021,rb_flex_rate_2022)
      rb_flex1_rate_avg = avg_flex_rates(rb_flex1_rate_2020, rb_flex1_rate_2021, rb_flex1_rate_2022)
      wr_flex_rate_avg = avg_flex_rates(wr_flex_rate_2020, wr_flex_rate_2021, wr_flex_rate_2022)
      wr_flex1_rate_avg = avg_flex_rates(wr_flex1_rate_2020, wr_flex1_rate_2021, wr_flex1_rate_2022)
      te_flex_rate_avg = avg_flex_rates(te_flex_rate_2020, te_flex_rate_2021, te_flex_rate_2022)
      te_flex1_rate_avg = avg_flex_rates(te_flex1_rate_2020, te_flex1_rate_2021, te_flex1_rate_2022)

      flex_rate_avgs = [rb_flex_rate_avg,wr_flex_rate_avg,te_flex_rate_avg]
      flex1_rate_avgs = [rb_flex1_rate_avg,wr_flex1_rate_avg,te_flex1_rate_avg]
      flex_rate_df = pd.DataFrame(data = flex_rate_avgs,columns=['avg'],index=['RB','WR','TE'])
      flex1_rate_df = pd.DataFrame(data=flex1_rate_avgs, columns=['avg'], index=['RB', 'WR', 'TE'])

      return offense_avg, flex_rate_df,flex1_rate_df

def median_avg_offense(year):
      if year == 2022:
            url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
            '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=14&CATEGORY=overall&' \
            'POSITION=QB%7CRB%7CWR%7CTE%7CPK&DISPLAY=points&TEAM=*&SORT=AVG'
      else:
            url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
            '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=16&CATEGORY=overall&' \
            'POSITION=QB%7CRB%7CWR%7CTE%7CPK&DISPLAY=points&TEAM=*&SORT=AVG'
      lis = pd.read_html(url)
      df = lis[1]
      columns = df.columns
      superflex = df[[columns[1],columns[3]]].copy()
      superflex.columns = ['player', 'avg']
      superflex = clean_df(superflex)
      median_avgs, flex = get_median_avgs(superflex)

      pos_list = ['QB1', 'QB2', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'FLEX1', 'FLEX2']
      median_avgs_offense_2022 = pd.DataFrame(data=median_avgs, index = pos_list, columns = ['avg'])

      return median_avgs_offense_2022, flex

def get_median_avgs(superflex):
      QBs, RBs, WRs, TEs = divide_pos(superflex)

      QB1s = [QBs['avg'][6], QBs['avg'][7], QBs['avg'][8], QBs['avg'][9]]
      QB2s = [QBs['avg'][22], QBs['avg'][23], QBs['avg'][24], QBs['avg'][25]]
      RB1s = [RBs['avg'][6], RBs['avg'][7], RBs['avg'][8], RBs['avg'][9]]
      RB2s = [RBs['avg'][22], RBs['avg'][23], RBs['avg'][24], RBs['avg'][25]]
      WR1s = [WRs['avg'][6], WRs['avg'][7], WRs['avg'][8], WRs['avg'][9]]
      WR2s = [WRs['avg'][22], WRs['avg'][23], WRs['avg'][24], WRs['avg'][25]]
      WR3s = [WRs['avg'][38], WRs['avg'][39], WRs['avg'][40], WRs['avg'][41]]
      TE1s = [TEs['avg'][6], TEs['avg'][7], TEs['avg'][8], TEs['avg'][9]]

      median_avgs_offense_list = [statistics.mean(QB1s),statistics.mean(QB2s),statistics.mean(RB1s),
                                  statistics.mean(RB2s),statistics.mean(WR1s),statistics.mean(WR2s),
                                  statistics.mean(WR3s),statistics.mean(TE1s)]

      flex = delete_starters(superflex)
      indices = flex.index
      droppable_indices = indices[80:]
      flex = flex.drop(droppable_indices)

      flex1s = flex['avg'].iloc[6:10].tolist()
      flex2s = flex['avg'].iloc[22:26].tolist()
      median_avgs_offense_list.append(statistics.mean(flex1s))
      median_avgs_offense_list.append(statistics.mean(flex2s))

      return median_avgs_offense_list, flex

def flex_distribution(flex):
      rb_sum, wr_sum, te_sum = 0, 0, 0

      for i in flex.index:
            pos = flex['pos'][i]
            if pos == 'RB':
                  rb_sum += 1
            if pos == 'WR':
                  wr_sum += 1
            if pos == 'TE':
                  te_sum += 1

      rb_rate = rb_sum / len(flex.index)
      wr_rate = wr_sum / len(flex.index)
      te_rate = te_sum / len(flex.index)

      return rb_rate, wr_rate, te_rate

def clean_df(df):
      positions, teams = [], []

      for index in df.index:
            player = df['player'].iloc[index]

            sl = slice(len(player) - 3, len(player), 1)
            if player[sl] == '(R)':
                  player = player[:len(player) - 4]

            sl = slice(len(player)-2,len(player),1)
            pos = player[sl]
            positions.append(pos)
            player = player[:len(player) - 3]

            sl = slice(len(player) - 4, len(player), 1)
            team = player[sl]
            teams.append(team)
            player = player[:len(player) - 3]
            df['player'].iloc[index] = player

      df['team'] = teams
      df['pos'] = positions
      df['pos'] = df.pos.astype('category')
      return df

def delete_starters(df):
      qb_indices, rb_indices, wr_indices, te_indices, pk_indices = [], [], [], [], []
      for index in df.index:
            if df['pos'].iloc[index] == 'QB':
                  qb_indices.append(index)
            if df['pos'].iloc[index] == 'RB':
                  rb_indices.append(index)
            if df['pos'].iloc[index] == 'WR':
                  wr_indices.append(index)
            if df['pos'].iloc[index] == 'TE':
                  te_indices.append(index)
            if df['pos'].iloc[index] == 'PK':
                  pk_indices.append(index)
      rb_indices = rb_indices[:32]
      wr_indices = wr_indices[:48]
      te_indices = te_indices[:16]

      df = df.drop(qb_indices)
      df = df.drop(rb_indices)
      df = df.drop(wr_indices)
      df = df.drop(te_indices)
      df = df.drop(pk_indices)

      return df

def divide_pos(df):
      RBs = pd.DataFrame(columns=df.columns)
      WRs = pd.DataFrame(columns=df.columns)
      TEs = pd.DataFrame(columns=df.columns)
      QBs = pd.DataFrame(columns=df.columns)
      for index in df.index:
            pos = df['pos'][index]
            if pos == 'QB':
                  QBs.loc[len(QBs.index)] = df.loc[index]
            if pos == 'RB':
                  RBs.loc[len(RBs.index)] = df.loc[index]
            if pos == 'WR':
                  WRs.loc[len(WRs.index)] = df.loc[index]
            if pos == 'TE':
                  TEs.loc[len(TEs.index)] = df.loc[index]

      return QBs, RBs, WRs, TEs

def avg_dfs(df1,df2,df3):
      avgs = []
      for pos in df1.index:
            v1 = df1['avg'][pos]
            v2 = df2['avg'][pos]
            v3 = df3['avg'][pos]
            avg = (v1+v2+v3)/3
            avgs.append(avg)
      final_df = pd.DataFrame(data=avgs,columns=df1.columns,index=df1.index)

      return final_df

def avg_flex_rates(rate1,rate2,rate3):
      return (rate3+rate1+rate2)/3

main()