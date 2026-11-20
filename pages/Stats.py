import streamlit as st

# Set the page title
st.title("Game Statistics")

# Retrieve the game statistics from session state
games = st.session_state.get("games_played", 0)
wins = st.session_state.get("wins", 0)
guesses = st.session_state.get("guesses_per_game", [])

# Display the total number of completed games and wins
st.metric("Games played", games)
st.metric("Games won", wins)

# Calculate and display the average number of guesses
if guesses:
    average = sum(guesses) / len(guesses)
    st.metric("Average guesses per game", round(average, 2))

    # Display a bar chart showing guesses per game
    st.subheader("Guesses per game")
    st.bar_chart(guesses)

else:
    st.write("No completed games yet.")
