import urllib.request
import pandas
import datetime
import os
import multiprocessing as mp
from multiprocessing.pool import ThreadPool

# Print iterations progress
def printProgressBar (i, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
    filledLength = int(length * i // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if i == total: 
        print()

nq100 = pandas.read_csv("nq100.csv", header=0, delimiter=",")
sp500 = pandas.read_csv("sp500.csv", header=0, delimiter=",")
symbol_list = list(set(nq100['Symbol'].append (sp500['Identifier'])))

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
chart_url = "https://c.stockcharts.com/c-sc/sc?s="
chart_url_suffix = "&p=D&b=5&g=0&i=0&r=1568448532473"

date_string = datetime.date.today()
date_string = str(date_string)

if not os.path.exists(date_string):
    os.makedirs(date_string)

def geturl(symbol):

    stock_url= chart_url + symbol + chart_url_suffix
    filename = date_string + "\\" + symbol + ".gif"
    if not os.path.exists(filename):
        try:
            urllib.request.urlretrieve(stock_url, filename)
            printProgressBar(symbol_list.index(symbol), 522, prefix = 'Progress:', suffix = 'Complete', length = 50)
        except Exception as e:
            print(e)
            pass 
    
start= datetime.datetime.now()
pool = ThreadPool(mp.cpu_count())
results = pool.map(geturl, symbol_list)
pool.close()
print("Download finished. Total time = ", datetime.datetime.now()-start)

# End of File