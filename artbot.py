from derpibooru import Search, sort
import telebot
import os


with open("Token.txt") as token:
    bot = telebot.TeleBot(token.read())
BAYANS = 'bayans.txt'
LOCKER = 'locker.txt'


def send_art(chat_id):
    if os.path.isfile(LOCKER):
        return
    open(LOCKER, 'w').close()
    with open(BAYANS) as b:
        bayan_ids = set(b.read().split())
    N = 10
    while True:
        for pic in Search().sort_by(sort.SCORE).limit(N)\
                .query("first_seen_at.gt:30 days ago", "safe", "-animated", "-comic", "-screencap"):
            if pic.id not in bayan_ids:
                bot.send_photo(chat_id, pic.large)
                with open(BAYANS, 'a') as b:
                    b.write(pic.id + '\n')
                os.remove(LOCKER)
                print("Anti-Hibonicus art sent!")
                return
        N *= 3


def informer(message):
    user = message.from_user
    print("User: {{id: {}, username: {}, first_name: {}, last_name: {}}}".format(
          user.id, user.username, user.first_name, user.last_name))
    print("Text:\n" + str(message.text))


@bot.message_handler(content_types=["photo"])
def hibonicus_detector(message):
    informer(message)
    print("Hibonicus detector activated!")
    if message.from_user.id in (235098742, 256490925):
        send_art(message.chat.id)
    else:
        print("Not Hibonicus, false alarm!")


@bot.message_handler(commands=['art'])
def find_file_ids(message):
    informer(message)
    print("Art command got!")
    send_art(chat_id=message.chat.id)
    print("Art command executed!")


@bot.message_handler()
def default(message):
    informer(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
