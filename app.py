import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(music_title):
    """Fetch poster URL for a given music title."""
    try:
        response = requests.get(f"https://saavn.me/search/songs?query={music_title}&page=1&limit=2")
        data = response.json()
        # Ensure that 'data' and 'requests' keys exist in the response
        if 'data' in data and 'requests' in data['data'] and len(data['data']['requests']) > 0:
            return data['data']['requests'][0]['image'][2]['link']
        else:
            return None
    except Exception as e:
        return None

def recommend(selected_music_title):
    """Recommend similar music and fetch their posters."""
    # Ensure that selected_music_title is correctly used
    if selected_music_title not in music['title'].values:
        st.error("Selected music title is not in the dataset.")
        return [], []

    music_index = music[music['title'] == selected_music_title].index[0]
    distance = similarity[music_index]
    music_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_music = []
    recommend_music_poster = []
    
    for i in music_list:
        music_title = music.iloc[i[0]].title
        recommend_music.append(music_title)
        poster_url = fetch_poster(music_title)
        recommend_music_poster.append(poster_url)
    
    return recommend_music, recommend_music_poster

# Load data
try:
    music_dict = pickle.load(open("C:/Users/adity/Downloads/musicrec.pkl", 'rb'))
    music = pd.DataFrame(music_dict)

    similarity = pickle.load(open('C:/Users/adity/Downloads/similarities.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")

# Streamlit app
st.markdown("<h1 style='text-align: center; color: red;'>Muse on Tunes</h1>", unsafe_allow_html=True)

# Use selectbox instead of selectionbox
selected_music_name = st.selectbox('Select a music you like', music['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

    # Display recommendations and posters one by one
    for i in range(len(names)):
        st.write(f"### {names[i]}")
        if posters[i]:
            st.image(posters[i])
        else:
            # Provide a clickable link to YouTube if the poster is not available
            youtube_search_url = f"https://www.youtube.com/results?search_query={names[i]}"
            st.markdown(f"[Search on YouTube](<{youtube_search_url}>)")
        st.write("---")  # Add a blank line for separation
