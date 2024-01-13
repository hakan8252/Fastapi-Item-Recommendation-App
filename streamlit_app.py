import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

# Streamlit app UI
st.title("Recommender System App")

# Sidebar radio for navigation
page_selection = st.sidebar.radio("Select Page", ["Recommendation System", "Customer Segmentation"])

# Function to create sorted stacked bar chart with a different color scale
def create_custom_colored_stacked_bar_chart(y_axis):
    avg_y_values = df.groupby("segment")[y_axis].mean().reset_index()
    avg_y_values = avg_y_values.sort_values(by=y_axis, ascending=False)  # Sort by y-axis values
    
    # Use the 'darkmint' color scale, you can replace it with any other color scale
    fig = px.bar(avg_y_values, x="segment", y=y_axis, title=f'Custom Colored Stacked Bar Chart for {y_axis}', 
                 labels={"segment": "Segment", y_axis: f"Avg {y_axis}"}, color=y_axis, color_continuous_scale='darkmint')
    
    return fig

# Function to create pie chart for segment distribution
def create_pie_chart():
    segment_distribution = df['segment'].value_counts().reset_index()
    segment_distribution.columns = ['segment', 'count']
    fig = px.pie(segment_distribution, names='segment', values='count', title='Segment Distribution')
    return fig



# Streamlit app UI for the second page
if page_selection == "Recommendation System":
    # Input for item_id and number of recommendations
    item_id = st.number_input("Enter Item ID:", value=1, step=1)
    n_recommendations = st.number_input("Number of Recommendations:", value=3, step=1)

    # Button to trigger the recommendation
    if st.button("Get Recommendations"):
        # Make a request to the FastAPI endpoint
        response = requests.get(f"https://item-recommender-fastapi-app.streamlit.app/recommend/{item_id}?n_recommendation={n_recommendations}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                st.success(result)
            except json.decoder.JSONDecodeError:
                st.error(f"Response: {response}")
                st.error(f"Invalid JSON format in response. Content: {response.text}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")



# Streamlit app UI for the second page
if page_selection == "Customer Segmentation":
    # Assuming df is your DataFrame, replace it with your actual DataFrame
    df = pd.read_csv("app/rfm_df.csv")  # Replace with your actual file path
    # Subheader
    st.subheader("Dataframe")
    st.dataframe(df.head())

    # Dropdown to select y-axis
    selected_y_axis = st.selectbox("Select Y-Axis", ["recency_score", "frequency_score", "total_events", "total_purchases"])

    st.subheader("Bar Chart")
    # Display custom colored stacked bar chart for the average of the selected y-axis
    if selected_y_axis:
        st.plotly_chart(create_custom_colored_stacked_bar_chart(selected_y_axis))

    st.subheader("Pie Chart")
    # Display pie chart for segment distribution
    st.plotly_chart(create_pie_chart())
