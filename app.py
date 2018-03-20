from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime, timedelta
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
import os

################################################################################
# Username and password for any account (Quandl in this case, in private file)
def loadApiKey( keyFile, keyName ) :
	with open(keyFile) as f:
		fromFile = {}
		for line in f:
			line = line.split() # to skip blank lines
			if len(line)==3:
				fromFile[line[0]] = line[2]			
	f.close()
	apiKey = fromFile[keyName]
	return apiKey


################################################################################
# Fetch table from Quandl
def fetchQuandl(ticker, apiKey) :

  # Form the request URL
	ticker = ticker.upper()

	end = datetime.now().date()
	start = end - timedelta(days=30)
	
  start_str = "&start_date=" + start.strftime("%Y-%m-%d")
	end_str  = "&end_date=" + end.strftime("%Y-%m-%d")

	reqUrl = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + \
					'.json?api_key=' + apiKey + start_str + end_str

	print(reqUrl)
  #End of URL generation

  # HTTP request for dataframe and column name
	r = requests.get(reqUrl)
	if r.status_code < 400 :
		# get name of company
		name = r.json()['dataset']['name']
		name = name.split('(')[0]

		# get data
		dat = r.json()['dataset']
		df = DataFrame(dat['data'], columns=dat['column_names'] )
		df = df.set_index(pd.DatetimeIndex(df['Date']))
	else :
		print("Stock ticker not valid")
		df = None
		name = None

  return df, name

app = Flask(__name__)

# Initialization
#app.vars = {}
#keyFile = 'API_KEYS'
#keyName = 'quandl'
#app.vars['apiKey'] = loadApiKey( keyFile, keyName)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
