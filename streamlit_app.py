import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import pickle

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


with open(f"recommendation_model.pkl", "rb") as f:
    model = joblib.load(f)

# Load the trainset from the file using pickle
with open("trainset", 'rb') as f:
    trainset = pickle.load(f)

def recommender_system(item_id, n_recommendation=3):
    try:
        # Find similar items based on the given item ID
        similar_items = model.get_neighbors(item_id, k=n_recommendation)  # Get top 3 similar items

        # Get the original item ID 
        original_item_id = trainset.to_raw_iid(item_id)
        # Convert the internal indices of similar items to original item IDs
        similar_item_ids = [trainset.to_raw_iid(similar_item) for similar_item in similar_items]

        result_message = f'Top {n_recommendation} Similar Items for Item {original_item_id}: {similar_item_ids}'
        st.write(result_message)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Streamlit app UI for the second page
if page_selection == "Recommendation System":
    # Input for item_id and number of recommendations
    item_id = st.number_input("Enter Item ID:", value=1, step=1)
    n_recommendations = st.number_input("Number of Recommendations:", value=3, step=1)

    # Button to trigger the recommendation
    if st.button("Get Recommendations"):
        # Make a request to the FastAPI endpoint
        recommender_system(item_id, n_recommendations)



# Streamlit app UI for the second page
if page_selection == "Customer Segmentation":
    # Assuming df is your DataFrame, replace it with your actual DataFrame
    df = pd.read_csv("rfm_df.csv")  # Replace with your actual file path
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
