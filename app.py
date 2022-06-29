#This app is for Movie-Tv prediction System
#User select a movie/tv and app shows 10 similar type of content
from flask import Flask ,render_template,request
from bs4 import BeautifulSoup
import requests
import pickle
import pandas as pd
app = Flask(__name__)
#momvie/tv dataframe
movieDf=pickle.load(open('movies.pkl','rb'))
movieList=movieDf['title'].values
#This is the similarity matrix which was created using cosine similarity of vectors
similarity=pickle.load(open('similarity.pkl','rb'))
#This is imdb dataset which have imdb id's which is used later to web scrapping the imdb ratings of the content
imdbData=pickle.load(open('imdbData.pkl','rb'))
#This is the final dataframe after merging cast and crew to movie/tv dataframe
finalData=pickle.load(open('finalData.pkl','rb'))

#This method get the recommendations from the similarity matrix
def recommend(movieName):
    recoList=[]
    content_index=movieDf[movieDf['title']==movieName].index[0]
    distances=similarity[content_index]
    #Getting the top 10 similar reccos
    content_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    #Appending the title of the reccos and returning back
    for i in content_list:
        recoList.append(movieDf.loc[i[0]].title)
    return recoList

#This method is for web scrapping and getting the imdb ratings of the content
#imdb id is passed and then we hit the url and scrap the page for ratings using Beautifulsoup
def getRatings(imdbid):
    response=requests.get('https://www.imdb.com/title/'+imdbid+'/ratings/?ref_=tt_ov_rt')
    htmlr=response.content
    soup = BeautifulSoup(htmlr,'html')
    soup_result = soup.find_all("div",{"class":"allText"})
    rating=0.0
    for i in soup_result:
        a=i.get_text()
        rating=(a[80:100])
        break
    return rating

@app.route("/",methods=['GET','POST'])
def home_page():
    #initial reccos list
    recoList=[]
    #final reccos list after fetching the poster using the api
    fRecoList=[]
    #this is the movie selected by user initially
    mr=''
    #this variable is to store the imdb id from the dataset
    idList=[]
    if request.method=='POST':
        mr=(request.form['title'])
        #getting the reccos
        recoList=recommend(mr)
        #iterating through the list to get the imdb id
        for i in recoList:
            df=imdbData.loc[imdbData[imdbData['title']==i].index]
            if df.shape[0]>0:
                imdbDict={'title':i,'imdbid':df.iloc[0].imdbid}
                idList.append(imdbDict)
            else:
                continue
        #Plz ignore these random variable names 
        #this list will have the ratings after web scrapping
        idFlist=[]
        idDf=pd.DataFrame(idList)
        #getting the ratings
        for i in idDf.imdbid:
            r=getRatings(i)
            r=r.strip()
            try:
                r=float(r[0:3])
            except:
                r=0.0
            idFdict={'rating':r}
            idFlist.append(idFdict)
        #converting rating list to dataframe 
        idFDf=pd.DataFrame(idFlist)
        #concating reccos df with rating list df 
        finalRatingDf=pd.concat([idDf,idFDf],axis=1)
        #Sorting based on ratings
        finalRatingDf.sort_values(by=['rating'],inplace=True,ascending=False)
        #After sorting, fetching movie/tv posters from api and sending that to index.html
        for i in finalRatingDf.title:
            posterDf=finalData.loc[finalData[finalData['title']==i].index]
            poster="https://image.tmdb.org/t/p/w500"+posterDf.iloc[0]['poster_path']
            fRecoList.append(poster)
        
    return render_template('index.html',movies=movieList,recoList=fRecoList,selectedMovie=mr)


if __name__=="__main__":
    app.run(debug=True)


