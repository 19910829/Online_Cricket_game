import streamlit as st
import random
import matplotlib.pyplot as plt


# Cricket Game Class
class CricketGame:
    def __init__(self):
        self.overs = 5
        self.balls_per_over = 6
        self.scoreboard = {"Team A": 0, "Team B": 0}
        self.wickets = {"Team A": 0, "Team B": 0}
        self.current_team = "Team A"
        self.balls_played = 0
        self.target = None
        self.game_over = False
        self.wickets_limit = 10

    def play_ball(self):
        if self.game_over:
            return "Game Over! Restart to play again."

        if random.random() < 0.15:  # 15% chance of a wicket
            self.wickets[self.current_team] += 1
            if self.wickets[self.current_team] >= self.wickets_limit:
                return self.end_innings()
            return f"Wicket! {self.current_team} lost a wicket. Total Wickets: {self.wickets[self.current_team]}"

        run_scored = random.choice([0, 1, 2, 3, 4, 6])
        self.scoreboard[self.current_team] += run_scored
        self.balls_played += 1

        if self.current_team == "Team B" and self.scoreboard["Team B"] > self.target:
            self.game_over = True
            return f"{self.current_team} wins by {self.scoreboard['Team B'] - self.target} runs!"

        if self.balls_played == self.overs * self.balls_per_over:
            return self.end_innings()

        return f"Ball {self.balls_played}: {run_scored} runs scored. Current Score: {self.scoreboard[self.current_team]}"

    def end_innings(self):
        if self.current_team == "Team A":
            self.target = self.scoreboard["Team A"] + 1
            self.current_team = "Team B"
            self.balls_played = 0
            return f"End of innings. Team B needs {self.target} to win."
        else:
            self.game_over = True
            return self.determine_winner()

    def determine_winner(self):
        if self.scoreboard["Team A"] == self.scoreboard["Team B"]:
            return "Match Drawn!!"
        else:
            winner = "Team A" if self.scoreboard["Team A"] > self.scoreboard["Team B"] else "Team B"
            runs_difference = abs(self.scoreboard["Team A"] - self.scoreboard["Team B"])
            return f"{winner} wins by {runs_difference} runs"


# Streamlit App
st.title("Interactive Cricket Game")

if 'game' not in st.session_state:
    st.session_state.game = CricketGame()

game = st.session_state.game

if st.button("Play Ball"):
    result = game.play_ball()
    st.write(result)
    st.write(
        f"Scoreboard:\n Team A: {game.scoreboard['Team A']} ({game.wickets['Team A']} wickets) | Team B: {game.scoreboard['Team B']} ({game.wickets['Team B']} wickets)")

if game.game_over:
    st.write("🏏 Game Over! Restart to play again.")
    if st.button("Restart Game"):
        st.session_state.game = CricketGame()

# Visualization
fig, ax = plt.subplots()
ax.bar(["Team A", "Team B"], [game.scoreboard["Team A"], game.scoreboard["Team B"]], color=["blue", "red"])
ax.set_ylabel("Runs")
ax.set_title("Team Runs Comparison")
st.pyplot(fig)
