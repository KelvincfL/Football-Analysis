import numpy as np
import pandas as pd
df = pd.read_csv("C:/Users/Administrator/Desktop/EPL_Set.csv")
#df=df[["HomeTeam","AwayTeam","FTHG","FTAG"]]
# df=df[["HomeTeam","AwayTeam","FTHG","FTAG","Season"]]
# df=df[df["Season"] == "2016-17"]
# df.drop(columns=["Season"])
#print(df.head())
#df.to_csv("C:/Users/Administrator/Desktop/EPL_Set.csv")
avg_home_goal = (df["FTHG"].sum())/ 380
avg_away_goal = (df["FTAG"].sum())/ 380
team_home_attack =(df.groupby("HomeTeam")["FTHG"].sum())/19
team_home_defense = (df.groupby("HomeTeam")["FTAG"].sum())/19
team_away_attack = (df.groupby("AwayTeam")["FTAG"].sum())/19
team_away_defense = (df.groupby("AwayTeam")["FTHG"].sum())/19
team_lambda_home = avg_home_goal*(team_home_attack/avg_home_goal)*(team_away_defense/avg_home_goal)
team_lambda_away = (team_away_attack*team_home_defense)/avg_away_goal
# lambda = attack factor * defense factor * avg home/away goal


def prediction_goals (lambdahome, lambdaaway):
    l_home = np.random.poisson(lambdahome,1)
    l_away = np.random.poisson(lambdaaway,1)
    result = int(l_home),int(l_away)
    return result


def score_line_home(team):
    points=0
    for i in (team_lambda_home.index.drop(team)):
        temp = prediction_goals(team_lambda_home[team],team_lambda_away[i])
        if temp[0] > temp [1]:
            points +=3
        elif temp[0] == temp[1]:
            points +=1
    return points


def score_line_away(team):
    points=0
    for i in (team_lambda_home.index.drop(team)):
        temp= prediction_goals(team_lambda_home[i], team_lambda_away[team])
        if temp[1] > temp[0]:
            points += 3
        elif temp[1] == temp[0]:
            points += 1
    return points


champions = dict()


def league_table_creator():
    league_table = pd.DataFrame(columns=["Team", "Points"])
    for t in team_lambda_home.index:
        a = score_line_home(t) + score_line_away(t)
        league_table.loc[t] = [t,a]
    league_table = league_table.sort_values(by=["Points"], ascending=False)
    Index = range(1,21)
    league_table.index=Index
    if league_table.iloc[0]["Team"] in champions:
        champions[league_table.iloc[0]["Team"]] += 1
    else:
        champions[league_table.iloc[0]["Team"]] = 1
    return league_table


for i in range(100):
    print(league_table_creator())
print(champions)
