import streamlit as st
import random
import io

try:
    from gtts import gTTS
    _HAS_TTS = True
except ImportError:
    _HAS_TTS = False

# ─────────────────────────────────────────────────────────────────────────────
# VOCABULARY — phrase-based, organised by telc A1 exam topic
# Each entry: "German phrase / sentence" : "English meaning"
# ─────────────────────────────────────────────────────────────────────────────
VOCAB_BY_CHAPTER = {

    # ── Sich vorstellen ───────────────────────────────────────────────────────
    "Sich vorstellen": {
        # Official TELC template phrases (Sprechen Teil 1)
        "Wie heißen Sie?": "What is your name?",
        "Mein Name ist Anna Schmidt.": "My name is Anna Schmidt.",
        "Ich heiße Maria Müller.": "My name is Maria Müller.",
        "Wie ist Ihr Familienname?": "What is your surname?",
        "Können Sie bitte Ihren Familiennamen buchstabieren?": "Can you please spell your surname?",
        "Wie ist Ihr Vorname?": "What is your first name?",
        "Wie alt sind Sie?": "How old are you?",
        "Ich bin 32 Jahre alt.": "I am 32 years old.",
        "Woher kommen Sie?": "Where do you come from?",
        "Ich komme aus Indien.": "I come from India.",
        "Wo wohnen Sie?": "Where do you live?",
        "Ich wohne in München.": "I live in Munich.",
        "Ich lebe in Berlin.": "I live in Berlin.",
        "Was sind Sie von Beruf?": "What is your job / profession?",
        "Von Beruf bin ich Arzt.": "By profession I am a doctor.",
        "Welche Sprachen sprechen Sie?": "Which languages do you speak?",
        "Ich spreche Deutsch und Englisch.": "I speak German and English.",
        "Ich spreche ein bisschen Deutsch.": "I speak a little German.",
        "Was machen Sie in Ihrer Freizeit?": "What do you do in your free time?",
        "Mein Hobby ist Musik.": "My hobby is music.",
        "Wie ist Ihre Telefonnummer?": "What is your telephone number?",
        "Wie ist Ihre Adresse?": "What is your address?",
        "Ich bin verheiratet.": "I am married.",
        "Ich bin ledig.": "I am single.",
        "Ich habe zwei Kinder.": "I have two children.",
        "Schön, Sie kennenzulernen!": "Nice to meet you!",
        "Ich lerne seit drei Monaten Deutsch.": "I have been learning German for three months.",
        "Möchten Sie bitte anfangen?": "Would you like to start please?",
    },

    # ── Essen und Trinken ─────────────────────────────────────────────────────
    "Essen und Trinken": {
        # Sprechen Teil 2 — Essen und Trinken topics
        "Was essen Sie gern?": "What do you like to eat?",
        "Was trinken Sie gern?": "What do you like to drink?",
        "Was essen Sie zum Frühstück?": "What do you eat for breakfast?",
        "Ich esse gern Brot und Obst.": "I like to eat bread and fruit.",
        "Was ist Ihr Lieblingsessen?": "What is your favourite meal?",
        "Mein Lieblingsessen ist Fisch.": "My favourite meal is fish.",
        "Was essen Sie am Sonntag?": "What do you eat on Sundays?",
        "Ich trinke gern Kaffee.": "I like to drink coffee.",
        "Zum Frühstück esse ich Brötchen.": "For breakfast I eat bread rolls.",
        # Hören Teil 1 — restaurant dialogue (exact test phrases)
        "Was wünschen Sie bitte?": "What would you like?",
        "Ich hätte gern die Salatplatte.": "I would like the salad plate.",
        "Entschuldigung, die Salatplatte ist leider aus.": "I'm sorry, the salad plate is unfortunately sold out.",
        "Die Salatplatte ist leider aus.": "The salad plate is unfortunately sold out.",
        "Aber die Bratwurst kann ich Ihnen empfehlen.": "But I can recommend the grilled sausage to you.",
        "Ich kann Ihnen den Fisch empfehlen.": "I can recommend the fish to you.",
        "Ich esse kein Fleisch.": "I don't eat meat.",
        "Gibt es etwas ohne Fleisch?": "Is there something without meat?",
        "Ich hätte gern die Bratwurst.": "I would like the grilled sausage.",
        "Guten Appetit!": "Enjoy your meal!",
        # Hören Teil 2 — Weihnachtsmarkt announcement
        "Eine Flasche Weißwein, bitte.": "A bottle of white wine, please.",
        "Das Bier kostet 3,50 Euro.": "The beer costs 3.50 euros.",
        "Ich möchte ein Glas Wasser.": "I would like a glass of water.",
        "Wir essen gern Brezeln und Sauerkraut.": "We like to eat pretzels and sauerkraut.",
    },

    # ── Einkaufen ─────────────────────────────────────────────────────────────
    "Einkaufen": {
        # Hören Teil 1 — Pullover dialogue (exact test phrases)
        "Entschuldigung, was kostet dieser Pullover?": "Excuse me, how much does this jumper cost?",
        "Was kostet dieser Pullover?": "How much does this jumper cost?",
        "Da steht 30 Prozent billiger.": "It says 30 percent cheaper.",
        "Das ist 30 Prozent billiger.": "That is 30 percent cheaper.",
        "Neunzehn Euro fünfundneunzig.": "Nineteen euros ninety-five.",
        "Der Pullover kostet 19,95 Euro.": "The jumper costs 19.95 euros.",
        "Ok, den nehme ich.": "Ok, I'll take it.",
        "Ich nehme den Pullover.": "I'll take the jumper.",
        # Sprechen Teil 2 — Einkaufen topics
        "Haben Sie eine Zeitung?": "Do you have a newspaper?",
        "Wo finde ich die Kasse?": "Where do I find the till / checkout?",
        "Ich suche einen Stadtplan.": "I am looking for a city map.",
        "Entschuldigung, ich suche Schuhe.": "Excuse me, I am looking for shoes.",
        "Wo bekomme ich Briefmarken?": "Where can I get stamps?",
        "Kann ich mit Kreditkarte bezahlen?": "Can I pay by credit card?",
        "Ich bezahle bar.": "I'll pay cash.",
        "Einen Moment bitte, ich schaue nach.": "One moment please, I'll check.",
        "Haben Sie das auch in Größe 42?": "Do you have that in size 42 as well?",
        "Wo ist die Umkleidekabine?": "Where is the changing room?",
        "Das ist zu teuer.": "That is too expensive.",
        "Ich möchte das bitte zurückgeben.": "I would like to return this please.",
        "Geben Sie mir bitte eine Quittung.": "Please give me a receipt.",
        "Wo kaufen Sie ein?": "Where do you go shopping?",
        "Im Supermarkt kaufe ich Obst und Gemüse.": "I buy fruit and vegetables at the supermarket.",
    },

    # ── Alltag & Unterwegs ────────────────────────────────────────────────────
    "Alltag & Unterwegs": {
        # Hören Teil 1 — department store (exact test phrases)
        "Entschuldigen Sie, wie komme ich in den zweiten Stock?": "Excuse me, how do I get to the second floor?",
        "Wie komme ich in den zweiten Stock?": "How do I get to the second floor?",
        "Die Rolltreppe da vorn ist kaputt.": "The escalator at the front is broken.",
        "Die Rolltreppe ist leider kaputt.": "The escalator is unfortunately broken.",
        "Da gehen Sie hier rechts um die Ecke und nehmen den Aufzug.": "Go right around the corner and take the lift.",
        "Gehen Sie hier rechts um die Ecke.": "Go right around the corner here.",
        "Nehmen Sie den Aufzug.": "Take the lift.",
        # Hören Teil 1 — travel dialogue (Herr Albers)
        "Wohin fahren Sie?": "Where are you going?",
        "Wohin fahren Sie im Urlaub?": "Where are you going on holiday?",
        "Ich fahre zu meinen Verwandten nach Polen.": "I am going to visit my relatives in Poland.",
        "Ich fahre zu meinen Verwandten.": "I am going to my relatives.",
        "Für drei Wochen.": "For three weeks.",
        # Hören Teil 2 — train/bus announcements (exact test phrases)
        "Wir treffen uns um halb eins am Bus.": "We'll meet at the bus at half past twelve.",
        "Bitte pünktlich sein!": "Please be on time!",
        "Bitte hier nicht aussteigen.": "Please do not get off here.",
        "In ein paar Minuten kommen wir an.": "We will arrive in a few minutes.",
        "Herr Albers, bitte zum Schalter F7.": "Mr Albers, please go to gate F7.",
        # Hören Teil 3 — phone messages
        "Ich warte an der Information auf dich.": "I'll wait for you at the information desk.",
        # Directions / getting around
        "Entschuldigen Sie, wie komme ich zum Bahnhof?": "Excuse me, how do I get to the train station?",
        "Wie komme ich zum Bahnhof?": "How do I get to the train station?",
        "Bitte gehen Sie geradeaus.": "Please go straight ahead.",
        "Wo ist die Information?": "Where is the information desk?",
        # Time-related travel
        "Wie spät ist es bitte?": "What time is it please?",
        "Es ist gleich fünf Uhr.": "It is almost five o'clock.",
        "Der Zug fährt um 7:34 Uhr ab.": "The train departs at 7:34.",
        "Der Zug kommt um 12:05 Uhr an.": "The train arrives at 12:05.",
        "Der nächste Zug fährt in 10 Minuten.": "The next train leaves in 10 minutes.",
        "Wann ist die nächste Abfahrt?": "When is the next departure?",
        "Auf welchem Gleis fährt der Zug ab?": "Which platform does the train leave from?",
    },

    # ── Alltagstexte & Formulare ──────────────────────────────────────────────
    "Alltagstexte & Formulare": {
        # Schreiben Teil 1 — Bodensee-Rundfahrt form (exact test content)
        "Bitte füllen Sie das Formular aus.": "Please fill in the form.",
        "Tragen Sie Ihren Familiennamen ein.": "Enter your surname.",
        "Wie viele Personen reisen mit?": "How many people are travelling?",
        "Wie viele Kinder haben Sie dabei?": "How many children do you have with you?",
        "Was ist Ihre Urlaubsadresse?": "What is your holiday address?",
        "Wie ist Ihre Postleitzahl?": "What is your postcode?",
        "Wie möchten Sie bezahlen?": "How would you like to pay?",
        "Ich bezahle mit Kreditkarte.": "I am paying by credit card.",
        "Ich bezahle bar.": "I am paying cash.",
        "Wann ist die Busfahrt?": "When is the bus trip?",
        "Vergessen Sie nicht die Unterschrift!": "Don't forget the signature!",
        # Schreiben Teil 2 — letter to tourist office
        "Sie kommen im August nach Dresden.": "You are coming to Dresden in August.",
        "Ich bitte um Informationen über Hotels.": "I am asking for information about hotels.",
        "Schicken Sie mir bitte das Kulturprogramm.": "Please send me the cultural programme.",
        "Ich möchte Informationen über Museen und Theater.": "I would like information about museums and theatres.",
        # Lesen Teil 3 — signs and notices (exact test phrases)
        "Das Sprachenzentrum ist umgezogen.": "The language centre has moved.",
        "Sie finden uns jetzt in der Beethovenstraße 23.": "You can now find us at Beethovenstraße 23.",
        "In der Pause gibt es belegte Brötchen.": "During the break there are sandwiches.",
        "Die Post ist montags bis freitags geöffnet.": "The post office is open Monday to Friday.",
        "Die Post ist samstags bis 12 Uhr geöffnet.": "The post office is open until 12 on Saturdays.",
        "Von 8 bis 12 Uhr und von 13 bis 18 Uhr.": "From 8 to 12 and from 1 to 6 pm.",
        "Am Samstagnachmittag ist die Post geschlossen.": "The post office is closed on Saturday afternoons.",
        "Auf dem Bahnhof ist Rauchen verboten.": "Smoking is forbidden at the train station.",
        "Heute Abend gibt es Volksmusik und Tanz.": "This evening there is folk music and dancing.",
        "Von 23 Uhr bis 1 Uhr fährt kein Bus.": "No buses run from 11 pm to 1 am.",
        "Kann ich hier Briefmarken kaufen?": "Can I buy stamps here?",
    },

    # ── Reise & Freizeit ──────────────────────────────────────────────────────
    "Reise & Freizeit": {
        # Lesen Teil 1 — birthday party letter (exact test phrases)
        "Am kommenden Sonntag habe ich Geburtstag.": "Next Sunday is my birthday.",
        "Ich lade euch herzlich ein.": "I warmly invite you.",
        "Wir fangen um 21 Uhr an.": "We start at 9 pm.",
        "Ist das okay für euch?": "Is that okay for you all?",
        "Es werden viele Leute da sein.": "There will be a lot of people there.",
        "Könntet ihr einen Salat mitbringen?": "Could you bring a salad along?",
        "Vergesst bitte nicht einen Pullover!": "Please don't forget a jumper!",
        "Wir wollen draußen im Garten feiern.": "We want to celebrate outside in the garden.",
        "Die Party findet draußen statt.": "The party takes place outside.",
        "Ich freue mich sehr auf euch!": "I'm really looking forward to seeing you!",
        # Lesen Teil 2 — Rhine cruise / Bodensee
        "Das Schiff fährt täglich von Rüdesheim.": "The ship goes daily from Rüdesheim.",
        "Wir machen eine Rundfahrt auf dem Bodensee.": "We are doing a tour of Lake Constance.",
        "Wir buchen eine Ferienwohnung.": "We are booking a holiday apartment.",
        # Holiday / travel
        "Ich fahre ans Meer.": "I am going to the sea.",
        "Wie lange bleiben Sie?": "How long are you staying?",
        "Ich bleibe drei Wochen.": "I am staying for three weeks.",
        "Ich möchte Informationen über das Hotel.": "I would like information about the hotel.",
        "Das Hotel hat ein Restaurant mit Terrasse.": "The hotel has a restaurant with a terrace.",
        # Greetings
        "Frohe Weihnachten!": "Merry Christmas!",
        "Schöne Ferien!": "Enjoy your holidays!",
    },

    # ── Zahlen, Zeit & Datum ──────────────────────────────────────────────────
    "Zahlen, Zeit & Datum": {
        "Wie spät ist es?": "What time is it?",
        "Es ist viertel nach zwei.": "It is quarter past two.",
        "Es ist viertel vor zwei.": "It is quarter to two.",
        "Es ist halb drei.": "It is half past two.",
        "Es ist kurz nach zwei.": "It is just after two.",
        "Es ist kurz vor zwei.": "It is just before two.",
        "Es ist gleich 5 Uhr.": "It is almost 5 o'clock.",
        "Der Zug kommt um 12.36 Uhr an.": "The train arrives at 12:36.",
        "Wann haben Sie Geburtstag?": "When is your birthday?",
        "Ich habe am neunzehnten September Geburtstag.": "My birthday is on the 19th of September.",
        "Der wievielte ist heute?": "What is today's date?",
        "Heute ist der zwanzigste Februar.": "Today is the 20th of February.",
        "Wann kommen Sie?": "When are you coming?",
        "Ich komme am Montag.": "I am coming on Monday.",
        "Die Post ist montags bis freitags geöffnet.": "The post office is open Monday to Friday.",
        "Von 8 bis 12 Uhr und von 13 bis 18 Uhr.": "From 8 to 12 and from 1 to 6 pm.",
        "Ich warte seit 20 Minuten.": "I have been waiting for 20 minutes.",
        "In ein paar Minuten kommen wir an.": "We will arrive in a few minutes.",
        "Am Samstagnachmittag ist die Post geschlossen.": "The post office is closed on Saturday afternoons.",
        "Der Kurs beginnt um 9 Uhr morgens.": "The course starts at 9 in the morning.",
    },

    # ── Nützliche Sätze ───────────────────────────────────────────────────────
    "Nützliche Sätze": {
        # Hören Teil 3 — phone messages (exact test phrases)
        "Kannst du schnell mal rüberkommen?": "Can you quickly come over?",
        "Kann ich schnell mal rüberkommen?": "Can I quickly come over?",
        "Mein Computer hat einen Fehler.": "My computer has an error.",
        "Ich kann nichts drucken.": "I cannot print anything.",
        "Melde dich bitte, wenn du nach Hause kommst.": "Please get in touch when you get home.",
        "Bitte rufen Sie uns zurück.": "Please call us back.",
        "Am Sonntag haben wir Zeit.": "We are free on Sunday.",
        "Rufen Sie uns zurück, ob Ihnen das passt.": "Call us back to let us know if that suits you.",
        "Passt Ihnen das?": "Does that suit you? / Is that okay for you?",
        "Wir können leider nicht kommen.": "Unfortunately we cannot come.",
        # Modal verb sentences
        "Ich kann gut schwimmen.": "I can swim well.",
        "Ich kann mit dem Bus kommen.": "I can come by bus.",
        "Ich muss für die Prüfung lernen.": "I must study for the exam.",
        "Ich will nach Deutschland fliegen.": "I want to fly to Germany.",
        "Sie soll viel Wasser trinken.": "She should drink a lot of water.",
        "Hier darf man nicht rauchen.": "You are not allowed to smoke here.",
        "Ich möchte einen Termin machen.": "I would like to make an appointment.",
        # Separable verbs in context
        "Er ruft mich morgen an.": "He will call me tomorrow.",
        "Ich hole dich vom Bahnhof ab.": "I'll pick you up from the train station.",
        "Kommst du mit?": "Are you coming along?",
        "Ich bringe Kuchen mit.": "I'll bring cake along.",
        "Der Film fängt um 20 Uhr an.": "The film starts at 8 pm.",
    },

    # ── Bitten & Reaktionen ───────────────────────────────────────────────────
    "Bitten & Reaktionen": {
        # Sprechen Teil 3 — exact test phrases
        "Ein Glas Wasser, bitte!": "A glass of water, please!",
        "Könnte ich bitte ein Glas Wasser haben?": "Could I please have a glass of water?",
        "Hier, bitte.": "Here you go.",
        "Tut mir leid, ich habe keins.": "I'm sorry, I don't have any.",
        "Tut mir leid.": "I'm sorry.",
        "Leider nicht.": "Unfortunately not.",
        "Ja, gern!": "Yes, gladly!",
        "Ja, natürlich.": "Yes, of course.",
        "Kein Problem.": "No problem.",
        "Das geht leider nicht.": "Unfortunately that's not possible.",
        # Polite requests and classroom language
        "Können Sie mir bitte helfen?": "Could you please help me?",
        "Können Sie bitte langsamer sprechen?": "Can you please speak more slowly?",
        "Können Sie das bitte wiederholen?": "Can you please repeat that?",
        "Wie bitte? Ich habe das nicht verstanden.": "Pardon? I didn't understand that.",
        "Sprechen Sie bitte langsamer!": "Please speak more slowly!",
        "Einen Moment bitte!": "One moment please!",
        "Entschuldigen Sie bitte!": "Excuse me please!",
        # Common polite phrases
        "Vielen Dank!": "Thank you very much!",
        "Bitte schön.": "You're welcome.",
        "Geben Sie mir bitte das Buch.": "Please give me the book.",
        "Öffnen Sie bitte die Tür.": "Please open the door.",
    },
}

# Flat vocab for "All chapters"
ALL_VOCAB: dict = {}
for chapter_vocab in VOCAB_BY_CHAPTER.values():
    ALL_VOCAB.update(chapter_vocab)

CHAPTER_NAMES = ["Alle Themen"] + list(VOCAB_BY_CHAPTER.keys())

