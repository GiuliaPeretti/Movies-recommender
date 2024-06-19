import pandas as pd
import numpy as np
import ast
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def remove_conmas(word):
    word=word.replace(",","")
    return(word)

def replace_space(word):
    l=[]
    for i in word:
        l.append(i.replace(" ", ""))
    return(l)

def get_list_word(word):
    l=[]
    word = ast.literal_eval(word)
    for w in word:
        l.append(w['name'])
    return(l)

def stems(text):
    l=[]
    for i in text.split():
        l.append(ps.stem(i))
    return(" ".join(l))

def recommend(movie, movies, similarity):
    index=movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
    for i in distances[1:6]:
        print(movies.iloc[i[0]].title)
    print(distances[:6])

def process_dataset():
    movies=pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')
    movies = movies.merge(credits, on='title')
    movies = pd.DataFrame(movies[['movie_id', 'title', 'overview','genres', 'keywords', 'cast','crew']])
    movies.dropna(inplace=True)
    return(movies)

def generate_similarity():
    movies=process_dataset()

    movies['overview'] = movies['overview'].apply(remove_conmas)
    movies['overview'] = movies['overview'].apply(lambda x:x.split(' '))
    movies['genres'] = movies['genres'].apply(get_list_word)
    movies['genres'] = movies['genres'].apply(replace_space)
    movies['keywords'] = movies['keywords'].apply(get_list_word)
    movies['keywords'] = movies['keywords'].apply(replace_space)
    movies['cast'] = movies['cast'].apply(get_list_word)
    movies['cast'] = movies['cast'].apply(replace_space)
    movies['crew'] = movies['crew'].apply(get_list_word)
    movies['crew'] = movies['crew'].apply(replace_space)

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    movies = movies.drop('overview', axis=1)
    movies = movies.drop('genres', axis=1)
    movies = movies.drop('keywords', axis=1)
    movies = movies.drop('cast', axis=1)
    movies = movies.drop('crew', axis=1)

    movies ['tags'] = movies ['tags'].apply(lambda x: " ".join(x))
    movies['tags'] = movies['tags'].apply(stems)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vector)
    np.savetxt("similarity.csv", similarity, delimiter=",")
    return(similarity)
    
# recommend("Pirates of the Caribbean: At World's End", movies, similarity)


similarity = np.genfromtxt('similarity.csv', delimiter=',')
movies=process_dataset()
recommend("Spider-Man", movies, similarity)