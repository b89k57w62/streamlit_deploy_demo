import streamlit as st
import time

st.title("Create a fragment across multiple containers")

row1 = st.columns(3)
row2 = st.columns(3)

grid = [col.container(height=200) for col in row1 + row2]
safe_grid = [card.empty() for card in grid] #DeltaGenerator

def black_cats():
    st.title("🐈‍⬛ 🐈‍⬛")
    st.markdown("🐾 🐾 🐾 🐾")


def orange_cats():
    st.title("🐈 🐈")
    st.markdown("🐾 🐾 🐾 🐾")


@st.fragment
def herd_black_cats(card_a, card_b, card_c):
    time.sleep(1.5)
    st.button(
        "Herd the black cats"
    )  # only rerun within this function scope, due to decorator
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        black_cats()
    with container_b:
        black_cats()
    with container_c:
        black_cats()


@st.fragment
def herd_orange_cats(card_a, card_b, card_c):
    time.sleep(1.5)
    st.button("Herd the orange cats")
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        orange_cats()
    with container_b:
        orange_cats()
    with container_c:
        orange_cats()


with st.sidebar:
    herd_black_cats(safe_grid[0], safe_grid[2], safe_grid[4])
    herd_orange_cats(safe_grid[1], safe_grid[3], safe_grid[5])
    st.button("Herd all the cats")
