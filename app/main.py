
from fastapi import FastAPI
# from model import recommender_system

app = FastAPI()

@app.get("/")
def health_check():
    # Add any additional checks for application health here
    # For simplicity, always return 200 OK for this example
    return {"status": "ok"}

# @app.get("/recommend/{item_id}")
# async def get_recommendations(item_id: int, n_recommendation: int = 1):
#     # Call your recommender_system function with the provided item ID and number of recommendations
#     recommendations = recommender_system(item_id, n_recommendation)
#     # Return the recommendations in the response
#     return {"item_id": item_id, "recommendations": recommendations}