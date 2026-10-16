from lib import *
import time
import random
import argparse
import streamlit as st


# Create strealit web app
def main():
    st.title("Countdown Numbers Game Solver")

    with st.form(key="input_nums"):
        target_box = st.number_input("Target", step=1, value=1)
        input_cols = st.columns(6)
        inputs = [col.number_input(f"number_{i+1}", step=1, value=1, label_visibility="collapsed") for i, col in enumerate(input_cols)]
        st.form_submit_button("Solve")
        start_state = State([Literal(value) for value in inputs])
        st.write(f"Solution: {solve(start_state, target_box)[0]}")


if __name__ == "__main__":
    main()