# ── Word-by-word breakdowns ───────────────────────────────────────────────────
WORD_BREAKDOWN: dict[str, str] = {
    # Sich vorstellen
    "Wie heißen Sie?":                              "Wie = How · heißen = are called · Sie = you (formal)",
    "Ich heiße Maria Müller.":                      "Ich = I · heiße = am called · Maria Müller = Maria Müller",
    "Wie ist Ihr Familienname?":                    "Wie = What · ist = is · Ihr = your · Familienname = surname",
    "Wie ist Ihr Vorname?":                         "Wie = What · ist = is · Ihr = your · Vorname = first name",
    "Wie alt sind Sie?":                            "Wie = How · alt = old · sind = are · Sie = you",
    "Ich bin 32 Jahre alt.":                        "Ich = I · bin = am · 32 Jahre = 32 years · alt = old",
    "Woher kommen Sie?":                            "Woher = From where · kommen = come · Sie = you",
    "Ich komme aus Indien.":                        "Ich = I · komme = come · aus = from · Indien = India",
    "Wo wohnen Sie?":                               "Wo = Where · wohnen = live · Sie = you",
    "Ich wohne in München.":                        "Ich = I · wohne = live · in = in · München = Munich",
    "Was sind Sie von Beruf?":                      "Was = What · sind = are · Sie = you · von Beruf = by profession",
    "Von Beruf bin ich Arzt.":                      "Von Beruf = By profession · bin = am · ich = I · Arzt = doctor",
    "Welche Sprachen sprechen Sie?":                "Welche = Which · Sprachen = languages · sprechen = speak · Sie = you",
    "Ich spreche Deutsch und Englisch.":            "Ich = I · spreche = speak · Deutsch = German · und = and · Englisch = English",
    "Was machen Sie in Ihrer Freizeit?":            "Was = What · machen = do · Sie = you · in = in · Ihrer = your · Freizeit = free time",
    "Mein Hobby ist Musik.":                        "Mein = My · Hobby = hobby · ist = is · Musik = music",
    "Können Sie bitte Ihren Namen buchstabieren?":  "Können = Can · Sie = you · bitte = please · Ihren = your · Namen = name · buchstabieren = spell",
    "Wie ist Ihre Telefonnummer?":                  "Wie = What · ist = is · Ihre = your · Telefonnummer = telephone number",
    "Wie ist Ihre Adresse?":                        "Wie = What · ist = is · Ihre = your · Adresse = address",
    "Ich bin verheiratet.":                         "Ich = I · bin = am · verheiratet = married",
    "Ich bin ledig.":                               "Ich = I · bin = am · ledig = single",
    "Ich habe zwei Kinder.":                        "Ich = I · habe = have · zwei = two · Kinder = children",
    "Schön, Sie kennenzulernen!":                   "Schön = Nice · Sie = you · kennenzulernen = to meet / get to know",
    "Ich lerne seit drei Monaten Deutsch.":         "Ich = I · lerne = learn · seit = for/since · drei = three · Monaten = months · Deutsch = German",
    # Essen und Trinken
    "Was essen Sie gern?":                          "Was = What · essen = eat · Sie = you · gern = like to",
    "Was trinken Sie gern?":                        "Was = What · trinken = drink · Sie = you · gern = like to",
    "Was essen Sie zum Frühstück?":                 "Was = What · essen = eat · Sie = you · zum = for · Frühstück = breakfast",
    "Ich esse gern Brot und Obst.":                 "Ich = I · esse = eat · gern = like to · Brot = bread · und = and · Obst = fruit",
    "Was ist Ihr Lieblingsessen?":                  "Was = What · ist = is · Ihr = your · Lieblingsessen = favourite meal",
    "Mein Lieblingsessen ist Fisch.":               "Mein = My · Lieblingsessen = favourite meal · ist = is · Fisch = fish",
    "Was essen Sie am Sonntag?":                    "Was = What · essen = eat · Sie = you · am = on · Sonntag = Sunday",
    "Ich trinke gern Kaffee.":                      "Ich = I · trinke = drink · gern = like to · Kaffee = coffee",
    "Ich esse kein Fleisch.":                       "Ich = I · esse = eat · kein = no · Fleisch = meat",
    "Ich hätte gern die Bratwurst.":                "Ich = I · hätte gern = would like · die = the · Bratwurst = grilled sausage",
    "Was wünschen Sie bitte?":                      "Was = What · wünschen = wish/would like · Sie = you · bitte = please",
    "Gibt es etwas ohne Fleisch?":                  "Gibt es = Is there · etwas = something · ohne = without · Fleisch = meat",
    "Die Salatplatte ist leider aus.":              "Die = The · Salatplatte = salad plate · ist = is · leider = unfortunately · aus = sold out",
    "Ich kann Ihnen den Fisch empfehlen.":          "Ich = I · kann = can · Ihnen = you · den = the · Fisch = fish · empfehlen = recommend",
    "Guten Appetit!":                               "Guten = Good · Appetit = appetite",
    "Das Bier kostet 3,50 Euro.":                   "Das = The · Bier = beer · kostet = costs · 3,50 Euro = 3.50 euros",
    "Eine Flasche Weißwein, bitte.":                "Eine = A · Flasche = bottle · Weißwein = white wine · bitte = please",
    "Ich möchte ein Glas Wasser.":                  "Ich = I · möchte = would like · ein = a · Glas = glass · Wasser = water",
    "Wir essen gern Brezeln und Sauerkraut.":       "Wir = We · essen = eat · gern = like to · Brezeln = pretzels · und = and · Sauerkraut = sauerkraut",
    "Zum Frühstück esse ich Brötchen.":             "Zum Frühstück = For breakfast · esse = eat · ich = I · Brötchen = bread rolls",
    # Einkaufen
    "Was kostet dieser Pullover?":                  "Was = What · kostet = costs · dieser = this · Pullover = jumper",
    "Der Pullover kostet 19,95 Euro.":              "Der = The · Pullover = jumper · kostet = costs · 19,95 Euro = 19.95 euros",
    "Das ist 30 Prozent billiger.":                 "Das = That · ist = is · 30 Prozent = 30 percent · billiger = cheaper",
    "Ich nehme den Pullover.":                      "Ich = I · nehme = take · den = the · Pullover = jumper",
    "Wo finde ich die Kasse?":                      "Wo = Where · finde = find · ich = I · die = the · Kasse = till/checkout",
    "Haben Sie eine Zeitung?":                      "Haben = Have · Sie = you · eine = a · Zeitung = newspaper",
    "Ich suche einen Stadtplan.":                   "Ich = I · suche = look for · einen = a · Stadtplan = city map",
    "Wo bekomme ich Briefmarken?":                  "Wo = Where · bekomme = get · ich = I · Briefmarken = stamps",
    "Kann ich mit Kreditkarte bezahlen?":           "Kann = Can · ich = I · mit = with · Kreditkarte = credit card · bezahlen = pay",
    "Ich bezahle bar.":                             "Ich = I · bezahle = pay · bar = cash",
    "Einen Moment bitte, ich schaue nach.":         "Einen Moment = One moment · bitte = please · ich = I · schaue nach = check/look",
    "Entschuldigung, ich suche Schuhe.":            "Entschuldigung = Excuse me · ich = I · suche = look for · Schuhe = shoes",
    "Haben Sie das auch in Größe 42?":              "Haben = Have · Sie = you · das = that · auch = also · in = in · Größe = size · 42 = 42",
    "Wo ist die Umkleidekabine?":                   "Wo = Where · ist = is · die = the · Umkleidekabine = changing room",
    "Das ist zu teuer.":                            "Das = That · ist = is · zu = too · teuer = expensive",
    "Ich möchte das bitte zurückgeben.":            "Ich = I · möchte = would like · das = that · bitte = please · zurückgeben = return",
    "Geben Sie mir bitte eine Quittung.":           "Geben = Give · Sie = you · mir = me · bitte = please · eine = a · Quittung = receipt",
    "Wo kaufen Sie ein?":                           "Wo = Where · kaufen ein = go shopping · Sie = you",
    "Im Supermarkt kaufe ich Obst und Gemüse.":     "Im Supermarkt = At the supermarket · kaufe = buy · ich = I · Obst = fruit · und = and · Gemüse = vegetables",
    # Hören – Alltag & Unterwegs
    "Entschuldigen Sie, wie komme ich zum Bahnhof?": "Entschuldigen Sie = Excuse me · wie = how · komme = get · ich = I · zum = to the · Bahnhof = station",
    "Gehen Sie hier rechts um die Ecke.":           "Gehen = Go · Sie = you · hier = here · rechts = right · um = around · die Ecke = the corner",
    "Nehmen Sie den Aufzug.":                       "Nehmen = Take · Sie = you · den = the · Aufzug = lift",
    "Die Rolltreppe ist leider kaputt.":            "Die = The · Rolltreppe = escalator · ist = is · leider = unfortunately · kaputt = broken",
    "Wie komme ich in den zweiten Stock?":          "Wie = How · komme = get · ich = I · in = to · den = the · zweiten = second · Stock = floor",
    "Bitte gehen Sie geradeaus.":                   "Bitte = Please · gehen = go · Sie = you · geradeaus = straight ahead",
    "Der Zug fährt um 7:34 Uhr ab.":               "Der = The · Zug = train · fährt ab = departs · um = at · 7:34 Uhr = 7:34",
    "Der Zug kommt um 12:05 Uhr an.":              "Der = The · Zug = train · kommt an = arrives · um = at · 12:05 Uhr = 12:05",
    "Wo ist die Information?":                      "Wo = Where · ist = is · die = the · Information = information desk",
    "Ich warte an der Information auf dich.":       "Ich = I · warte = wait · an der = at the · Information = information desk · auf dich = for you",
    "Bitte pünktlich sein!":                        "Bitte = Please · pünktlich = on time · sein = be",
    "Wir treffen uns um halb eins am Bus.":         "Wir = We · treffen uns = meet · um = at · halb eins = half past twelve · am Bus = at the bus",
    "Herr Albers, bitte zum Schalter F7.":          "Herr = Mr · Albers = Albers · bitte = please · zum = to the · Schalter = counter/gate · F7 = F7",
    "Bitte hier nicht aussteigen.":                 "Bitte = Please · hier = here · nicht = not · aussteigen = get off",
    "Wie spät ist es bitte?":                       "Wie = How · spät = late · ist = is · es = it · bitte = please",
    "Es ist gleich fünf Uhr.":                      "Es = It · ist = is · gleich = almost · fünf = five · Uhr = o'clock",
    "Wohin fahren Sie?":                            "Wohin = Where to · fahren = go/travel · Sie = you",
    "Ich fahre zu meinen Verwandten.":              "Ich = I · fahre = travel · zu = to · meinen = my · Verwandten = relatives",
    "Der nächste Zug fährt in 10 Minuten.":        "Der = The · nächste = next · Zug = train · fährt = goes · in = in · 10 Minuten = 10 minutes",
    "Auf welchem Gleis fährt der Zug ab?":          "Auf = On · welchem = which · Gleis = platform/track · fährt ab = departs · der = the · Zug = train",
    # Lesen & Schreiben
    "Bitte füllen Sie das Formular aus.":           "Bitte = Please · füllen aus = fill in · Sie = you · das = the · Formular = form",
    "Tragen Sie Ihren Familiennamen ein.":          "Tragen ein = Enter · Sie = you · Ihren = your · Familiennamen = surname",
    "Wie viele Personen reisen mit?":               "Wie viele = How many · Personen = persons · reisen = travel · mit = along",
    "Wie viele Kinder haben Sie dabei?":            "Wie viele = How many · Kinder = children · haben = have · Sie = you · dabei = with you",
    "Was ist Ihre Urlaubsadresse?":                 "Was = What · ist = is · Ihre = your · Urlaubsadresse = holiday address",
    "Wie ist Ihre Postleitzahl?":                   "Wie = What · ist = is · Ihre = your · Postleitzahl = postcode",
    "Wie möchten Sie bezahlen?":                    "Wie = How · möchten = would like · Sie = you · bezahlen = pay",
    "Ich bezahle mit Kreditkarte.":                 "Ich = I · bezahle = pay · mit = with · Kreditkarte = credit card",
    "Wann ist die Busfahrt?":                       "Wann = When · ist = is · die = the · Busfahrt = bus trip",
    "Vergessen Sie nicht die Unterschrift!":        "Vergessen = Forget · Sie = you · nicht = not · die = the · Unterschrift = signature",
    "Die Post ist samstags bis 12 Uhr geöffnet.":  "Die = The · Post = post office · ist = is · samstags = on Saturdays · bis = until · 12 Uhr = 12 o'clock · geöffnet = open",
    "Kann ich hier Briefmarken kaufen?":            "Kann = Can · ich = I · hier = here · Briefmarken = stamps · kaufen = buy",
    "Auf dem Bahnhof ist Rauchen verboten.":        "Auf = At · dem = the · Bahnhof = station · ist = is · Rauchen = smoking · verboten = forbidden",
    "Heute Abend gibt es Volksmusik und Tanz.":     "Heute Abend = This evening · gibt es = there is · Volksmusik = folk music · und = and · Tanz = dancing",
    "Sie kommen im August nach Dresden.":           "Sie = You · kommen = come · im = in · August = August · nach = to · Dresden = Dresden",
    "Ich bitte um Informationen über Hotels.":      "Ich = I · bitte um = ask for · Informationen = information · über = about · Hotels = hotels",
    "Schicken Sie mir bitte das Kulturprogramm.":   "Schicken = Send · Sie = you · mir = me · bitte = please · das = the · Kulturprogramm = cultural programme",
    "In der Pause gibt es belegte Brötchen.":       "In der = During the · Pause = break · gibt es = there are · belegte = topped/filled · Brötchen = rolls",
    "Von 23 Uhr bis 1 Uhr fährt kein Bus.":        "Von = From · 23 Uhr = 11 pm · bis = until · 1 Uhr = 1 am · fährt = runs · kein = no · Bus = bus",
    "Das Sprachenzentrum ist umgezogen.":           "Das = The · Sprachenzentrum = language centre · ist umgezogen = has moved",
    # Reise & Freizeit
    "Wohin fahren Sie im Urlaub?":                  "Wohin = Where to · fahren = travel · Sie = you · im = on · Urlaub = holiday",
    "Ich fahre ans Meer.":                          "Ich = I · fahre = go · ans = to the · Meer = sea",
    "Ich mache eine Rundfahrt auf dem Bodensee.":   "Ich = I · mache = do · eine = a · Rundfahrt = tour · auf dem = on the · Bodensee = Lake Constance",
    "Wie lange bleiben Sie?":                       "Wie = How · lange = long · bleiben = stay · Sie = you",
    "Ich bleibe drei Wochen.":                      "Ich = I · bleibe = stay · drei = three · Wochen = weeks",
    "Wir wollen draußen im Garten feiern.":         "Wir = We · wollen = want to · draußen = outside · im = in the · Garten = garden · feiern = celebrate",
    "Ich lade euch herzlich ein.":                  "Ich = I · lade ein = invite · euch = you (plural) · herzlich = warmly",
    "Wir fangen um 21 Uhr an.":                     "Wir = We · fangen an = start · um = at · 21 Uhr = 9 pm",
    "Könntet ihr einen Salat mitbringen?":          "Könntet = Could · ihr = you (plural) · einen = a · Salat = salad · mitbringen = bring along",
    "Vergess nicht einen Pullover!":                "Vergess = Forget · nicht = not · einen = a · Pullover = jumper",
    "Am kommenden Sonntag habe ich Geburtstag.":    "Am = On · kommenden = coming/next · Sonntag = Sunday · habe = have · ich = I · Geburtstag = birthday",
    "Es werden viele Leute da sein.":               "Es = There · werden = will · viele = many · Leute = people · da = there · sein = be",
    "Die Party findet draußen statt.":              "Die = The · Party = party · findet statt = takes place · draußen = outside",
    "Ich möchte Informationen über das Hotel.":     "Ich = I · möchte = would like · Informationen = information · über = about · das = the · Hotel = hotel",
    "Wir buchen eine Ferienwohnung.":               "Wir = We · buchen = book · eine = a · Ferienwohnung = holiday apartment",
    "Das Hotel hat ein Restaurant mit Terrasse.":   "Das = The · Hotel = hotel · hat = has · ein = a · Restaurant = restaurant · mit = with · Terrasse = terrace",
    "Wann ist die nächste Abfahrt?":                "Wann = When · ist = is · die = the · nächste = next · Abfahrt = departure",
    "Das Schiff fährt täglich von Rüdesheim.":      "Das = The · Schiff = ship · fährt = goes · täglich = daily · von = from · Rüdesheim = Rüdesheim",
    "Frohe Weihnachten!":                           "Frohe = Merry/Happy · Weihnachten = Christmas",
    "Schöne Ferien!":                               "Schöne = Nice/Happy · Ferien = holidays",
    # Zahlen, Zeit & Datum
    "Wie spät ist es?":                             "Wie = How · spät = late · ist = is · es = it",
    "Es ist viertel nach zwei.":                    "Es = It · ist = is · viertel = quarter · nach = past · zwei = two",
    "Es ist viertel vor zwei.":                     "Es = It · ist = is · viertel = quarter · vor = to/before · zwei = two",
    "Es ist halb drei.":                            "Es = It · ist = is · halb = half · drei = three (= half past two)",
    "Es ist kurz nach zwei.":                       "Es = It · ist = is · kurz = just/shortly · nach = after · zwei = two",
    "Es ist kurz vor zwei.":                        "Es = It · ist = is · kurz = just/shortly · vor = before · zwei = two",
    "Es ist gleich 5 Uhr.":                         "Es = It · ist = is · gleich = almost · 5 = five · Uhr = o'clock",
    "Der Zug kommt um 12.36 Uhr an.":              "Der = The · Zug = train · kommt an = arrives · um = at · 12.36 Uhr = 12:36",
    "Wann haben Sie Geburtstag?":                   "Wann = When · haben = have · Sie = you · Geburtstag = birthday",
    "Ich habe am neunzehnten September Geburtstag.": "Ich = I · habe = have · am = on the · neunzehnten = nineteenth · September = September · Geburtstag = birthday",
    "Der wievielte ist heute?":                     "Der wievielte = What date · ist = is · heute = today",
    "Heute ist der zwanzigste Februar.":            "Heute = Today · ist = is · der = the · zwanzigste = twentieth · Februar = February",
    "Wann kommen Sie?":                             "Wann = When · kommen = come · Sie = you",
    "Ich komme am Montag.":                         "Ich = I · komme = come · am = on · Montag = Monday",
    "Die Post ist montags bis freitags geöffnet.":  "Die = The · Post = post office · ist = is · montags = on Mondays · bis = to · freitags = Fridays · geöffnet = open",
    "Von 8 bis 12 Uhr und von 13 bis 18 Uhr.":     "Von = From · bis = until · Uhr = o'clock · und = and",
    "Ich warte seit 20 Minuten.":                   "Ich = I · warte = wait · seit = for/since · 20 Minuten = 20 minutes",
    "In ein paar Minuten kommen wir an.":           "In = In · ein paar = a few · Minuten = minutes · kommen an = arrive · wir = we",
    "Am Samstagnachmittag ist die Post geschlossen.": "Am = On · Samstagnachmittag = Saturday afternoon · ist = is · die = the · Post = post office · geschlossen = closed",
    "Der Kurs beginnt um 9 Uhr morgens.":           "Der = The · Kurs = course · beginnt = starts · um = at · 9 Uhr = 9 o'clock · morgens = in the morning",
    # Modalverben & Alltagssätze
    "Ich kann gut schwimmen.":                      "Ich = I · kann = can · gut = well · schwimmen = swim",
    "Ich kann mit dem Bus kommen.":                 "Ich = I · kann = can · mit = by · dem = the · Bus = bus · kommen = come",
    "Ich muss für die Prüfung lernen.":             "Ich = I · muss = must · für = for · die = the · Prüfung = exam · lernen = study/learn",
    "Ich will nach Deutschland fliegen.":           "Ich = I · will = want to · nach = to · Deutschland = Germany · fliegen = fly",
    "Sie soll viel Wasser trinken.":                "Sie = She · soll = should · viel = a lot of · Wasser = water · trinken = drink",
    "Hier darf man nicht rauchen.":                 "Hier = Here · darf = may · man = one/you · nicht = not · rauchen = smoke",
    "Ich möchte einen Termin machen.":              "Ich = I · möchte = would like · einen = a · Termin = appointment · machen = make",
    "Können Sie bitte langsamer sprechen?":         "Können = Can · Sie = you · bitte = please · langsamer = more slowly · sprechen = speak",
    "Er ruft mich morgen an.":                      "Er = He · ruft an = calls · mich = me · morgen = tomorrow",
    "Ich hole dich vom Bahnhof ab.":                "Ich = I · hole ab = pick up · dich = you · vom = from the · Bahnhof = station",
    "Kommst du mit?":                               "Kommst = Are coming · du = you · mit = along",
    "Ich bringe Kuchen mit.":                       "Ich = I · bringe mit = bring along · Kuchen = cake",
    "Der Film fängt um 20 Uhr an.":                 "Der = The · Film = film · fängt an = starts · um = at · 20 Uhr = 8 pm",
    "Bitte rufen Sie uns zurück.":                  "Bitte = Please · rufen zurück = call back · Sie = you · uns = us",
    "Kann ich schnell mal rüberkommen?":            "Kann = Can · ich = I · schnell = quickly · mal = just · rüberkommen = come over",
    "Mein Computer hat einen Fehler.":              "Mein = My · Computer = computer · hat = has · einen = a · Fehler = error/mistake",
    "Ich kann nichts drucken.":                     "Ich = I · kann = can · nichts = nothing · drucken = print",
    "Wir können leider nicht kommen.":              "Wir = We · können = can · leider = unfortunately · nicht = not · kommen = come",
    "Am Sonntag haben wir Zeit.":                   "Am = On · Sonntag = Sunday · haben = have · wir = we · Zeit = time",
    "Passt Ihnen das?":                             "Passt = Suits/Works · Ihnen = you · das = that",
    # Bitten & Reaktionen
    "Können Sie mir bitte helfen?":                 "Können = Can · Sie = you · mir = me · bitte = please · helfen = help",
    "Geben Sie mir bitte das Buch.":                "Geben = Give · Sie = you · mir = me · bitte = please · das = the · Buch = book",
    "Öffnen Sie bitte die Tür.":                    "Öffnen = Open · Sie = you · bitte = please · die = the · Tür = door",
    "Ein Glas Wasser, bitte!":                      "Ein = A · Glas = glass · Wasser = water · bitte = please",
    "Könnte ich bitte ein Glas Wasser haben?":      "Könnte = Could · ich = I · bitte = please · ein = a · Glas = glass · Wasser = water · haben = have",
    "Hier, bitte.":                                 "Hier = Here · bitte = please / you go",
    "Tut mir leid, ich habe keins.":                "Tut mir leid = I'm sorry · ich = I · habe = have · keins = none",
    "Tut mir leid.":                                "Tut = Does · mir = me · leid = sorrow → I'm sorry",
    "Leider nicht.":                                "Leider = Unfortunately · nicht = not",
    "Ja, gern!":                                    "Ja = Yes · gern = gladly / with pleasure",
    "Ja, natürlich.":                               "Ja = Yes · natürlich = of course / naturally",
    "Kein Problem.":                                "Kein = No · Problem = problem",
    "Einen Moment bitte!":                          "Einen = A/One · Moment = moment · bitte = please",
    "Wie bitte? Ich habe das nicht verstanden.":    "Wie bitte = Pardon · ich = I · habe = have · das = that · nicht = not · verstanden = understood",
    "Können Sie das bitte wiederholen?":            "Können = Can · Sie = you · das = that · bitte = please · wiederholen = repeat",
    "Sprechen Sie bitte langsamer!":                "Sprechen = Speak · Sie = you · bitte = please · langsamer = more slowly",
    "Vielen Dank!":                                 "Vielen = Many · Dank = thanks",
    "Bitte schön.":                                 "Bitte schön = You're welcome / Here you go",
    "Entschuldigen Sie bitte!":                     "Entschuldigen = Excuse · Sie = you · bitte = please",
    "Das geht leider nicht.":                       "Das = That · geht = goes/works · leider = unfortunately · nicht = not",
}

