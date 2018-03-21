from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
import datetime

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def main():
  return redirect(url_for('stock'))

@app.route('/about')
def about():
  return render_template('about.html')

#Main Process
@app.route('/stock')
def stock():
  stockticker = request.args.get('stockticker')
  stockperiod = str(request.args.get('period'))

  if stockticker and stockticker.strip():
    #Request data from Quandl
    #https://www.quandl.com/api/v3/datasets/WIKI/A.json?api_key=bFyyXx1cePZvde71f-cF&start_date=2018-02-18&end_date=2018-03-20
    baseURL = 'https://www.quandl.com/api/v3/datasets/WIKI/'
    periodURL = {'1M':'&start_date=' + (datetime.datetime.now() - datetime.timedelta(days=30) ).strftime('%Y-%m-%d') + '&end_date=' + datetime.datetime.now().strftime('%Y-%m-%d'),
                 '6M':'&start_date=' + (datetime.datetime.now() - datetime.timedelta(days=183)).strftime('%Y-%m-%d') + '&end_date=' + datetime.datetime.now().strftime('%Y-%m-%d'),
                 '1Y':'&start_date=' + (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d') + '&end_date=' + datetime.datetime.now().strftime('%Y-%m-%d'),
                 'All':'',
                 'None':''}
    jsonURL = baseURL + stockticker + '.json?api_key=bFyyXx1cePZvde71f-cF' + periodURL[stockperiod]
    jsonRespond = requests.get(jsonURL)
    HTTPstatusCode = jsonRespond.status_code

    print('[URL]        ' + jsonURL)
    print('[HTTP]       ' + str(HTTPstatusCode))
    print('[StockTicker]' + stockticker)
    print('[Period]     ' + stockperiod)

    #Parse data if HTTP Status is OK
    if HTTPstatusCode == 200:
      jheader = (jsonRespond.json())['dataset']['column_names']
      jdata = (jsonRespond.json())['dataset']['data']
      stockdata = pd.DataFrame(jdata, columns=jheader)
      stockdata["Date"] = pd.to_datetime(stockdata["Date"])
      print(stockdata.head())

      #Calculate the positions of the bars
      mids = (stockdata.Open + stockdata.Close)/2
      spans = abs(stockdata.Close-stockdata.Open)
      #Check the up/down of the day to determin the bar color
      inc = stockdata.Close > stockdata.Open
      dec = stockdata.Open > stockdata.Close

      w = 12*60*60*1000 # half day in ms

      #Render Plot
      fig = figure(title = None, plot_width = 800, plot_height = 600, x_axis_type = "datetime", toolbar_location = "below", tools = "crosshair, pan, wheel_zoom, box_zoom, reset")
      fig.segment(stockdata.Date, stockdata.High, stockdata.Date, stockdata.Low, color = "black")
      fig.rect(stockdata.Date[inc], mids[inc], w, spans[inc], fill_color = "#D5E1DD", line_color = "black")
      fig.rect(stockdata.Date[dec], mids[dec], w, spans[dec], fill_color = "#F2583E", line_color = "black")

      js_resources = INLINE.render_js()
      css_resources = INLINE.render_css()

      script, div = components(fig, INLINE)

      html = render_template('stock.html', status = {'code':1, 'msg':'OK'}, stock = {'ticker':stockticker, 'period':stockperiod}, plot = {'script':script, 'div':div}, js_resources=js_resources, css_resources=css_resources)
    else:
      html = render_template('stock.html', status = {'code':2, 'msg':'Server Error'}, stock = {'ticker':stockticker, 'period':stockperiod})
  else:
    html = render_template('stock.html', status = {'code':3, 'msg':'Please Enter a stock ticker'}, stock = {'ticker':'None', 'period':'None'})

  return html

if __name__ == '__main__':
  app.run(debug = True)
