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
        "[Erhalte einen OpenAI API-Schlüssel](https://platform.openai.com/account/api-keys)"
    )

# Title and caption
st.title("🤖🔍 SEO-Assistent")
st.caption("🚀 Generiere Keyword-Listen und erstelle SEO-optimierte Blogbeiträge!")

# OpenAI client initialization
client = openai.OpenAI(api_key=openai_api_key)


# Function to generate a list of 30 keywords
def generate_keywords_list(topic):
    prompt = f""" Du bist ein erfahrener SEO-Experte mit spezialisiertem Wissen Bereich E-Commerce. Deine Aufgabe ist es, eine Liste von 30 relevanten und hochvolumigen SEO-Suchbegriffen für das Thema ''{topic}'' zu erstellen. Berücksichtige folgende Kriterien:

-Priorisiere Suchbegriffen mit hohem monatlichen Suchvolumen aus Google Keyword Planner oder anderen vertrauenswürdigen SEO-Tools.
- Die Suchbegriffen sollen minimal 1 und maximal 3 Wörter enthalten.
- Fokussiere dich auf produktbezogene Keywords!
- Kombiniere Head Keywords (breite Begriffe mit hohem Suchvolumen) und Long-Tail-Keywords (spezifische Suchanfragen mit klarer Suchintention).
- Berücksichtige kommerzielle Relevanz: Wähle Begriffe, die Nutzer mit einer Kauf- oder Informationsabsicht suchen könnten.
- Achte auf eine sinnvolle Keyword-Diversität, um verschiedene Aspekte des Themas abzudecken (z. B. Material, Zielgruppe: Damen, Herren und Kinder, Saison: Frühling).
- Beziehe dich auf aktuelle trends, insbesondere für 2025.
-Bitte liefere genau 30 Keywords. 

Beispiel für eine gute Liste:

bio-baumwolle kleidung kaufen
nachhaltige mode aus bio-baumwolle
bio baumwolle kleidung damen
bio baumwolle kleidung männer
bio-baumwolle kleidung 2025
bio baumwollkleidung
bio-baumwolle vs. konventionelle Baumwolle
beste marken für nachhaltige kleidung
nachhaltige mode online shops
nachhaltige mode trends
bio klamotten
bio baumwolle t shirt
frühling mode 2025"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Generieren von Keywords: {e}")
        return None


# Function to select top keywords
def select_top_keywords(keywords):
    prompt = f"Aus der folgenden Liste von Keywords wähle die zehn relevantesten basierend auf Relevanz und Suchpotential aus: {', '.join(keywords)}."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "system", "content": "Du bist ein erfahrener SEO-Experte."},
            ],
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Auswählen der Top-Keywords: {e}")
        return None


# Function to group keywords by topic
def group_keywords(keywords):
    prompt = f"Gruppiere die folgenden Keywords in relevante Themen mit kurzen Beschreibungen und teile sie nach Suchintention in 3 Gruppen: Navigational, Transactional und Informational. : {', '.join(keywords)}."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "system", "content": "Du bist ein erfahrener SEO-Experte."},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler beim Gruppieren von Keywords: {e}")
        return None


# Function to generate an SEO-optimized blog post
def generate_blog_post(topic, keywords):
    prompt = f"""Du bist ein erfahrener SEO-Experte mit spezialisiertem Wissen im Bereich E-Commerce und On-Page SEO. Deine Aufgabe ist es, einen ausführlichen, SEO-optimierten Blogpost über das Thema '{topic}' zu schreiben.
Verwendet werden sollen die folgenden Keywords: {', '.join(keywords)}. Berücksichtige folgende Kriterien:
-Der Blogpost soll eine **klare Struktur mit Überschriften (H1 und H2 in fett geschrieben)** haben.
-Der Text soll 500 Wörter lang sein.
-Qualität und Originalität: Der Text muss hohe Qualität und Originalität aufweisen und den Leser sowohl informieren als auch ansprechen.
Keyword-Integration: Integriere die Keywords sinnvoll in den Text. Vermeide Keyword-Stuffing, aber stelle sicher, dass die Keywords in einem natürlichen Kontext erscheinen und für die Lesbarkeit und Relevanz des Textes wichtig sind.
Die Keywords sollen auf keine bestimmte Reinfolge sein und müssten nicht mit Zahlen aufgelistät werden sonder rein im Text eingebaut.
Tonalität: Nutze aktive, aber pröffesionäle und kreative Sprache („Wir bieten…“ statt „Es wird angeboten…“)
Kommerzielle Relevanz: Der Blogpost soll sowohl informativ als auch conversion-orientiert sein und den Leser's Kaufintension zu steigern.
SEO-Fokus: Achte darauf, dass der Blogpost SEO-optimiert ist, indem du die Keywords in den Absätzen, Überschriften und innerhalb des Textes sinnvoll einfügst.
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


# user prompt function
def user_prompt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Fehler bei der Verarbeitung des Benutzer-Prompts: {e}")
        return None


# Initialize session state if not yet
if "history" not in st.session_state:
    st.session_state.history = []

# Instructions
topic = st.text_input("Gib hier ein Thema für die Keyword-Recherche ein:")

# Generate keywords list button
if st.button("Keywords generieren") and openai_api_key:
    with st.spinner("Generiere Keywords..."):
        keywords = generate_keywords_list(topic)
        if keywords:
            st.session_state.keywords = (
                keywords  # Store generated keywords in session state
            )
            st.text_area("Generierte Keywords (30):", "\n".join(keywords), height=250)
            st.session_state.history.append(
                {"type": "Keywords", "content": "\n".join(keywords)}
            )  # Save to session history

# Select top 10 keywords button
if "keywords" in st.session_state and st.button("Top 10 Keywords auswählen"):
    with st.spinner("Top 10 Keywords werden ausgewählt..."):
        top_keywords = select_top_keywords(st.session_state.keywords)
        if top_keywords:
            st.session_state.top_keywords = top_keywords
            st.text_area("Top 10 Keywords:", "\n".join(top_keywords), height=300)
            st.session_state.history.append(
                {"type": "Top 10 Keywords", "content": "\n".join(top_keywords)}
            )  # Save to session history

# Group keywords button
if "keywords" in st.session_state and st.button("Keywords gruppieren"):
    with st.spinner("Keywords werden gruppiert..."):
        grouped_keywords = group_keywords(st.session_state.keywords)
        if grouped_keywords:
            st.text_area("Gruppierte Keywords:", grouped_keywords, height=300)
            st.session_state.history.append(
                {"type": "Gruppierte Keywords", "content": grouped_keywords}
            )  # Save to session history

# Generate blog post button
if "top_keywords" in st.session_state and st.button("Blogpost generieren"):
    with st.spinner("Generiere Blogpost..."):
        blog_post = generate_blog_post(topic, st.session_state.top_keywords)
        if blog_post:
            st.text_area("Generierter Blogpost:", blog_post, height=500)
            st.session_state.history.append(
                {"type": "Blogpost", "content": blog_post}
            )  # Save to session history

# user prompt function initiation
user_custom_prompt = st.text_area("Deinen Prompt eingeben:")

if st.button("Prompt ausführen"):
    with st.spinner("Antwort wird generiert..."):
        if user_custom_prompt:
            custom_response = user_prompt(user_custom_prompt)
            if custom_response:
                st.text_area(
                    "Generierte Antwort:",
                    custom_response,
                    height=300,
                )
                st.session_state.history.append(
                    {"type": "Benutzerdefinierter Prompt", "content": custom_response}
                )  # Save to session history

# Display response history
st.write("Antwortverlauf")
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
