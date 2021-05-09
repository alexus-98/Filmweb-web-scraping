from selenium import webdriver
import pandas as pd
import time

start_time = time.time()

path = '/Users/aleksander/Desktop/programowanie/chromedriver'

options = webdriver.chrome.options.Options()
driver = webdriver.Chrome(options = options, executable_path = path)

d = pd.DataFrame({'title': [], 'year': [], 'rate': [], 'votes': []})

k = 1
some_bool = True

while some_bool :

	url = 'https://www.filmweb.pl/serials/search?orderBy=popularity&descending=true&page={}'.format(k)

	driver.get(url)

	movies = driver.find_elements_by_class_name('hits__item')

	for movie in movies:
			title = movie.find_element_by_class_name('filmPreview__title').text
			year = movie.find_element_by_class_name('filmPreview__year').text
			try:
				rate = movie.find_element_by_class_name('rateBox__rate').text
			except:
				continue
			try:
				votes = movie.find_element_by_xpath('.//span[contains(@class, "rateBox__votes")]').text
			except:
				continue

			series = {'title':title, 'year':year, 'rate':rate, 'votes':votes}
			d = d.append(series, ignore_index = True)

	k = k + 1

	if k > 100:
		some_bool = False

driver.quit()

print(d)
d.to_csv('series.csv')

print("--- %s seconds ---" % (time.time() - start_time))
