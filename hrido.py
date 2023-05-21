from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import polib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# local variables
from selenium.webdriver.chrome.options import Options as ChromeOptions
chrome_op = ChromeOptions()

browser = webdriver.Firefox();
pot = polib.pofile('divi-essential.pot')
po = polib.POFile()

for entry in pot:
	browser.get('https://translate.google.com/?sl=en&tl=nl&text='+entry.msgid+'&op=translate');
	# browser.implicitly_wait(3);
	result = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[9]/div/div[1]/span[1]/span/span'))
	);
	browser.implicitly_wait(2)
	
	po_entry = polib.POEntry(
		msgid=entry.msgid,
		msgstr=result.text
	);
	# print(entry.msgid)
	po.append(po_entry)

po.save('my_file.es.po')



def takeInput():
	languages = {"English": 'en', "French": 'fr',
				"Spanish": 'es', "German": 'de', "Italian": 'it'}

	print("Select a source and target language (enter codes)")
	print("Language", " ", "Code")

	for x in languages:
		print(x, " ", languages[x])

	print("\n\nSource: ", end ="")
	src = input()
	sflag = 0

	for x in languages:
		if(languages[x] == src and not sflag):
			sflag = 1
			break
	if(not sflag):
		print("Source code not from the list, Exiting....")
		exit()

	print("Target: ", end ="")
	trg = input()
	tflag = 0

	for x in languages:
		if(languages[x] == trg and not tflag):
			tflag = 1
			break

	if(not tflag):
		print("Target code not from the list, Exiting....")
		exit()

	if(src == trg):
		print("Source and Target cannot be same, Exiting...")
		exit()

	print("Enter the phrase: ", end ="")
	phrase = input()

	return src, trg, phrase

def makeCall(url, script, default):
	response = default
	try:
		browser.get(url)
		while(response == default):
			response = browser.execute_script(script)

	except JavascriptException:
		print(JavascriptException.args)

	except NoSuchElementException:
		print(NoSuchElementException.args)

	if(response != default):
		return response
	else:
		return 'Not Available'


def googleTranslate(src, trg, phrase):
	url = 'https://translate.google.co.in/# view = home&op = translate&sl =' + \
		src + '&tl =' + trg+'&text ='+phrase
	script = 'return document.getElementsByClassName("tlid-translation")[0].textContent'
	# return makeCall(url, script, None)
	return;

# if __name__ == "__main__":
# 	src, trg, phrase = takeInput()
# 	# print("\nResult: ", googleTranslate(src, trg, phrase))
# 	print( src, trg, phrase )
