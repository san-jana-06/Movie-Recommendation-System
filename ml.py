import pandas as pd

import ast # dataset store in json like string so we apply this for convert in list form
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle # save python file and hepls to read in future


credits=pd.read_csv(r"\tmdb_5000_credits.csv") 
movies=pd.read_csv(r"tmdb_5000_movies.csv")
# preprocessing

# print(credits.head())
# print(movies.head())

# print(movies.columns.tolist())
# print(credits.columns.tolist())

movies=movies.merge(credits,on="title")
# print(movies.columns.tolist())

# required columns
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
# print(movies.head())

# ckeck missing values
print(movies.isnull().sum())
print(movies.dropna(inplace=True))

# ckeck dublicate
print(movies.duplicated().sum())
print(movies.drop_duplicates(inplace=True))

def convert(text):
    List=[]
    for i in ast.literal_eval(text):
        List.append(i['name'])
    return List
movies['genres']=movies["genres"].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)
# print(movies['keywords'])

def convert2(text):
    List=[]
    counter=0
    for i in ast.literal_eval(text):
        if counter<5:
            List.append(i["name"])
            counter+=1
        else:
            break
    return List
movies['cast']=movies['cast'].apply(convert2)
# print(movies['cast'].head())

def director(text):
    List=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            List.append(i["name"])
            break
    return List
movies['crew']=movies['crew'].apply(director)
# print(movies['crew'].head())

# # ckeck null is present or not
print(movies['overview'].isnull().sum())
# # remove missing value column
print(movies.dropna(subset=['overview'],inplace=True))
# # again check
print(movies['overview'].isnull().sum())

movies['overview']=movies['overview'].apply(lambda x:x.split())
# print(movies['overview'].head())


# print(movies['overview'].iloc[0])
# print(type(movies['overview'].iloc[0]))

# tag column
movies['tags']=(
    movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
)
# print(movies['tags'])
movies['tags']=movies['tags'].apply(lambda x:" ".join(x))
movies['tags']=movies['tags'].apply(lambda x:x.lower())
# print(type(movies['tags'].iloc[0]))
# CounterVectorizer ML can't understand text so it convert in numbers

cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(movies['tags']).toarray()
# print(vectors.shape)

# cosine similarity compare similar type 
similarity=cosine_similarity(vectors)
# print(similarity.shape)

# recommendation function
def recommendation(movie):
    movieRec=movies[movies['title']==movie].index[0]
    distance=similarity[movieRec]
    moviesList=sorted(list(enumerate(distance)),
                      reverse=True,
                      key=lambda x:x[1])[1:6]
    recommendated_movies=[]
    for i in moviesList:
        recommendated_movies.append(movies.iloc[i[0]].title)
    return recommendated_movies

# save file
pickle.dump(movies,open("movies.pkl","wb"))
pickle.dump(similarity,open("similarity.pkl","wb"))







