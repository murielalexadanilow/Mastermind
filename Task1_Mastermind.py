import streamlit as st
import random

# title
st.title("Mastermind")
st.write("Are you a mastermind?")

# Rules
st.subheader("How to play")

st.write("""
Guess the secret combination of 4 colors!

- Choose 4 colors from the 6 available colors.
- You have 8 attempts to find the correct combination.
- After each guess, you receive feedback:
    - **Correct colors:** The number of colors that are in the secret combination but in the wrong position.
    - **Correct positions:** The number of colors that are in both the correct color and the correct position.
- Colors can appear more than once.
- Find all 4 correct positions to win!
""")

# Create 6 colors
colors = ["red", "blue", "green", "yellow", "purple", "orange"]

# Compare the user's guess with the secret sequence
# Count correct colors and correct positions separately.
def evaluate_guess (secret, guess):

    # Initialize return values
    correct_placement = 0
    correct_color = 0

    # Duplicate secret to track the remaining colors
    remaining_secret = secret.copy()
    
    # Compare colors at the same position
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            correct_placement +=1
            # Delete matched colors
            remaining_secret.remove(secret[i])

    # Compare colors regardless of position
    for j in range(len(guess)):
        if guess[j] in remaining_secret:
            correct_color +=1
            remaining_secret.remove(guess[j])

    return correct_color, correct_placement

# Make it real colors: display a list of colors as colored circles
def display_colors(color_list):
    circles = ""

    for color in color_list:
        circles += f"""
        <span style="
            display: block;
            width: 30px;
            height: 30px;
            min-width: 30px;
            background-color: {color};
            border-radius: 50%;
            border: 1px solid #888;
        "></span>
        """

    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 10px;
            padding: 5px 0;
            width: 100%;
        ">
            {circles}
        </div>
        """,
        unsafe_allow_html=True
    )

# Create a random color sequence --> should not be generated each rerun
# secret = random.choices(colors, k = 4)
if "secret" not in st.session_state:
    st.session_state.secret = random.choices(colors, k=4)

# Initialize game variables for stats later
if "guesses" not in st.session_state:
    st.session_state.guesses = []

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "games_played" not in st.session_state:
    st.session_state.games_played = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "guesses_per_game" not in st.session_state:
    st.session_state.guesses_per_game = []

# Create colums for display
col1, col2, col3, col4 = st.columns(4)

# Create colums for display and create in each the selectboxes with the color in right colums
with col1:
    color1 = st.selectbox("Position 1", colors, index=None, placeholder="Choose a color")

with col2:
    color2 = st.selectbox("Position 2", colors, index=None, placeholder="Choose a color")

with col3:
    color3 = st.selectbox("Position 3", colors, index=None, placeholder="Choose a color")

with col4:
    color4 = st.selectbox("Position 4", colors, index=None, placeholder="Choose a color")

# Display the currently selected colors
current_guess = [color1, color2, color3, color4]

if None not in current_guess:
    st.write("Your current guess:")
    display_colors(current_guess)

# Create a button to submit the save user's guesses
if st.button("Submit guess"):

    # Combine the four selected colors into one list
    guess = [color1, color2, color3, color4]

    # Check whether the user has selected all four colors
    if None in guess:
        st.warning("Select all four colors!")

    # Check whether the game has already ended
    # If user must start a new game to keep guessing
    elif st.session_state.game_over:
        st.warning("Please start a new game!")

    else:
        # Compare the user's guess with the secret color sequence
        # The function returns the number of correct colors
        # and correct positions
        correct_color, correct_placement = evaluate_guess(
            st.session_state.secret, guess
        )

        # Save the current guess in the list of previous guesses ans also the feedback
        st.session_state.guesses.append({
            "guess": guess,
            "correct_color": correct_color,
            "correct_placement": correct_placement
})

        # Display the feedback to the user
        st.write(f"Correct colors: {correct_color}")
        st.write(f"Correct positions: {correct_placement}")

        # Check whether all four colors are in the correct position (WIN)
        if correct_placement == 4:
            st.success("You won!")

            # Increase the total number of wins by one
            st.session_state.wins += 1

            # Mark the game as finished
            st.session_state.game_over = True

        # Check whether the user has used all eight attempts
        elif len(st.session_state.guesses) == 8:
            st.error("Game over!")

            # Reveal the secret sequence if the user has lost
            st.write(f"The secret was: {st.session_state.secret}")

            # Mark the game as finished
            st.session_state.game_over = True

        # If the game has ended, update the statistics
        if st.session_state.game_over:

            # Increase the total number of completed games by one
            st.session_state.games_played += 1

            # Save the number of attempts used in this game
            # len() counts the number of guesses in the list
            st.session_state.guesses_per_game.append(
                len(st.session_state.guesses)
            )

# Create a button to start a new game
if st.button("New Game"):

    # Generate a new random secret sequence
    st.session_state.secret = random.choices(colors, k=4)

    # Reset the guesses for new game
    st.session_state.guesses = []

    # Set game status back to active
    st.session_state.game_over = False

    # Rerun app to display the new game
    st.rerun()


# Display previous guesses using Streamlit chat messages
st.subheader("Game History")

for i, attempt in enumerate(st.session_state.guesses):

    # Display the users guess as colored circles
    with st.chat_message("user"):
        st.write(f"Attempt {i+1}:")
        display_colors(attempt["guess"])

    # Display the feedback for the respective guess
    with st.chat_message("assistant"):
        st.write(f"Correct colors: {attempt['correct_color']}")
        st.write(f"Correct positions: {attempt['correct_placement']}")