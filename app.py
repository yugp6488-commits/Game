import streamlit as st
import random
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Retro RPS", layout="centered")

# ------------------ SESSION STATE ------------------
if "me" not in st.session_state:
    st.session_state.me = 0
if "bot" not in st.session_state:
    st.session_state.bot = 0
if "result" not in st.session_state:
    st.session_state.result = ""
if "bot_move" not in st.session_state:
    st.session_state.bot_move = ""
if "history" not in st.session_state:
    st.session_state.history = []

choices = ["rock", "paper", "scissor"]

# ------------------ LOGIC ------------------
def play(user_move):
    bot_move = random.choice(choices)
    st.session_state.bot_move = bot_move

    if user_move == bot_move:
        st.session_state.result = "⚖️ TIE"
    elif (user_move == "rock" and bot_move == "scissor") or \
         (user_move == "paper" and bot_move == "rock") or \
         (user_move == "scissor" and bot_move == "paper"):
        st.session_state.me += 1
        st.session_state.result = "🟢 YOU WIN"
    else:
        st.session_state.bot += 1
        st.session_state.result = "🔴 BOT WINS"

    # Save history
    st.session_state.history.append({
        "You": st.session_state.me,
        "Bot": st.session_state.bot
    })

    # Game End
    if st.session_state.me == 5:
        st.session_state.result = "🏆 YOU WON THE GAME!"
        st.balloons()
        reset_scores()

    elif st.session_state.bot == 5:
        st.session_state.result = "💀 BOT DOMINATED!"
        reset_scores()

def reset_scores():
    st.session_state.me = 0
    st.session_state.bot = 0


# ------------------ RETRO STYLE ------------------
st.markdown("""
    <style>
    body {
        background-color: black;
    }
    .title {
        text-align: center;
        font-size: 50px;
        color: #00ffcc;
        text-shadow: 0 0 20px #00ffcc;
        font-family: monospace;
    }
    .score {
        text-align: center;
        font-size: 25px;
        color: #ff00ff;
        text-shadow: 0 0 10px #ff00ff;
    }
    .result {
        text-align: center;
        font-size: 30px;
        margin-top: 20px;
        color: yellow;
        text-shadow: 0 0 15px yellow;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ UI ------------------
st.markdown('<div class="title">🕹️ RETRO RPS</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="score">YOU {st.session_state.me} : {st.session_state.bot} BOT</div>',
    unsafe_allow_html=True
)

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨"):
        play("rock")

with col2:
    if st.button("📄"):
        play("paper")

with col3:
    if st.button("✂️"):
        play("scissor")

# Result Display
if st.session_state.result:
    st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)

if st.session_state.bot_move:
    st.write(f"🤖 Bot chose: **{st.session_state.bot_move.upper()}**")

# ------------------ GRAPH ------------------
if len(st.session_state.history) > 0:
    st.subheader("📊 Score Progress")

    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df)

# ------------------ RESET ------------------
if st.button("🔄 RESET GAME"):
    st.session_state.me = 0
    st.session_state.bot = 0
    st.session_state.history = []
    st.session_state.result = ""
    st.session_state.bot_move = ""