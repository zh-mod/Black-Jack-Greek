from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
# import gunicorn
# import psycopg
import json
import random
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Bootstrap5(app)

card_list = {
    '♠A': (1, 11),
    '♥A': (1, 11),
    '♦A': (1, 11),
    '♣A': (1, 11),
    '♠2': (2, 2),
    '♥2': (2, 2),
    '♦2': (2, 2),
    '♣2': (2, 2),
    '♠3': (3, 3),
    '♥3': (3, 3),
    '♦3': (3, 3),
    '♣3': (3, 3),
    '♠4': (4, 4),
    '♥4': (4, 4),
    '♦4': (4, 4),
    '♣4': (4, 4),
    '♠5': (5, 5),
    '♥5': (5, 5),
    '♦5': (5, 5),
    '♣5': (5, 5),
    '♠6': (6, 6),
    '♥6': (6, 6),
    '♦6': (6, 6),
    '♣6': (6, 6),
    '♠7': (7, 7),
    '♥7': (7, 7),
    '♦7': (7, 7),
    '♣7': (7, 7),
    '♠8': (8, 8),
    '♥8': (8, 8),
    '♦8': (8, 8),
    '♣8': (8, 8),
    '♠9': (9, 9),
    '♥9': (9, 9),
    '♦9': (9, 9),
    '♣9': (9, 9),
    '♠10': (10, 10),
    '♥10': (10, 10),
    '♦10': (10, 10),
    '♣10': (10, 10),
    '♠J': (11, 10),
    '♥J': (11, 10),
    '♦J': (11, 10),
    '♣J': (11, 10),
    '♠Q': (12, 10),
    '♥Q': (12, 10),
    '♦Q': (12, 10),
    '♣Q': (12, 10),
    '♠K': (13, 10),
    '♥K': (13, 10),
    '♦K': (13, 10),
    '♣K': (13, 10),
}


def bj_assess_hand(hand):
    value = 0
    for card in hand:
        value += card_list[card][1]
    if value > 21 and ('♠A' in hand or '♥A' in hand or '♦A' in hand or '♣A' in hand):
        value -= 10
    return value


