import pyowm
import telebot
from pyowm.utils.config import get_default_config

#поставить русский язык в модуле
config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = pyowm.OWM('e064528ce83fca7a43f7737a49aba944')
bot = telebot.TeleBot("1387537120:AAGZLeT74HZOunv0inH5MMR4oddsRup4im0")

#функция определения погода
def get_weather(place):
	mgr = owm.weather_manager() #менеджер погоды
	observation = mgr.weather_at_place(place) #получить погоду в городе по его названию
	weather = observation.weather #получение информации о погоде
	wds = weather.detailed_status #статус погоды
	temp = weather.temperature('celsius')["temp"] #температура в градусах

	return wds, temp #вернуть статус и температуру


@bot.message_handler(content_types=['text'])
def send_echo(message):
	answer="" #объявление переменной чтоб не было ошибок local variable
	if message.text.split()[0] == "/weather": #команду /weather <место> можно разделить на две части, одна сама команда
		try:
			place = message.text.split()[1] #вторая часть аргумент 
			w = get_weather(place) #получение погоды из ранее созданной функции
		except IndexError: #обработка ошибки не введен город или неправильно введен
			bot.send_message(message.chat.id, "Неправильно введена команда!")
		except pyowm.commons.exceptions.NotFoundError: #обработка ошибки не найден город
			bot.send_message(message.chat.id, "Не найден город!")
		else:
			status = w[0] # [<цифра>] это индекс, из списков можно получить одну строку, в данном случае статус погоды
			temp = w[1] #получить из списка температуру
			answer = "В городе " + place + " сейчас " + status+ "\n" #ответ 1
			answer += "Температура сейчас в районе " + str(int(temp)) + "\n\n" #ответ2

			#условия получения ответа 3, по температуре
			if temp < 10:
				answer += "Сейчас ппц холодно, одевайся потеплее"
			elif temp < 20:
				answer += "Сейчас не так холодно но все же лучше оденься теплее"
			else:
				answer += "Темп. норм, одевайся по летнему"

			bot.send_message(message.chat.id, answer) #отправка сообщения

	#обработка команды /help
	elif message.text == "/help":
		bot.send_message(message.chat.id, "Чтобы получить погоду - напиши команду /weather <город>")
	else:
		bot.send_message(message.chat.id, "Я тебя не понимаю, напиши /help")


bot.polling ( none_stop = True )
