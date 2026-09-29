import streamlit as st
import requests
import random
import os
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="Movie Night Agent", page_icon="🎬")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


@tool
def search_movie(title: str) -> str:
    """Search for a movie by title and return its year, genre, and plot."""
    url = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": OMDB_API_KEY}
    data = requests.get(url, params=params).json()

    if data.get("Response") == "False":
        return f"OMDb error for '{title}': {data.get('Error')}"

    return (
        f"Title: {data['Title']}\n"
        f"Year: {data['Year']}\n"
        f"Genre: {data['Genre']}\n"
        f"Plot: {data['Plot']}"
    )


@tool
def get_movie_rating(title: str) -> str:
    """Get the IMDb rating and runtime of a movie by title."""
    url = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": OMDB_API_KEY}
    data = requests.get(url, params=params).json()

    if data.get("Response") == "False":
        return f"OMDb error for '{title}': {data.get('Error')}"

    return f"IMDb Rating: {data['imdbRating']}, Runtime: {data['Runtime']}"


MOVIE_LIST = {
    "comedy": ["Superbad", "The Hangover", "Bridesmaids"],
    "action": ["Mad Max: Fury Road", "John Wick", "Die Hard"],
    "horror": ["Hereditary", "Get Out", "A Quiet Place"],
    "romance": ["La La Land", "The Notebook", "Pride and Prejudice"],
    "sci-fi": ["Interstellar", "Arrival", "Blade Runner 2049"]
}


@tool
def pick_random_movie(genre: str) -> str:
    """Pick a random movie suggestion for a given genre, e.g. comedy, action, horror, romance, sci-fi."""
    genre = genre.lower().strip()
    if genre not in MOVIE_LIST:
        return f"No suggestions available for genre '{genre}'"
    return random.choice(MOVIE_LIST[genre])


@st.cache_resource
def load_agent():
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    tools = [search_movie, get_movie_rating, pick_random_movie]
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful movie night assistant. Use the tools to answer the user's question."
    )


agent = load_agent()

st.title("🎬 Movie Night Decision Agent")
st.caption("Ask about a movie, check its rating, or get a random pick by genre.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("What movie should we watch tonight?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
            answer = response["messages"][-1].content

            
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})