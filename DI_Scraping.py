### Importing

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import warnings
import sys
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_date
from datetime import datetime , timedelta
import pytz

### Setting the Date to the actual day of the data

if datetime.now(pytz.timezone('America/Sao_Paulo')).hour < 21:
  Data = (datetime.now(pytz.timezone('America/Sao_Paulo')) - timedelta(1)).strftime("%Y-%m-%d") 
else:
  Data = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d")
print(Data)

### Web Scraping

# warnings.simplefilter(action='ignore', category=FutureWarning)
url='https://br.advfn.com/investimentos/futuros/di-depositos-interfinanceiros/cotacoes'
options = Options()
options.add_argument("--headless") ### not seeing the window oppening
options.add_argument("--no-sandbox") ### evit bugs 
driver = webdriver.Chrome("chromedriver", options=options) ### chossing a web driver
driver.get(url) ### giving the location and oppening
time.sleep  = 5

di1 = driver.find_elements("xpath" , "//td[@class='String Column1']")
Vencimentos = driver.find_elements("xpath" , "//td[@class='String Column2']") ### getting the path to the information that we want
Taxas = driver.find_elements("xpath" , "//td[@class='Numeric Column3']") ### getting the path to the information that we want

# Putting the Data in a DataFrame

df = pd.DataFrame()

for i in range(len(Vencimentos)):
    df=df.append({'DI':di1[i].text,'Vencimento':Vencimentos[i].text,str(Data):Taxas[i].text}, ignore_index=True)

### Treating the Data

df['DI'] = df['DI'].str.replace('BMF:', '')
df[str(Data)] = pd.to_numeric(df[str(Data)].str.replace(',', '.'))
df[str(Data)]=df[str(Data)]/100
print(df)
# with pd.ExcelWriter(Planilha, engine='openpyxl', datetime_format='dd/mm/yyyy', mode='a') as writer:
#     df.to_excel(writer, sheet_name=str(data))


### Ploting Graphics

plt.plot(df['Vencimento'],df[str(Data)],color='k')
plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)
plt.title('Curva de Jurso ' + Data )
plt.tight_layout()
plt.show()

### Importing to a excel

df.to_excel('Di_Historico.xlsx')

### Once Imported to excel you just need to concat with the news collumns evry day!! 

# existing_df = pd.read_excel('Di_pro_Juppa.xlsx')

# new_df = pd.concat([existing_df, df[str(Data)]], axis=1) ### Concating the new collumn

# new_df.to_excel('Di_pro_Juppa.xlsx', index=False) ### Saving above the old one