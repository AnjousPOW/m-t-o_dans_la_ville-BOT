import telebot
import requests
import config


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_handlers(message):
    bot.send_message(message.chat.id, "Привет, в котором городе хочешь узнать погоду 😉?")

@bot.message_handler(content_types=['text'])
def msg_handler(message):
    city = message.text
    params = dict(q=city, units='metric', appid='2e704245de2cfc9b8ea4144006c759d8')
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
    print(city)

    try:
        data = response.json()
        main = data['main']
        wind = data['wind']
        temperature = int(main['temp'])             # температура
        feels_like = int(main['feels_like'])        # Ощущается как
        humidity = int(main['humidity'])            # Влажность
        pressure = int(main['pressure'] * 0.75)     # Давление РТ столба
        windSpeed = int(wind['speed'])              # Скорость ветра

        bot.send_message(message.chat.id, f"{city}"
                                          f"\nТемпература: {temperature} градусов;"
                                          f"\nОщущается как {feels_like} градусов;"
                                          f"\nВлажность {humidity}%;"
                                          f"\nДавление {pressure} РТ столба;"
                                          f"\nСкорость ветра {windSpeed} м/с;\n")

    except KeyError:
        bot.send_message(message.chat.id, f'Я незнаю что ответить 😢')


bot.polling()
