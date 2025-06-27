import telebot
import random
import threading
import time
TOKEN = "7783014657:AAFAv_IQkNmW3le5HAoidTSzaskJ1o5wq0I"   #   Token
OWNER_ID = 7783014657            #     (Admin)

bot = telebot.TeleBot(TOKEN)

users = set()

# text.txt  Q/A   
def load_qa(filename="text.txt"):
    qa_dict = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if "=" in line:
                q, a = line.strip().split("=", 1)
                qa_dict[q.strip().lower()] = a.strip()
    return qa_dict

qa_data = load_qa()

photo_reactions = [
    "   ! ",
    "!   ",
    "     "
]

random_reactions = [
    "  ? ",
    "   ! ",
    "    ! "
]

def is_admin(user_id):
    return user_id == OWNER_ID

@bot.message_handler(content_types=["text"])
def handle_text(message):
    users.add(message.from_user.id)
    user_msg = message.text.lower()
    answer = qa_data.get(user_msg)
    if answer:
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, ",       ?")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    users.add(message.from_user.id)
    reaction = random.choice(photo_reactions)
    bot.reply_to(message, reaction)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, " admin ,    ")
        return
    text = message.text[len('/broadcast'):].strip()
    if not text:
        bot.reply_to(message, "  , : /broadcast  ")
        return
    count = 0
    for user_id in users:
        try:
            bot.send_message(user_id, text)
            count += 1
        except:
            pass
    bot.reply_to(message, f"  !  : {count} ")

@bot.message_handler(commands=['who', 'list'])
def who_list(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, " admin ,    ")
        return
    if users:
        user_list = "\n".join(str(u) for u in users)
        bot.reply_to(message, f"Active users:\n{user_list}")
    else:
        bot.reply_to(message, "    ")

#       ()
def random_messages():
    while True:
        for user_id in list(users):
            try:
                msg = random.choice(random_reactions)
                bot.send_message(user_id, msg)
            except:
                pass
        time.sleep(300)  #   

threading.Thread(target=random_messages, daemon=True).start()

print("Bot is running...")
bot.infinity_polling()