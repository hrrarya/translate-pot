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
from selenium.webdriver.firefox.options import Options
opt = Options()

opt.add_argument('-headless')

browser = webdriver.Firefox(options=opt);

# pot = polib.pofile('divi-essential-1.pot')
pot = polib.pofile('lol.pot')
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

po.save('lol-nl_BQ.po')
