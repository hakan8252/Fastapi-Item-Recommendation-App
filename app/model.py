import joblib
import pickle

with open(f"recommendation_model.pkl", "rb") as f:
    model = joblib.load(f)

# Load the trainset from the file using pickle
with open("trainset", 'rb') as f:
    trainset = pickle.load(f)


def recommender_system(item_id, n_recommendation = 3):
    # Find similar items based on the given item ID
    similar_items = model.get_neighbors(item_id, k=n_recommendation)  # Get top 3 similar items

    # Get the original item ID 
    original_item_id = trainset.to_raw_iid(item_id)
    # Convert the internal indices of similar items to original item IDs
    similar_item_ids = [trainset.to_raw_iid(similar_item) for similar_item in similar_items]

    print(f'Top {n_recommendation} Similar Items for Item {original_item_id}: {similar_item_ids}')
    return (f'Top {n_recommendation} Similar Items for Item {original_item_id}: {similar_item_ids}')
