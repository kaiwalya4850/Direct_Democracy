from googletrans import Translator

def lan(ip):
	translator = Translator()
	translated = translator.translate(ip)
	a = translated.text
	return a
#sentence = lan(input)
#print(sentence)