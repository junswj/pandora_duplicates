# Import libraries
import pandas  as pd
import requests
from bs4 import BeautifulSoup
import pickle
import os
import flask
from flask import Flask, render_template, request
import json

#create instance
app=Flask(__name__)

#flask! run index!
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


def dupli_check(url):
    '''
    Input
    URL(Sting): Pandora Playlist URL 

    Output
    df_numbers(DataFrame): Number of duplicate songs in playlist
    df_loc(DataFrame): Location of duplicate songs in playlist
    '''
    
    #request playlist information by using ‘requests’ and parse with 'BeautifulSoup'
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html")
    page_str=str(soup)
    json_dict=page_str.split('var ')[4].replace(';\n    ','').replace('storeData = ','')
    
    #Convert this information to Dictionary using Json
    dic=json.loads(json_dict)
    
    #This dictionary contains two keys:
    #['v4/catalog/annotateObjects', 'v7/playlists/getTracks']
    #Our plans is to create two DataFrame, for each key in the dictionary, and merging it at the end:
    df_tracks=pd.DataFrame(dic['v7/playlists/getTracks'][0]['tracks'])

    #Each song is displayed as a 'trackPandoraId', so we need to pull song information from the other part of dictionary, annotateObjects.
    df_info=pd.DataFrame.from_dict(dic['v4/catalog/annotateObjects'][0], orient='index')
    df_info=df_info.reset_index()
    df_info.rename(columns={'index':'trackPandoraId'}, inplace=True)
    
    #Now we have all the information we needed. Let’s merge these DataFrames:
    df=df_tracks.merge(df_info, left_on='trackPandoraId', right_on='trackPandoraId').sort_values(by=['itemId'])

    #Simply, use groupby function to display how many duplicates are in this playlist:
    df_numbers=df[['name','artistName','itemId']].groupby(['name','artistName']).count().sort_values(by='itemId', ascending=False)

    #Use duplicated function to see where the duplicate songs are located in the playlist:
    df['duplicated']=df.duplicated(subset='name')
    df_loc=df[['name','duplicated']]
    
    return df_numbers, df_loc

def df_to_html(df):
        #converting pd.DataFrame to html readable form
        return [df.to_html(classes='data', header="True")]

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':

        #Receive playlist URL
        posturl = request.form['posturl']

        # Create DataFrames
        df_numbers, df_loc = dupli_check(posturl)
        df_numbers=df_to_html(df_numbers)
        df_loc=df_to_html(df_loc )
       
  
        return render_template("result.html",posturl=posturl, df_loc=df_loc, df_numbers=df_numbers)

if __name__ == '__main__':
    app.run(port=5000, debug=True)