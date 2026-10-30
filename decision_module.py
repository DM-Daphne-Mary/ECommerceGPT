import pandas as pd

# Load datasets
products = pd.read_csv("data/cleaned_products.csv")
reviews = pd.read_csv("data/analyzed_reviews.csv")

# Calculate average rating for each product
ratings = reviews.groupby("ProductID")["Rating"].mean()

# Calculate positive review percentage
sentiments = reviews.groupby("ProductID")["Sentiment"].apply(
    lambda x: (x == "Positive").mean() * 100
)

# Combine product information
products["AverageRating"] = products["ProductID"].map(ratings)
products["PositiveReviews"] = products["ProductID"].map(sentiments)

products["AverageRating"] = products["AverageRating"].fillna(0)
products["PositiveReviews"] = products["PositiveReviews"].fillna(0)

# Decision-making function
def recommend_best_products():

    products["DecisionScore"] = (
        products["AverageRating"] * 20
        + products["PositiveReviews"] * 0.2
    )

    best_products = products.sort_values(
        by="DecisionScore", ascending=False
    ).head(5)

    print("\nTOP 5 RECOMMENDED PRODUCTS")
    print(
        best_products[
            ["ProductName", "Brand", "Price",
             "AverageRating", "PositiveReviews"]
        ].to_string(index=False)
    )

    best_products.to_csv(
        "data/best_products.csv", index=False
    )

    print("\nDecision making completed successfully!")


# Run the system
recommend_best_products()