import streamlit as st
import openai
import pandas as pd
import os

# Set the CSV filename for storing history
history_file = "response_history.csv"


# Function for loading session history
def display_session_history():
    return st.session_state.history if "history" in st.session_state else []


# Function to save new responses to the CSV file only for the current session
def save_history_csv():
    if "history" in st.session_state and st.session_state.history:
        new_entry = pd.DataFrame(st.session_state.history)
        new_entry.to_csv(history_file, mode="w", header=True, index=False)


# Function to reset session history
def reset_history():
    if "history" in st.session_state:
        st.session_state.history = []


# Sidebar for API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API-Schlüssel", type="password")
    st.markdown(
        "[Erhalten Sie einen OpenAI API-Schlüssel](https://platform.openai.com/account/api-keys)"
    )


# Initialize OpenAI Client
def get_openai_client():
    return openai.OpenAI(api_key=openai_api_key) if openai_api_key else None


# Function to generate a list of 30 keywords
def generate_keywords_list(topic):
    client = get_openai_client()
    if not client:
        st.error("Bitte geben Sie Ihren OpenAI API-Schlüssel ein.")
        return None

    prompt = f""" Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, eine Liste mit 30 SEO-Keywords für das Thema '{topic}' zu erstellen... """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Generieren von Keywords: {e}")
        return None


# Function to select the top 10 keywords
def select_top_keywords(keywords):
    client = get_openai_client()
    if not client:
        return None

    prompt = f"Aus der folgenden Liste von Keywords wähle die top zehn aus: {', '.join(keywords)}."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Auswählen der Top-Keywords: {e}")
        return None


# Function to group keywords by topic
def group_keywords(keywords):
    client = get_openai_client()
    if not client:
        return None

    prompt = f"Gruppiere die folgenden Top 10 Keywords in relevante Themen: {', '.join(keywords)}."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler beim Gruppieren von Keywords: {e}")
        return None


# Function for blog post generation
def write_blog_post(topic, keywords):
    client = get_openai_client()
    if not client:
        return None

    prompt = f""" Du bist ein erfahrener SEO-Texter. Schreibe einen hochwertigen Blogartikel über **{topic}** mit den Keywords **{', '.join(keywords)}**... """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler beim Generieren des Blogbeitrags: {e}")
        return None


# Function for user prompt
def user_prompt_response(prompt_response):
    client = get_openai_client()
    if not client:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_response}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler beim Generieren einer Antwort: {e}")
        return None


# Initialize session state if not yet
if "history" not in st.session_state:
    st.session_state.history = []

# User input for topic
topic = st.text_input("Geben Sie ein Thema für die Keyword-Recherche ein:")

# Buttons and actions
if st.button("Keywords generieren") and openai_api_key:
    with st.spinner("Generiere Keywords..."):
        keywords = generate_keywords_list(topic)
        if keywords:
            st.session_state.keywords = keywords
            st.text_area("Generierte Keywords (30):", "\n".join(keywords), height=300)
            st.session_state.history.append(
                {"type": "Keywords", "content": "\n".join(keywords)}
            )

if st.button("Top 10 Keywords auswählen") and openai_api_key:
    with st.spinner("Wähle die Top 10 Keywords aus..."):
        if "keywords" in st.session_state:
            top_keywords = select_top_keywords(st.session_state.keywords)
            if top_keywords:
                st.session_state.top_keywords = top_keywords
                st.text_area("Top 10 Keywords:", "\n".join(top_keywords), height=100)
                st.session_state.history.append(
                    {"type": "Top 10 Keywords", "content": "\n".join(top_keywords)}
                )

if st.button("Blogbeitrag generieren") and openai_api_key:
    with st.spinner("Generiere Blogbeitrag..."):
        if "top_keywords" in st.session_state:
            blog_post = write_blog_post(topic, st.session_state.top_keywords)
            if blog_post:
                st.text_area("Generierter Blogbeitrag:", blog_post, height=300)
                st.session_state.history.append(
                    {"type": "Blogbeitrag", "content": blog_post}
                )

# Display response history
st.write("### Antwortverlauf")
if st.session_state.history:
    for entry in st.session_state.history:
        st.write(f"**{entry['type']}:** {entry['content']}")

# Download CSV file
if st.button("Antwortverlauf herunterladen"):
    save_history_csv()
    with open(history_file, "rb") as f:
        st.download_button(
            "Download CSV", f, file_name="response_history.csv", mime="text/csv"
        )

# Reset history when a new topic starts
if topic and st.button("Neues Thema starten"):
    reset_history()
