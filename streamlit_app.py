import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit app UI
st.title("Recommender System App")

# Sidebar radio for navigation
page_selection = st.sidebar.radio("Select Page", ["Recommendation System", "Customer Segmentation"])

# Function to create sorted stacked bar chart with a different color scale
@st.cache_data
def create_custom_colored_stacked_bar_chart(y_axis, df):
    avg_y_values = df.groupby("segment")[y_axis].mean().reset_index()
    avg_y_values = avg_y_values.sort_values(by=y_axis, ascending=False)  # Sort by y-axis values
    
    # Use the 'darkmint' color scale, you can replace it with any other color scale
    fig = px.bar(avg_y_values, x="segment", y=y_axis, title=f'Custom Colored Stacked Bar Chart for {y_axis}', 
                 labels={"segment": "Segment", y_axis: f"Avg {y_axis}"}, color=y_axis, color_continuous_scale='darkmint')
    
    return fig

# Function to create pie chart for segment distribution
@st.cache_data
def create_pie_chart(df):
    segment_distribution = df['segment'].value_counts().reset_index()
    segment_distribution.columns = ['segment', 'count']
    fig = px.pie(segment_distribution, names='segment', values='count', title='Segment Distribution')
    return fig


# Streamlit app UI for the "Recommendation System" page
if page_selection == "Recommendation System":
    # Input for item_id and number of recommendations
    item_id = st.number_input("Enter Item ID:", value=1, step=1)

    # Validate that item_id is within the desired range
    if item_id > 745:
        st.error("Error: Item ID should be 745 or less.")
    else:
        n_recommendations = st.number_input("Number of Recommendations:", value=3, step=1)

        # Validate that the number of recommendations is within the desired range
        if n_recommendations > 10:
            st.error("Error: Number of Recommendations should be 10 or less.")
        else:
            # Button to trigger the recommendation
            if st.button("Get Recommendations"):
                # Make a request to the FastAPI endpoint
                response = requests.get(f"https://fastapi-item-recommendation-app-production.up.railway.app/recommend/{item_id}?n_recommendation={n_recommendations}")

                # Display the result
                if response.status_code == 200:
                    result = response.json()
                    st.success(result)
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
        st.plotly_chart(create_custom_colored_stacked_bar_chart(selected_y_axis, df))

    st.subheader("Pie Chart")
    # Display pie chart for segment distribution
    st.plotly_chart(create_pie_chart(df))