def bj_choose_action_ai(hand, dealer_hand):
    w = str(bj_assess_hand(hand))
    if '♠A' in hand or '♥A' in hand or '♦A' in hand or '♣A' in hand:
        value_without_ace = 0
        for card in hand:
            value_without_ace += card_list[card][1] if card_list[card][1] != 11 else 0
        if value_without_ace <= 10:
            x = "A"
        else:
            x = ""
    else:
        x = ""
    y = str("S" if len(hand) == 2 and card_list[hand[0]][1] == card_list[hand[1]][1] else "")
    z = str(bj_assess_hand(dealer_hand))
    bj_strategy = {
        "202": "Stand",
        "192": "Stand",
        "182": "Stand",
        "172": "Stand",
        "162": "Stand",
        "152": "Stand",
        "142": "Stand",
        "132": "Stand",
        "122": "Hit",
        "112": "Double",
        "102": "Double",
        "92": "Hit",
        "82": "Hit",
        "72": "Hit",
        "62": "Hit",
        "52": "Hit",
        "20A2": "Stand",
        "19A2": "Stand",
        "18A2": "Stand",
        "17A2": "Hit",
        "16A2": "Hit",
        "15A2": "Hit",
        "14A2": "Hit",
        "13A2": "Hit",
        "12AS2": "Split",
        "20S2": "Stand",
        "18S2": "Split",
        "16S2": "Split",
        "14S2": "Split",
        "12S2": "Split",
        "10S2": "Double",
        "8S2": "Hit",
        "6S2": "Split",
        "4S2": "Split",
        "203": "Stand",
        "193": "Stand",
        "183": "Stand",
        "173": "Stand",
        "163": "Stand",
        "153": "Stand",
        "143": "Stand",
        "133": "Stand",
        "123": "Hit",
        "113": "Double",
        "103": "Double",
        "93": "Double",
        "83": "Hit",
        "73": "Hit",
        "63": "Hit",
        "53": "Hit",
        "20A3": "Stand",
        "19A3": "Stand",
        "18A3": "Double",
        "17A3": "Double",
        "16A3": "Hit",
        "15A3": "Hit",
        "14A3": "Hit",
        "13A3": "Hit",
        "12AS3": "Split",
        "20S3": "Stand",
        "18S3": "Split",
        "16S3": "Split",
        "14S3": "Split",
        "12S3": "Split",
        "10S3": "Double",
        "8S3": "Hit",
        "6S3": "Split",
        "4S3": "Split",
        "204": "Stand",
        "194": "Stand",
        "184": "Stand",
        "174": "Stand",
        "164": "Stand",
        "154": "Stand",
        "144": "Stand",
        "134": "Stand",
        "124": "Stand",
        "114": "Double",
        "104": "Double",
        "94": "Double",
        "84": "Hit",
        "74": "Hit",
        "64": "Hit",
        "54": "Hit",
        "20A4": "Stand",
        "19A4": "Stand",
        "18A4": "Double",
        "17A4": "Double",
        "16A4": "Double",
        "15A4": "Double",
        "14A4": "Hit",
        "13A4": "Hit",
        "12AS4": "Split",
        "20S4": "Stand",
        "18S4": "Split",
        "16S4": "Split",
        "14S4": "Split",
        "12S4": "Split",
        "10S4": "Double",
        "8S4": "Hit",
        "6S4": "Split",
        "4S4": "Split",
        "205": "Stand",
        "195": "Stand",
        "185": "Stand",
        "175": "Stand",
        "165": "Stand",
        "155": "Stand",
        "145": "Stand",
        "135": "Stand",
        "125": "Stand",
        "115": "Double",
        "105": "Double",
        "95": "Double",
        "85": "Hit",
        "75": "Hit",
        "65": "Hit",
        "55": "Hit",
        "20A5": "Stand",
        "19A5": "Stand",
        "18A5": "Double",
        "17A5": "Double",
        "16A5": "Double",
        "15A5": "Double",
        "14A5": "Double",
        "13A5": "Double",
        "12AS5": "Split",
        "20S5": "Stand",
        "18S5": "Split",
        "16S5": "Split",
        "14S5": "Split",
        "12S5": "Split",
        "10S5": "Double",
        "8S5": "Split",
        "6S5": "Split",
        "4S5": "Split",
        "206": "Stand",
        "196": "Stand",
        "186": "Stand",
        "176": "Stand",
        "166": "Stand",
        "156": "Stand",
        "146": "Stand",
        "136": "Stand",
        "126": "Stand",
        "116": "Double",
        "106": "Double",
        "96": "Double",
        "86": "Hit",
        "76": "Hit",
        "66": "Hit",
        "56": "Hit",
        "20A6": "Stand",
        "19A6": "Stand",
        "18A6": "Double",
        "17A6": "Double",
        "16A6": "Double",
        "15A6": "Double",
        "14A6": "Double",
        "13A6": "Double",
        "12AS6": "Split",
        "20S6": "Stand",
        "18S6": "Split",
        "16S6": "Split",
        "14S6": "Split",
        "12S6": "Split",
        "10S6": "Double",
        "8S6": "Split",
        "6S6": "Split",
        "4S6": "Split",
        "207": "Stand",
        "197": "Stand",
        "187": "Stand",
        "177": "Stand",
        "167": "Hit",
        "157": "Hit",
        "147": "Hit",
        "137": "Hit",
        "127": "Hit",
        "117": "Double",
        "107": "Double",
        "97": "Hit",
        "87": "Hit",
        "77": "Hit",
        "67": "Hit",
        "57": "Hit",
        "20A7": "Stand",
        "19A7": "Stand",
        "18A7": "Stand",
        "17A7": "Hit",
        "16A7": "Hit",
        "15A7": "Hit",
        "14A7": "Hit",
        "13A7": "Hit",
        "12AS7": "Split",
        "20S7": "Stand",
        "18S7": "Stand",
        "16S7": "Split",
        "14S7": "Split",
        "12S7": "Hit",
        "10S7": "Double",
        "8S7": "Hit",
        "6S7": "Split",
        "4S7": "Split",
        "208": "Stand",
        "198": "Stand",
        "188": "Stand",
        "178": "Stand",
        "168": "Hit",
        "158": "Hit",
        "148": "Hit",
        "138": "Hit",
        "128": "Hit",
        "118": "Double",
        "108": "Double",
        "98": "Hit",
        "88": "Hit",
        "78": "Hit",
        "68": "Hit",
        "58": "Hit",
        "20A8": "Stand",
        "19A8": "Stand",
        "18A8": "Stand",
        "17A8": "Hit",
        "16A8": "Hit",
        "15A8": "Hit",
        "14A8": "Hit",
        "13A8": "Hit",
        "12AS8": "Split",
        "20S8": "Stand",
        "18S8": "Split",
        "16S8": "Split",
        "14S8": "Hit",
        "12S8": "Hit",
        "10S8": "Double",
        "8S8": "Hit",
        "6S8": "Hit",
        "4S8": "Hit",
        "209": "Stand",
        "199": "Stand",
        "189": "Stand",
        "179": "Stand",
        "169": "Hit",
        "159": "Hit",
        "149": "Hit",
        "139": "Hit",
        "129": "Hit",
        "119": "Double",
        "109": "Double",
        "99": "Hit",
        "89": "Hit",
        "79": "Hit",
        "69": "Hit",
        "59": "Hit",
        "20A9": "Stand",
        "19A9": "Stand",
        "18A9": "Hit",
        "17A9": "Hit",
        "16A9": "Hit",
        "15A9": "Hit",
        "14A9": "Hit",
        "13A9": "Hit",
        "12AS9": "Split",
        "20S9": "Stand",
        "18S9": "Split",
        "16S9": "Split",
        "14S9": "Hit",
        "12S9": "Hit",
        "10S9": "Double",
        "8S9": "Hit",
        "6S9": "Hit",
        "4S9": "Hit",
        "2010": "Stand",
        "1910": "Stand",
        "1810": "Stand",
        "1710": "Stand",
        "1610": "Hit",
        "1510": "Hit",
        "1410": "Hit",
        "1310": "Hit",
        "1210": "Hit",
        "1110": "Double",
        "1010": "Hit",
        "910": "Hit",
        "810": "Hit",
        "710": "Hit",
        "610": "Hit",
        "510": "Hit",
        "20A10": "Stand",
        "19A10": "Stand",
        "18A10": "Hit",
        "17A10": "Hit",
        "16A10": "Hit",
        "15A10": "Hit",
        "14A10": "Hit",
        "13A10": "Hit",
        "12AS10": "Split",
        "20S10": "Stand",
        "18S10": "Stand",
        "16S10": "Split",
        "14S10": "Hit",
        "12S10": "Hit",
        "10S10": "Hit",
        "8S10": "Hit",
        "6S10": "Hit",
        "4S10": "Hit",
        "2011": "Stand",
        "1911": "Stand",
        "1811": "Stand",
        "1711": "Stand",
        "1611": "Hit",
        "1511": "Hit",
        "1411": "Hit",
        "1311": "Hit",
        "1211": "Hit",
        "1111": "Double",
        "1011": "Hit",
        "911": "Hit",
        "811": "Hit",
        "711": "Hit",
        "611": "Hit",
        "511": "Hit",
        "20A11": "Stand",
        "19A11": "Stand",
        "18A11": "Hit",
        "17A11": "Hit",
        "16A11": "Hit",
        "15A11": "Hit",
        "14A11": "Hit",
        "13A11": "Hit",
        "12AS11": "Split",
        "20S11": "Stand",
        "18S11": "Stand",
        "16S11": "Split",
        "14S11": "Hit",
        "12S11": "Hit",
        "10S11": "Hit",
        "8S11": "Hit",
        "6S11": "Hit",
        "4S11": "Hit",
    }
    return bj_strategy[w + x + y + z]


