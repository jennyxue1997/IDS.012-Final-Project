import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import random

def parse_data(team, season):
    # Read data
    data = pd.read_csv("events_" + season + "_pbp.csv")
    team_data = data.loc[(data["HOME_TEAM"] == team) | (data["AWAY_TEAM"] == team)]

    data_array = []
    game_data = {}
    for idx, event in team_data.iterrows():
        game_id = event["GAME_ID"]
        period = event["PERIOD"]
        home_team = event["HOME_TEAM"]
        away_team = event["AWAY_TEAM"]
        home_score = event["HOME_SCORE"]
        away_score = event["AWAY_SCORE"]
        score_difference = home_score - away_score
        time = event["TIME"]
        
        description_team = np.nan
        free_throw_made = event["FREE_THROW_MADE"]
        shot_made = event["SHOT_MADE"]
        
        # Start of period
        if event["PERIOD_START"] is True:
            description = "start" 
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
        
        # Free Throw
        elif not np.isnan(event["FREE_THROW_PLAYER_ID"]):
            description = "free throw"
            if event["PLAYER1_TEAM_NICKNAME"] == home_team:
                description_team = home_team
            else:
                description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
        
        # Shot
        elif type(event["SHOT_TYPE"]) != float:
            description = "shot"
            if event["PLAYER1_TEAM_NICKNAME"] == home_team:
                description_team = home_team
            else:
                description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
            
        
        # Foul
        elif type(event["FOUL_TYPE"]) != float:
            description = "foul"
            if event["PLAYER1_TEAM_NICKNAME"] == home_team:
                description_team = home_team
            else:
                description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
        
        # Turnover
        elif type(event["TURNOVER_TYPE"]) != float:
            description = "turnover"
            if event["TURNOVER_PLAYER_ID"] == event["PLAYER1_ID"]:
                if event["PLAYER1_TEAM_NICKNAME"] == home_team:
                    description_team = home_team
                else:
                    description_team = away_team
            
            elif event["TURNOVER_PLAYER_ID"] == event["PLAYER2_ID"]:
                if event["PLAYER2_TEAM_NICKNAME"] == home_team:
                    description_team = home_team
                else:
                    description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
        
        # Rebound
        elif not np.isnan(event["REBOUND_PLAYER_ID"]):
            description = "rebound"
            if type(event["HOMEDESCRIPTION"]) != float:
                description_team = home_team
            else:
                description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])

        # Timeout
        elif type(event["TIMEOUT_TYPE"]) != float:
            description = "timeout"
            if type(event["HOMEDESCRIPTION"]) != float:
                description_team = home_team
            else:
                description_team = away_team
            data_array.append([game_id, period, home_team, away_team, time, home_score, away_score, score_difference, description, description_team, free_throw_made, shot_made])
    
    # Array to DataFrame
    parsed_data = pd.DataFrame(data_array, columns=["game_id", "period", "home_team", "away_team", "time", "home_score", "away_score", "score_difference", "description", "description_team", "free_throw_made", "shot_made"])

    # Calculate points of shot
    shot_points = []
    for idx, row in parsed_data.iterrows():
        if row["shot_made"] == True:
            points = abs(row["score_difference"] - parsed_data.iloc[idx-1]["score_difference"])
            shot_points.append(points)
        else:
            shot_points.append(0)

    parsed_data["shot_points"] = shot_points


    # Dataframe to CSV
    parsed_data.to_csv(season + "_" + team + ".csv")

if __name__ == "__main__":
    team = "Celtics"
    season = "2017-2018"
    parse_data(team, season)