# ── Grammar notes ─────────────────────────────────────────────────────────────
# Format: sentence → (short label, plain-English explanation, word-order pattern)
GRAMMAR_NOTES: dict[str, tuple[str, str, str]] = {
    "Wie heißen Sie?":          ("Question word first", "German questions that start with a question word (Wie=How, Was=What, Wo=Where…) always put the action word second and the person third.", "Question word → Action word → Person"),
    "Wie ist Ihr Familienname?": ("Question word first", "Start with the question word (Wie=What), then the action word (ist=is), then the thing you're asking about.", "Question word → Action word → Thing"),
    "Wie ist Ihr Vorname?":     ("Question word first", "Same pattern. Wie starts the question, ist comes second.", "Question word → Action word → Thing"),
    "Wie alt sind Sie?":        ("Question word first", "'Wie alt' = How old — treated as one question phrase. The action word (sind=are) comes right after it.", "Question phrase → Action word → Person"),
    "Woher kommen Sie?":        ("Question word first", "Woher = From where. Action word (kommen=come) comes second, person (Sie=you) third.", "Question word → Action word → Person"),
    "Wo wohnen Sie?":           ("Question word first", "Wo = Where. Action word second, person third.", "Question word → Action word → Person"),
    "Was sind Sie von Beruf?":  ("Question word first", "Was = What. Action word second, person third, then extra info at the end.", "Question word → Action word → Person → Extra info"),
    "Was essen Sie gern?":      ("Question word first + 'gern'", "Was = What. Action word second. 'gern' (= like to) always goes near the end.", "Question word → Action word → Person → gern"),
    "Was trinken Sie gern?":    ("Question word first + 'gern'", "Same pattern. 'gern' after the person means 'like to'.", "Question word → Action word → Person → gern"),
    "Was essen Sie zum Frühstück?": ("Question word first", "What do you eat for breakfast? Extra info (zum Frühstück) goes at the end.", "Question word → Action word → Person → Extra info"),
    "Was ist Ihr Lieblingsessen?": ("Question word first", "Was = What. 'Ihr' = your (polite). Action word (ist) second.", "Question word → Action word → Thing"),
    "Was essen Sie am Sonntag?": ("Question word first", "Time info (am Sonntag = on Sunday) goes at the end of the question.", "Question word → Action word → Person → Time"),
    "Welche Sprachen sprechen Sie?": ("Question word first", "Welche Sprachen = Which languages — this whole phrase is the question opener. Action word second.", "Question phrase → Action word → Person"),
    "Was machen Sie in Ihrer Freizeit?": ("Question word first", "Was = What. Extra info (in Ihrer Freizeit = in your free time) at the end.", "Question word → Action word → Person → Extra info"),
    "Wie ist Ihre Telefonnummer?": ("Question word first", "Wie = What (used for numbers in German). Action word second.", "Question word → Action word → Thing"),
    "Wie ist Ihre Adresse?":    ("Question word first", "Wie = What. Same simple question pattern.", "Question word → Action word → Thing"),
    "Wie lange bleiben Sie?":   ("Question word first", "'Wie lange' = How long — one question phrase. Action word second.", "Question phrase → Action word → Person"),
    "Wohin fahren Sie im Urlaub?": ("Question word first", "Wohin = Where to. Action word second, person third, time at the end.", "Question word → Action word → Person → Time"),
    "Wohin fahren Sie?":        ("Question word first", "Wohin = Where to. Short version of the same question pattern.", "Question word → Action word → Person"),
    "Wie spät ist es?":         ("Question word first", "'Wie spät' = What time — one question phrase. Action word (ist) second.", "Question phrase → Action word → 'it'"),
    "Wie spät ist es bitte?":   ("Question word first", "Same as above. 'bitte' (= please) can go anywhere — it just softens the question.", "Question phrase → Action word → 'it' → bitte"),
    "Wann haben Sie Geburtstag?": ("Question word first", "Wann = When. Action word second, person third.", "Question word → Action word → Person → Noun"),
    "Wann ist die Busfahrt?":   ("Question word first", "Wann = When. Action word (ist) second.", "Question word → Action word → Thing"),
    "Wann kommen Sie?":         ("Question word first", "Wann = When. Action word second, person third.", "Question word → Action word → Person"),
    "Wann ist die nächste Abfahrt?": ("Question word first", "Wann = When. Action word (ist) second.", "Question word → Action word → Thing"),
    "Wo ist die Information?":  ("Question word first", "Wo = Where. Action word (ist) second.", "Question word → Action word → Thing"),
    "Wo finde ich die Kasse?":  ("Question word first", "Wo = Where. Action word second, then the person (ich=I) after.", "Question word → Action word → Person → Thing"),
    "Wo bekomme ich Briefmarken?": ("Question word first", "Wo = Where. Action word second, person third.", "Question word → Action word → Person → Thing"),
    "Wo kaufen Sie ein?":       ("Split verb — second part jumps to end", "'Einkaufen' (= to shop) is a verb that splits in two. The first part (kaufen) stays near the front, and 'ein' jumps to the very end of the sentence.", "Question word → Main part → Person → [ein]"),
    "Wie komme ich in den zweiten Stock?": ("Question word first", "Wie = How. Action word second, person (ich) third, then the destination.", "Question word → Action word → Person → Destination"),
    "Wie komme ich zum Bahnhof?": ("Question word first", "Wie = How. Action word second. 'zum' = to the (used for going somewhere).", "Question word → Action word → Person → Destination"),
    "Wie möchten Sie bezahlen?": ("Question word + 'want/would like'", "Wie = How. The 'want' word (möchten) comes second. The main action (bezahlen) jumps to the very END.", "Question word → 'want' word → Person → [main action]"),
    "Wie viele Personen reisen mit?": ("Split verb — second part jumps to end", "'Mitreisen' (= travel along) splits: 'reisen' stays near the front, 'mit' jumps to the END.", "Question phrase → Main part → Person → [mit]"),
    "Wie viele Kinder haben Sie dabei?": ("Question word first", "'Wie viele' = How many. Action word second, person third, extra word at end.", "Question phrase → Action word → Person → Extra"),
    "Was kostet dieser Pullover?": ("Question word first", "Was = What / How much. Action word (kostet=costs) second.", "Question word → Action word → Thing"),
    "Wo ist die Umkleidekabine?": ("Question word first", "Wo = Where. Action word (ist) second.", "Question word → Action word → Thing"),
    "Was ist Ihre Urlaubsadresse?": ("Question word first", "Was = What. 'Ihre' = your (polite form).", "Question word → Action word → Thing"),
    "Wie ist Ihre Postleitzahl?": ("Question word first", "Wie = What (used for codes and numbers in German).", "Question word → Action word → Thing"),
    "Der wievielte ist heute?":  ("Question word first", "'Der wievielte' = What date. Action word (ist) second.", "Question phrase → Action word → 'today'"),
    "Auf welchem Gleis fährt der Zug ab?": ("Split verb — second part jumps to end", "'Abfahren' (= to depart) splits: 'fährt' stays near the front, 'ab' jumps to the END.", "Question phrase → Main part → Subject → [ab]"),
    "Haben Sie eine Zeitung?":  ("Yes/No question — action word first", "When you ask a yes/no question, the action word goes FIRST (no question word needed). Person comes second.", "Action word → Person → Thing"),
    "Haben Sie das auch in Größe 42?": ("Yes/No question — action word first", "Action word first, person second. Same yes/no pattern.", "Action word → Person → Thing → Extra"),
    "Kann ich mit Kreditkarte bezahlen?": ("'Can/must/want' word first in question", "When you use a 'can/must/want' word in a yes/no question, it goes FIRST. The main action (bezahlen) jumps to the very END.", "'Can' word → Person → Info → [main action]"),
    "Gibt es etwas ohne Fleisch?": ("Yes/No question — action word first", "'Gibt es' = Is there. Action word (gibt) first, then 'es'.", "Action word → es → Thing → Info"),
    "Kommst du mit?":           ("Split verb in yes/no question", "Yes/no question. 'Mitkommen' (= come along) splits: 'Kommst' first, 'mit' jumps to the END.", "Main part → Person → [mit]"),
    "Passt Ihnen das?":         ("Yes/No question — action word first", "Action word (passt=suits) first, then 'Ihnen' (=you, polite), then 'das' (=that).", "Action word → Person (polite) → Subject"),
    "Ich heiße Maria Müller.":  ("Normal order: Person → Action → Rest", "In a normal statement, the person (Ich=I) comes first and the action word (heiße=am called) is always second.", "Person → Action word → Name"),
    "Ich komme aus Indien.":    ("Normal order + 'from'", "Person first, action second. 'aus' + country = from [country].", "Person → Action word → aus + Country"),
    "Ich wohne in München.":    ("Normal order + 'in'", "Person first, action second. 'in' + city = in [city].", "Person → Action word → in + City"),
    "Ich bin verheiratet.":     ("Normal order with 'am/is/are'", "'bin' = am. Person first, 'am/is/are' second, then describing word.", "Person → am/is/are → Describing word"),
    "Ich bin ledig.":           ("Normal order with 'am/is/are'", "Simple: I am [something]. Person → am → describing word.", "Person → am → Describing word"),
    "Ich bin 32 Jahre alt.":    ("Normal order with 'am/is/are'", "Person → am → age → Jahre (years) → alt (old). The word 'alt' always goes at the end.", "Person → am → Age → Jahre → alt"),
    "Ich habe zwei Kinder.":    ("Normal order with 'have'", "Person first, 'have' word second, then what you have.", "Person → have → Number → Thing"),
    "Ich spreche Deutsch und Englisch.": ("Normal order", "Person first, action second, then the things, joined with 'und' (and).", "Person → Action word → Thing 1 → und → Thing 2"),
    "Mein Hobby ist Musik.":    ("Normal order with 'is'", "The thing (Mein Hobby) first, 'ist' (=is) second, then what it equals.", "Thing → is → What it equals"),
    "Ich esse gern Brot und Obst.": ("Normal order + 'gern' = like to", "Put 'gern' after the action word to say you LIKE doing something. It means 'gladly / like to'.", "Person → Action word → gern → Thing"),
    "Ich trinke gern Kaffee.":  ("Normal order + 'gern' = like to", "'gern' after the action word = I like to drink. Very useful little word!", "Person → Action word → gern → Thing"),
    "Ich esse kein Fleisch.":   ("Saying 'no' with kein", "'kein/keine' before a noun means 'no / not any'. It replaces 'ein/eine'.", "Person → Action → kein/keine → Thing"),
    "Ich bezahle bar.":         ("Normal order", "Simple statement. Person → action → how you do it.", "Person → Action word → How"),
    "Ich bezahle mit Kreditkarte.": ("Normal order + 'with'", "'mit' = with/using. No need for 'a/the' after 'mit Kreditkarte'.", "Person → Action word → mit → Thing"),
    "Ich nehme den Pullover.":  ("Normal order", "Person → action → thing. Simple sentence.", "Person → Action word → Thing"),
    "Ich suche einen Stadtplan.": ("Normal order", "Person → action → thing. Simple sentence.", "Person → Action word → Thing"),
    "Ich fahre ans Meer.":      ("Normal order + direction", "'ans' = an + das = to the. Used for going towards something.", "Person → Action word → to the + Place"),
    "Ich fahre zu meinen Verwandten.": ("Normal order + 'zu' = to (people)", "'zu' is used when going to people or their home. 'meinen' = my (in this form).", "Person → Action word → zu → Person/Place"),
    "Ich bleibe drei Wochen.":  ("Normal order + duration", "How long you stay — just put the time after the action word. No extra word needed.", "Person → Action word → Length of time"),
    "Ich warte an der Information auf dich.": ("Normal order", "'warten auf' = to wait for (someone). 'dich' = you (casual). Place comes before the person.", "Person → wait → at the place → for → Person"),
    "Ich lerne seit drei Monaten Deutsch.": ("'seit' = for/since (ongoing)", "'seit' + time = for [length of time]. Use present tense — the action is still happening now!", "Person → Action word → seit → Time → Thing"),
    "Ich komme am Montag.":     ("Normal order + day", "'am' + day of the week = on [day]. Am Montag = on Monday.", "Person → Action word → am + Day"),
    "Ich bringe Kuchen mit.":   ("Split verb — second part jumps to end", "'Mitbringen' (= bring along) splits: 'bringe' stays near front, 'mit' jumps to the END.", "Person → Main part → Thing → [mit]"),
    "Ich hole dich vom Bahnhof ab.": ("Split verb — second part jumps to end", "'Abholen' (= pick up) splits: 'hole' stays near front, 'ab' jumps to the END.", "Person → Main part → Who → Place → [ab]"),
    "Ich warte seit 20 Minuten.": ("'seit' = for/since (ongoing)", "'seit' + time = I have been waiting for [time]. Still happening now — so use present tense.", "Person → Action word → seit → Time"),
    "Ich bitte um Informationen über Hotels.": ("Normal order + 'about'", "'bitten um' = to ask for. 'über' = about.", "Person → ask for → Thing → about → Thing"),
    "Ich möchte Informationen über das Hotel.": ("'Would like'", "'möchte' = would like. Just put what you want after it.", "Person → would like → Thing"),
    "Ich möchte einen Termin machen.": ("'Would like' + main action at end", "'möchte' = would like. The MAIN action (machen=make) always jumps to the very END.", "Person → would like → Thing → [main action]"),
    "Ich möchte das bitte zurückgeben.": ("'Would like' + main action at end", "Split verb 'zurückgeben' (= return/give back) goes as one piece to the END.", "Person → would like → Thing → bitte → [return]"),
    "Wir buchen eine Ferienwohnung.": ("Normal order", "Person (Wir=We) first, action second, thing third.", "Person → Action word → Thing"),
    "Wir fangen um 21 Uhr an.": ("Split verb — second part jumps to end", "'Anfangen' (= start) splits: 'fangen' stays near front, 'an' jumps to the END.", "Person → Main part → Time → [an]"),
    "Wir wollen draußen im Garten feiern.": ("'Want to' + main action at end", "'wollen' = want to. The main action (feiern=celebrate) jumps to the END. Place goes before it.", "Person → want to → Place → [main action]"),
    "Wir können leider nicht kommen.": ("'Can' word + main action at end", "'können' = can. 'nicht' = not. Main action (kommen=come) jumps to the END.", "Person → can → unfortunately → not → [main action]"),
    "Wir treffen uns um halb eins am Bus.": ("Action + 'each other'", "'uns' = each other (we meet each other). Time (um halb eins) comes before place (am Bus).", "Person → Action → each other → Time → Place"),
    "Er ruft mich morgen an.":  ("Split verb — second part jumps to end", "'Anrufen' (= call) splits: 'ruft' stays near front, 'an' jumps to END. Time (morgen=tomorrow) in the middle.", "Person → Main part → Who → Time → [an]"),
    "Der Film fängt um 20 Uhr an.": ("Split verb — second part jumps to end", "'Anfangen' (= start) splits: 'fängt' near front, 'an' at END. Time in the middle.", "Subject → Main part → Time → [an]"),
    "Von Beruf bin ich Arzt.":  ("Time/topic first — action stays second", "When you START with something other than the person, the action word still stays second — and the person shifts AFTER it.", "Topic first → Action word → Person → ..."),
    "Zum Frühstück esse ich Brötchen.": ("Time/topic first — action stays second", "Topic (Zum Frühstück) first → action word (esse) second → person (ich) third. The person moves after the action.", "Topic → Action word → Person → Thing"),
    "Am Sonntag haben wir Zeit.": ("Time first — action stays second", "Time (Am Sonntag) first → action word (haben) second → person (wir) third.", "Time → Action word → Person → Thing"),
    "Heute ist der zwanzigste Februar.": ("Time first — action stays second", "Today (Heute) first → action word (ist) second → subject after.", "Time → Action word → Subject"),
    "Heute Abend gibt es Volksmusik und Tanz.": ("Time first + 'there is'", "'Es gibt' = there is/are. When time comes first, 'gibt' moves to position 2, 'es' follows.", "Time → gibt → es → Things"),
    "In der Pause gibt es belegte Brötchen.": ("Place/time first + 'there is'", "'Es gibt' = there is/are. Place or time first, 'gibt' moves to position 2.", "Place/Time → gibt → es → Thing"),
    "Hier darf man nicht rauchen.": ("Place first + 'allowed to'", "Place (Hier=Here) first → 'allowed to' word (darf) second → 'man' (=one/people in general) third → main action at END.", "Place → allowed word → people → not → [main action]"),
    "Gehen Sie hier rechts um die Ecke.": ("Giving an instruction (polite)", "To give a polite instruction in German, start with the action word, then 'Sie' immediately after. Directions follow.", "Action word → Sie → Directions"),
    "In ein paar Minuten kommen wir an.": ("Time first + split verb at end", "Time phrase first → action word second → person third → split part at END.", "Time → Action word → Person → [an]"),
    "Am Samstagnachmittag ist die Post geschlossen.": ("Time first — action stays second", "Time first → action word (ist) second → subject → describing word at end.", "Time → Action word → Subject → Describing word"),
    "Der Kurs beginnt um 9 Uhr morgens.": ("Normal order + time at end", "Subject first, action second, time info at the end.", "Subject → Action word → Time"),
    "Ich kann gut schwimmen.":  ("'Can/must/want' + main action at end", "'kann' = can. The main action (schwimmen=swim) ALWAYS jumps to the very END. 'gut' (=well) goes in the middle.", "Person → can → well → [main action]"),
    "Ich kann mit dem Bus kommen.": ("'Can' + main action at end", "'kann' = can. Main action (kommen=come) at END. 'mit dem Bus' = by bus.", "Person → can → by bus → [main action]"),
    "Ich muss für die Prüfung lernen.": ("'Must' + main action at end", "'muss' = must/have to. Main action (lernen=study) at END.", "Person → must → for the exam → [main action]"),
    "Ich will nach Deutschland fliegen.": ("'Want to' + main action at end", "'will' = want to. Main action (fliegen=fly) at END. 'nach' + country = to [country].", "Person → want to → to Germany → [main action]"),
    "Sie soll viel Wasser trinken.": ("'Should' + main action at end", "'soll' = should (someone else is telling her). Main action (trinken=drink) at END.", "Person → should → a lot of water → [main action]"),
    "Können Sie bitte langsamer sprechen?": ("Question with 'can' + main action at end", "'Können' = Can (question). Main action (sprechen=speak) jumps to the very END.", "'Can' word → Person → bitte → slower → [main action]"),
    "Können Sie mir bitte helfen?": ("Question with 'can' + main action at end", "'mir' = to me. Main action (helfen=help) at END.", "'Can' word → Person → to me → bitte → [main action]"),
    "Können Sie das bitte wiederholen?": ("Question with 'can' + main action at end", "Main action (wiederholen=repeat) at END.", "'Can' word → Person → that → bitte → [main action]"),
    "Können Sie bitte Ihren Namen buchstabieren?": ("Question with 'can' + main action at end", "Main action (buchstabieren=spell) at END.", "'Can' word → Person → bitte → Name → [main action]"),
    "Kann ich schnell mal rüberkommen?": ("Question with 'can' + main action at end", "'Kann' first in a yes/no question. Main action at END.", "'Can' word → Person → quickly → [main action]"),
    "Ich kann nichts drucken.":  ("'Can' word + 'nothing' + main action at end", "'nichts' = nothing. 'kann' = can. Main action (drucken=print) at END.", "Person → can → nothing → [main action]"),
    "Nehmen Sie den Aufzug.":   ("Polite instruction — action word first", "For polite instructions, start with the action word, then 'Sie' straight after.", "Action word → Sie → Thing"),
    "Bitte gehen Sie geradeaus.": ("Polite instruction — action word first", "'bitte' before the action word makes it extra polite. Action → Sie → direction.", "bitte → Action word → Sie → Direction"),
    "Bitte pünktlich sein!":    ("Short instruction without a person", "This is a sign/announcement style. Just: bitte + describing word + main action. No 'Sie' needed.", "bitte → Describing word → Main action"),
    "Bitte hier nicht aussteigen.": ("Short instruction without a person", "Sign style. 'nicht' = not. 'aussteigen' = get off. No person needed.", "bitte → Place → not → Main action"),
    "Sprechen Sie bitte langsamer!": ("Polite instruction — action word first", "Action word (Sprechen) first → Sie → bitte. 'langsamer' = more slowly (add -er for 'more ...').", "Action word → Sie → bitte → More slowly"),
    "Öffnen Sie bitte die Tür.": ("Polite instruction — action word first", "Action word first → Sie → bitte → thing to be acted on.", "Action word → Sie → bitte → Thing"),
    "Geben Sie mir bitte das Buch.": ("Polite instruction with two things", "Action word first → Sie → 'mir' (= to me, the receiver) → bitte → the thing given.", "Action word → Sie → to me → bitte → the Thing"),
    "Bitte rufen Sie uns zurück.": ("Polite instruction + split verb", "'Zurückrufen' (= call back) splits: 'rufen' stays near front, 'zurück' at END.", "bitte → Main part → Sie → us → [zurück]"),
    "Vergessen Sie nicht die Unterschrift!": ("Polite instruction + 'not'", "Action word → Sie → 'nicht' (not) → the thing.", "Action word → Sie → not → Thing"),
    "Tragen Sie Ihren Familiennamen ein.": ("Polite instruction + split verb", "'Eintragen' (= enter/fill in) splits: 'Tragen' near front, 'ein' at END.", "Main part → Sie → Thing → [ein]"),
    "Der Zug fährt um 7:34 Uhr ab.": ("Split verb — second part jumps to end", "'Abfahren' (= depart) splits: 'fährt' near front, 'ab' at END. Time goes in the middle.", "Subject → Main part → Time → [ab]"),
    "Der Zug kommt um 12:05 Uhr an.": ("Split verb — second part jumps to end", "'Ankommen' (= arrive) splits: 'kommt' near front, 'an' at END.", "Subject → Main part → Time → [an]"),
    "Das Sprachenzentrum ist umgezogen.": ("Talking about the past", "To talk about a past event, use 'ist/hat' + the past form of the verb at the END. Moving verbs use 'ist'.", "Subject → ist/hat → [past form of verb]"),
    "Es ist viertel nach zwei.": ("Telling the time", "'Es ist' = It is. For quarter past: viertel nach [hour]. For quarter to: viertel vor [hour].", "Es ist → viertel → nach/vor → hour"),
    "Es ist viertel vor zwei.": ("Telling the time — 'to'", "'vor' = to/before. Viertel vor zwei = 15 minutes before 2 o'clock.", "Es ist → viertel → vor → hour"),
    "Es ist halb drei.":        ("Telling the time — WATCH OUT!", "German 'halb' (=half) counts towards the NEXT hour, not the last one. 'halb drei' = half past TWO (not three!).", "Es ist → halb → NEXT hour"),
    "Es ist kurz nach zwei.":   ("Telling the time", "'kurz nach' = just after. Informal way to say a few minutes past.", "Es ist → kurz → nach → hour"),
    "Es ist kurz vor zwei.":    ("Telling the time", "'kurz vor' = just before. Informal way to say a few minutes to.", "Es ist → kurz → vor → hour"),
    "Es ist gleich 5 Uhr.":     ("Telling the time", "'gleich' = almost / just about. The time is about to be 5.", "Es ist → gleich → hour → Uhr"),
    "Der Zug kommt um 12.36 Uhr an.": ("Split verb + time", "'um' + time = at [time]. 'Ankommen' splits: 'kommt' near front, 'an' at END.", "Subject → Main part → um + Time → [an]"),
    "Ich habe am neunzehnten September Geburtstag.": ("Saying your birthday date", "'am' + date + month. Dates end in -ten (1st–19th) or -sten (20th+) when used with 'am'.", "Person → have → am + Date + Month → birthday"),
    "Heute ist der zwanzigste Februar.": ("Stating today's date", "Dates end in -te (1st–19th) or -ste (20th+) when used after 'der'.", "Today is → der → Date + Month"),
    "Die Post ist montags bis freitags geöffnet.": ("Days of the week with -s = 'every ...'", "Add -s to a day of the week to say 'every [day]'. montags = every Monday.", "Subject → is → every [day] → bis → every [day] → open"),
    "Von 8 bis 12 Uhr und von 13 bis 18 Uhr.": ("Opening hours pattern", "'von … bis …' = from … to … Perfect for opening hours.", "von + time → bis + time"),
    "Die Post ist samstags bis 12 Uhr geöffnet.": ("Days with -s = 'every ...'", "samstags = every Saturday. 'geöffnet' = open. Describing word goes at end with 'is'.", "Subject → is → every Saturday → bis + time → open"),
    "Mein Lieblingsessen ist Fisch.": ("Normal order with 'is'", "Thing (My favourite food) first, 'ist' second, then what it equals.", "Thing → is → What it equals"),
    "Das Bier kostet 3,50 Euro.": ("Normal order", "Thing → costs → price. Simple.", "Thing → costs → Price"),
    "Der Pullover kostet 19,95 Euro.": ("Normal order", "Thing → costs → price.", "Thing → costs → Price"),
    "Das ist 30 Prozent billiger.": ("Comparing things", "Add -er to an adjective to say 'more ...'. billig → billiger = cheaper.", "That → is → % → more [adjective]"),
    "Das ist zu teuer.":         ("'Too' + describing word", "'zu' before a describing word = too. zu teuer = too expensive.", "That → is → too → Describing word"),
    "Es werden viele Leute da sein.": ("Talking about the future", "'werden' + action at END = future tense (will). Similar to 'will' in English.", "There → will → many people → [be there]"),
    "Die Party findet draußen statt.": ("Split verb — second part jumps to end", "'Stattfinden' (= take place) splits: 'findet' near front, 'statt' at END.", "Subject → Main part → Place → [statt]"),
    "Das Hotel hat ein Restaurant mit Terrasse.": ("Normal order with 'has'", "Subject → has → thing. 'mit' = with (describing a feature).", "Subject → has → a + Thing → with + Feature"),
    "Das Schiff fährt täglich von Rüdesheim.": ("Normal order + time word", "'täglich' = daily (every day). Placed after the action word.", "Subject → Action word → daily → from + Place"),
    "Das geht leider nicht.":   ("Saying something isn't possible", "'geht' here = is possible / works. 'nicht' at end = not. 'leider' = unfortunately (softens it).", "That → works → unfortunately → not"),
    "Mein Computer hat einen Fehler.": ("Normal order with 'has'", "Subject → has → thing. Simple statement.", "Subject → has → a + Thing"),
    "Ich hätte gern die Bratwurst.": ("Polite way to order", "'hätte gern' = would like (very polite). Use this when ordering food or drinks.", "Person → would like → the + Thing"),
    "Ich lade euch herzlich ein.": ("Split verb — second part jumps to end", "'Einladen' (= invite) splits: 'lade' near front, 'ein' at END. 'euch' = you all. 'herzlich' = warmly.", "Person → Main part → you all → warmly → [ein]"),
    "Schicken Sie mir bitte das Kulturprogramm.": ("Polite instruction with two things", "Action first → Sie → 'mir' (to me, the receiver) → bitte → the thing being sent.", "Action word → Sie → to me → bitte → the Thing"),
    "Ich warte an der Information auf dich.": ("Waiting for someone", "'warten auf' = to wait for (someone). 'dich' = you (casual). Place comes before the person.", "Person → wait → at the Place → for → Person"),
    "Könntet ihr einen Salat mitbringen?": ("Polite request with 'could'", "'Könntet' = could (more polite than 'könnt'). Split verb 'mitbringen': main action at END.", "'Could' word → you all → Thing → [bring along]"),
    "Könnte ich bitte ein Glas Wasser haben?": ("Polite request with 'could'", "'Könnte ich' = Could I. Main action (haben=have) at END. Very polite way to ask for something.", "'Could' word → Person → bitte → Thing → [have]"),
    "Schön, Sie kennenzulernen!": ("Fixed phrase — nice to meet you", "This is a fixed phrase. Just learn it as a whole: 'Schön, Sie kennenzulernen!' = Nice to meet you!", "Fixed phrase — learn as a whole"),
    "Guten Appetit!":           ("Fixed phrase — enjoy your meal", "A set expression said before eating. Just learn it as a whole.", "Fixed phrase — learn as a whole"),
    "Frohe Weihnachten!":       ("Fixed phrase — Merry Christmas", "A set expression. Just learn it as a whole.", "Fixed phrase — learn as a whole"),
    "Schöne Ferien!":           ("Fixed phrase — enjoy your holidays", "A set expression. Just learn it as a whole.", "Fixed phrase — learn as a whole"),
    "Tut mir leid.":            ("Fixed phrase — I'm sorry", "'Tut mir leid' = I'm sorry. Literally 'does sorrow to me'. Just learn it as one fixed phrase.", "Fixed phrase — learn as a whole"),
    "Tut mir leid, ich habe keins.": ("Fixed phrase + 'I have none'", "'keins' = none (when no noun follows). 'Ich habe keins' = I don't have any.", "Fixed phrase + Person → have → none"),
    "Leider nicht.":            ("Short answer — No, unfortunately", "Short answer. 'Leider' = unfortunately. The action word is dropped — just say these two words.", "unfortunately + not"),
    "Ja, gern!":                ("Short answer — Yes, gladly!", "Short answer. 'gern' = gladly / with pleasure. Very common and friendly response in German.", "Yes + gladly"),
    "Ja, natürlich.":           ("Short answer — Yes, of course", "Short answer. 'natürlich' = of course / naturally.", "Yes + of course"),
    "Kein Problem.":            ("Short answer — No problem", "'kein' = no (used before nouns). Just a fixed short phrase.", "No + Problem"),
    "Hier, bitte.":             ("Short answer — Here you go", "Short response when handing something over. 'bitte' = please AND 'here you go'.", "Here + please/here you go"),
    "Vielen Dank!":             ("Fixed phrase — Thank you very much", "'Vielen Dank' = Many thanks. Just learn as a whole phrase.", "Fixed phrase — learn as a whole"),
    "Bitte schön.":             ("Fixed phrase — You're welcome", "Response to 'Danke'. Also said when handing something over.", "Fixed phrase — learn as a whole"),
    "Wie bitte? Ich habe das nicht verstanden.": ("Talking about the past", "'Ich habe … verstanden' = I have understood (talking about the past). 'nicht' goes before the past form.", "Person → have → thing → not → [past form]"),
    "Eine Flasche Weißwein, bitte.": ("Ordering — short version", "To order something, just say the item + 'bitte'. No verb needed!", "a/the + Thing + bitte"),
    "Ein Glas Wasser, bitte!":  ("Ordering — short version", "To order, just say the item + 'bitte'. Very natural in German.", "a/the + Thing + bitte"),
    "Einen Moment bitte.":      ("Short request", "'Einen Moment' = One moment. Short polite request with no verb needed.", "One + Moment + bitte"),
    "Einen Moment bitte!":      ("Short request", "Same as above — just said with more urgency.", "One + Moment + bitte"),
    "Die Salatplatte ist leider aus.": ("Normal order + 'unfortunately'", "'leider' = unfortunately. 'aus' here = sold out / finished.", "Thing → is → unfortunately → sold out"),
    "Ich kann Ihnen den Fisch empfehlen.": ("'Can' word + main action at end", "'kann' = can. 'Ihnen' = to you (polite). Main action (empfehlen=recommend) at END.", "Person → can → to you → the + Thing → [recommend]"),
    "Auf dem Bahnhof ist Rauchen verboten.": ("Place first — action stays second", "Place first → action word (ist) second. 'Rauchen' = smoking (used as a noun here). 'verboten' = forbidden.", "Place → is → smoking → forbidden"),
    "Sie kommen im August nach Dresden.": ("Normal order + time + direction", "'im August' = in August. 'nach' + city = to [city].", "Person → Action word → in + Month → nach + City"),
    "Von 23 Uhr bis 1 Uhr fährt kein Bus.": ("Time first — action stays second", "Time phrase first → action word second → 'kein' (=no) before the noun.", "Time → Action word → no + Thing"),
    "Bitte füllen Sie das Formular aus.": ("Polite instruction + split verb", "'Ausfüllen' (= fill in) splits: 'füllen' near front, 'aus' at END.", "bitte → Main part → Sie → Thing → [aus]"),
    "Am kommenden Sonntag habe ich Geburtstag.": ("Time first — action stays second", "Time phrase first → action word (habe) second → person (ich) third.", "Time → Action word → Person → birthday"),
    "Ich bezahle mit Kreditkarte.": ("Normal order + 'with'", "'mit' = with/using. 'mit Kreditkarte' = by credit card.", "Person → Action word → mit → Thing"),
    "Wie möchten Sie bezahlen?": ("Question with 'would like' + main action at end", "Question word first, 'would like' word second, person third, main action at END.", "Question word → 'would like' → Person → [main action]"),
    "Geben Sie mir bitte eine Quittung.": ("Polite instruction with two things", "Action first → Sie → 'mir' (to me) → bitte → the thing being given.", "Action word → Sie → to me → bitte → a + Thing"),
    "Entschuldigen Sie bitte!":  ("Polite instruction — action word first", "Getting someone's attention. Action word first, Sie after, bitte to be polite.", "Action word → Sie → bitte"),
    "Entschuldigung, ich suche Schuhe.": ("Fixed opener + normal sentence", "'Entschuldigung' = Excuse me — a fixed opener. Normal sentence follows.", "Excuse me, Person → looking for → Thing"),
    "Herr Albers, bitte zum Schalter F7.": ("Short announcement — verb left out", "In announcements and signs, the action word is often left out. 'bitte' + place = please go to [place].", "Name + bitte → Place (verb left out)"),
    "Bitte pünktlich sein!":    ("Short instruction without a person", "Sign/announcement style. No person needed, just bitte + describing word + action at end.", "bitte + on time + [main action]"),
    "Das Sprachenzentrum ist umgezogen.": ("Talking about the past", "'ist umgezogen' = has moved. Talking about a past event. The past form goes at the END.", "Subject → ist/hat → [past form of verb]"),
    "Ich warte an der Information auf dich.": ("Normal order", "'warten auf' = to wait for someone. 'dich' = you (casual). Place before person.", "Person → wait → at the Place → for → Person"),
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def render_breakdown_and_grammar(german_sentence: str):
    """Render word-by-word breakdown + grammar note for a sentence."""
    breakdown = WORD_BREAKDOWN.get(german_sentence, "")
    grammar = GRAMMAR_NOTES.get(german_sentence, None)

    if breakdown:
        parts_html = "<br>".join(
            f"<span style='color:#cdd6f4; font-weight:600;'>{p.split(' = ')[0].strip()}</span>"
            f" = <span style='color:#a6e3a1;'>{p.split(' = ')[1].strip()}</span>"
            if " = " in p else f"<span style='color:#9399b2;'>{p}</span>"
            for p in breakdown.split(" · ")
        )
        st.markdown(
            f"<div style='padding:12px 16px; background:#1e1e2e; border-radius:10px; "
            f"border-left:4px solid #89b4fa; margin-top:8px;'>"
            f"<div style='font-size:0.9rem; font-weight:700; color:#89b4fa; margin-bottom:6px; "
            f"text-transform:uppercase; letter-spacing:0.05em;'>🔍 Wort für Wort</div>"
            f"<div style='font-size:0.92rem; line-height:1.9;'>{parts_html}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    if grammar:
        rule_name, explanation, pattern = grammar
        st.markdown(
            f"<div style='padding:12px 16px; background:#1e1e2e; border-radius:10px; "
            f"border-left:4px solid #f38ba8; margin-top:8px;'>"
            f"<div style='font-size:0.9rem; font-weight:700; color:#f38ba8; margin-bottom:4px; "
            f"text-transform:uppercase; letter-spacing:0.05em;'>💡 How this sentence works: {rule_name}</div>"
            f"<div style='font-size:0.92rem; color:#cdd6f4; margin-bottom:6px;'>{explanation}</div>"
            f"<div style='font-size:0.85rem; color:#fab387; font-family:monospace; "
            f"background:#313244; padding:5px 10px; border-radius:6px;'>{pattern}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

def get_pool(chapter: str) -> dict:
    if chapter == "Alle Themen":
        return ALL_VOCAB
    return VOCAB_BY_CHAPTER[chapter]


def build_deck(pool: dict) -> list:
    keys = list(pool.keys())
    random.shuffle(keys)
    return keys


def make_mc_question(pool: dict, word: str):
    """Multiple-choice: show German phrase, pick English meaning."""
    all_answers = list(pool.values())
    correct_en = pool[word]
    wrong_pool = [a for a in all_answers if a != correct_en]
    distractors = random.sample(wrong_pool, min(3, len(wrong_pool)))
    options = distractors + [correct_en]
    random.shuffle(options)
    return word, correct_en, options


def make_tile_question(pool: dict, word: str):
    """Tile mode: show English meaning, sort German words."""
    question_en = pool[word]
    return question_en, word


def make_tiles(correct_german: str) -> list[str]:
    """Split German sentence into word tiles, shuffle them."""
    import re
    # Split on spaces but keep punctuation attached to words
    tokens = re.findall(r"\S+", correct_german)
    shuffled = tokens[:]
    # Ensure it's not already in order
    for _ in range(10):
        random.shuffle(shuffled)
        if shuffled != tokens:
            break
    return shuffled


# ── Grammar tables for the typing quiz ───────────────────────────────────────
# ── Dedicated tile vocab — longer sentences from the TELC A1 test ─────────────
# Organised by the same chapter names so the sidebar filter still works.
TILE_VOCAB_BY_CHAPTER: dict[str, dict[str, str]] = {

    "Sich vorstellen": {
        "Können Sie bitte Ihren Familiennamen buchstabieren?":
            "Can you please spell your surname?",
        "Ich lerne seit drei Monaten Deutsch.":
            "I have been learning German for three months.",
        "Von Beruf bin ich Ärztin und ich arbeite in Berlin.":
            "By profession I am a doctor and I work in Berlin.",
        "Ich spreche Deutsch, Englisch und ein bisschen Spanisch.":
            "I speak German, English and a little Spanish.",
        "Wie lange leben Sie schon in Deutschland?":
            "How long have you been living in Germany?",
        "Was machen Sie in Ihrer Freizeit?":
            "What do you do in your free time?",
        "Ich bin verheiratet und habe zwei Kinder.":
            "I am married and have two children.",
        "Möchten Sie bitte anfangen?":
            "Would you like to start please?",
        "Wir beginnen mit Teil eins.":
            "We are starting with part one.",
        "Bitte sagen Sie uns etwas über sich.":
            "Please tell us something about yourself.",
    },

    "Essen und Trinken": {
        "Was essen Sie gern zum Frühstück?":
            "What do you like to eat for breakfast?",
        "Entschuldigung, die Salatplatte ist leider aus.":
            "I'm sorry, the salad plate is unfortunately sold out.",
        "Aber die Bratwurst kann ich Ihnen empfehlen.":
            "But I can recommend the grilled sausage to you.",
        "Ich esse kein Fleisch. Gibt es etwas ohne Fleisch?":
            "I don't eat meat. Is there something without meat?",
        "Ich hätte gern eine Flasche Weißwein, bitte.":
            "I would like a bottle of white wine, please.",
        "Zum Frühstück esse ich Brot und trinke Kaffee.":
            "For breakfast I eat bread and drink coffee.",
        "Was ist Ihr Lieblingsessen und warum?":
            "What is your favourite meal and why?",
        "Wir essen am Sonntag gern Fisch mit Salat.":
            "On Sundays we like to eat fish with salad.",
        "Könnte ich bitte die Speisekarte haben?":
            "Could I please have the menu?",
        "Heute Abend gibt es Brezeln, Weißwürste und Sauerkraut.":
            "This evening there are pretzels, white sausages and sauerkraut.",
    },

    "Einkaufen": {
        "Entschuldigung, was kostet dieser Pullover jetzt?":
            "Excuse me, how much does this jumper cost now?",
        "Da steht dreißig Prozent billiger.":
            "It says thirty percent cheaper.",
        "Kann ich mit Kreditkarte oder bar bezahlen?":
            "Can I pay by credit card or cash?",
        "Haben Sie diesen Pullover auch in Größe zweiundvierzig?":
            "Do you also have this jumper in size forty-two?",
        "Geben Sie mir bitte eine Quittung für den Pullover.":
            "Please give me a receipt for the jumper.",
        "Ich möchte diese Jacke bitte zurückgeben.":
            "I would like to return this jacket please.",
        "Entschuldigung, wo finde ich die Umkleidekabine?":
            "Excuse me, where do I find the changing room?",
        "Wo bekomme ich Briefmarken und einen Stadtplan?":
            "Where can I get stamps and a city map?",
        "Das ist mir leider zu teuer. Haben Sie etwas Billigeres?":
            "Unfortunately that is too expensive for me. Do you have something cheaper?",
        "Im Supermarkt kaufe ich Obst, Gemüse und Brot ein.":
            "At the supermarket I buy fruit, vegetables and bread.",
    },

    "Alltag & Unterwegs": {
        "Entschuldigen Sie, wie komme ich in den zweiten Stock?":
            "Excuse me, how do I get to the second floor?",
        "Da gehen Sie hier rechts um die Ecke und nehmen den Aufzug.":
            "Go right around the corner here and take the lift.",
        "Ich warte an der Information auf dich.":
            "I'll wait for you at the information desk.",
        "Der Zug fährt um sieben Uhr vierunddreißig ab.":
            "The train departs at seven thirty-four.",
        "In ein paar Minuten kommen wir am Bahnhof an.":
            "In a few minutes we will arrive at the station.",
        "Wir treffen uns um halb eins am Bus, bitte pünktlich sein.":
            "We'll meet at the bus at half past twelve, please be on time.",
        "Bitte beachten Sie: Hier ist ein außerplanmäßiger Halt.":
            "Please note: this is an unscheduled stop.",
        "Auf welchem Gleis fährt der nächste Zug nach Hamburg ab?":
            "Which platform does the next train to Hamburg leave from?",
        "Wie lange fährt man mit dem Bus von hier zum Bahnhof?":
            "How long does it take by bus from here to the station?",
        "Herr Janda, bitte sofort zum Schalter F sieben.":
            "Mr Janda, please go immediately to gate F seven.",
    },

    "Alltagstexte & Formulare": {
        "Bitte füllen Sie das Formular vollständig aus.":
            "Please fill in the form completely.",
        "Vergessen Sie bitte nicht die Unterschrift am Ende.":
            "Please don't forget the signature at the end.",
        "Auf dem gesamten Bahnhof ist das Rauchen verboten.":
            "Smoking is forbidden throughout the entire station.",
        "Von dreiundzwanzig Uhr bis ein Uhr fährt kein Bus.":
            "No buses run from eleven pm to one am.",
        "Die Post ist montags bis freitags von acht bis zwölf Uhr geöffnet.":
            "The post office is open Monday to Friday from eight to twelve.",
        "Das Sprachenzentrum ist umgezogen. Sie finden uns jetzt in der Beethovenstraße.":
            "The language centre has moved. You can now find us in Beethovenstraße.",
        "In der Pause gibt es belegte Brötchen und Getränke für zwei Euro.":
            "During the break there are sandwiches and drinks for two euros.",
        "Heute Abend im Bavaria: Volksmusik und ab zwanzig Uhr Tanz.":
            "This evening at the Bavaria: folk music and dancing from 8 pm.",
        "Tragen Sie bitte Ihren Familiennamen und Ihren Vornamen ein.":
            "Please enter your surname and your first name.",
        "Der Reisepreis ist mit der Anmeldung zu bezahlen.":
            "The travel price is to be paid with the registration.",
    },

    "Reise & Freizeit": {
        "Am kommenden Sonntag habe ich Geburtstag und ich lade euch herzlich ein.":
            "Next Sunday is my birthday and I warmly invite you all.",
        "Wir fangen um einundzwanzig Uhr an. Ist das okay für euch?":
            "We start at nine pm. Is that okay for you all?",
        "Könntet ihr vielleicht einen Salat oder Brot mitbringen?":
            "Could you perhaps bring a salad or bread along?",
        "Wir wollen nämlich draußen im Garten feiern.":
            "We actually want to celebrate outside in the garden.",
        "Vergesst bitte nicht einen Pullover oder eine Jacke mitzubringen!":
            "Please don't forget to bring a jumper or a jacket!",
        "Die Party findet draußen statt, es werden viele Leute da sein.":
            "The party takes place outside, there will be a lot of people there.",
        "Ich fahre für drei Wochen zu meinen Verwandten nach Polen.":
            "I am going to visit my relatives in Poland for three weeks.",
        "Das Schiff fährt täglich von Rüdesheim nach Koblenz.":
            "The ship goes daily from Rüdesheim to Koblenz.",
        "Wir buchen eine Ferienwohnung am Bodensee für zwei Wochen.":
            "We are booking a holiday apartment at Lake Constance for two weeks.",
        "Wohin fahren Sie dieses Jahr im Urlaub?":
            "Where are you going on holiday this year?",
    },

    "Zahlen, Zeit & Datum": {
        "Dein Zug kommt hier in Hannover um zwölf Uhr sechsunddreißig an.":
            "Your train arrives here in Hanover at twelve thirty-six.",
        "Ich bin ab zwölf Uhr fünfzehn im Hauptbahnhof und warte auf dich.":
            "I'll be at the main station from twelve fifteen and will wait for you.",
        "Am neunzehnten September habe ich Geburtstag.":
            "My birthday is on the nineteenth of September.",
        "Heute ist der zwanzigste Februar zweitausendvierundzwanzig.":
            "Today is the twentieth of February two thousand and twenty-four.",
        "Die Post ist samstags nur bis zwölf Uhr geöffnet.":
            "The post office is only open until twelve on Saturdays.",
        "Von acht bis zwölf Uhr und von dreizehn bis achtzehn Uhr.":
            "From eight to twelve and from one to six pm.",
        "Ich warte schon seit zwanzig Minuten an der Information.":
            "I have been waiting at the information desk for twenty minutes already.",
        "Es ist gleich fünf Uhr, vielen Dank und auf Wiedersehen.":
            "It is almost five o'clock, thank you very much and goodbye.",
        "Der Kurs beginnt am Montag um neun Uhr morgens.":
            "The course starts on Monday at nine in the morning.",
        "Am Samstagnachmittag ist die Post leider geschlossen.":
            "Unfortunately the post office is closed on Saturday afternoons.",
    },

    "Nützliche Sätze": {
        "Kannst du schnell mal rüberkommen? Mein Computer hat einen Fehler.":
            "Can you quickly come over? My computer has an error.",
        "Ich kann nichts drucken. Melde dich bitte gleich.":
            "I cannot print anything. Please get in touch right away.",
        "Wir können leider am Samstag nicht kommen, aber am Sonntag haben wir Zeit.":
            "Unfortunately we can't come on Saturday, but we are free on Sunday.",
        "Rufen Sie uns bitte zurück, ob Ihnen das passt.":
            "Please call us back to let us know if that suits you.",
        "Können Sie bitte langsamer sprechen? Ich verstehe Sie nicht.":
            "Can you please speak more slowly? I don't understand you.",
        "Ich möchte einen Termin machen. Wann haben Sie Zeit?":
            "I would like to make an appointment. When do you have time?",
        "Er ruft mich morgen an und ich hole ihn vom Bahnhof ab.":
            "He will call me tomorrow and I will pick him up from the station.",
        "Hier darf man leider nicht rauchen.":
            "Unfortunately you are not allowed to smoke here.",
        "Der Film fängt um zwanzig Uhr an. Kommst du mit?":
            "The film starts at eight pm. Are you coming along?",
        "Ich kann mit dem Bus kommen oder ich nehme ein Taxi.":
            "I can come by bus or I'll take a taxi.",
    },

    "Bitten & Reaktionen": {
        "Könnte ich bitte ein Glas Wasser haben? Ich habe großen Durst.":
            "Could I please have a glass of water? I am very thirsty.",
        "Können Sie mir bitte helfen? Ich suche den Schalter F sieben.":
            "Could you please help me? I am looking for gate F seven.",
        "Können Sie das bitte noch einmal wiederholen? Ich habe das nicht verstanden.":
            "Can you please repeat that once more? I didn't understand that.",
        "Tut mir leid, das geht leider nicht. Kein Problem?":
            "I'm sorry, unfortunately that's not possible. No problem?",
        "Sprechen Sie bitte etwas langsamer. Ich lerne noch Deutsch.":
            "Please speak a little more slowly. I am still learning German.",
        "Wie bitte? Ich habe das leider nicht verstanden.":
            "Pardon? I unfortunately didn't understand that.",
        "Geben Sie mir bitte eine Quittung und vielen Dank.":
            "Please give me a receipt and thank you very much.",
        "Entschuldigen Sie bitte! Wie komme ich zum Hauptbahnhof?":
            "Excuse me please! How do I get to the main station?",
        "Ich hätte gern die Bratwurst mit Pommes, bitte.":
            "I would like the grilled sausage with chips, please.",
        "Schicken Sie mir bitte das Kulturprogramm und Hoteladressen.":
            "Please send me the cultural programme and hotel addresses.",
    },
}

# Flat tile vocab for "Alle Themen"
ALL_TILE_VOCAB: dict = {}
for _tv in TILE_VOCAB_BY_CHAPTER.values():
    ALL_TILE_VOCAB.update(_tv)


# ── PDF-based vocab: German shown → user types English ───────────────────────
# Sourced directly from A1-Vocab-and-Phrases-Only-Notes.pdf
PDF_VOCAB_BY_CHAPTER: dict[str, dict[str, str]] = {

    "Begrüßung & Verabschiedung": {
        "Wie geht es dir?": "How are you?",
        "Wie geht's?": "How are you?",
        "Wie geht es Ihnen?": "How are you? (formal)",
        "Es geht mir gut.": "I am doing well.",
        "Es geht mir nicht gut.": "I am not doing well.",
        "Mir geht es auch gut. Danke.": "I am also well. Thank you.",
        "Und wie geht es dir?": "And how are you?",
        "Auf Wiedersehen.": "Goodbye.",
        "Auf Wiederhören.": "Goodbye. (on the telephone)",
        "Guten Morgen, Frank!": "Good morning, Frank!",
        "Guten Abend.": "Good evening.",
        "Gute Nacht.": "Good night.",
    },

    "Grundphrasen": {
        "Vielen Dank.": "Thank you very much.",
        "Danke schön.": "Thank you very much.",
        "Bitte sehr.": "You are welcome.",
        "Entschuldigen Sie bitte.": "Excuse me please.",
        "Es tut mir leid.": "I am sorry.",
        "Es tut mir sehr leid.": "I am very sorry.",
        "Kein Problem.": "No problem.",
        "Ja, Klar. Mache ich!": "Sure, I will do that.",
        "Sehr gut!": "Very good!",
        "Super, Danke.": "Great, thanks.",
        "Alles Klar.": "Understood.",
        "Das klingt gut!": "That sounds good!",
    },

    "Sich vorstellen": {
        "Mein Name ist Usama Ehsan.": "My name is Usama Ehsan.",
        "Ich heiße Usama Ehsan.": "My name is Usama Ehsan.",
        "Ich komme aus Pakistan.": "I am from Pakistan.",
        "Ich wohne in Berlin.": "I live in Berlin.",
        "Ich bin Student.": "I am a student.",
        "Was ist dein Lieblingstag?": "What is your favourite day?",
        "Freitag ist mein Lieblingstag.": "Friday is my favourite day.",
        "Wie ist deine Telefonnummer?": "What is your telephone number?",
        "Meine Telefonnummer ist 0154 71232123.": "My telephone number is 0154 71232123.",
        "Kannst du mir deine Nummer per Whatsapp schicken?": "Can you send me your number via WhatsApp?",
    },

    "Verständnisprobleme": {
        "Das verstehe ich nicht.": "I do not understand that.",
        "Was bedeutet das?": "What does that mean?",
        "Ich weiß nicht.": "I don't know.",
        "Keine Ahnung.": "No idea.",
        "Langsam bitte.": "Slowly please.",
        "Können Sie bitte langsamer sprechen?": "Can you please speak more slowly?",
        "Ich spreche kein Deutsch.": "I don't speak German.",
        "Ich spreche nicht so gut Deutsch.": "I don't speak German very well.",
        "Sprechen Sie Englisch?": "Do you speak English?",
        "Können Sie das bitte wiederholen?": "Can you please repeat that?",
        "Können Sie das bitte aufschreiben?": "Can you please write that down?",
        "Wie bitte?": "Pardon?",
        "Jetzt verstehe ich.": "Now I understand.",
    },

    "Wochentage & Uhrzeit": {
        "Welcher Tag ist heute?": "Which day is it today?",
        "Heute ist Samstag.": "Today is Saturday.",
        "Und welcher Tag war gestern?": "And which day was yesterday?",
        "Gestern war Freitag.": "Yesterday was Friday.",
        "Ist morgen Sonntag?": "Is tomorrow Sunday?",
        "Ja, morgen ist Sonntag.": "Yes, tomorrow is Sunday.",
        "Am Vormittag arbeite ich.": "I work before noon.",
        "Am Mittag mache ich Mittagspause.": "At noon I take the lunch break.",
        "Am Nachmittag lerne ich Deutsch.": "In the afternoon I learn German.",
        "Am Abend sehe ich einen Film.": "In the evening I watch a film.",
        "In der Nacht schlafe ich.": "At night I sleep.",
    },

    "Transport & Termine": {
        "Ich fahre mit dem Bus.": "I travel by bus.",
        "Ich fahre mit dem Zug.": "I travel by train.",
        "Ich fahre mit dem Fahrrad.": "I travel by bicycle.",
        "Ich gehe zu Fuß.": "I go on foot.",
        "Hallo Julia, wann treffen wir uns?": "Hello Julia, when do we meet?",
        "Wir können uns am Montag um 18 Uhr treffen.": "We can meet on Monday at 6 pm.",
        "Leider, das geht bei mir nicht.": "Unfortunately, that is not possible for me.",
        "Okay. Wie wäre es am Mittwoch um 19 Uhr?": "Okay. How about Wednesday at 7 pm?",
        "Ja, das passt gut für mich.": "Yes, that suits me well.",
        "Entschuldigung, ich komme zu spät.": "I'm sorry, I am late.",
        "Mein Zug hatte Verspätung.": "My train was delayed.",
        "Ich war im Stau.": "I was stuck in traffic.",
        "Alles Klar. Dann bis Mittwoch!": "Understood. See you on Wednesday!",
    },

    "Wohnen": {
        "Hast du eine neue Wohnung?": "Do you have a new apartment?",
        "Ja, ich bin eingezogen.": "Yes, I have moved in.",
        "In welchem Stock ist deine Wohnung?": "On which floor is your apartment?",
        "Meine Wohnung ist im fünften Stock.": "My apartment is on the fifth floor.",
        "Gibt es einen Aufzug im Gebäude?": "Is there a lift in the building?",
        "Ja, es gibt einen Aufzug.": "Yes, there is a lift.",
        "Wie viele Zimmer hat die Wohnung?": "How many rooms does the apartment have?",
        "Die Wohnung hat drei Zimmer.": "The apartment has three rooms.",
        "Gibt es eine Küche?": "Is there a kitchen?",
        "Ja, die Küche ist groß.": "Yes, the kitchen is big.",
        "Hast du einen Balkon?": "Do you have a balcony?",
        "Ja, ich habe einen kleinen Balkon.": "Yes, I have a small balcony.",
        "Sind die Nachbarn nett?": "Are the neighbours nice?",
        "Ja, die Nachbarn sind freundlich.": "Yes, the neighbours are friendly.",
    },

    "Freizeit & Wochenende": {
        "Was hast du am Wochenende gemacht?": "What did you do at the weekend?",
        "Am Wochenende habe ich meine Freunde besucht.": "At the weekend I visited my friends.",
        "An welchen Tagen arbeitest du?": "On which days do you work?",
        "Ich arbeite von Montag bis Freitag.": "I work from Monday to Friday.",
        "Wann hast du frei?": "When do you have time off?",
        "Ich habe am Samstag und Sonntag frei.": "I have Saturday and Sunday off.",
        "Was machst du am Samstag?": "What do you do on Saturday?",
        "Samstags gehe ich ins Kino.": "On Saturdays I go to the cinema.",
        "Und was machst du am Sonntag?": "And what do you do on Sunday?",
        "Sonntags schlafe ich lange.": "On Sundays I sleep in.",
        "Ich freue mich auf das Wochenende.": "I am looking forward to the weekend.",
    },

    "Wegbeschreibung": {
        "Entschuldigung, können Sie mir helfen?": "Excuse me, can you help me?",
        "Ja, gerne. Wohin möchten Sie?": "Yes, of course. Where would you like to go?",
        "Ich suche die Apotheke.": "I am looking for the pharmacy.",
        "Gehen Sie den Fluss entlang.": "Go along the river.",
        "Dann über die Brücke.": "Then over the bridge.",
        "Am Kreisverkehr nehmen Sie die zweite Ausfahrt.": "At the roundabout take the second exit.",
        "Die Apotheke finden Sie dann an der linken Seite.": "You will find the pharmacy on the left side.",
        "Folgen Sie der Hauptstraße.": "Follow the main road.",
        "Dann sind Sie in zehn Minuten da.": "Then you will be there in ten minutes.",
        "Der ist nicht so weit entfernt.": "It is not so far away.",
        "Vielen Dank für Ihre Hilfe.": "Thank you very much for your help.",
        "Sehr gerne!": "You are very welcome!",
    },

    "Kleidung & Alltag": {
        "Ich ziehe gern bequeme Kleidung an.": "I like to wear comfortable clothes.",
        "Was ziehen Sie gern an?": "What do you like to wear?",
        "Zum Beispiel eine Jeans und eine Bluse.": "For example jeans and a blouse.",
        "Magst du Mäntel?": "Do you like coats?",
        "Ich trage gern einen Mantel.": "I like to wear a coat.",
        "Berlin liegt nordöstlich von Potsdam.": "Berlin is in the northeast of Potsdam.",
        "Wo liegt Berlin?": "Where is Berlin?",
        "Ich komme zu Fuß.": "I am coming on foot.",
        "Wie kommst du? Mit dem Zug?": "How are you coming? By train?",
        "Nein, ich fahre mit dem Bus.": "No, I am going by bus.",
    },
}

ALL_PDF_VOCAB: dict = {}
for _pv in PDF_VOCAB_BY_CHAPTER.values():
    ALL_PDF_VOCAB.update(_pv)

PDF_CHAPTER_NAMES = ["Alle Themen"] + list(PDF_VOCAB_BY_CHAPTER.keys())


# ── Wortschatzliste: Einfach gut A1 (alphabetisch) — with English meanings ───
# Organised by lesson theme (L1–L12).  Single words and short phrases only.
WORTSCHATZ_BY_CHAPTER: dict[str, dict[str, str]] = {

    "Wortschatz: Grundlagen (L1)": {
        "hallo": "hello",
        "gut": "good",
        "danke": "thank you",
        "bitte": "please",
        "ja": "yes",
        "nein": "no",
        "tschüss": "bye",
        "Entschuldigung": "excuse me",
        "Guten Morgen": "good morning",
        "Guten Abend": "good evening",
        "Gute Nacht": "good night",
        "richtig": "correct / right",
        "falsch": "wrong / incorrect",
        "heißen": "to be called",
        "kommen": "to come",
        "sprechen": "to speak",
        "hören": "to listen / hear",
        "schreiben": "to write",
        "verstehen": "to understand",
        "Name": "name",
        "Sprache": "language",
        "Kurs": "course",
        "Land": "country",
        "Tag": "day",
        "Nacht": "night",
        "Wort": "word",
        "Satz": "sentence",
        "Frage": "question",
        "neu": "new",
        "alles": "everything",
        "sehr": "very",
        "ganz": "quite / whole",
    },

    "Wortschatz: Familie & Person (L2)": {
        "Familie": "family",
        "Vater": "father",
        "Mutter": "mother",
        "Bruder": "brother",
        "Schwester": "sister",
        "Sohn": "son",
        "Tochter": "daughter",
        "Kind": "child",
        "Eltern": "parents",
        "Geschwister": "siblings",
        "Familienname": "surname / family name",
        "Vorname": "first name",
        "Adresse": "address",
        "Straße": "street",
        "Postleitzahl": "postcode",
        "Handynummer": "mobile number",
        "E-Mail": "email",
        "ledig": "single (unmarried)",
        "verheiratet": "married",
        "verwitwet": "widowed",
        "geschieden": "divorced",
        "Heimatland": "home country",
        "wohnen": "to live",
        "Wohnort": "place of residence",
        "vorstellen": "to introduce",
        "anmelden": "to register",
        "Jahr": "year",
        "alt": "old",
        "Kindergarten": "kindergarten",
        "Schwägerin": "sister-in-law",
        "Schwiegervater": "father-in-law",
        "Schwiegertochter": "daughter-in-law",
    },

    "Wortschatz: Kursraum & Lernen (L3)": {
        "Buch": "book",
        "Heft": "notebook",
        "Bleistift": "pencil",
        "Kugelschreiber": "ballpoint pen",
        "Radiergummi": "eraser",
        "Tasche": "bag",
        "Rucksack": "rucksack",
        "Tisch": "table",
        "Stuhl": "chair",
        "Tafel": "board / blackboard",
        "Lampe": "lamp",
        "Tür": "door",
        "Fenster": "window",
        "Wand": "wall",
        "Landkarte": "map",
        "Schlüssel": "key",
        "Lehrer/in": "teacher",
        "Pause": "break",
        "Hausaufgabe": "homework",
        "langsam": "slow / slowly",
        "schnell": "fast / quickly",
        "klein": "small",
        "groß": "big / large",
        "nett": "nice / friendly",
        "lernen": "to learn",
        "lesen": "to read",
        "erklären": "to explain",
        "heute": "today",
        "gestern": "yesterday",
        "morgen": "tomorrow",
        "vorgestern": "the day before yesterday",
        "übermorgen": "the day after tomorrow",
    },

    "Wortschatz: Essen & Lebensmittel (L4)": {
        "Apfel": "apple",
        "Banane": "banana",
        "Orange": "orange",
        "Birne": "pear",
        "Erdbeere": "strawberry",
        "Himbeere": "raspberry",
        "Kirsche": "cherry",
        "Zitrone": "lemon",
        "Traube": "grape",
        "Mango": "mango",
        "Melone": "melon",
        "Kartoffel": "potato",
        "Tomate": "tomato",
        "Möhre": "carrot",
        "Paprika": "pepper",
        "Pilz": "mushroom",
        "Bohne": "bean",
        "Zwiebel": "onion",
        "Brot": "bread",
        "Brötchen": "bread roll",
        "Käse": "cheese",
        "Butter": "butter",
        "Milch": "milk",
        "Ei": "egg",
        "Fisch": "fish",
        "Fleisch": "meat",
        "Rindfleisch": "beef",
        "Schweinefleisch": "pork",
        "Lammfleisch": "lamb",
        "Nudeln": "pasta / noodles",
        "Reis": "rice",
        "Kuchen": "cake",
        "Keks": "biscuit / cookie",
        "Schokolade": "chocolate",
        "Honig": "honey",
        "Marmelade": "jam",
        "Zucker": "sugar",
        "Salz": "salt",
        "Öl": "oil",
        "Kaffee": "coffee",
        "Tee": "tea",
        "Saft": "juice",
        "Bier": "beer",
        "Wein": "wine",
        "Wasser": "water",
        "Joghurt": "yoghurt",
        "Flasche": "bottle",
        "Dose": "tin / can",
        "Packung": "packet",
        "Tasse": "cup",
        "Glas": "glass",
        "lecker": "delicious / tasty",
        "teuer": "expensive",
        "billig": "cheap",
        "einkaufen": "to go shopping",
        "kaufen": "to buy",
        "kosten": "to cost",
        "brauchen": "to need",
        "essen": "to eat",
        "trinken": "to drink",
        "schmecken": "to taste",
    },

    "Wortschatz: Alltag & Tagesablauf (L5)": {
        "aufstehen": "to get up",
        "schlafen": "to sleep",
        "frühstücken": "to have breakfast",
        "kochen": "to cook",
        "fernsehen": "to watch TV",
        "Sport machen": "to do sport",
        "spazieren gehen": "to go for a walk",
        "telefonieren": "to phone",
        "putzen": "to clean",
        "Frühstück": "breakfast",
        "Mittag": "noon / midday",
        "Mittagspause": "lunch break",
        "Nachmittag": "afternoon",
        "Abend": "evening",
        "Morgen": "morning",
        "morgens": "in the morning",
        "mittags": "at noon",
        "nachmittags": "in the afternoon",
        "abends": "in the evening",
        "nachts": "at night",
        "Uhr": "clock / o'clock",
        "Stunde": "hour",
        "früh": "early",
        "spät": "late",
        "müde": "tired",
        "Hunger": "hunger",
        "Musik": "music",
        "Film": "film / movie",
        "oft": "often",
        "manchmal": "sometimes",
        "immer": "always",
        "nie": "never",
        "Supermarkt": "supermarket",
        "Schule": "school",
        "Unterricht": "lessons / class",
    },

    "Wortschatz: Wohnung & Haus (L6)": {
        "Wohnung": "apartment / flat",
        "Haus": "house",
        "Zimmer": "room",
        "Wohnzimmer": "living room",
        "Schlafzimmer": "bedroom",
        "Badezimmer": "bathroom",
        "Küche": "kitchen",
        "Arbeitszimmer": "study / office",
        "Kinderzimmer": "children's room",
        "Flur": "hallway",
        "Keller": "basement",
        "Balkon": "balcony",
        "Terrasse": "terrace",
        "Garage": "garage",
        "Garten": "garden",
        "Dusche": "shower",
        "Badewanne": "bathtub",
        "Toilette": "toilet",
        "Herd": "cooker / stove",
        "Kühlschrank": "fridge",
        "Waschmaschine": "washing machine",
        "Spülmaschine": "dishwasher",
        "Möbel": "furniture",
        "Sofa": "sofa",
        "Bett": "bed",
        "Schrank": "wardrobe / cupboard",
        "Regal": "shelf",
        "Teppich": "carpet / rug",
        "Miete": "rent",
        "Nebenkosten": "additional costs",
        "Kaution": "deposit",
        "Quadratmeter": "square metre",
        "hell": "bright / light",
        "dunkel": "dark",
        "laut": "loud / noisy",
        "ruhig": "quiet",
        "gemütlich": "cosy",
        "modern": "modern",
        "Heizung": "heating",
        "suchen": "to look for / search",
        "Einfamilienhaus": "detached house",
        "Mehrfamilienhaus": "apartment building",
        "Hochhaus": "tower block",
        "Reihenhaus": "terraced house",
    },

    "Wortschatz: Transport & Wegbeschreibung (L7)": {
        "Bus": "bus",
        "Zug": "train",
        "U-Bahn": "underground / subway",
        "S-Bahn": "city/suburban train",
        "Straßenbahn": "tram",
        "Taxi": "taxi",
        "Auto": "car",
        "Fahrrad": "bicycle",
        "Motorrad": "motorbike",
        "Flughafen": "airport",
        "Bahnhof": "train station",
        "Haltestelle": "stop",
        "Bushaltestelle": "bus stop",
        "Fahrkarte": "ticket",
        "Gleis": "platform",
        "links": "left",
        "rechts": "right",
        "geradeaus": "straight ahead",
        "gegenüber": "opposite",
        "Kreuzung": "crossroads / intersection",
        "Ampel": "traffic light",
        "Apotheke": "pharmacy",
        "Krankenhaus": "hospital",
        "Post": "post office",
        "Rathaus": "town hall",
        "Kino": "cinema",
        "Restaurant": "restaurant",
        "Park": "park",
        "Bibliothek": "library",
        "Kirche": "church",
        "Schwimmbad": "swimming pool",
        "Stadtplan": "city map",
        "Meter": "metre",
        "umsteigen": "to change (transport)",
        "fahren": "to drive / travel",
        "Tageskarte": "day ticket",
        "Einzelfahrkarte": "single ticket",
        "Auskunft": "information",
    },

    "Wortschatz: Berufe & Arbeit (L8)": {
        "Beruf": "profession / job",
        "arbeiten": "to work",
        "Arbeit": "work",
        "Büro": "office",
        "Firma": "company",
        "Chef/in": "boss",
        "Kollege/Kollegin": "colleague",
        "Kantine": "canteen",
        "Feierabend": "end of working day",
        "Stress": "stress",
        "stressig": "stressful",
        "langweilig": "boring",
        "kreativ": "creative",
        "flexibel": "flexible",
        "pünktlich": "punctual / on time",
        "freundlich": "friendly",
        "Ausbildung": "apprenticeship / training",
        "studieren": "to study",
        "Universität": "university",
        "Lehrer/in": "teacher",
        "Koch/Köchin": "cook / chef",
        "Bäcker/in": "baker",
        "Kellner/in": "waiter / waitress",
        "Kassierer/in": "cashier",
        "Verkäufer/in": "sales person",
        "Krankenpfleger/Krankenschwester": "nurse",
        "Automechaniker/in": "car mechanic",
        "Taxifahrer/in": "taxi driver",
        "Hausmann/Hausfrau": "house husband / housewife",
        "Traumberuf": "dream job",
        "Führerschein": "driving licence",
        "Werkstatt": "workshop / garage",
        "reparieren": "to repair",
        "halbtags": "part time",
        "Lohn": "wage",
        "Praktikum": "internship / work placement",
    },

    "Wortschatz: Gesundheit & Körper (L9)": {
        "Kopf": "head",
        "Haar": "hair",
        "Gesicht": "face",
        "Auge": "eye",
        "Nase": "nose",
        "Mund": "mouth",
        "Ohr": "ear",
        "Hals": "throat / neck",
        "Brust": "chest",
        "Arm": "arm",
        "Hand": "hand",
        "Finger": "finger",
        "Bein": "leg",
        "Knie": "knee",
        "Fuß": "foot",
        "Zeh": "toe",
        "Bauch": "stomach / belly",
        "Rücken": "back",
        "Schulter": "shoulder",
        "Stirn": "forehead",
        "krank": "ill / sick",
        "Kopfschmerzen": "headache",
        "Bauchschmerzen": "stomach ache",
        "Halsweh": "sore throat",
        "Erkältung": "cold (illness)",
        "Grippe": "flu",
        "Fieber": "fever",
        "Husten": "cough",
        "Schnupfen": "runny nose",
        "Schmerz": "pain",
        "wehtun": "to hurt",
        "Arzt/Ärztin": "doctor",
        "Tablette": "tablet / pill",
        "Medikament": "medication",
        "Rezept": "prescription",
        "Termin": "appointment",
        "Untersuchung": "examination",
        "Sprechstunde": "surgery hours / consultation",
        "Wartezimmer": "waiting room",
        "Pflaster": "plaster / bandage",
        "Salbe": "ointment / cream",
    },

    "Wortschatz: Reise & Freizeit (L10)": {
        "Urlaub": "holiday",
        "Reise": "journey / trip",
        "Koffer": "suitcase",
        "Meer": "sea",
        "Strand": "beach",
        "Insel": "island",
        "Natur": "nature",
        "Wald": "forest",
        "Fluss": "river",
        "Berg": "mountain",
        "Tennis": "tennis",
        "Ski": "ski",
        "schwimmen": "to swim",
        "wandern": "to hike",
        "fotografieren": "to take photos",
        "Postkarte": "postcard",
        "Tourist": "tourist",
        "Wetter": "weather",
        "packen": "to pack",
        "Hobby": "hobby",
        "Nachbar/in": "neighbour",
        "früher": "previously / in the past",
        "Ferienhaus": "holiday house",
        "Schiff": "ship",
        "stressig": "stressful",
        "Suppe": "soup",
        "süß": "sweet / cute",
    },

    "Wortschatz: Kleidung & Mode (L11)": {
        "Jacke": "jacket",
        "Hose": "trousers",
        "Kleid": "dress",
        "Rock": "skirt",
        "Bluse": "blouse",
        "Hemd": "shirt",
        "Pullover": "jumper / pullover",
        "Mantel": "coat",
        "Strickjacke": "cardigan",
        "Jeans": "jeans",
        "Schuh": "shoe",
        "Socke": "sock",
        "Mütze": "hat / cap",
        "Schal": "scarf",
        "Handschuh": "glove",
        "Anorak": "anorak",
        "blau": "blue",
        "rot": "red",
        "grün": "green",
        "gelb": "yellow",
        "schwarz": "black",
        "weiß": "white",
        "grau": "grey",
        "braun": "brown",
        "orange": "orange",
        "lila": "purple",
        "beige": "beige",
        "bequem": "comfortable",
        "eng": "tight / narrow",
        "Größe": "size",
        "passen": "to fit",
        "tragen": "to wear / carry",
        "anziehen": "to put on / get dressed",
        "Kaufhaus": "department store",
        "Sonderangebot": "special offer",
        "umtauschen": "to exchange / return",
        "Kassenbon": "receipt",
    },

    "Wortschatz: Jahreszeiten & Feste (L12)": {
        "Frühling": "spring",
        "Sommer": "summer",
        "Herbst": "autumn",
        "Winter": "winter",
        "Schnee": "snow",
        "Regen": "rain",
        "Wind": "wind",
        "Sonne": "sun",
        "sonnig": "sunny",
        "bewölkt": "cloudy",
        "nebelig": "foggy",
        "windig": "windy",
        "warm": "warm",
        "kalt": "cold",
        "regnen": "to rain",
        "schneien": "to snow",
        "Grad": "degree (temperature)",
        "Geburtstag": "birthday",
        "Hochzeit": "wedding",
        "Weihnachten": "Christmas",
        "Ostern": "Easter",
        "Einladung": "invitation",
        "Geschenk": "gift / present",
        "Torte": "cake / gateau",
        "feiern": "to celebrate",
        "tanzen": "to dance",
        "schenken": "to give as a gift",
        "Jahreszeit": "season",
        "Januar": "January",
        "Februar": "February",
        "März": "March",
        "April": "April",
        "Mai": "May",
        "Juni": "June",
        "Juli": "July",
        "August": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Dezember": "December",
        "Norden": "north",
        "Süden": "south",
        "Osten": "east",
        "Westen": "west",
        "Weihnachtsbaum": "Christmas tree",
        "Weihnachtsmann": "Father Christmas / Santa Claus",
        "Osterhase": "Easter bunny",
        "Luftballon": "balloon",
        "glücklich": "happy",
        "lustig": "funny / fun",
    },
}

ALL_WORTSCHATZ: dict = {}
for _wv in WORTSCHATZ_BY_CHAPTER.values():
    ALL_WORTSCHATZ.update(_wv)

WORTSCHATZ_CHAPTER_NAMES = ["Alle Themen"] + list(WORTSCHATZ_BY_CHAPTER.keys())


GRAMMAR_TABLES = {
    "Pronouns (Pronomen)": [
        ("I",               "ich"),
        ("you (casual)",    "du"),
        ("he",              "er"),
        ("she",             "sie"),
        ("it",              "es"),
        ("we",              "wir"),
        ("you (plural)",    "ihr"),
        ("they",            "sie"),
        ("you (formal)",    "Sie"),
    ],
    "sein – to be (present)": [
        ("I am",            "ich bin"),
        ("you are (casual)","du bist"),
        ("he / she / it is","er / sie / es ist"),
        ("we are",          "wir sind"),
        ("you are (plural)","ihr seid"),
        ("they are",        "sie sind"),
        ("you are (formal)","Sie sind"),
    ],
    "haben – to have (present)": [
        ("I have",          "ich habe"),
        ("you have (casual)","du hast"),
        ("he / she / it has","er / sie / es hat"),
        ("we have",         "wir haben"),
        ("you have (plural)","ihr habt"),
        ("they have",       "sie haben"),
        ("you have (formal)","Sie haben"),
    ],
    "kommen – to come (present)": [
        ("I come",          "ich komme"),
        ("you come (casual)","du kommst"),
        ("he / she / it comes","er / sie / es kommt"),
        ("we come",         "wir kommen"),
        ("you come (plural)","ihr kommt"),
        ("they come",       "sie kommen"),
        ("you come (formal)","Sie kommen"),
    ],
    "möchten – would like (present)": [
        ("I would like",            "ich möchte"),
        ("you would like (casual)", "du möchtest"),
        ("he / she / it would like","er / sie / es möchte"),
        ("we would like",           "wir möchten"),
        ("you would like (plural)", "ihr möchtet"),
        ("they would like",         "sie möchten"),
        ("you would like (formal)", "Sie möchten"),
    ],
    "können – can (present)": [
        ("I can",           "ich kann"),
        ("you can (casual)","du kannst"),
        ("he / she / it can","er / sie / es kann"),
        ("we can",          "wir können"),
        ("you can (plural)","ihr könnt"),
        ("they can",        "sie können"),
        ("you can (formal)","Sie können"),
    ],
    "müssen – must / have to (present)": [
        ("I must",          "ich muss"),
        ("you must (casual)","du musst"),
        ("he / she / it must","er / sie / es muss"),
        ("we must",         "wir müssen"),
        ("you must (plural)","ihr müsst"),
        ("they must",       "sie müssen"),
        ("you must (formal)","Sie müssen"),
    ],
    "Articles (Artikel)": [
        ("the (masculine)",  "der"),
        ("the (feminine)",   "die"),
        ("the (neuter)",     "das"),
        ("the (plural)",     "die"),
        ("a / an (masculine)","ein"),
        ("a / an (feminine)", "eine"),
        ("a / an (neuter)",   "ein"),
        ("no / not a (masculine)","kein"),
        ("no / not a (feminine)", "keine"),
        ("no / not a (neuter)",   "kein"),
    ],
    "Question words (Fragewörter)": [
        ("What?",           "Was?"),
        ("Who?",            "Wer?"),
        ("Where?",          "Wo?"),
        ("Where to?",       "Wohin?"),
        ("Where from?",     "Woher?"),
        ("When?",           "Wann?"),
        ("How?",            "Wie?"),
        ("How much?",       "Wie viel?"),
        ("How many?",       "Wie viele?"),
        ("Which?",          "Welche/r/s?"),
        ("Why?",            "Warum?"),
    ],
    "Days of the week (Wochentage)": [
        ("Monday",    "Montag"),
        ("Tuesday",   "Dienstag"),
        ("Wednesday", "Mittwoch"),
        ("Thursday",  "Donnerstag"),
        ("Friday",    "Freitag"),
        ("Saturday",  "Samstag"),
        ("Sunday",    "Sonntag"),
        ("on Monday", "am Montag"),
        ("every Monday", "montags"),
    ],
    "Months (Monate)": [
        ("January",   "Januar"),
        ("February",  "Februar"),
        ("March",     "März"),
        ("April",     "April"),
        ("May",       "Mai"),
        ("June",      "Juni"),
        ("July",      "Juli"),
        ("August",    "August"),
        ("September", "September"),
        ("October",   "Oktober"),
        ("November",  "November"),
        ("December",  "Dezember"),
        ("in January","im Januar"),
    ],
    "Numbers 1–20 (Zahlen)": [
        ("one",     "eins"),
        ("two",     "zwei"),
        ("three",   "drei"),
        ("four",    "vier"),
        ("five",    "fünf"),
        ("six",     "sechs"),
        ("seven",   "sieben"),
        ("eight",   "acht"),
        ("nine",    "neun"),
        ("ten",     "zehn"),
        ("eleven",  "elf"),
        ("twelve",  "zwölf"),
        ("thirteen","dreizehn"),
        ("fourteen","vierzehn"),
        ("fifteen", "fünfzehn"),
        ("sixteen", "sechzehn"),
        ("seventeen","siebzehn"),
        ("eighteen","achtzehn"),
        ("nineteen","neunzehn"),
        ("twenty",  "zwanzig"),
    ],
}


def normalise(text: str) -> str:
    """Lowercase, strip punctuation and extra whitespace for loose comparison."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[.!?,;:]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


@st.cache_data(show_spinner=False)
def tts_bytes(text: str) -> bytes | None:
    """Generate German TTS audio and return raw MP3 bytes (cached per sentence)."""
    if not _HAS_TTS:
        return None
    try:
        buf = io.BytesIO()
        gTTS(text=text, lang="de", slow=False).write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None


def play_button(german_text: str, key: str) -> None:
    """Render a 🔊 audio player for the given German text."""
    audio = tts_bytes(german_text)
    if audio:
        st.audio(audio, format="audio/mp3")


def init_session():
    defaults = {
        # shared
        "streak": 0,
        # multiple-choice tab
        "mc_score": 0, "mc_total": 0,
        "mc_answered": False, "mc_selected": None,
        "mc_question": None, "mc_correct": None, "mc_options": [],
        "mc_deck": [], "mc_round": 1,
        "mc_active_chapter": None, "mc_round_complete": False,
        "mc_revealed": False,
        # tile tab
        "tl_score": 0, "tl_total": 0,
        "tl_answered": False, "tl_revealed": False,
        "tl_question": None, "tl_correct": None,
        "tl_deck": [], "tl_round": 1,
        "tl_active_chapter": None, "tl_round_complete": False,
        "tiles_bank": [], "tiles_chosen": [],
        # grammar typing tab
        "gt_table": list(GRAMMAR_TABLES.keys())[0],
        "gt_deck": [], "gt_index": 0,
        "gt_score": 0, "gt_total": 0,
        "gt_answered": False, "gt_correct_answer": "",
        "gt_english": "", "gt_user_input": "",
        # pdf typing tab (German shown → type English)
        "tp_score": 0, "tp_total": 0,
        "tp_answered": False, "tp_revealed": False,
        "tp_german": None, "tp_english": None,
        "tp_user_input": "",
        "tp_deck": [], "tp_round": 1,
        "tp_active_chapter": None, "tp_round_complete": False,
        # listening tab (audio only → type English)
        "ls_score": 0, "ls_total": 0,
        "ls_answered": False, "ls_revealed": False,
        "ls_german": None, "ls_english": None,
        "ls_user_input": "",
        "ls_deck": [], "ls_round": 1,
        "ls_active_chapter": None, "ls_round_complete": False,
        # wortschatz 3-option quiz
        "wq_score": 0, "wq_total": 0,
        "wq_answered": False, "wq_selected": None, "wq_revealed": False,
        "wq_question": None, "wq_correct": None, "wq_options": [],
        "wq_deck": [], "wq_round": 1,
        "wq_active_chapter": None, "wq_round_complete": False,
        "wq_mastered": set(),   # words answered correctly on first try
        # navigation
        "active_tab": "📋 Vokabelquiz",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_mc(pool, chapter):
    if chapter != st.session_state.mc_active_chapter:
        st.session_state.mc_deck = build_deck(pool)
        st.session_state.mc_round = 1
        st.session_state.mc_active_chapter = chapter
        st.session_state.mc_round_complete = False
        st.session_state.mc_question = None  # force a fresh question
    if st.session_state.mc_question is not None:
        return  # already showing a question — nothing to do
    if not st.session_state.mc_deck:
        st.session_state.mc_deck = build_deck(pool)
        st.session_state.mc_round += 1
        st.session_state.mc_round_complete = True
    else:
        st.session_state.mc_round_complete = False
    word = st.session_state.mc_deck.pop()
    q, c, opts = make_mc_question(pool, word)
    st.session_state.mc_question = q
    st.session_state.mc_correct = c
    st.session_state.mc_options = opts
    st.session_state.mc_answered = False
    st.session_state.mc_selected = None
    st.session_state.mc_revealed = False


def get_tile_pool(chapter: str) -> dict:
    """Return the dedicated tile vocab for the selected chapter."""
    if chapter == "Alle Themen":
        return ALL_TILE_VOCAB
    return TILE_VOCAB_BY_CHAPTER.get(chapter, ALL_TILE_VOCAB)


def load_tile(tile_pool, chapter):
    if chapter != st.session_state.tl_active_chapter:
        st.session_state.tl_deck = build_deck(tile_pool)
        st.session_state.tl_round = 1
        st.session_state.tl_active_chapter = chapter
        st.session_state.tl_round_complete = False
        st.session_state.tl_question = None  # force a fresh question
    if st.session_state.tl_question is not None:
        return  # already showing a question — nothing to do
    if not st.session_state.tl_deck:
        st.session_state.tl_deck = build_deck(tile_pool)
        st.session_state.tl_round += 1
        st.session_state.tl_round_complete = True
    else:
        st.session_state.tl_round_complete = False
    word = st.session_state.tl_deck.pop()
    q, c = make_tile_question(tile_pool, word)
    st.session_state.tl_question = q
    st.session_state.tl_correct = c
    st.session_state.tl_answered = False
    st.session_state.tl_revealed = False
    st.session_state.tiles_bank = make_tiles(c)
    st.session_state.tiles_chosen = []


def get_pdf_pool(chapter: str) -> dict:
    """Return PDF vocab for the selected chapter, or all if 'Alle Themen'."""
    if chapter == "Alle Themen":
        return ALL_PDF_VOCAB
    return PDF_VOCAB_BY_CHAPTER.get(chapter, ALL_PDF_VOCAB)


def get_wortschatz_pool(chapter: str) -> dict:
    """Return Wortschatzliste vocab for the selected chapter."""
    if chapter == "Alle Themen":
        return ALL_WORTSCHATZ
    return WORTSCHATZ_BY_CHAPTER.get(chapter, ALL_WORTSCHATZ)


def load_wq(pool, chapter):
    """Load a 3-option MC question; skip mastered words (correct on first try)."""
    if chapter != st.session_state.wq_active_chapter:
        st.session_state.wq_mastered = set()
        st.session_state.wq_deck = []
        st.session_state.wq_round = 1
        st.session_state.wq_active_chapter = chapter
        st.session_state.wq_round_complete = False
        st.session_state.wq_question = None

    if st.session_state.wq_question is not None:
        return

    # Only words not yet mastered
    unmastered = {k: v for k, v in pool.items() if k not in st.session_state.wq_mastered}
    if not unmastered:
        return  # all done — handled in render

    # Refill deck from unmastered words if empty
    if not st.session_state.wq_deck:
        st.session_state.wq_deck = build_deck(unmastered)
        st.session_state.wq_round += 1
        st.session_state.wq_round_complete = True
    else:
        st.session_state.wq_round_complete = False

    # Skip any mastered words that may have lingered in deck
    while st.session_state.wq_deck and st.session_state.wq_deck[-1] in st.session_state.wq_mastered:
        st.session_state.wq_deck.pop()
    if not st.session_state.wq_deck:
        return

    word = st.session_state.wq_deck.pop()
    correct = pool[word]
    others = [v for k, v in pool.items() if k != word and v != correct]
    distractors = random.sample(others, min(2, len(others)))
    opts = distractors + [correct]
    random.shuffle(opts)
    st.session_state.wq_question = word
    st.session_state.wq_correct = correct
    st.session_state.wq_options = opts
    st.session_state.wq_answered = False
    st.session_state.wq_selected = None
    st.session_state.wq_revealed = False


def load_tp(pdf_pool, chapter):
    if chapter != st.session_state.tp_active_chapter:
        st.session_state.tp_deck = build_deck(pdf_pool)
        st.session_state.tp_round = 1
        st.session_state.tp_active_chapter = chapter
        st.session_state.tp_round_complete = False
        st.session_state.tp_german = None
    if st.session_state.tp_german is not None:
        return
    if not st.session_state.tp_deck:
        st.session_state.tp_deck = build_deck(pdf_pool)
        st.session_state.tp_round += 1
        st.session_state.tp_round_complete = True
    else:
        st.session_state.tp_round_complete = False
    word = st.session_state.tp_deck.pop()
    st.session_state.tp_german = word
    st.session_state.tp_english = pdf_pool[word]
    st.session_state.tp_answered = False
    st.session_state.tp_revealed = False
    st.session_state.tp_user_input = ""


def load_ls(pdf_pool, chapter):
    if chapter != st.session_state.ls_active_chapter:
        st.session_state.ls_deck = build_deck(pdf_pool)
        st.session_state.ls_round = 1
        st.session_state.ls_active_chapter = chapter
        st.session_state.ls_round_complete = False
        st.session_state.ls_german = None
    if st.session_state.ls_german is not None:
        return
    if not st.session_state.ls_deck:
        st.session_state.ls_deck = build_deck(pdf_pool)
        st.session_state.ls_round += 1
        st.session_state.ls_round_complete = True
    else:
        st.session_state.ls_round_complete = False
    word = st.session_state.ls_deck.pop()
    st.session_state.ls_german = word
    st.session_state.ls_english = pdf_pool[word]
    st.session_state.ls_answered = False
    st.session_state.ls_revealed = False
    st.session_state.ls_user_input = ""


# ── App ───────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="telc A1 Vokabelquiz", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 telc Deutsch A1 — Vokabelquiz")

init_session()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📚 Thema wählen")
    chapter = st.selectbox("Thema", CHAPTER_NAMES)

    st.divider()
    active_tab = st.radio(
        "Modus",
        ["📋 Vokabelquiz", "🔤 Wörter sortieren", "✏️ Grammatik tippen", "🖊️ Deutsch → Englisch", "🎧 Hören & Schreiben", "📚 Wortschatz Quiz"],
        key="active_tab",
    )

    st.divider()
    st.caption("🔥 Streak")
    st.metric("Serie", st.session_state.streak)

    if st.button("🔄 Alles zurücksetzen", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

active_tab = st.session_state.active_tab
pool = get_pool(chapter)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — Multiple choice (German phrase → pick English meaning)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "📋 Vokabelquiz":
    load_mc(pool, chapter)

    # score bar
    pool_size = len(pool)
    mc_seen = pool_size - len(st.session_state.mc_deck)
    c1, c2 = st.columns(2)
    c1.metric("Punkte", f"{st.session_state.mc_score} / {st.session_state.mc_total}")
    pct = int(st.session_state.mc_score / st.session_state.mc_total * 100) if st.session_state.mc_total else 0
    c2.metric("Genauigkeit", f"{pct}%")
    st.progress(max(0.0, min(1.0, mc_seen / pool_size)) if pool_size else 0,
                text=f"Runde {st.session_state.mc_round} · {mc_seen}/{pool_size} Sätze gesehen")

    st.divider()
    st.markdown("**Was bedeutet dieser Satz auf Englisch?**")
    st.markdown(
        f"<div style='font-size:1.75rem; font-weight:700; padding:18px 22px; "
        f"background:#1e1e2e; border-radius:14px; color:#cdd6f4; "
        f"text-align:center; margin-bottom:18px; line-height:1.5;'>"
        f"{st.session_state.mc_question}</div>",
        unsafe_allow_html=True,
    )
    play_button(st.session_state.mc_question, key="mc_audio")

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.mc_options):
        with cols[i % 2]:
            if st.button(opt, key=f"mc_{i}", disabled=st.session_state.mc_answered,
                         use_container_width=True):
                st.session_state.mc_selected = opt
                st.session_state.mc_answered = True
                st.session_state.mc_total += 1
                if opt == st.session_state.mc_correct:
                    st.session_state.mc_score += 1
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 0
                st.rerun()

    if not st.session_state.mc_answered:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("👁️ Antwort zeigen", use_container_width=True, key="mc_reveal"):
                st.session_state.mc_revealed = True
        with btn_col2:
            if st.button("⏭️ Überspringen", use_container_width=True, key="mc_skip"):
                st.session_state.mc_question = None
                st.session_state.mc_revealed = False
                load_mc(pool, chapter)
                st.rerun()
        if st.session_state.mc_revealed:
            st.info(f"💡 Antwort: **{st.session_state.mc_correct}**")

    if st.session_state.mc_answered:
        if st.session_state.mc_selected == st.session_state.mc_correct:
            st.success(f"✅ Richtig!  **{st.session_state.mc_correct}**")
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.error(
                f"❌ Falsch.  Du hast gewählt: **{st.session_state.mc_selected}**\n\n"
                f"Richtige Antwort: **{st.session_state.mc_correct}**"
            )

        render_breakdown_and_grammar(st.session_state.mc_question)

        st.divider()
        if st.session_state.mc_round_complete:
            st.info(f"🎉 Runde abgeschlossen! Weiter mit Runde {st.session_state.mc_round}…")
        if st.button("➡️ Nächster Satz", type="primary", use_container_width=True, key="mc_next"):
            st.session_state.mc_question = None
            load_mc(pool, chapter)
            st.rerun()

    # ── Vocabulary reference list ─────────────────────────────────────────────
    st.divider()
    with st.expander("📖 Alle Vokabeln dieses Themas anzeigen", expanded=False):

        def render_vocab_table(vocab: dict):
            for de, en in vocab.items():
                breakdown = WORD_BREAKDOWN.get(de, "")
                grammar = GRAMMAR_NOTES.get(de, None)
                breakdown_html = (
                    f"<div style='font-size:0.8rem; color:#9399b2; margin-top:4px;'>🔍 {breakdown}</div>"
                    if breakdown else ""
                )
                grammar_html = (
                    f"<div style='font-size:0.8rem; color:#fab387; margin-top:4px;'>"
                    f"💡 <b>{grammar[0]}</b> — {grammar[2]}</div>"
                    if grammar else ""
                )
                st.markdown(
                    f"<div style='padding:10px 14px; margin-bottom:6px; "
                    f"background:#1e1e2e; border-radius:10px; border-left:4px solid #89b4fa;'>"
                    f"<div style='font-size:1.05rem; font-weight:700; color:#cdd6f4;'>{de}</div>"
                    f"<div style='font-size:0.95rem; color:#a6e3a1; margin-top:2px;'>🇬🇧 {en}</div>"
                    + breakdown_html + grammar_html +
                    "</div>",
                    unsafe_allow_html=True,
                )

        if chapter == "Alle Themen":
            for ch_name, ch_vocab in VOCAB_BY_CHAPTER.items():
                st.markdown(f"### {ch_name}")
                render_vocab_table(ch_vocab)
                st.markdown("")
        else:
            render_vocab_table(pool)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — Word tiles (English shown → sort German words into order)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "🔤 Wörter sortieren":
    tile_pool = get_tile_pool(chapter)
    load_tile(tile_pool, chapter)

    pool_size = len(tile_pool)
    tl_seen = pool_size - len(st.session_state.tl_deck)
    c1, c2 = st.columns(2)
    c1.metric("Punkte", f"{st.session_state.tl_score} / {st.session_state.tl_total}")
    pct2 = int(st.session_state.tl_score / st.session_state.tl_total * 100) if st.session_state.tl_total else 0
    c2.metric("Genauigkeit", f"{pct2}%")
    st.progress(max(0.0, min(1.0, tl_seen / pool_size)) if pool_size else 0,
                text=f"Runde {st.session_state.tl_round} · {tl_seen}/{pool_size} Sätze gesehen")

    st.divider()
    st.markdown("**Klicke die Wörter in der richtigen Reihenfolge:**")
    st.markdown(
        f"<div style='font-size:1.75rem; font-weight:700; padding:18px 22px; "
        f"background:#1e1e2e; border-radius:14px; color:#cdd6f4; "
        f"text-align:center; margin-bottom:18px; line-height:1.5;'>"
        f"{st.session_state.tl_question}</div>",
        unsafe_allow_html=True,
    )

    # Answer tray
    if st.session_state.tiles_chosen:
        tray_html = " ".join(
            f"<span style='display:inline-block; background:#313244; color:#cdd6f4; "
            f"border:2px solid #89b4fa; border-radius:8px; padding:6px 12px; "
            f"margin:4px; font-size:1.05rem; font-weight:600;'>{w}</span>"
            for w in st.session_state.tiles_chosen
        )
    else:
        tray_html = "<span style='color:#585b70; font-style:italic;'>— tippe auf Wörter unten —</span>"

    st.markdown(
        f"<div style='min-height:54px; padding:10px 14px; background:#181825; "
        f"border-radius:10px; border:2px dashed #585b70; margin-bottom:10px;'>"
        f"{tray_html}</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.tiles_chosen and not st.session_state.tl_answered:
        if st.button("⌫ Letztes Wort entfernen", use_container_width=True, key="tl_back"):
            removed = st.session_state.tiles_chosen.pop()
            st.session_state.tiles_bank.append(removed)
            st.rerun()

    # Word bank
    if not st.session_state.tl_answered:
        st.markdown("**Wortbank:**")
        bank = st.session_state.tiles_bank
        cols_per_row = 4
        for row in [bank[i:i+cols_per_row] for i in range(0, len(bank), cols_per_row)]:
            cols = st.columns(len(row))
            for col, word in zip(cols, row):
                with col:
                    if st.button(word, key=f"tile_{word}_{bank.index(word)}", use_container_width=True):
                        st.session_state.tiles_bank.remove(word)
                        st.session_state.tiles_chosen.append(word)
                        st.rerun()

        st.markdown("")
        rev_col, skip2_col = st.columns(2)
        with rev_col:
            if st.button("👁️ Antwort zeigen", use_container_width=True, key="tl_reveal"):
                st.session_state.tl_revealed = True
        with skip2_col:
            if st.button("⏭️ Überspringen", use_container_width=True, key="tl_skip2"):
                st.session_state.tl_question = None
                st.session_state.tl_revealed = False
                load_tile(tile_pool, chapter)
                st.rerun()
        if st.session_state.tl_revealed:
            st.info(f"💡 Antwort: **{st.session_state.tl_correct}**")

        check_col, reset_col, skip_col = st.columns([3, 1, 1])
        with check_col:
            if st.button("✔️ Überprüfen", type="primary", use_container_width=True,
                         disabled=not st.session_state.tiles_chosen, key="tl_check"):
                st.session_state.tl_answered = True
                st.session_state.tl_total += 1
                user_sentence = " ".join(st.session_state.tiles_chosen)
                if normalise(user_sentence) == normalise(st.session_state.tl_correct):
                    st.session_state.tl_score += 1
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 0
                st.rerun()
        with reset_col:
            if st.button("🔄", use_container_width=True, key="tl_reset",
                         help="Zurücksetzen"):
                st.session_state.tiles_bank = make_tiles(st.session_state.tl_correct)
                st.session_state.tiles_chosen = []
                st.rerun()
        with skip_col:
            if st.button("🔁", use_container_width=True, key="tl_skip",
                         help="Neu mischen"):
                st.session_state.tiles_bank = make_tiles(st.session_state.tl_correct)
                st.session_state.tiles_chosen = []
                st.rerun()

    if st.session_state.tl_answered:
        user_sentence = " ".join(st.session_state.tiles_chosen)
        if normalise(user_sentence) == normalise(st.session_state.tl_correct):
            st.success("✅ Richtig!")
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.error("❌ Falsch.")
            st.markdown(
                f"<div style='font-size:1rem; padding:12px 16px; "
                f"background:#2a2a3e; border-radius:10px; color:#a6e3a1; "
                f"margin-top:6px;'>"
                f"<b>Richtige Antwort:</b><br>{st.session_state.tl_correct}</div>",
                unsafe_allow_html=True,
            )

        play_button(st.session_state.tl_correct, key="tl_audio")
        render_breakdown_and_grammar(st.session_state.tl_correct)

        st.divider()
        if st.session_state.tl_round_complete:
            st.info(f"🎉 Runde abgeschlossen! Weiter mit Runde {st.session_state.tl_round}…")
        if st.button("➡️ Nächster Satz", type="primary", use_container_width=True, key="tl_next"):
            st.session_state.tl_question = None
            load_tile(tile_pool, chapter)
            st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — Grammar typing quiz (English → type German)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "✏️ Grammatik tippen":
    TABLE_NAMES = list(GRAMMAR_TABLES.keys())

    selected_table = st.selectbox("Tabelle wählen", TABLE_NAMES, key="gt_table_select")

    # Reset deck when table changes
    if selected_table != st.session_state.gt_table:
        st.session_state.gt_table = selected_table
        st.session_state.gt_deck = []
        st.session_state.gt_score = 0
        st.session_state.gt_total = 0
        st.session_state.gt_answered = False
        st.session_state.gt_english = ""
        st.session_state.gt_correct_answer = ""
        st.session_state.gt_user_input = ""

    rows = GRAMMAR_TABLES[st.session_state.gt_table]

    # Build / refill deck
    if not st.session_state.gt_deck:
        deck = list(rows)
        random.shuffle(deck)
        st.session_state.gt_deck = deck

    # Pick current item (top of deck, don't pop yet)
    current_en, current_de = st.session_state.gt_deck[0]

    # Progress
    seen = len(rows) - len(st.session_state.gt_deck)
    st.progress(max(0.0, min(1.0, seen / len(rows))),
                text=f"{seen}/{len(rows)} in dieser Runde")

    c1, c2 = st.columns(2)
    c1.metric("Richtig", f"{st.session_state.gt_score} / {st.session_state.gt_total}")
    pct_gt = int(st.session_state.gt_score / st.session_state.gt_total * 100) if st.session_state.gt_total else 0
    c2.metric("Genauigkeit", f"{pct_gt}%")

    st.divider()

    # Show the reference table in an expander
    with st.expander(f"📖 Tabelle anzeigen: {st.session_state.gt_table}", expanded=False):
        header_cols = st.columns(2)
        header_cols[0].markdown("**English**")
        header_cols[1].markdown("**Deutsch**")
        st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)
        for en_item, de_item in rows:
            r = st.columns(2)
            r[0].write(en_item)
            r[1].write(de_item)

    st.markdown("### Schreibe das deutsche Wort / den deutschen Satz:")
    st.markdown(
        f"<div style='font-size:1.9rem; font-weight:700; padding:20px 24px; "
        f"background:#1e1e2e; border-radius:14px; color:#cdd6f4; "
        f"text-align:center; margin-bottom:18px;'>"
        f"{current_en}</div>",
        unsafe_allow_html=True,
    )

    if not st.session_state.gt_answered:
        with st.form(key=f"gt_form_{seen}", clear_on_submit=True):
            user_ans = st.text_input("Deine Antwort auf Deutsch:",
                                     placeholder="Tippe hier und drücke Enter…")
            submitted = st.form_submit_button("✅ Prüfen", type="primary", use_container_width=True)
        if submitted:
            if user_ans.strip():
                st.session_state.gt_total += 1
                st.session_state.gt_user_input = user_ans.strip()
                st.session_state.gt_correct_answer = current_de
                alternatives = [normalise(a.strip()) for a in current_de.replace("·", "/").split("/")]
                if normalise(user_ans) in alternatives:
                    st.session_state.gt_score += 1
                    st.session_state.streak += 1
                    st.session_state.gt_answered = True
                else:
                    st.session_state.streak = 0
                    st.session_state.gt_answered = True
    else:
        correct_de = st.session_state.gt_correct_answer
        user_was = st.session_state.gt_user_input
        alternatives = [normalise(a.strip()) for a in correct_de.replace("·", "/").split("/")]
        is_correct = normalise(user_was) in alternatives

        if is_correct:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #a6e3a1; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>✅</span> "
                f"<span style='color:#a6e3a1; font-size:1.1rem; font-weight:700;'>Richtig!</span> "
                f"<span style='color:#cdd6f4;'><b>{correct_de}</b></span>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #f38ba8; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>❌</span> "
                f"<span style='color:#f38ba8; font-size:1.1rem; font-weight:700;'>Falsch.</span> "
                f"Du hast geschrieben: <span style='color:#fab387;'>{user_was}</span><br>"
                f"Richtige Antwort: <span style='color:#a6e3a1; font-weight:700;'>{correct_de}</span>"
                "</div>",
                unsafe_allow_html=True,
            )

        with st.form(key=f"gt_next_form_{seen}"):
            st.text_input("Drücke Enter für die nächste Frage:", placeholder="Enter drücken…",
                          label_visibility="collapsed", key="gt_next_dummy")
            next_pressed = st.form_submit_button("➡️ Nächste", type="primary", use_container_width=True)
        if next_pressed:
            st.session_state.gt_deck.pop(0)
            st.session_state.gt_answered = False
            st.session_state.gt_user_input = ""
            st.session_state.gt_correct_answer = ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — PDF vocab: German shown → type English translation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "🖊️ Deutsch → Englisch":

    tp_source = st.radio(
        "Vokabelquelle",
        ["📄 TELC Sätze", "📚 Wortschatzliste (Einfach gut A1)"],
        horizontal=True,
        key="tp_source",
    )

    if tp_source == "📄 TELC Sätze":
        tp_chapter_names = PDF_CHAPTER_NAMES
        tp_chapter = st.selectbox("Thema wählen", tp_chapter_names, key="tp_chapter_select")
        pdf_pool = get_pdf_pool(tp_chapter)
    else:
        tp_chapter_names = WORTSCHATZ_CHAPTER_NAMES
        tp_chapter = st.selectbox("Thema wählen", tp_chapter_names, key="tp_chapter_select")
        pdf_pool = get_wortschatz_pool(tp_chapter)

    load_tp(pdf_pool, tp_chapter)

    pool_size = len(pdf_pool)
    tp_seen = pool_size - len(st.session_state.tp_deck)
    c1, c2 = st.columns(2)
    c1.metric("Punkte", f"{st.session_state.tp_score} / {st.session_state.tp_total}")
    pct_tp = int(st.session_state.tp_score / st.session_state.tp_total * 100) if st.session_state.tp_total else 0
    c2.metric("Genauigkeit", f"{pct_tp}%")
    st.progress(
        max(0.0, min(1.0, tp_seen / pool_size)) if pool_size else 0,
        text=f"Runde {st.session_state.tp_round} · {tp_seen}/{pool_size} Sätze gesehen",
    )

    st.divider()
    st.markdown("**Wie heißt dieser Satz auf Englisch?**")
    st.markdown(
        f"<div style='font-size:1.75rem; font-weight:700; padding:18px 22px; "
        f"background:#1e1e2e; border-radius:14px; color:#cdd6f4; "
        f"text-align:center; margin-bottom:18px; line-height:1.5;'>"
        f"{st.session_state.tp_german}</div>",
        unsafe_allow_html=True,
    )
    play_button(st.session_state.tp_german, key="tp_audio")

    if not st.session_state.tp_answered:
        with st.form(key=f"tp_form_{tp_seen}", clear_on_submit=True):
            user_tp = st.text_input(
                "Deine Übersetzung auf Englisch:",
                placeholder="Type your English translation and press Enter…",
            )
            fc1, fc2, fc3 = st.columns([4, 1, 1])
            with fc1:
                tp_submitted = st.form_submit_button("✅ Prüfen", type="primary", use_container_width=True)
            with fc2:
                tp_reveal = st.form_submit_button("👁️", use_container_width=True, help="Antwort zeigen")
            with fc3:
                tp_skip = st.form_submit_button("⏭️", use_container_width=True, help="Überspringen")
        if tp_reveal:
            st.session_state.tp_revealed = True
        if st.session_state.tp_revealed:
            st.info(f"💡 Antwort: **{st.session_state.tp_english}**")
        if tp_skip:
            st.session_state.tp_german = None
            st.session_state.tp_revealed = False
            load_tp(pdf_pool, tp_chapter)
        if tp_submitted and user_tp.strip():
            st.session_state.tp_total += 1
            st.session_state.tp_user_input = user_tp.strip()
            correct_en = st.session_state.tp_english
            # Allow loose match: normalised, and also accept any key phrase present
            norm_user = normalise(user_tp)
            norm_correct = normalise(correct_en)
            is_correct = norm_user == norm_correct
            if is_correct:
                st.session_state.tp_score += 1
                st.session_state.streak += 1
            else:
                st.session_state.streak = 0
            st.session_state.tp_answered = True
    else:
        correct_en = st.session_state.tp_english
        user_was = st.session_state.tp_user_input
        is_correct = normalise(user_was) == normalise(correct_en)

        if is_correct:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #a6e3a1; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>✅</span> "
                f"<span style='color:#a6e3a1; font-size:1.1rem; font-weight:700;'>Richtig!</span> "
                f"<span style='color:#cdd6f4;'><b>{correct_en}</b></span>"
                "</div>",
                unsafe_allow_html=True,
            )
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #f38ba8; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>❌</span> "
                f"<span style='color:#f38ba8; font-size:1.1rem; font-weight:700;'>Falsch.</span> "
                f"Du hast geschrieben: <span style='color:#fab387;'>{user_was}</span><br>"
                f"Richtige Antwort: <span style='color:#a6e3a1; font-weight:700;'>{correct_en}</span>"
                "</div>",
                unsafe_allow_html=True,
            )

        render_breakdown_and_grammar(st.session_state.tp_german)

        st.divider()
        if st.session_state.tp_round_complete:
            st.info(f"🎉 Runde abgeschlossen! Weiter mit Runde {st.session_state.tp_round}…")

        with st.form(key=f"tp_next_form_{tp_seen}"):
            st.text_input("Drücke Enter für den nächsten Satz:", placeholder="Enter drücken…",
                          label_visibility="collapsed", key="tp_next_dummy")
            tp_next = st.form_submit_button("➡️ Nächster Satz", type="primary", use_container_width=True)
        if tp_next:
            st.session_state.tp_german = None
            load_tp(pdf_pool, tp_chapter)

    # Reference list
    st.divider()
    with st.expander("📖 Alle Wörter / Sätze dieses Themas anzeigen", expanded=False):
        if tp_source == "📄 TELC Sätze":
            display_vocab = ALL_PDF_VOCAB if tp_chapter == "Alle Themen" else PDF_VOCAB_BY_CHAPTER.get(tp_chapter, {})
        else:
            display_vocab = ALL_WORTSCHATZ if tp_chapter == "Alle Themen" else WORTSCHATZ_BY_CHAPTER.get(tp_chapter, {})
        for de, en in display_vocab.items():
            st.markdown(
                f"<div style='padding:8px 14px; margin-bottom:5px; "
                f"background:#1e1e2e; border-radius:10px; border-left:4px solid #cba6f7;'>"
                f"<div style='font-size:1.0rem; font-weight:700; color:#cdd6f4;'>{de}</div>"
                f"<div style='font-size:0.9rem; color:#a6e3a1; margin-top:2px;'>🇬🇧 {en}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5 — Listening: hear German audio only → type English translation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "🎧 Hören & Schreiben":

    ls_source = st.radio(
        "Vokabelquelle",
        ["📄 TELC Sätze", "📚 Wortschatzliste (Einfach gut A1)"],
        horizontal=True,
        key="ls_source",
    )

    if ls_source == "📄 TELC Sätze":
        ls_chapter_names = PDF_CHAPTER_NAMES
        ls_chapter = st.selectbox("Thema wählen", ls_chapter_names, key="ls_chapter_select")
        ls_pool = get_pdf_pool(ls_chapter)
    else:
        ls_chapter_names = WORTSCHATZ_CHAPTER_NAMES
        ls_chapter = st.selectbox("Thema wählen", ls_chapter_names, key="ls_chapter_select")
        ls_pool = get_wortschatz_pool(ls_chapter)

    load_ls(ls_pool, ls_chapter)

    pool_size = len(ls_pool)
    ls_seen = pool_size - len(st.session_state.ls_deck)
    c1, c2 = st.columns(2)
    c1.metric("Punkte", f"{st.session_state.ls_score} / {st.session_state.ls_total}")
    pct_ls = int(st.session_state.ls_score / st.session_state.ls_total * 100) if st.session_state.ls_total else 0
    c2.metric("Genauigkeit", f"{pct_ls}%")
    st.progress(
        max(0.0, min(1.0, ls_seen / pool_size)) if pool_size else 0,
        text=f"Runde {st.session_state.ls_round} · {ls_seen}/{pool_size} Sätze gehört",
    )

    st.divider()

    # Big audio-only prompt — German text is hidden
    st.markdown(
        "<div style='font-size:1.1rem; font-weight:600; color:#cdd6f4; "
        "margin-bottom:10px;'>🎧 Höre zu und schreibe die englische Bedeutung:</div>",
        unsafe_allow_html=True,
    )

    # Audio player (German text deliberately NOT shown)
    audio = tts_bytes(st.session_state.ls_german)
    if audio:
        col_audio, col_replay = st.columns([5, 1])
        with col_audio:
            st.audio(audio, format="audio/mp3")
        with col_replay:
            st.markdown(
                "<div style='padding-top:8px; font-size:0.85rem; color:#585b70;'>▲ Drücke Play</div>",
                unsafe_allow_html=True,
            )
    else:
        st.warning("Audio nicht verfügbar — bitte Internetverbindung prüfen.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not st.session_state.ls_answered:
        with st.form(key=f"ls_form_{ls_seen}", clear_on_submit=True):
            user_ls = st.text_input(
                "Deine Übersetzung auf Englisch:",
                placeholder="Type the English meaning and press Enter…",
            )
            lc1, lc2, lc3 = st.columns([4, 1, 1])
            with lc1:
                ls_submitted = st.form_submit_button("✅ Prüfen", type="primary", use_container_width=True)
            with lc2:
                ls_reveal = st.form_submit_button("👁️", use_container_width=True, help="Antwort zeigen")
            with lc3:
                ls_skip = st.form_submit_button("⏭️", use_container_width=True, help="Überspringen")
        if ls_reveal:
            st.session_state.ls_revealed = True
        if st.session_state.ls_revealed:
            st.info(
                f"💡 🇩🇪 **{st.session_state.ls_german}**  \n"
                f"🇬🇧 **{st.session_state.ls_english}**"
            )
        if ls_skip:
            st.session_state.ls_german = None
            st.session_state.ls_revealed = False
            load_ls(ls_pool, ls_chapter)
        if ls_submitted and user_ls.strip():
            st.session_state.ls_total += 1
            st.session_state.ls_user_input = user_ls.strip()
            is_correct = normalise(user_ls) == normalise(st.session_state.ls_english)
            if is_correct:
                st.session_state.ls_score += 1
                st.session_state.streak += 1
            else:
                st.session_state.streak = 0
            st.session_state.ls_answered = True
    else:
        correct_en = st.session_state.ls_english
        user_was = st.session_state.ls_user_input
        is_correct = normalise(user_was) == normalise(correct_en)

        # Reveal the German sentence now
        st.markdown(
            f"<div style='font-size:1.4rem; font-weight:700; padding:14px 20px; "
            f"background:#1e1e2e; border-radius:12px; color:#89b4fa; "
            f"text-align:center; margin-bottom:12px;'>"
            f"🇩🇪 {st.session_state.ls_german}</div>",
            unsafe_allow_html=True,
        )

        if is_correct:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #a6e3a1; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>✅</span> "
                f"<span style='color:#a6e3a1; font-size:1.1rem; font-weight:700;'>Richtig!</span> "
                f"<span style='color:#cdd6f4;'><b>{correct_en}</b></span>"
                "</div>",
                unsafe_allow_html=True,
            )
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.markdown(
                "<div style='padding:14px 18px; background:#1e1e2e; border-radius:12px; "
                "border-left:5px solid #f38ba8; margin-bottom:10px;'>"
                "<span style='font-size:1.4rem;'>❌</span> "
                f"<span style='color:#f38ba8; font-size:1.1rem; font-weight:700;'>Falsch.</span> "
                f"Du hast geschrieben: <span style='color:#fab387;'>{user_was}</span><br>"
                f"Richtige Antwort: <span style='color:#a6e3a1; font-weight:700;'>{correct_en}</span>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        if st.session_state.ls_round_complete:
            st.info(f"🎉 Runde abgeschlossen! Weiter mit Runde {st.session_state.ls_round}…")

        with st.form(key=f"ls_next_form_{ls_seen}"):
            st.text_input("Drücke Enter für den nächsten Satz:", placeholder="Enter drücken…",
                          label_visibility="collapsed", key="ls_next_dummy")
            ls_next = st.form_submit_button("➡️ Nächster Satz", type="primary", use_container_width=True)
        if ls_next:
            st.session_state.ls_german = None
            load_ls(ls_pool, ls_chapter)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 6 — Wortschatz Quiz: German word shown → pick 1 of 3 English options
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if active_tab == "📚 Wortschatz Quiz":

    wq_chapter = st.selectbox(
        "Thema wählen",
        WORTSCHATZ_CHAPTER_NAMES,
        key="wq_chapter_select",
    )

    wq_pool = get_wortschatz_pool(wq_chapter)
    load_wq(wq_pool, wq_chapter)

    pool_size = len(wq_pool)
    mastered_count = len(st.session_state.wq_mastered)
    remaining = pool_size - mastered_count

    c1, c2, c3 = st.columns(3)
    c1.metric("Punkte", f"{st.session_state.wq_score} / {st.session_state.wq_total}")
    pct_wq = int(st.session_state.wq_score / st.session_state.wq_total * 100) if st.session_state.wq_total else 0
    c2.metric("Genauigkeit", f"{pct_wq}%")
    c3.metric("✅ Gelernt", f"{mastered_count} / {pool_size}")
    st.progress(
        max(0.0, min(1.0, mastered_count / pool_size)) if pool_size else 0,
        text=f"{mastered_count}/{pool_size} Wörter gemeistert · noch {remaining} übrig",
    )

    st.divider()

    # All words mastered — celebration screen
    if remaining == 0:
        st.balloons()
        st.markdown(
            "<div style='text-align:center; padding:40px 20px; background:#1e1e2e; "
            "border-radius:16px; border:2px solid #a6e3a1;'>"
            "<div style='font-size:3rem;'>🎉</div>"
            "<div style='font-size:1.6rem; font-weight:800; color:#a6e3a1; margin:10px 0;'>"
            "Alle Wörter gemeistert!</div>"
            f"<div style='color:#cdd6f4;'>Du hast alle <b>{pool_size}</b> Wörter beim ersten Versuch richtig beantwortet.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("🔄 Neu starten", type="primary", use_container_width=True, key="wq_restart"):
            st.session_state.wq_mastered = set()
            st.session_state.wq_deck = []
            st.session_state.wq_question = None
            st.session_state.wq_active_chapter = None
            st.rerun()
        st.stop()

    # German word card
    st.markdown(
        f"<div style='font-size:2.2rem; font-weight:800; padding:22px 28px; "
        f"background:#1e1e2e; border-radius:16px; color:#cdd6f4; "
        f"text-align:center; margin-bottom:20px; letter-spacing:0.02em;'>"
        f"{st.session_state.wq_question}</div>",
        unsafe_allow_html=True,
    )
    play_button(st.session_state.wq_question, key="wq_audio")

    # 3 answer buttons (stacked vertically for clarity)
    for i, opt in enumerate(st.session_state.wq_options):
        if st.session_state.wq_answered:
            if opt == st.session_state.wq_correct:
                colour = "#a6e3a1"
                icon = "✅ "
            elif opt == st.session_state.wq_selected:
                colour = "#f38ba8"
                icon = "❌ "
            else:
                colour = "#585b70"
                icon = ""
            st.markdown(
                f"<div style='padding:14px 20px; margin-bottom:8px; border-radius:12px; "
                f"background:#1e1e2e; border:2px solid {colour}; "
                f"color:{colour}; font-size:1.1rem; font-weight:600;'>"
                f"{icon}{opt}</div>",
                unsafe_allow_html=True,
            )
        else:
            if st.button(opt, key=f"wq_{i}", use_container_width=True):
                st.session_state.wq_selected = opt
                st.session_state.wq_answered = True
                st.session_state.wq_total += 1
                if opt == st.session_state.wq_correct:
                    st.session_state.wq_score += 1
                    st.session_state.streak += 1
                    # Mark as mastered only if answer was not peeked at
                    if not st.session_state.wq_revealed:
                        st.session_state.wq_mastered.add(st.session_state.wq_question)
                else:
                    st.session_state.streak = 0
                st.rerun()

    if not st.session_state.wq_answered:
        st.markdown("")
        rc1, rc2 = st.columns(2)
        with rc1:
            if st.button("👁️ Antwort zeigen", use_container_width=True, key="wq_reveal"):
                st.session_state.wq_revealed = True
        with rc2:
            if st.button("⏭️ Überspringen", use_container_width=True, key="wq_skip"):
                st.session_state.wq_question = None
                st.session_state.wq_revealed = False
                load_wq(wq_pool, wq_chapter)
                st.rerun()
        if st.session_state.wq_revealed:
            st.info(f"💡 Antwort: **{st.session_state.wq_correct}**")

    if st.session_state.wq_answered:
        word_is_mastered = st.session_state.wq_question in st.session_state.wq_mastered
        if st.session_state.wq_selected == st.session_state.wq_correct:
            if word_is_mastered:
                st.success(f"✅ Richtig! **Gelernt** — dieses Wort wird nicht mehr wiederholt. 🎓")
            else:
                st.success("✅ Richtig!")
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.error(
                f"❌ Falsch. Richtige Antwort: **{st.session_state.wq_correct}**  \n"
                f"🔁 Dieses Wort kommt wieder vor."
            )

        st.divider()
        if st.button("➡️ Nächstes Wort", type="primary", use_container_width=True, key="wq_next"):
            st.session_state.wq_question = None
            load_wq(wq_pool, wq_chapter)
            st.rerun()
