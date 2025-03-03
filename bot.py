### **2️⃣ bot.py (Main Telegram Bot Code)**
```python
import telebot
import json
import random
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Load questions
with open('data/questions.json', 'r') as file:
    questions = json.load(file)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎓 Welcome to ExamPilot!\nUse /quiz to start answering questions.")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    question = random.choice(questions)
    users[message.chat.id] = question
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in question["options"]:
        markup.add(option)
    bot.send_message(message.chat.id, f"❓ {question['question']}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in users)
def check_answer(message):
    question = users[message.chat.id]
    if message.text == question["answer"]:
        bot.send_message(message.chat.id, "✅ Correct!")
    else:
        bot.send_message(message.chat.id, f"❌ Wrong! The correct answer is {question['answer']}.")
    del users[message.chat.id]

bot.polling()
