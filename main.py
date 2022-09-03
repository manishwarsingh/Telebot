import telebot
import stripe
from datetime import datetime

TOKEN = '5361539650:AAGOKpdd7RmQ8ZIaTTnS2gbRR-mPGVJvCGs'

bot = telebot.TeleBot(TOKEN)

print(bot.get_me())

data = {'number': "", 'cvc': "", 'exp_year': "", 'exp_month': ""}
# --- states use in conversation ---

bot.state = None

NUMBER = 1
CVC = 2
EXP_YEAR = 3
EXP_MONTH = 4
STRIPE = 5


@bot.message_handler(commands=['start'])
def card(message):
    global state
    global data

    data = {'number': "", 'cvc': "", 'exp_year': "", 'exp_month': ""}
    bot.send_message(
        message.chat.id,
        'Add card details \nnumber, cvc, exp_year, exp_month in separated messages\n\n Enter the card number.'
    )

    state = NUMBER


@bot.message_handler()
def card_details(message):
    stripe.api_key = "sk_test_51H7NCGKebr7ly2dMDkL8cNEdmPOb5Zuv13erDWnqCL11WjUnkIMoOEy2lgC3I2SltKbpMf4YyiSu0dsCBbCG09I7005yMBC8YI"
    global state
    try:

        if state == NUMBER:

            user_input_card_number = message.text
            data['number'] = user_input_card_number
            print(' user_input_card_number', user_input_card_number)

            if len(user_input_card_number) == 16:
                msg_to_user = "\n Please Enter the card cvc"
                state = CVC
            else:
                state = NUMBER
                msg_to_user = "Card number is Invalid.\n\n Please Enter Number Again"

            print('msg_to_user = ', msg_to_user)
            bot.send_message(message.chat.id, f"{msg_to_user}")

        elif state == CVC:

            user_input_card_cvc = message.text
            data['cvc'] = user_input_card_cvc
            print(' user_input_card_cvc', user_input_card_cvc)

            if len(user_input_card_cvc) == 3:
                msg_to_user = "\n Please Enter the card exp_year"
                state = EXP_YEAR
            else:
                state = CVC
                msg_to_user = "CVC is Invalid.\n\n Please enter cvc again"

            print('msg_to_user = ', msg_to_user)
            bot.send_message(message.chat.id, f"{msg_to_user}")

        elif state == EXP_YEAR:

            user_input_card_exp_year = message.text
            data['exp_year'] = user_input_card_exp_year
            print(' user_input_card_exp_year', type(user_input_card_exp_year))
            currentYear = datetime.now().year
            print(currentYear)

            if (len(user_input_card_exp_year)
                    == 4) or (len(user_input_card_exp_year) == 2):
                msg_to_user = "\n Please Enter the card exp_month"
                state = EXP_MONTH
            else:
                state = EXP_YEAR
                msg_to_user = " exp_year is Invalid.\n\n Please enter exp_year again"

            print('msg_to_user = ', msg_to_user)
            bot.send_message(message.chat.id, f"{msg_to_user}")

        elif state == EXP_MONTH:

            user_input_card_exp_month = message.text
            data['exp_month'] = user_input_card_exp_month
            print(' user_input_card_exp_month', user_input_card_exp_month)
            print('data ------ = ', data)

            # print(number)
            currentMonth = datetime.now().month
            print(currentMonth)

            if (len(user_input_card_exp_month)
                    == 1) or (len(user_input_card_exp_month) == 2):

                try:

                    strapi = stripe.PaymentMethod.create(
                        type="card",
                        card={
                            "number": data['number'],
                            "cvc": data['cvc'],
                            "exp_year": data['exp_year'],
                            "exp_month": user_input_card_exp_month,
                        },
                    )
                    print("my stripeApi data-----------------", strapi)
                    msg_to_user = "Your card is Validated Successfully."
                    msg = """I got all your card details.
      number: {}
      cvc: {}
      exp_year:{}
      exp_month: {}""".format(data['number'], data['cvc'], data['exp_year'],
                              data['exp_month'])
                    bot.send_message(message.chat.id, msg)

                except Exception as e:
                    print('exception = ', str(e))

                    msg_to_user = str(
                        f"{e} \n Please full card details Again correctly /start."
                    )

                state = STRIPE
            else:
                state = EXP_MONTH
                msg_to_user = "Exp_month is Invalid.\n\n Please enter Exp_month again"

            print('msg_to_user = ', msg_to_user)
            bot.send_message(message.chat.id, f"{msg_to_user}")

        elif state == STRIPE:

            user_input = message.text
            print("user_input_verify-----------------", type(user_input))

            state = None
    except RuntimeError as err:
        print("Oops!  That was no valid number.  Try again...", err)

        bot.send_message(message.chat.id, f"{err}")


print("Bot started...")
bot.polling()
