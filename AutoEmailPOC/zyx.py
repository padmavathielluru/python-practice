from googletrans import Translator

translator = Translator()
result = translator.translate("Hello", dest="hi")

print(result.text)
