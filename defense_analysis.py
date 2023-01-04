import pandas as pd
import statistics

# Between LB and S, I need to start 7 players every week.
# Probably need something like 10-11 threshold LB/S. Threshold is top 112 LB/S. Around 12.7 pts.
# 3 DTs max.
# 4 DEs max.
# 3 CBs max.
# Total Roster Spots: 20-21

def main():
      defense_avgs, flex_rates, flex1_rates = get_finals()

def get_finals():
      defense_2022, flex_2022 = median_avg_defense(2022)
      dt_flex_rate_2022, de_flex_rate_2022, lb_flex_rate_2022, cb_flex_rate_2022, s_flex_rate_2022 = flex_distribution(flex_2022)
      dt_flex1_rate_2022, de_flex1_rate_2022, lb_flex1_rate_2022, cb_flex1_rate_2022, s_flex1_rate_2022 = flex_distribution(flex_2022.iloc[0:16])

      defense_2021, flex_2021 = median_avg_defense(2021)
      dt_flex_rate_2021, de_flex_rate_2021, lb_flex_rate_2021, cb_flex_rate_2021, s_flex_rate_2021 = flex_distribution(flex_2022)
      dt_flex1_rate_2021, de_flex1_rate_2021, lb_flex1_rate_2021, cb_flex1_rate_2021, s_flex1_rate_2021 = flex_distribution(flex_2022.iloc[0:16])

      defense_2020, flex_2020 = median_avg_defense(2020)
      dt_flex_rate_2020, de_flex_rate_2020, lb_flex_rate_2020, cb_flex_rate_2020, s_flex_rate_2020 = flex_distribution(flex_2022)
      dt_flex1_rate_2020, de_flex1_rate_2020, lb_flex1_rate_2020, cb_flex1_rate_2020, s_flex1_rate_2020 = flex_distribution(flex_2022.iloc[0:16])

      defense_avg = avg_dfs(defense_2022,defense_2021,defense_2020)

      dt_flex_rate_avg = avg_flex_rates(dt_flex_rate_2020,dt_flex_rate_2021,dt_flex_rate_2022)
      dt_flex1_rate_avg = avg_flex_rates(dt_flex1_rate_2020, dt_flex1_rate_2021, dt_flex1_rate_2022)
      de_flex_rate_avg = avg_flex_rates(de_flex_rate_2020, de_flex_rate_2021, de_flex_rate_2022)
      de_flex1_rate_avg = avg_flex_rates(de_flex1_rate_2020, de_flex1_rate_2021, de_flex1_rate_2022)
      lb_flex_rate_avg = avg_flex_rates(lb_flex_rate_2020, lb_flex_rate_2021, lb_flex_rate_2022)
      lb_flex1_rate_avg = avg_flex_rates(lb_flex1_rate_2020, lb_flex1_rate_2021, lb_flex1_rate_2022)
      cb_flex_rate_avg = avg_flex_rates(cb_flex_rate_2020, cb_flex_rate_2021, cb_flex_rate_2022)
      cb_flex1_rate_avg = avg_flex_rates(cb_flex1_rate_2020, cb_flex1_rate_2021, cb_flex1_rate_2022)
      s_flex_rate_avg = avg_flex_rates(s_flex_rate_2020, s_flex_rate_2021, s_flex_rate_2022)
      s_flex1_rate_avg = avg_flex_rates(s_flex1_rate_2020, s_flex1_rate_2021, s_flex1_rate_2022)

      flex_rate_avgs = [dt_flex_rate_avg,de_flex_rate_avg,lb_flex_rate_avg,cb_flex_rate_avg,s_flex_rate_avg]
      flex1_rate_avgs = [dt_flex1_rate_avg,de_flex1_rate_avg,lb_flex1_rate_avg,cb_flex1_rate_avg,s_flex1_rate_avg]
      flex_rate_df = pd.DataFrame(data = flex_rate_avgs,columns=['avg'],index=['DT','DE','LB','CB','S'])
      flex1_rate_df = pd.DataFrame(data=flex1_rate_avgs, columns=['avg'], index=['DT', 'DE', 'LB','CB','S'])

      return defense_avg, flex_rate_df,flex1_rate_df

def median_avg_defense(year):
      if year == 2022:
            url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
                  '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=13&CATEGORY=overall' \
                  '&POSITION=DT%7CDE%7CLB%7CCB%7CS&DISPLAY=points&TEAM=*'
      else:
            url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
                  '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=16&CATEGORY=overall' \
                  '&POSITION=DT%7CDE%7CLB%7CCB%7CS&DISPLAY=points&TEAM=*'

      lis = pd.read_html(url)
      df = lis[1]
      columns = df.columns
      df1 = df[[columns[1],columns[3]]].copy()
      df1.columns = ['player', 'avg']
      df1 = clean_df(df1)
      median_avgs, dflex = get_median_avgs(df1)

      pos_list = ['DT1', 'DE1', 'DE2', 'LB1', 'LB2', 'LB3', 'CB1', 'CB2', 'S1', 'S2', 'FLEX1', 'FLEX2']
      median_avgs_defense_2022 = pd.DataFrame(data=median_avgs, index = pos_list, columns = ['avg'])

      return median_avgs_defense_2022, dflex