@app.route("/")
def blackjack():
    player_hand = ['♠A', '♠10']
    dealer_hand = []
    while bj_assess_hand(player_hand) == 21:
        player_hand = []
        for i in range(2):
            player_hand.append(random.choice(list(card_list)))
    dealer_hand.append(random.choice(list(card_list)))
    ideal_strategy = bj_choose_action_ai(player_hand, dealer_hand)
    return render_template("index.html", player_hand=player_hand, dealer_hand=dealer_hand, ideal_strategy=ideal_strategy)


def read_data(category=False):
    with open("vocabulary.csv", encoding="utf-8") as file:
        data = csv.reader(file, delimiter=";")
        next(data)
        vocabulary = {}
        for row in data:
            if row[2] not in vocabulary:
                vocabulary.update({row[2]: []})
            vocabulary[row[2]].append({row[1]: row[0]})
            if row[3] not in vocabulary:
                vocabulary.update({row[3]: []})
            vocabulary[row[3]].append({row[1]: row[0]})
        if category:
            return vocabulary[category]
        else:
            categories = list(vocabulary)
            return categories


@app.route("/save_current_rotationter>")
def save_current_rotation():
    with open("focus.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        for word in session["vocabulary"]:
            entry = (list(word.values()) + list(word.keys()) + ["Fokus Training"] + ["Fokus Training"])
            writer.writerow(entry)
        return redirect(url_for('greek'))


@app.route("/continue_focus")
def continue_focus():
    with open("focus.csv", encoding="utf-8") as file:
        data = csv.reader(file, delimiter=";")
        vocabulary = []
        for row in data:
            vocabulary.append({row[1]: row[0]})
        session["vocabulary"] = vocabulary
        session.modified = True
        print(vocabulary)
    return redirect(url_for('quiz_write_greek', chapter="a"))


@app.route("/lerne_griechisch")
def greek():
    session["vocabulary"] = None
    chapters = read_data()
    return render_template("greek.html", chapters=chapters)


@app.route("/add_unknown/<german>/<greek>/<chapter>")
def add_unknown(german, greek, chapter):
    session["unknown"].append({german: greek})
    session.modified = True
    return redirect(url_for('quiz_write_greek', chapter=chapter))


@app.route("/continue_unknown")
def continue_unknown():
    session["vocabulary"] = session["unknown"]
    random.shuffle(session["vocabulary"])
    session["unknown"] = []
    session.modified = True
    return redirect(url_for('quiz_write_greek', chapter="a"))


@app.route("/quiz_write_greek/<chapter>")
def quiz_write_greek(chapter):
    if session["vocabulary"] is None:
        session["unknown"] = []
        chosen_quiz = read_data(chapter)
        random.shuffle(chosen_quiz)
        session["vocabulary"] = chosen_quiz
        session.modified = True
    print(len(session["vocabulary"]))
    words_left = len(session["vocabulary"])
    count_unknown = len(session["unknown"])
    try:
        current_word = session["vocabulary"].pop()
        session.modified = True
    except IndexError:
        return redirect(url_for('greek'))
    print(len(session["vocabulary"]))
    for key, value in current_word.items():
        german = key
        greek = value
    return render_template("quiz.html", german=german, greek=greek, chapter=chapter, words_left=words_left, count_unknown=count_unknown)


if __name__ == '__main__':
    app.run(debug=True)
