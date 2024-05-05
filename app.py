import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# title of page
st.set_page_config(layout="wide", page_title="UFC Winner Analysis")

# cache data
@st.cache_data
def load_data(csv_file):
    data = pd.read_csv(csv_file)
    data = data.dropna(subset=['Weight Class', 'Fighter Age', 'Fighter Stance'])
    data['Win'] = data['Win Count'].apply(lambda x: 1 if x == 1 else 0)
    return data

# Load the data
df = load_data('data/Joined-UFC.csv')

# Streamlit title
st.markdown("<h1 style='text-align: center; color: #31333f;'>Decoding the Anatomy of a UFC <span style='color: #b09424;'>Winner</span></h1>", unsafe_allow_html=True)

# Creating tabs
tab1, tab2, tab3 = st.tabs(["The Fights Themselves", "Age: The Goldilocks Zone", "The Dominance of the Orthodox Stance"])

# Establishing variables for plot background
plot_bgcolor = 'rgba(0,0,0,0)'
paper_bgcolor = 'rgba(211,211,211,1)'

# Sidebar for weight class selection
weight_classes = ['All'] + sorted(df['Weight Class'].unique().tolist())
selected_class = st.sidebar.selectbox('Select a Weight Class:', weight_classes)

# Filter function encapsulates the logic for filtering the dataframe
def filter_data(data, weight_class):
    return data if weight_class == 'All' else data[data['Weight Class'] == weight_class]

# Use the filter function to get the filtered dataframe
filtered_data = filter_data(df, selected_class)

# Function to create and sort a summary dataframe for plotting
def create_summary(dataframe, group_column, value_column):
    summary = dataframe.groupby(group_column)[value_column].sum().reset_index()
    return summary.sort_values(by=value_column, ascending=False)

# UFC logo on the bottom
def show_image_on_tab():
    image = Image.open('data/UFC.png')
    st.image(image, use_column_width='auto', clamp=True, channels="RGB", output_format="auto")

with tab1:
    st.markdown("""
    The majority of 2023's UFC fights are determined by decision, but removing this factor reveals that victories primarily occur via <span style='font-weight: bold; color: #b09424;'>KO/TKO</span>, particularly in the earlier rounds.
    Notably, the <span style='font-weight: bold; color: #b09424;'>5th round</span> holds a major advantage over the <span style='font-weight: bold; color: #b09424;'>4th</span>, in <span style='font-weight: bold; color: #b09424;'>Title Fights</span> specifically, potentially due to the urgency for a losing fighter to secure a KO before the match goes to decision but its more likely that the fighters dont knock each other out and the fight ends in a decision.
    """, unsafe_allow_html=True)

    win_summary = create_summary(filtered_data, 'Result', 'Win')
    fig1 = px.bar(win_summary, x='Result', y='Win', title=f"{selected_class} - Results Distribution",
                  text='Win', color='Win', 
                  color_continuous_scale=['#d80804', 'white', '#b09424'])
    fig1.update_layout(plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor, xaxis={'categoryorder':'total descending'}, showlegend=False)
    st.plotly_chart(fig1)

    # Only plot this on the first tab
    title_fight_data = filtered_data[filtered_data['Title Fight'] == True]
    round_summary = create_summary(title_fight_data, 'Finish Round', 'Win')
    fig2 = px.bar(round_summary, x='Finish Round', y='Win', title=f"{selected_class} - Title Fight Finish Round Distribution",
                  text='Win', color='Win', 
                  color_continuous_scale=['#d80804', 'white', '#b09424'])
    fig2.update_layout(plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor, 
                       xaxis={'categoryorder':'total descending'}, showlegend=False)
    st.plotly_chart(fig2)

    show_image_on_tab()

with tab2:
    st.markdown("""
Age is more than just a number in the UFC. A vivid picture of success clustered within a specific age range: <span style='color: #b09424; font-weight: bold;'>late 20s to early 30s.</span> Fighters in this <span style='color: #b09424; font-weight: bold;'>Goldilocks Zone</span> exhibit a blend of youthful vigor and seasoned experience, allowing them to navigate the rigors of the octagon with precision and poise.
""", unsafe_allow_html=True)
    age_summary = create_summary(filtered_data, 'Fighter Age', 'Win')
    fig3 = px.bar(age_summary, x='Fighter Age', y='Win', title=f"{selected_class} - Age Distribution",
                  text='Win', color='Win', 
                  color_continuous_scale=['#d80804', 'white', '#b09424'])
    fig3.update_layout(plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor, xaxis={'categoryorder':'total descending'}, showlegend=False)
    st.plotly_chart(fig3)
    show_image_on_tab()

with tab3:
    st.markdown("""
In the 2023 UFC sphere, the <span style='color: #b09424; font-weight: bold;'>orthodox stance</span> Fighters in this <span> is favored by winners, partly due to the prevalence of right-handed individuals who naturally align with this stance. With a majority of fighters being right-handed, the pool of potential <span style='color: #b09424; font-weight: bold;'>orthodox fighters</span> Fighters in this <span> expands, contributing to their dominance in the octagon.
""", unsafe_allow_html=True)

    stance_summary = create_summary(filtered_data, 'Fighter Stance', 'Win')
    fig4 = px.bar(stance_summary, x='Fighter Stance', y='Win', title=f"{selected_class} - Stance Distribution",
                  text='Win', color='Win', 
                  color_continuous_scale=['#d80804', 'white', '#b09424'])
    fig4.update_layout(plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor, xaxis={'categoryorder':'total descending'}, showlegend=False)
    st.plotly_chart(fig4)
    show_image_on_tab()
