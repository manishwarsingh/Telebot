import telebot
import stripe
from csv import reader

API_KEY= "5361539650:AAGOKpdd7RmQ8ZIaTTnS2gbRR-mPGVJvCGs"
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Bot'])
def Bot(message):
  bot.reply_to(message, "Hey! I m credit card BOT ?")
  
@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "hey")

@bot.message_handler(commands=['hru'])
def hru(message):
  bot.send_message(message.chat.id, "hey! I m Good, you say?")
  bot.send_message(message.chat.id,"Select /start or /card_validate")

@bot.message_handler(commands=['card_validate'])
def card_validate(message):  
  stripe.api_key = "sk_test_51H7NCGKebr7ly2dMDkL8cNEdmPOb5Zuv13erDWnqCL11WjUnkIMoOEy2lgC3I2SltKbpMf4YyiSu0dsCBbCG09I7005yMBC8YI"

  with open('cards.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
          
            number = row[0]
            cvc = row[1]
            expiry_date = row[2]
            expiry_date = expiry_date.split('|')
            exp_month = expiry_date[0]
            exp_year = expiry_date[1]
            print('number = ', number)
            print('cvc = ', cvc)
            print('exp_month = ', exp_month)
            print('exp_year = ', exp_year)
            stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
            )
         
  bot.send_message(message.chat.id,f"My card no. is >> {number} \n cvc >> {cvc} \n exp_month >> {exp_month} \n exp_year >> {exp_year}")
  # bot.send_message(message.chat.id,"Select /start or /card_validate")
  # bot.send_message(message.chat.id,f"cvc {cvc}")
  # bot.send_message(message.chat.id,f"expire month {exp_month}")
  # bot.send_message(message.chat.id,f"expire year {exp_year}")
  
bot.polling()