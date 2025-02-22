import streamlit as st
import random
import matplotlib.pyplot as plt

# Player class representing an individual player with statistics
class Player:
    def __init__(self, name):
        self.name = name
        self.balls_faced = 0
        self.runs_scored = 0
        self.wickets_taken = 0
        self.last_strike = None

# Team class representing a cricket team with 11 players
class Team:
    def __init__(self, name):
        self.name = name
        self.players = [Player(f"Player {i+1}") for i in range(11)]
        self.score = 0
        self.wickets = 0

# Main game logic
class CricketGame:
    def __init__(self, team_a_name, team_b_name):
        self.team_a = Team(team_a_name)
        self.team_b = Team(team_b_name)
        self.current_batting_team = self.team_a
        self.current_bowling_team = self.team_b
        self.balls_bowled = 0
        self.max_overs = 5  # Maximum number of overs
        self.balls_per_over = 6  # Balls per over
        self.max_wickets = 10  # Wickets limit
        self.game_completed = False
        self.target_score = None
        self.current_batsman_index = 0  # Track current batsman

    def play_delivery(self):
        if self.game_completed:
            return "Game Over! Restart to play again."

        # Check if innings should end
        if self.current_batting_team.wickets >= self.max_wickets or self.balls_bowled == self.max_overs * self.balls_per_over:
            return self.end_innings()

        batsman = self.current_batting_team.players[self.current_batsman_index]
        bowler = random.choice(self.current_bowling_team.players)
        
        if random.random() < 0.15:  # 15% chance of a wicket
            self.current_batting_team.wickets += 1
            bowler.wickets_taken += 1
            batsman.last_strike = "Wicket"
            self.current_batsman_index += 1  # Move to next batsman
            return f"Wicket! {batsman.name} is out. Total Wickets: {self.current_batting_team.wickets}"

        runs_scored = random.choice([0, 1, 2, 3, 4, 6])
        self.current_batting_team.score += runs_scored
        batsman.runs_scored += runs_scored
        batsman.balls_faced += 1
        batsman.last_strike = runs_scored
        self.balls_bowled += 1
        
        # Check if Team B has exceeded Team A's score
        if self.current_batting_team == self.team_b and self.current_batting_team.score > self.target_score:
            self.game_completed = True
            return f"{self.current_batting_team.name} wins by {self.current_batting_team.score - self.target_score} runs!"

        return f"Ball {self.balls_bowled}: {runs_scored} runs scored. Current Score: {self.current_batting_team.score}/{self.current_batting_team.wickets}"

    def end_innings(self):
        if self.current_batting_team == self.team_a:
            self.target_score = self.team_a.score + 1
            self.current_batting_team, self.current_bowling_team = self.team_b, self.team_a
            self.balls_bowled = 0
            self.current_batsman_index = 0
            return f"End of innings. {self.team_b.name} needs {self.target_score} to win."
        else:
            self.game_completed = True
            return self.determine_winner()

    def determine_winner(self):
        if self.team_a.score == self.team_b.score:
            return "Match Drawn!"
        winner = self.team_a if self.team_a.score > self.team_b.score else self.team_b
        return f"{winner.name} wins by {abs(self.team_a.score - self.team_b.score)} runs"

    def display_summary(self):
        st.write("Match Summary:")
        for team in [self.team_a, self.team_b]:
            st.write(f"{team.name} - Score: {team.score}/{team.wickets}")
            for player in team.players:
                st.write(f"{player.name}: Runs - {player.runs_scored}, Balls Faced - {player.balls_faced}, Wickets Taken - {player.wickets_taken}, Last Strike - {player.last_strike}")
            st.write("---")
        
        # Plot Score Comparison
        plt.figure(figsize=(8, 4))
        scores = [team.score for team in [self.team_a, self.team_b]]
        teams = [self.team_a.name, self.team_b.name]
        plt.bar(teams, scores, color=['blue', 'red'])
        plt.xlabel("Teams")
        plt.ylabel("Total Score")
        plt.title("Team Score Comparison")
        st.pyplot(plt)

# Streamlit UI
st.title("Cricket Game Simulator")

if "game" not in st.session_state:
    team_a_name = st.text_input("Enter Team A name", "Team A")
    team_b_name = st.text_input("Enter Team B name", "Team B")
    if st.button("Start Game"):
        st.session_state.game = CricketGame(team_a_name, team_b_name)
        st.rerun()

if "game" in st.session_state:
    game = st.session_state.game
    if st.button("Play Ball"):
        st.write(game.play_delivery())

    st.write(f"Current Score: {game.current_batting_team.score}/{game.current_batting_team.wickets}")
    st.write(f"Balls Bowled: {game.balls_bowled}/{game.max_overs * game.balls_per_over}")

    if game.game_completed:
        game.display_summary()
        st.write("Game Over!", game.determine_winner())