def get_median_avgs(df):
      DTs, DEs, LBs, CBs, Ss = divide_pos(df)

      DT1s = [DTs['avg'][6], DTs['avg'][7], DTs['avg'][8], DTs['avg'][9]]
      DE1s = [DEs['avg'][6], DEs['avg'][7], DEs['avg'][8], DEs['avg'][9]]
      DE2s = [DEs['avg'][22], DEs['avg'][23], DEs['avg'][24], DEs['avg'][25]]
      LB1s = [LBs['avg'][6], LBs['avg'][7], LBs['avg'][8], LBs['avg'][9]]
      LB2s = [LBs['avg'][22], LBs['avg'][23], LBs['avg'][24], LBs['avg'][25]]
      LB3s = [LBs['avg'][38], LBs['avg'][39], LBs['avg'][40], LBs['avg'][41]]
      CB1s = [CBs['avg'][6], CBs['avg'][7], CBs['avg'][8], CBs['avg'][9]]
      CB2s = [CBs['avg'][22], CBs['avg'][23], CBs['avg'][24], CBs['avg'][25]]
      S1s = [Ss['avg'][6], Ss['avg'][7], Ss['avg'][8], Ss['avg'][9]]
      S2s = [Ss['avg'][22], Ss['avg'][23], Ss['avg'][24], Ss['avg'][25]]

      median_avgs_defense_list = [statistics.mean(DT1s),statistics.mean(DE1s),statistics.mean(DE2s),
                                  statistics.mean(LB1s),statistics.mean(LB2s),statistics.mean(LB3s),
                                  statistics.mean(CB1s),statistics.mean(CB2s),statistics.mean(S1s),
                                  statistics.mean(S2s)]

      dflex = delete_starters(df)
      indices = dflex.index
      droppable_indices = indices[32:]
      dflex = dflex.drop(droppable_indices)

      dflex1s = dflex['avg'].iloc[6:10].tolist()
      dflex2s = dflex['avg'].iloc[22:26].tolist()
      median_avgs_defense_list.append(statistics.mean(dflex1s))
      median_avgs_defense_list.append(statistics.mean(dflex2s))

      return median_avgs_defense_list, dflex

def flex_distribution(dflex):
      dt_sum, de_sum, lb_sum, cb_sum, s_sum = 0, 0, 0, 0, 0

      for i in dflex.index:
            pos = dflex['pos'][i]
            if pos == 'DT':
                  dt_sum += 1
            if pos == 'DE':
                  de_sum += 1
            if pos == 'LB':
                  lb_sum += 1
            if pos == 'CB':
                  cb_sum += 1
            if pos == 'S':
                  s_sum += 1

      dt_rate = dt_sum / len(dflex.index)
      de_rate = de_sum / len(dflex.index)
      lb_rate = lb_sum / len(dflex.index)
      cb_rate = cb_sum / len(dflex.index)
      s_rate = s_sum / len(dflex.index)

      return dt_rate, de_rate, lb_rate, cb_rate, s_rate

def clean_df(df):
      positions, teams = [], []

      for index in df.index:
            player = df['player'].iloc[index]

            sl = slice(len(player) - 3, len(player), 1)
            if player[sl] == '(R)':
                  player = player[:len(player) - 4]

            if player[len(player) - 1] == 'S':
                  sl = slice(len(player) - 1, len(player), 1)
                  pos = player[sl]
                  positions.append(pos)
                  player = player[:len(player) - 2]

                  sl = slice(len(player) - 4, len(player), 1)
                  team = player[sl]
                  teams.append(team)
                  player = player[:len(player) - 3]
                  df['player'].iloc[index] = player
            else:
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
      dt_indices, de_indices, lb_indices, cb_indices, s_indices = [], [], [], [], []
      for index in df.index:
            if df['pos'].iloc[index] == 'DT':
                  dt_indices.append(index)
            if df['pos'].iloc[index] == 'DE':
                  de_indices.append(index)
            if df['pos'].iloc[index] == 'LB':
                  lb_indices.append(index)
            if df['pos'].iloc[index] == 'CB':
                  cb_indices.append(index)
            if df['pos'].iloc[index] == 'S':
                  s_indices.append(index)

      dt_indices = dt_indices[:16]
      de_indices = de_indices[:32]
      lb_indices = lb_indices[:48]
      cb_indices = cb_indices[:32]
      s_indices = s_indices[:32]

      df = df.drop(dt_indices)
      df = df.drop(de_indices)
      df = df.drop(lb_indices)
      df = df.drop(cb_indices)
      df = df.drop(s_indices)

      return df

def divide_pos(df):
      DTs = pd.DataFrame(columns=df.columns)
      DEs = pd.DataFrame(columns=df.columns)
      LBs = pd.DataFrame(columns=df.columns)
      CBs = pd.DataFrame(columns=df.columns)
      Ss = pd.DataFrame(columns=df.columns)
      for index in df.index:
            pos = df['pos'][index]
            if pos == 'DT':
                  DTs.loc[len(DTs.index)] = df.loc[index]
            if pos == 'DE':
                  DEs.loc[len(DEs.index)] = df.loc[index]
            if pos == 'LB':
                  LBs.loc[len(LBs.index)] = df.loc[index]
            if pos == 'CB':
                  CBs.loc[len(CBs.index)] = df.loc[index]
            if pos == 'S':
                  Ss.loc[len(Ss.index)] = df.loc[index]

      return DTs, DEs, LBs, CBs, Ss

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