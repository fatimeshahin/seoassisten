# importing all the needed libraries

import os

import openai
import pandas as pd
import streamlit as st

# seting the CSV filename for storing history
history_file = "response_history.csv"


# function for loading session history
def display_session_history():
    if "history" in st.session_state:
        return st.session_state.history
    return []


# function to save new responses to the CSV file only for the current session
def save_history_csv():
    if "history" in st.session_state and len(st.session_state.history) > 0:
        new_entry = pd.DataFrame(st.session_state.history)
        new_entry.to_csv(history_file, mode="w", header=True, index=False)


# function to reset session history
def reset_history():
    if "history" in st.session_state:
        st.session_state.history = []


# sidebar for API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API-Schlüssel", type="password")
    st.markdown(
        "[Erhalten Sie einen OpenAI API-Schlüssel](https://platform.openai.com/account/api-keys)"
    )

# title and caption
st.title("🤖🔍 SEO-Assistent")
st.caption(
    "🚀 Generieren Sie Keyword-Listen, SEO-optimierte Blogbeiträge und analysieren Sie Suchvolumen!"
)


# function to generate a list of 30 keywords
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
- Achte darauf, dass die Liste eine Vielfalt an Keywords enthält. Versuche, nicht jedes Keyword mit dem Thema zu beginnen. Verwende verschiedene Varianten und relevante Begriffe rund um das Thema, um die Liste abwechslungsreicher zu gestalten.
Gib nur die Liste mit den Keywords aus, ohne zusätzliche Erklärungen.
    Gruppiere die Keywords nach ihrer Nutzerintention und füge für jede Kategorie passende Long-Tail-Varianten hinzu.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, hochwertige SEO-optimierte Inhalte zu generieren, Keywords zu analysieren und basierend auf bewährten SEO-Prinzipien Empfehlungen zu geben.",
                },
            ],
            api_key=openai_api_key,
        )
        return response["choices"][0]["message"]["content"].strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Generieren von Keywords: {e}")
        return None


# function to select the top 10 keywords
def select_top_keywords(keywords):
    prompt = f"Aus der folgenden Liste von Keywords wähle die top zehn relevantesten basierend auf Relevanz und Suchpotential aus: {', '.join(keywords)}."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, hochwertige SEO-optimierte Inhalte zu generieren, Keywords zu analysieren und basierend auf bewährten SEO-Prinzipien Empfehlungen zu geben.",
                },
                {"role": "user", "content": prompt},
            ],
            api_key=openai_api_key,
        )
        return response["choices"][0]["message"]["content"].strip().split("\n")
    except Exception as e:
        st.error(f"Fehler beim Auswählen der Top-Keywords: {e}")
        return None


# function to group keywords by topic
def group_keywords(keywords):
    prompt = f"Gruppiere die folgenden Top 10 Keywords in relevante Themen mit kurzen Beschreibungen: {', '.join(keywords)}."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, hochwertige SEO-optimierte Inhalte zu generieren, Keywords zu analysieren und basierend auf bewährten SEO-Prinzipien Empfehlungen zu geben.",
                },
            ],
            api_key=openai_api_key,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"Fehler beim Gruppieren von Keywords: {e}")
        return None


