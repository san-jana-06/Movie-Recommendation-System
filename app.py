import streamlit as st
import pickle



movies=pickle.load(open('movies.pkl','rb'))

similarity=pickle.load(open('similarity.pkl','rb'))

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

# website
st.set_page_config(
page_title="Movie Recommendation System",
page_icon="🎬",
layout="wide"

)
st.markdown(
    "<h1 style='text-ali:centre;'>🎬Movie Recommendation System</h1>",
    unsafe_allow_html=True,
)

movie_list=movies['title'].values
selected_movie=st.selectbox("Select a movie",movie_list)

if st.button("Recommend"):
    recommendate=recommendation(selected_movie)
    for i in recommendate:
        st.write(i)

st.markdown("""
<style>
.stButton>button{
background-color:pink;
color:black;
border-radius:10px;
font-weight:25px;
margin-top:30px;
    }
.stButton>button:hover{
background-color:red;
color:black;
            }
</style>
""",unsafe_allow_html=True
)
movie_data=movies[movies['title']==selected_movie]

st.subheader("🎬 Movie Details")
st.write("🎭 genre:",movie_data.iloc[0]['genres'])
st.write(" 📝  overview:",movie_data.iloc[0]['overview'])
st.write("⭐ Rating:",movie_data.iloc[0]['vote_average'])
st.write("📅 Release:",movie_data.iloc[0]['release_date'])



            
        