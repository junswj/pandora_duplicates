
# How to find duplicate songs in Pandora playlist: Pandas and Dictionary

I am big fan of Pandora Radio, and I love their automated music recommendations, which is powered by the Music Genome Project. Only thing they are missing is removing the duplicated songs in the playlist, and I wanted to share the method how I do it.

<img src=./static/pweb.png>

# Importing Libraries and Functions:
*Following packages and functions are used in this work:*
-	Requests: Playlist data request and receive
-	BeautifulSoup: Good friend of Web scraper, used for parsing html
-	Json: Converting string to dictionary form
-	Pandas: Dictionary to DataFrame



```python
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
```

First, request playlist information by using ‘requests’ and parse with 'BeautifulSoup':


```python
url=input("Input Pandora Playlist URL: ")
```

    Input Pandora Playlist URL: https://www.pandora.com/playlist/PL:...



```python
r=requests.get(url)
soup=BeautifulSoup(r.content,"html")
print(soup)
```

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <script type="application/ld+json">{"@type":"MusicPlaylist","@id":"PL: ... }</script>
    <script>
        var hasCommand = ....

        ....

        var storeData = {"v4/catalog/annotateObjects":[{"TR:11...":{"name":"Candle In The Wind (Remastered)","sortableName":"Candle In The Wind (Remastered)","duration":229,"trackNumber":9,"volumeNumber":1,"icon":{...}]}

        ...

All the data you need is included in 'var storeData =', which is dictionary form. Let's extract this:

```python
page_str=str(soup)
json_dict=page_str.split('var ')[4].replace(';\n    ','').replace('storeData = ','')
```
    {"v4/catalog/annotateObjects":
      [{"TR:11...":{"name":"Candle In The Wind (Remastered)",
      "sortableName":"Candle In The Wind (Remastered)","duration":229,
      "trackNumber":9,"volumeNumber":1,...}]

    ...

Convert this information to Dictionary using Json:


```python
type(json_dict)
```




    str




```python
dic=json.loads(json_dict)
```


```python
type(dic)
```




    dict



This dictionary contains two keys:
-	__*v7/playlists/getTracks:*__ Contains order of songs, denoted as trackID, in the playlist
-	__*v4/catalog/annotateObjects:*__ Contains basic information of songs included in the playlist


```python
dic.keys()
```




    dict_keys(['v4/catalog/annotateObjects', 'v7/playlists/getTracks'])



Our plans is to create two DataFrame, for each key in the dictionary, and merging it at the end:


```python
df_tracks=pd.DataFrame(dic['v7/playlists/getTracks'][0]['tracks'])
df_tracks.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>addedTimestamp</th>
      <th>duration</th>
      <th>itemId</th>
      <th>trackPandoraId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1564722184825</td>
      <td>337</td>
      <td>1</td>
      <td>TR:71794</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1564722203547</td>
      <td>229</td>
      <td>2</td>
      <td>TR:11053912</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1564722203547</td>
      <td>191</td>
      <td>3</td>
      <td>TR:30999</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1564722203547</td>
      <td>165</td>
      <td>4</td>
      <td>TR:13247705</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1564722203547</td>
      <td>221</td>
      <td>5</td>
      <td>TR:5593489</td>
    </tr>
  </tbody>
</table>
</div>



Each song is displayed as a 'trackPandoraId', so we need to pull song information from the other part of dictionary, annotateObjects.


```python
df_info=pd.DataFrame.from_dict(dic['v4/catalog/annotateObjects'][0], orient='index')
df_info=df_info.reset_index()
df_info.rename(columns={'index':'trackPandoraId'}, inplace=True)
```


```python
df_info.tail()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>trackPandoraId</th>
      <th>name</th>
      <th>sortableName</th>
      <th>duration</th>
      <th>trackNumber</th>
      <th>volumeNumber</th>
      <th>icon</th>
      <th>rightsInfo</th>
      <th>albumId</th>
      <th>artistId</th>
      <th>...</th>
      <th>twitterHandle</th>
      <th>collaboration</th>
      <th>primaryArtists</th>
      <th>variousArtist</th>
      <th>listenerId</th>
      <th>webname</th>
      <th>displayname</th>
      <th>releaseDate</th>
      <th>isCompilation</th>
      <th>tracks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23</th>
      <td>TR:5593489</td>
      <td>She's Always A Woman (Live)</td>
      <td>She's Always A Woman (Live)</td>
      <td>221.0</td>
      <td>21.0</td>
      <td>1.0</td>
      <td>{'dominantColor': 'd8152d', 'thorId': 'images/...</td>
      <td>{'hasInteractive': True, 'hasOffline': False, ...</td>
      <td>AL:648110</td>
      <td>AR:3215</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>24</th>
      <td>TR:5671030</td>
      <td>Faithfully</td>
      <td>Faithfully</td>
      <td>267.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '00638a', 'thorId': 'images/...</td>
      <td>{'hasInteractive': False, 'hasOffline': False,...</td>
      <td>AL:656195</td>
      <td>AR:1522</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>25</th>
      <td>TR:5792678</td>
      <td>Fly Me To The Moon</td>
      <td>Fly Me To The Moon</td>
      <td>148.0</td>
      <td>29.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '90693f', 'thorId': 'images/...</td>
      <td>{'hasInteractive': True, 'hasOffline': False, ...</td>
      <td>AL:668431</td>
      <td>AR:135252</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>26</th>
      <td>TR:71794</td>
      <td>Piano Man</td>
      <td>Piano Man</td>
      <td>337.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '212121', 'thorId': 'images/...</td>
      <td>{'hasInteractive': True, 'hasOffline': False, ...</td>
      <td>AL:5719</td>
      <td>AR:3215</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>27</th>
      <td>TR:9902220</td>
      <td>Misty</td>
      <td>Misty</td>
      <td>173.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '454b54', 'thorId': 'images/...</td>
      <td>{'hasInteractive': True, 'hasOffline': False, ...</td>
      <td>AL:1046111</td>
      <td>AR:106698</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>



Now we have all the information we needed. Let’s merge these DataFrames:


```python
df=df_tracks.merge(df_info, left_on='trackPandoraId', right_on='trackPandoraId').sort_values(by=['itemId'])
df.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>addedTimestamp</th>
      <th>duration_x</th>
      <th>itemId</th>
      <th>trackPandoraId</th>
      <th>name</th>
      <th>sortableName</th>
      <th>duration_y</th>
      <th>trackNumber</th>
      <th>volumeNumber</th>
      <th>icon</th>
      <th>...</th>
      <th>twitterHandle</th>
      <th>collaboration</th>
      <th>primaryArtists</th>
      <th>variousArtist</th>
      <th>listenerId</th>
      <th>webname</th>
      <th>displayname</th>
      <th>releaseDate</th>
      <th>isCompilation</th>
      <th>tracks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1564722184825</td>
      <td>337</td>
      <td>1</td>
      <td>TR:71794</td>
      <td>Piano Man</td>
      <td>Piano Man</td>
      <td>337.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '212121', 'thorId': 'images/...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1564722203547</td>
      <td>229</td>
      <td>2</td>
      <td>TR:11053912</td>
      <td>Candle In The Wind (Remastered)</td>
      <td>Candle In The Wind (Remastered)</td>
      <td>229.0</td>
      <td>9.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '000c5d', 'thorId': 'images/...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1564722203547</td>
      <td>191</td>
      <td>3</td>
      <td>TR:30999</td>
      <td>Lights</td>
      <td>Lights</td>
      <td>191.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>{'dominantColor': '812433', 'thorId': 'images/...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1564722203547</td>
      <td>165</td>
      <td>4</td>
      <td>TR:13247705</td>
      <td>With A Little Help From My Friends (Remix)</td>
      <td>With A Little Help From My Friends (Remix)</td>
      <td>165.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>{'dominantColor': 'e7c051', 'thorId': 'images/...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1564722203547</td>
      <td>221</td>
      <td>5</td>
      <td>TR:5593489</td>
      <td>She's Always A Woman (Live)</td>
      <td>She's Always A Woman (Live)</td>
      <td>221.0</td>
      <td>21.0</td>
      <td>1.0</td>
      <td>{'dominantColor': 'd8152d', 'thorId': 'images/...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 36 columns</p>
</div>



Simply, use __*groupby*__ function to display how many duplicates are in this playlist:


```python
df[['name','artistName','itemId']].groupby(['name','artistName']).count().sort_values(by='itemId', ascending=False)
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>itemId</th>
    </tr>
    <tr>
      <th>name</th>
      <th>artistName</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Faithfully</th>
      <th>Journey</th>
      <td>5</td>
    </tr>
    <tr>
      <th>Fly Me To The Moon</th>
      <th>Frank Sinatra</th>
      <td>3</td>
    </tr>
    <tr>
      <th>Man In The Mirror</th>
      <th>Michael Jackson</th>
      <td>3</td>
    </tr>
    <tr>
      <th>Misty</th>
      <th>Ella Fitzgerald</th>
      <td>3</td>
    </tr>
    <tr>
      <th>Candle In The Wind (Remastered)</th>
      <th>Elton John</th>
      <td>1</td>
    </tr>
    <tr>
      <th>Don't Let The Sun Go Down On Me</th>
      <th>Elton John</th>
      <td>1</td>
    </tr>
    <tr>
      <th>Lights</th>
      <th>Journey</th>
      <td>1</td>
    </tr>
    <tr>
      <th>Piano Man</th>
      <th>Billy Joel</th>
      <td>1</td>
    </tr>
    <tr>
      <th>She's Always A Woman (Live)</th>
      <th>Billy Joel</th>
      <td>1</td>
    </tr>
    <tr>
      <th>With A Little Help From My Friends (Remix)</th>
      <th>The Beatles</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Use __*duplicated*__ function to see where the duplicate songs are located in the playlist ('True' means duplicate):


```python
df['duplicated']=df.duplicated(subset='name')
df[['name','duplicated']]
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>duplicated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Piano Man</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Candle In The Wind (Remastered)</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Lights</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>With A Little Help From My Friends (Remix)</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>She's Always A Woman (Live)</td>
      <td>False</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Don't Let The Sun Go Down On Me</td>
      <td>False</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Misty</td>
      <td>False</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Misty</td>
      <td>True</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Misty</td>
      <td>True</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Fly Me To The Moon</td>
      <td>False</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Fly Me To The Moon</td>
      <td>True</td>
    </tr>

  </tbody>
</table>
</div>



Entire code of function is shown below:
```python
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
```

![](static/pandora_dup_demo.gif)