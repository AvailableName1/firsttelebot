import telebot
import config
import random


def random_sentence(sentences):
    i = random.randint(0, len(sentences) - 1)
    return sentences[i]


def get_sentence(path):
    with open(path, 'r', encoding='utf-8') as file_object:
        sentences = file_object.readlines()
    return sentences


def string_without_comma(string):
    if not string.endswith(','):
        return string
    else:
        return string[:len(string)-2]


boulevard_sentences = get_sentence('BLDVR_DEPO_TEXT.txt')

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.send_message(message.chat.id, "Hi! I will send you some random quote, if you command /send")


@bot.message_handler(commands='send')
def quote_message(message):
    bot.send_message(message.chat.id, string_without_comma(random_sentence(boulevard_sentences)))


@bot.message_handler(func=lambda m: True)
def query_of_quote(message):
    query = message.text
    response = [sentence for sentence in boulevard_sentences if query.lower() in sentence.lower()]
    if len(response) != 0:
        bot.send_message(message.chat.id, string_without_comma(random_sentence(response)))
    else:
        bot.send_message(message.chat.id, 'There are no matches with your word in my book')


@bot.message_handler(content_types=["audio, document, photo, sticker, video, video_note, voice"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Unfortunately, I can't reply to this type of message")


bot.polling(none_stop=True)
