import streamlit as st
import random

# ─────────────────────────────────────────────────────────────────────────────
# VOCABULARY  (German → English, organised by topic)
# ─────────────────────────────────────────────────────────────────────────────
VOCAB: dict[str, dict[str, str]] = {

    # ── Kapitel 5.1 — Uhrzeiten ───────────────────────────────────────────────
    "⏰ Time Expressions": {
        "die Zeit": "time",
        "die Uhr": "clock / watch / o'clock",
        "die Uhrzeit": "the time of day",
        "die Stunde": "hour",
        "die Minute": "minute",
        "die Sekunde": "second",
        "Wie spät ist es?": "What time is it?",
        "Es ist … Uhr.": "It is … o'clock.",
        "morgens": "in the morning",
        "mittags": "at noon",
        "abends": "in the evening",
        "nachts": "at night",
        "kurz nach …": "just after …",
        "kurz vor …": "just before …",
        "viertel nach …": "quarter past …",
        "viertel vor …": "quarter to …",
        "halb …": "half past … (the next hour)",
        "früh": "early",
        "spät": "late",
        "pünktlich": "on time / punctual",
    },

    # ── Kapitel 5.2 — Familie ─────────────────────────────────────────────────
    "👨‍👩‍👧 Family": {
        "die Familie": "family",
        "die Mutter / Mama": "mother / mum",
        "der Vater / Papa": "father / dad",
        "die Eltern": "parents",
        "die Tochter": "daughter",
        "der Sohn": "son",
        "die Schwester": "sister",
        "der Bruder": "brother",
        "die Geschwister": "siblings",
        "die Großmutter / Oma": "grandmother / grandma",
        "der Großvater / Opa": "grandfather / grandpa",
        "die Großeltern": "grandparents",
        "die Tante": "aunt",
        "der Onkel": "uncle",
        "das Kind": "child",
        "das Baby": "baby",
        "der Mann": "husband / man",
        "die Frau": "wife / woman",
        "verheiratet": "married",
        "ledig": "single",
        "geschieden": "divorced",
        "verwitwet": "widowed",
    },

    # ── Kapitel 5.3 — Tagesablauf ─────────────────────────────────────────────
    "🌅 Daily Routine": {
        "aufstehen": "to get up",
        "aufwachen": "to wake up",
        "sich waschen": "to wash oneself",
        "sich duschen": "to shower",
        "sich anziehen": "to get dressed",
        "frühstücken": "to have breakfast",
        "zur Arbeit gehen": "to go to work",
        "arbeiten": "to work",
        "Mittagessen essen": "to eat lunch",
        "nach Hause kommen": "to come home",
        "kochen": "to cook",
        "Abendessen essen": "to eat dinner",
        "fernsehen": "to watch TV",
        "schlafen gehen": "to go to sleep",
        "schlafen": "to sleep",
        "einkaufen gehen": "to go shopping",
        "putzen": "to clean",
        "das Frühstück": "breakfast",
        "das Mittagessen": "lunch",
        "das Abendessen": "dinner",
        "die Mittagspause": "lunch break",
        "der Feierabend": "end of the working day",
    },

    # ── Kapitel 5.5 — Wohnen ──────────────────────────────────────────────────
    "🏠 Home & Living": {
        "die Wohnung": "apartment",
        "das Haus": "house",
        "das Zimmer": "room",
        "das Schlafzimmer": "bedroom",
        "das Badezimmer": "bathroom",
        "das Wohnzimmer": "living room",
        "die Küche": "kitchen",
        "der Flur": "hallway",
        "der Balkon": "balcony",
        "die Möbel": "furniture",
        "das Bett": "bed",
        "der Tisch": "table",
        "der Stuhl": "chair",
        "das Sofa": "sofa",
        "der Schrank": "wardrobe / cabinet",
        "die Lampe": "lamp",
        "das Fenster": "window",
        "die Tür": "door",
        "mieten": "to rent",
        "wohnen": "to live / reside",
        "die Miete": "rent",
        "die Nebenkosten": "additional costs / utilities",
        "das Erdgeschoss": "ground floor",
        "das Obergeschoss": "upper floor",
    },

    # ── Kapitel 6.2 — Trennbare Verben ───────────────────────────────────────
    "🔗 Separable Verbs": {
        "anfangen": "to start / begin",
        "anrufen": "to call (phone)",
        "abholen": "to pick up",
        "einladen": "to invite",
        "mitkommen": "to come along",
        "mitbringen": "to bring along",
        "aufräumen": "to tidy up",
        "anmelden": "to register",
        "ausfüllen": "to fill in (a form)",
        "umsteigen": "to change (trains/bus)",
        "einkaufen": "to go shopping",
        "aufstehen": "to get up",
        "fernsehen": "to watch TV",
        "zurückrufen": "to call back",
        "aussteigen": "to get off (transport)",
        "einsteigen": "to get on (transport)",
        "weitergehen": "to continue / go on",
        "zurückkommen": "to come back",
    },

    # ── Kapitel 6.3 — Freizeit & Hobbys ──────────────────────────────────────
    "🎉 Free Time & Hobbies": {
        "die Freizeit": "free time",
        "das Hobby": "hobby",
        "das Fest": "celebration / party",
        "das Picknick": "picnic",
        "die Party": "party",
        "die Einladung": "invitation",
        "der Ausflug": "trip / outing",
        "der Park": "park",
        "das Kino": "cinema",
        "das Theater": "theatre",
        "das Konzert": "concert",
        "das Museum": "museum",
        "das Café": "café",
        "das Restaurant": "restaurant",
        "Sport machen": "to do sport",
        "Fußball spielen": "to play football",
        "schwimmen": "to swim",
        "tanzen": "to dance",
        "lesen": "to read",
        "Musik hören": "to listen to music",
        "spazieren gehen": "to go for a walk",
        "sich treffen": "to meet (up)",
        "fotografieren": "to take photos",
        "reisen": "to travel",
        "Gitarre spielen": "to play guitar",
    },

    # ── Kapitel 6.6 — Verabredungen ───────────────────────────────────────────
    "📅 Making Arrangements": {
        "Hast du am … Zeit?": "Are you free on …?",
        "Ja, gern!": "Yes, I'd love to!",
        "Leider nicht.": "Unfortunately not.",
        "Das geht nicht.": "That doesn't work.",
        "Wir treffen uns um … Uhr.": "We'll meet at … o'clock.",
        "Wann fängt es an?": "When does it start?",
        "Wo treffen wir uns?": "Where shall we meet?",
        "Ich komme mit.": "I'll come along.",
        "Passt dir das?": "Does that suit you?",
        "Können wir das verschieben?": "Can we postpone that?",
        "Ich freue mich!": "I'm looking forward to it!",
        "Das ist super!": "That's great!",
    },

    # ── Kapitel 8.1 — Körperteile ─────────────────────────────────────────────
    "🫀 Body Parts": {
        "der Kopf": "head",
        "das Haar": "hair",
        "das Gesicht": "face",
        "das Auge": "eye",
        "das Ohr": "ear",
        "die Nase": "nose",
        "der Mund": "mouth",
        "der Zahn": "tooth",
        "der Hals": "neck / throat",
        "die Schulter": "shoulder",
        "der Arm": "arm",
        "der Ellenbogen": "elbow",
        "die Hand": "hand",
        "der Finger": "finger",
        "die Brust": "chest",
        "der Bauch": "stomach / belly",
        "der Rücken": "back",
        "das Bein": "leg",
        "das Knie": "knee",
        "der Fuß": "foot",
        "der Zeh": "toe",
        "der Nacken": "nape / back of neck",
        "die Stirn": "forehead",
    },

    # ── Kapitel 8.2 — Krankheiten ─────────────────────────────────────────────
    "🤒 Health & Illness": {
        "krank": "sick / ill",
        "gesund": "healthy",
        "die Krankheit": "illness",
        "die Erkältung": "cold",
        "der Husten": "cough",
        "der Schnupfen": "runny nose",
        "das Fieber": "fever",
        "die Grippe": "flu",
        "die Kopfschmerzen": "headache",
        "die Bauchschmerzen": "stomach ache",
        "die Halsschmerzen": "sore throat",
        "die Rückenschmerzen": "back pain",
        "die Zahnschmerzen": "toothache",
        "der Schmerz": "pain",
        "wehtun": "to hurt",
        "Mir ist schlecht.": "I feel sick / nauseous.",
        "Ich fühle mich nicht gut.": "I don't feel well.",
        "Ich habe Fieber.": "I have a fever.",
        "Mein … tut weh.": "My … hurts.",
        "sich erholen": "to recover",
        "Gute Besserung!": "Get well soon!",
    },

    # ── Kapitel 8.3 — Beim Arzt ───────────────────────────────────────────────
    "🏥 At the Doctor": {
        "der Arzt / die Ärztin": "doctor",
        "das Krankenhaus": "hospital",
        "die Praxis": "(doctor's) practice",
        "der Termin": "appointment",
        "das Rezept": "prescription",
        "die Tablette": "tablet / pill",
        "das Medikament": "medicine",
        "das Pflaster": "plaster / band-aid",
        "die Krankenversicherung": "health insurance",
        "Was fehlt Ihnen?": "What is wrong with you?",
        "Wo tut es weh?": "Where does it hurt?",
        "Seit wann?": "Since when?",
        "Ich brauche einen Termin.": "I need an appointment.",
        "im Bett bleiben": "to stay in bed",
        "viel trinken": "to drink a lot",
        "sich ausruhen": "to rest",
        "Trinken Sie viel Wasser!": "Drink lots of water!",
        "Nehmen Sie die Tabletten!": "Take the tablets!",
        "Bleiben Sie im Bett!": "Stay in bed!",
    },

    # ── Sich vorstellen ───────────────────────────────────────────────────────
    "👋 Introducing Yourself": {
        "Wie heißen Sie?": "What is your name?",
        "Mein Name ist …": "My name is …",
        "Wie ist Ihr Familienname?": "What is your surname?",
        "Wie ist Ihr Vorname?": "What is your first name?",
        "Wie alt sind Sie?": "How old are you?",
        "Ich bin … Jahre alt.": "I am … years old.",
        "Woher kommen Sie?": "Where do you come from?",
        "Ich komme aus …": "I come from …",
        "Wo wohnen Sie?": "Where do you live?",
        "Ich wohne in …": "I live in …",
        "Was sind Sie von Beruf?": "What is your job?",
        "Welche Sprachen sprechen Sie?": "Which languages do you speak?",
        "Ich spreche Deutsch und Englisch.": "I speak German and English.",
        "Was machen Sie in Ihrer Freizeit?": "What do you do in your free time?",
        "Ich bin verheiratet.": "I am married.",
        "Ich bin ledig.": "I am single.",
        "Schön, Sie kennenzulernen!": "Nice to meet you!",
        "Auf Wiedersehen!": "Goodbye!",
        "Tschüss!": "Bye!",
        "Guten Morgen!": "Good morning!",
        "Guten Tag!": "Good day / Hello!",
        "Guten Abend!": "Good evening!",
    },

    # ── Essen & Trinken ───────────────────────────────────────────────────────
    "🍎 Food & Drink": {
        "das Brot": "bread",
        "das Brötchen": "bread roll",
        "der Käse": "cheese",
        "die Butter": "butter",
        "das Ei": "egg",
        "der Apfel": "apple",
        "die Banane": "banana",
        "die Erdbeere": "strawberry",
        "die Tomate": "tomato",
        "die Kartoffel": "potato",
        "das Gemüse": "vegetables",
        "das Obst": "fruit",
        "das Fleisch": "meat",
        "der Fisch": "fish",
        "die Nudel": "pasta / noodle",
        "der Reis": "rice",
        "die Suppe": "soup",
        "der Salat": "salad",
        "der Kuchen": "cake",
        "das Wasser": "water",
        "der Saft": "juice",
        "die Milch": "milk",
        "der Kaffee": "coffee",
        "der Tee": "tea",
        "das Bier": "beer",
        "der Wein": "wine",
        "die Cola": "cola",
        "das Frühstück": "breakfast",
        "lecker": "delicious",
        "Guten Appetit!": "Enjoy your meal!",
    },

    # ── Unterwegs & Verkehr ───────────────────────────────────────────────────
    "🚌 Getting Around": {
        "der Bahnhof": "train station",
        "der Bus": "bus",
        "die Straßenbahn": "tram",
        "das Taxi": "taxi",
        "das Fahrrad": "bicycle",
        "das Auto": "car",
        "der Zug": "train",
        "das Flugzeug": "airplane",
        "die Fahrkarte": "ticket",
        "die Haltestelle": "stop (bus/tram)",
        "der Flughafen": "airport",
        "Entschuldigung, wie komme ich zum …?": "Excuse me, how do I get to the …?",
        "Bitte gehen Sie geradeaus.": "Please go straight ahead.",
        "links": "left",
        "rechts": "right",
        "geradeaus": "straight ahead",
        "gegenüber": "opposite",
        "neben": "next to",
        "weit": "far",
        "nah": "near / close",
        "umsteigen": "to change (trains/bus)",
        "Wann fährt der nächste Zug?": "When does the next train leave?",
        "Eine Fahrkarte nach … bitte.": "One ticket to … please.",
    },

    # ── Einkaufen ─────────────────────────────────────────────────────────────
    "🛍️ Shopping": {
        "das Geschäft": "shop",
        "der Supermarkt": "supermarket",
        "das Kaufhaus": "department store",
        "der Markt": "market",
        "kaufen": "to buy",
        "verkaufen": "to sell",
        "bezahlen": "to pay",
        "kosten": "to cost",
        "teuer": "expensive",
        "billig / günstig": "cheap",
        "die Größe": "size",
        "die Farbe": "colour",
        "Was kostet das?": "How much does that cost?",
        "Das ist zu teuer.": "That is too expensive.",
        "Ich nehme das.": "I'll take that.",
        "Haben Sie das auch in …?": "Do you have that in … too?",
        "Kann ich mit Karte bezahlen?": "Can I pay by card?",
        "die Quittung / der Kassenbon": "receipt",
        "das Sonderangebot": "special offer",
        "der Preis": "price",
    },

    # ── Nützliche Kurzsätze ───────────────────────────────────────────────────
    "💬 Useful Phrases": {
        "Bitte.": "Please. / Here you go.",
        "Danke.": "Thank you.",
        "Bitte sehr.": "You're welcome.",
        "Entschuldigung!": "Excuse me! / Sorry!",
        "Tut mir leid.": "I'm sorry.",
        "Kein Problem.": "No problem.",
        "Ja, natürlich.": "Yes, of course.",
        "Leider nicht.": "Unfortunately not.",
        "Das geht leider nicht.": "Unfortunately that's not possible.",
        "Wie bitte?": "Pardon? / Could you repeat that?",
        "Ich verstehe nicht.": "I don't understand.",
        "Können Sie das bitte wiederholen?": "Can you please repeat that?",
        "Können Sie bitte langsamer sprechen?": "Can you please speak more slowly?",
        "Können Sie mir bitte helfen?": "Could you please help me?",
        "Ich möchte …": "I would like …",
        "Darf ich …?": "May I …?",
        "Was bedeutet …?": "What does … mean?",
        "Wie schreibt man das?": "How do you write / spell that?",
        "Ich weiß nicht.": "I don't know.",
        "Alles klar!": "All good! / Got it!",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="German Flashcards A1",
    page_icon="🇩🇪",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* dark background */
  .stApp { background-color: #1e1e2e; color: #cdd6f4; }

  /* card container */
  .card {
    background: #313244;
    border-radius: 20px;
    padding: 48px 36px;
    text-align: center;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 24px;
    position: relative;
  }
  .card-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6c7086;
    margin-bottom: 16px;
  }
  .card-front {
    font-size: 2.2rem;
    font-weight: 700;
    color: #89b4fa;
    line-height: 1.3;
  }
  .card-back {
    font-size: 1.9rem;
    font-weight: 600;
    color: #a6e3a1;
    line-height: 1.3;
  }
  .card-hint {
    font-size: 0.9rem;
    color: #585b70;
    margin-top: 12px;
    font-style: italic;
  }
  .progress-text {
    text-align: center;
    color: #6c7086;
    font-size: 0.88rem;
    margin-bottom: 8px;
  }
  /* hide Streamlit default header & footer */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — topic selector & controls
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇩🇪 German A1 Flashcards")
    st.divider()

    topic_options = ["✨ All Topics"] + list(VOCAB.keys())
    selected_topic = st.selectbox("Topic", topic_options, key="topic")

    st.divider()
    shuffle = st.toggle("Shuffle cards", value=True, key="shuffle")
    show_chapter = st.toggle("Show topic on card", value=True, key="show_chapter")

    st.divider()
    if st.button("🔄 Restart deck", use_container_width=True):
        for k in ["deck", "idx", "flipped", "seen"]:
            st.session_state.pop(k, None)
        st.rerun()

    # skipped words panel
    skipped: set = st.session_state.get("skipped", set())
    if skipped:
        st.divider()
        st.markdown(f"**Known words: {len(skipped)}**")
        if st.button("↩️ Restore all known words", use_container_width=True):
            st.session_state.skipped = set()
            for k in ["deck", "idx", "flipped", "seen"]:
                st.session_state.pop(k, None)
            st.rerun()
        with st.expander("Show known words"):
            for w in sorted(skipped):
                st.markdown(f"- {w}")

# ─────────────────────────────────────────────────────────────────────────────
# BUILD DECK
# ─────────────────────────────────────────────────────────────────────────────
def build_deck(topic: str, do_shuffle: bool) -> list[tuple[str, str, str]]:
    """Return list of (german, english, topic_label) tuples, excluding skipped words."""
    skipped: set = st.session_state.get("skipped", set())
    items: list[tuple[str, str, str]] = []
    if topic == "✨ All Topics":
        for lbl, vocab in VOCAB.items():
            for de, en in vocab.items():
                if de not in skipped:
                    items.append((de, en, lbl))
    else:
        for de, en in VOCAB[topic].items():
            if de not in skipped:
                items.append((de, en, topic))
    if do_shuffle:
        random.shuffle(items)
    return items


# Rebuild deck when topic, shuffle, or skipped set changes
topic_key = (
    st.session_state.get("topic", ""),
    st.session_state.get("shuffle", True),
    frozenset(st.session_state.get("skipped", set())),
)
if "deck" not in st.session_state or st.session_state.get("_last_key") != topic_key:
    st.session_state.deck = build_deck(
        st.session_state.get("topic", "✨ All Topics"),
        st.session_state.get("shuffle", True),
    )
    st.session_state.idx = 0
    st.session_state.flipped = False
    st.session_state.seen = set()
    st.session_state._last_key = topic_key
    if "skipped" not in st.session_state:
        st.session_state.skipped = set()

deck: list[tuple[str, str, str]] = st.session_state.deck
total = len(deck)

if total == 0:
    st.warning("No cards in this topic.")
    st.stop()

idx: int = st.session_state.idx
flipped: bool = st.session_state.flipped
seen: set = st.session_state.seen
seen.add(idx)

german, english, topic_label = deck[idx]

# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS BAR
# ─────────────────────────────────────────────────────────────────────────────
pct = len(seen) / total
n_skipped = len(st.session_state.get("skipped", set()))
skip_text = f"&nbsp;·&nbsp; {n_skipped} known" if n_skipped else ""
st.markdown(
    f"<div class='progress-text'>Card {idx + 1} of {total} &nbsp;·&nbsp; "
    f"{len(seen)} seen{skip_text} &nbsp;·&nbsp; {int(pct*100)}% complete</div>",
    unsafe_allow_html=True,
)
st.progress(pct)

# ─────────────────────────────────────────────────────────────────────────────
# FLASH CARD
# ─────────────────────────────────────────────────────────────────────────────
topic_html = (
    f"<div class='card-label'>{topic_label}</div>"
    if st.session_state.get("show_chapter", True)
    else ""
)

if not flipped:
    st.markdown(
        f"""<div class='card'>
          {topic_html}
          <div class='card-label'>GERMAN</div>
          <div class='card-front'>{german}</div>
          <div class='card-hint'>Click <b>Flip</b> to see the English meaning</div>
        </div>""",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"""<div class='card'>
          {topic_html}
          <div class='card-label'>ENGLISH</div>
          <div class='card-back'>{english}</div>
          <div class='card-label' style='margin-top:20px; color:#89b4fa;'>{german}</div>
        </div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# BUTTONS — row 1: navigation + flip
# ─────────────────────────────────────────────────────────────────────────────
b_prev, b_flip, b_next = st.columns([1, 2, 1])

with b_prev:
    if st.button("⬅️ Prev", use_container_width=True, disabled=(idx == 0)):
        st.session_state.idx = idx - 1
        st.session_state.flipped = False
        st.rerun()

with b_flip:
    label = "🔄 Flip to English" if not flipped else "🔄 Flip to German"
    if st.button(label, type="primary", use_container_width=True):
        st.session_state.flipped = not flipped
        st.rerun()

with b_next:
    if idx < total - 1:
        if st.button("Next ➡️", use_container_width=True):
            st.session_state.idx = idx + 1
            st.session_state.flipped = False
            st.rerun()
    else:
        if st.button("Restart ✅", use_container_width=True, type="primary"):
            st.session_state.idx = 0
            st.session_state.flipped = False
            st.session_state.seen = set()
            if st.session_state.get("shuffle", True):
                random.shuffle(st.session_state.deck)
            st.rerun()

# ── row 2: "I know this" ──────────────────────────────────────────────────────
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
if st.button(
    "✅ I know this — don't show again",
    use_container_width=True,
    help="Removes this word from the deck permanently (until you restore it from the sidebar)",
):
    st.session_state.skipped.add(german)
    # advance to next card (or stay at boundary)
    new_idx = min(idx, total - 2)  # total will shrink by 1 after rebuild
    st.session_state.idx = max(new_idx, 0)
    st.session_state.flipped = False
    # force deck rebuild by clearing it
    st.session_state.pop("deck", None)
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# DECK COMPLETE BANNER
# ─────────────────────────────────────────────────────────────────────────────
if len(seen) == total:
    st.divider()
    st.success(f"You've seen all {total} cards! Press **Restart** to go again.")
    st.balloons()
