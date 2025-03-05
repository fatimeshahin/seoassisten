import streamlit as st
import openai
import pandas as pd
import os

# Setting the CSV filename for storing history
history_file = "response_history.csv"


# Function for loading session history
def display_session_history():
    if "history" in st.session_state:
        return st.session_state.history
    return []


# Function to save new responses to the CSV file only for the current session
def save_history_csv():
    if "history" in st.session_state and len(st.session_state.history) > 0:
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

# Title and caption
st.title("🤖🔍 SEO-Assistent")
st.caption(
    "🚀 Generieren Sie Keyword-Listen, SEO-optimierte Blogbeiträge und analysieren Sie Suchvolumen!"
)

# OpenAI client initialization
client = openai.OpenAI(api_key=openai_api_key)


# Function to generate a list of 30 keywords
def generate_keywords_list(topic):
    prompt = f""" Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, eine Liste mit 30 SEO-Keywords für das Thema '{topic}' zu erstellen.  
Berücksichtige dabei folgende Kriterien:  
- Priorisiere Keywords mit einem hohen monatlichen Suchvolumen (mindestens 1.000 Suchanfragen pro Monat).  
- Bevorzuge Suchbegriffe, die in Google Keyword Planner oder anderen SEO-Tools hohe Werte haben.  
- Erstelle eine Mischung aus **Head Keywords** (breit gefächerte Begriffe mit hohem Suchvolumen) und **Long-Tail-Keywords** (spezifische Suchanfragen mit klarer Suchintention).  
- Vermeide unnötig lange oder zu komplizierte Phrasen.  

**Beispiel für eine gute Liste:**  
- Katze kaufen  
- Katzenrassen Vergleich  
- Katzenfutter ohne Getreide  
- Katze anschaffen Kosten  
- Katzenkratzbaum kaufen  
- Wohnungskatze oder Freigänger  
- Beste Katzenrasse für Allergiker  
- Katzenversicherung Vergleich  
- Katze allein zuhause lassen  
- Erstausstattung für Katzen  
Achte darauf, dass die Liste eine Vielfalt an Keywords enthält. Versuche, nicht jedes Keyword mit dem Thema zu beginnen. Verwende verschiedene Varianten und relevante Begriffe rund um das Thema, um die Liste abwechslungsreicher zu gestalten.
Gib nur die Liste mit den Keywords aus, ohne zusätzliche Erklärungen.
    Gruppiere die Keywords nach ihrer Nutzerintention und füge für jede Kategorie passende Long-Tail-Varianten hinzu.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Generieren von Keywords: {e}")
        return None


# Function to generate an SEO-optimized blog post
def generate_blog_post(topic, keywords):
    prompt = f"""Schreibe einen ausführlichen, SEO-optimierten Blogpost über das Thema '{topic}'.
Verwende dabei folgende Keywords: {', '.join(keywords)}.
Der Blogpost sollte eine klare Struktur mit Überschriften (H2, H3) haben, relevante Absätze enthalten und sowohl informativ als auch ansprechend für den Leser sein.
Gib nur den Blogpost-Text aus, ohne zusätzliche Erklärungen.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler beim Generieren des Blogposts: {e}")
        return None


# Initialize session state if not yet
if "history" not in st.session_state:
    st.session_state.history = []

# Instructions
topic = st.text_input("Geben Sie ein Thema für die Keyword-Recherche ein:")

# Generate keywords list button
if st.button("Keywords generieren") and openai_api_key:
    with st.spinner("Generiere Keywords..."):
        keywords = generate_keywords_list(topic)
        if keywords:
            st.session_state.keywords = (
                keywords  # Store generated keywords in session state
            )
            st.text_area("Generierte Keywords (30):", "\n".join(keywords), height=300)
            st.session_state.history.append(
                {"type": "Keywords", "content": "\n".join(keywords)}
            )  # Save to session history

# Generate blog post button
if "keywords" in st.session_state and st.button("Blogpost generieren"):
    with st.spinner("Generiere Blogpost..."):
        blog_post = generate_blog_post(topic, st.session_state.keywords)
        if blog_post:
            st.text_area("Generierter Blogpost:", blog_post, height=500)
            st.session_state.history.append(
                {"type": "Blogpost", "content": blog_post}
            )  # Save to session history

# Display response history
st.write("### Antwortverlauf")
if st.session_state.history:
    for entry in st.session_state.history:
        st.write(f"**{entry['type']}:** {entry['content']}")

# Button to download the CSV file
if st.button("Antwortverlauf herunterladen"):
    save_history_csv()
    with open(history_file, "rb") as f:
        st.download_button(
            "Download CSV", f, file_name="response_history.csv", mime="text/csv"
        )

# Reset history when new session started
if topic:
    if st.button("Neues Thema starten"):
        reset_history()