# function for blog post generation
def write_blog_post(topic, keywords):
    prompt = f""" Du bist ein erfahrener SEO-Texter. Schreibe einen hochwertigen, SEO-optimierten Blogartikel über **{topic}**. Der Artikel soll informativ, ansprechend und gut lesbar und leicht verständlich sein.
    Integriere die folgenden Keywords **{', '.join(keywords)}** auf natürliche Weise in den Text. Vermeide dabei eine zu direkte Aufzählung der Keywords oder eine bestimmte Reihenfolge, sondern stelle sicher, dass sie fließend im gesamten Text eingebaut werden, ohne jede Abschnit mit einem Keyword zu beginnen. 
    Orientiere  dich auch hier an der verspielten Tonalität. Der Beitrag soll ein Hauptüberschrift (H1), Zwischenüberschriften (H2) und Unterübeschriften enthalten.
    Der Blogartikel soll den Leser durch relevante und spannende Informationen führen. 
    Achte darauf, dass der Text sowohl für den Leser als auch für Suchmaschinen ansprechend ist. Es sollte ein klarer Mehrwert geboten werden, und die Keywords sollen in einem natürlichen Kontext verwendet werden, ohne den Lesefluss zu stören. 
    Verwende den Schreibstil eines erfahrenen Bloggers, der informativ und zugleich unterhaltsam ist. Schaffe einen Blogbeitrag, der sowohl Fragen der Leser beantwortet als auch ihre Neugier weckt, ohne dass es zu einem starren, strukturierten Text wird. Vermeide dabei Modalwörter und Substantivierungen. Schreibe aktiv und nutze verschiedenen Sätzlängerungen - aber keine verschachtelten Sätze. Halte eine gute Qualität beim Schreiben und bitte original schreiben. 
    Stellst du sicher, dass du einen Call to Action hinzufügen.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, hochwertige SEO-optimierte Inhalte zu generieren, Keywords zu analysieren und basierend auf bewährten SEO-Prinzipien Empfehlungen zu geben.",
                },
            ],
            api_key=openai_api_key,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"Fehler beim Generieren des Blogbeitrags: {e}")
        return None


# function for user prompt
def user_response(user_prompt_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_prompt_input},
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener SEO-Experte. Deine Aufgabe ist es, hochwertige SEO-optimierte Inhalte zu generieren, Keywords zu analysieren und basierend auf bewährten SEO-Prinzipien Empfehlungen zu geben.",
                },
            ],
            api_key=openai_api_key,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(
            f"Fehler beim Generieren einer Antwort auf die benutzerdefinierte Eingabeaufforderung: {e}"
        )
        return None


# initialize session state if not yet
if "history" not in st.session_state:
    st.session_state.history = []

# instructions
topic = st.text_input("Geben Sie ein Thema für die Keyword-Recherche ein:")

# generate keywords list button
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

# select top 10 keywords button
if st.button("Top 10 Keywords auswählen") and openai_api_key:
    with st.spinner("Wähle die Top 10 Keywords aus..."):
        if "keywords" in st.session_state:
            top_keywords = select_top_keywords(st.session_state.keywords)
            if top_keywords:
                st.session_state.top_keywords = (
                    top_keywords  # Store top keywords in session state
                )
                st.text_area("Top 10 Keywords:", "\n".join(top_keywords), height=100)
                st.session_state.history.append(
                    {"type": "Top 10 Keywords", "content": "\n".join(top_keywords)}
                )  # Save to session history

# group top 10 keywords button
if st.button("Top 10 Keywords gruppieren") and openai_api_key:
    with st.spinner("Gruppiere die Top 10 Keywords..."):
        if "top_keywords" in st.session_state:
            grouped_keywords = group_keywords(st.session_state.top_keywords)
            if grouped_keywords:
                st.session_state.grouped_keywords = (
                    grouped_keywords  # Store grouped keywords in session state
                )
                st.text_area("Gruppierte Keywords:", grouped_keywords, height=300)
                st.session_state.history.append(
                    {"type": "Gruppierte Keywords", "content": grouped_keywords}
                )  # Save to session history

# generate blog post button
if st.button("Blogbeitrag generieren") and openai_api_key:
    with st.spinner("Generiere Blogbeitrag..."):
        if "top_keywords" in st.session_state:
            blog_post = write_blog_post(topic, st.session_state.top_keywords)
            if blog_post:
                st.text_area("Generierter Blogbeitrag:", blog_post, height=300)
                st.session_state.history.append(
                    {"type": "Blogbeitrag", "content": blog_post}
                )  # Save to session history

# user prompt area
user_prompt_input = st.text_area("Write your prompt here")
user_response_content = None
if st.button("Run") and openai_api_key:
    with st.spinner("Antwort generieren..."):
        user_response_content = user_response(
            user_prompt_input
        )  # Changed to call the function correctly
if user_response_content:
    st.text_area("Generierte Antwort:", user_response_content, height=300)
    st.session_state.history.append(
        {"type": "Benutzerdefinierte Antwort", "content": user_response_content}
    )  # Save to session history

# display response history
st.write("Antwortverlauf")
if st.session_state.history:
    for entry in st.session_state.history:
        st.write(f"**{entry['type']}:** {entry['content']}")

# button to download the CSV file
if st.button("CVS file herunterladen"):
    save_history_csv()
with open(history_file, "rb") as f:
    st.download_button(
        "Download CSV file", f, file_name="response_history.csv", mime="text/csv"
    )

# reset history when new session started
if topic:
    if st.button("Neues Thema starten"):
        reset_history()
