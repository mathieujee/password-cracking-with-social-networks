from utils.textCleaner import *


def test_remove_htm_tags():
    text1 = "<div>This is a <p>small text.</p></div>"
    assert remove_html_tags(text1) == "This is a small text."


def test_remove_emojis():
    text1 = "This is a smiley face: 😊"
    text2 = "I love u lt3" # lt3 represents <3
    assert remove_emojis(text1) == "This is a smiley face: "
    assert remove_emojis(text2) == "I love u "


def test_remove_http_links():
    text1 = "This is a text with a link http://www.google.com"
    text2 = "Click on this link https://www.becomeRich.fake to become rich !"
    assert remove_http_links(text1) == "This is a text with a link "
    assert remove_http_links(text2) == "Click on this link  to become rich !"


def test_remove_special_chars():
    text1 = "Hello, my name is Bob."
    text2 = "Hello, I'm Bob."
    text3 = "C'est-à-dire ?"
    assert remove_special_chars(text1) == "Hello my name is Bob"
    assert remove_special_chars(text2) == "Hello I'm Bob"
    assert remove_special_chars(remove_accents(text3)) == "C'est-a-dire "


def test_remove_accents():
    text1 = "Bonjour, j'aime le maïs."
    text2 = "François aime le blé."
    text3 = "àâäéèêëïîöôûüùç"
    assert remove_accents(text1) == "Bonjour, j'aime le mais."
    assert remove_accents(text2) == "Francois aime le ble."
    assert remove_accents(text3) == "aaaeeeeiioouuuc"


def test_clean_html_text():
    text1 = "<div>This is a typical <p>html text.</p></div> Click on this link: https://www.google.com :)"
    text2 = "Ma Reine devant l’Éternel. lt3"
    text3 = "Ah l'hiver!"
    assert clean_html_text(text1) == "this is a typical html text click on this link  "
    assert clean_html_text(text2) == "ma reine devant l’eternel "
    assert clean_html_text(text3) == "ah l'hiver"

def test_lowercase_text():
    text1 = "This is a small text"
    text2 = "AaAaAAAAAa"
    assert lowercase_text(text1) == "this is a small text"
    assert lowercase_text(text2) == "aaaaaaaaaa"
