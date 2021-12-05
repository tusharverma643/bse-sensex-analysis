import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px


st.set_page_config(
    page_title = 'BSE:SENSEX  ANALYIS',
    layout = 'wide'
)
img = Image.open("img/bseimgpng.png")
st.image(img,width=200)
# st.title('BSE:SENSEX  ANALYIS')_

st.markdown(f"<h1 style='text-align: center; color: white;'>{'BSE:SENSEX ANALYSIS'}</h1>", unsafe_allow_html=True)

df=pd.read_csv('Datasets/Sensex-30.csv')
st.write(df,height=300)
sector_freq={}
for item in df.iloc[:,df.shape[1]-1]:
  if item in sector_freq:
    sector_freq[item] += 1
  else:
    sector_freq[item] = 1

sectors=list(sector_freq.keys())
freq=list(sector_freq.values())

fig=px.pie(values=freq, names=sectors,title='Sector wise categorization ')
st.markdown(f"<hr>", unsafe_allow_html=True)

TotalMarketCap=0
TotalMarketCapOfTopFive=0
for index,i in enumerate(df.iloc[:,1]):
  TotalMarketCap=TotalMarketCap+i
  if(index<5):
    TotalMarketCapOfTopFive+=i
TopFiveCompanies=df.sort_values('Market Cap (Cr.)',ignore_index=True,ascending=False).iloc[0:5,:]
companies=list(TopFiveCompanies.iloc[:,0])
companies.append('Others')
market_cap=list(TopFiveCompanies.iloc[:,1])
market_cap.append(TotalMarketCap-TotalMarketCapOfTopFive)


col1,col2 = st.columns(2)
with col1:
  st.plotly_chart(fig, use_container_width=True)
with col2:
  fig=px.pie(values=market_cap, names=companies,title='Market Cap share of top Five Companies')
  st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<hr>", unsafe_allow_html=True)

#roe vs pe
# fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
companies=['RIL','TCS','HDFC','INFY','HUL']
col1,col2,col3 = st.columns((2,2,2))
with col1:
  st.write('Return on Equity %')
  roe=list(TopFiveCompanies.iloc[:,4])
  df1 = pd.DataFrame(roe,index=companies)
  st.line_chart(df1)

with col2:
  st.write('Price-Earnings Ratio %')
  pe=list(TopFiveCompanies.iloc[:,2])
  df2 = pd.DataFrame(pe,index=companies)
  st.line_chart(df2 )

with col3:
  st.write('Profit Margin (Net Profit / Revenue Ratio)')
  net_profit=[int(i.replace(',','')) for i in TopFiveCompanies.iloc[:,9]]
  revenue=[int(i.replace(',','')) for i in TopFiveCompanies.iloc[:,3]]
  prof_ratio=list(map(lambda x,y : x/y,net_profit,revenue))
  df3 = pd.DataFrame(prof_ratio,index=companies)
  st.line_chart(df3)

st.markdown(f"<hr>", unsafe_allow_html=True)

#sectorial market cap vs net profit

from copy import deepcopy
market_cap_sectorial=deepcopy(sector_freq)
netprofit_sectorial=deepcopy(sector_freq)
rev_sectorial=deepcopy(sector_freq)

# print(type(market_cap_sectorial.values()))
df['Revenue (Cr.)'] =df['Revenue (Cr.)'].astype(str)
for i in market_cap_sectorial:
  market_cap_sectorial[i]=0
  netprofit_sectorial[i]=0
  rev_sectorial[i]=0
for index,i in enumerate(df.iloc[:,11]):
  market_cap_sectorial[i]+=df.iloc[index,1]
  netprofit_sectorial[i]+=int(df.iloc[index,10].replace(',', ''))
  rev_sectorial[i]+=int(df.iloc[index,3].replace(',',''))

fig=px.scatter(x=rev_sectorial,y=netprofit_sectorial,size=market_cap_sectorial,color=sectors)
fig.update_layout(
    title="Sector wise relation between Net profit, Revenue and Market Cap",
    xaxis_title="Revenue (Cr. (Rs))",
    yaxis_title="Net Profit (Cr. (Rs))")
st.plotly_chart(fig, use_container_width=True)
st.markdown(f"<hr>", unsafe_allow_html=True)


dff1=pd.read_csv('Datasets/INFY.csv')
dff2=pd.read_csv('Datasets/RELIANCE.csv')
dff3=pd.read_csv('Datasets/HDFCBANK.csv')
dff4=pd.read_csv('Datasets/HINDUNILVR.csv')
dff5=pd.read_csv('Datasets/TCS.csv')
l=[]
l.append(dff1)
l.append(dff2)
l.append(dff3)
l.append(dff4)
l.append(dff5)
for i in range(5):
  l[i]=l[i].loc[(l[i]['Date']>='2017-04-01')]

dffinal=pd.concat([l[i] for i in range(5)], axis=0)
dffinal.reset_index(drop=True,inplace=True)
col1,col2 =st.columns((3,1))
with col2:
  point = st.selectbox("Stock price type: ",
                     ['Open','VWAP','High', 'Low','Last','Close'])
  st.write("Stock price selected: ", point)
with col1:
  fig = px.box(dffinal, x="Symbol", y=point,title="Variance of Stock prices of Top 5 companies (Mark. cap wise) for last 3 years.")
  st.plotly_chart(fig, use_container_width=True)
  
st.markdown(f"<hr>", unsafe_allow_html=True)


fig = px.line(dffinal, x="Date", y="VWAP",color='Symbol',title='Timeline',
labels={"VWAP": "Volue weighted average price (Rs.)"})
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<hr>", unsafe_allow_html=True)

st.markdown(f"<h3>Tushar Verma</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>402083001</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>3COE-30</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>TIET</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>Note:</h3>", unsafe_allow_html=True)
st.markdown(f"<h5>Dataset 1 - (Sensex 30.csv) was web scrapped by me on 29th Nov,2021 using ParseHub Tool and python.All values correspond to the above mentioned date.</h5>", unsafe_allow_html=True)
st.markdown(f"<h5>Dataset 2 - (stock values of Top five companies). Data spans to 30th April, 2021.</h5>", unsafe_allow_html=True)
