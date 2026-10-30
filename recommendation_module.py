
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import SnowballStemmer
import re

# Load product dataset
products = pd.read_csv("data/cleaned_products.csv").fillna("")

# Prepare product columns
columns = [
    col for col in products.columns
    if col.lower() in [
        "productname", "category", "brand", "description"
    ]
]

products["combined"] = (
    products[columns].astype(str).agg(" ".join, axis=1)
)

# Normalize words (Laptop and Laptops become similar)
stemmer = SnowballStemmer("english")

def tokenize(text):
    words = re.findall(r"\b[a-zA-Z]+\b", str(text).lower())
    return [stemmer.stem(word) for word in words]

# Create TF-IDF vectors
vectorizer = TfidfVectorizer(
    tokenizer=tokenize,
    token_pattern=None
)

product_vectors = vectorizer.fit_transform(
    products["combined"]
)


def recommend_products(user_input):
    query_vector = vectorizer.transform([user_input])

    scores = cosine_similarity(
        query_vector, product_vectors
    )[0]

    if scores.max() == 0:
        return products.iloc[0:0].copy()

    top_indices = scores.argsort()[::-1][:3]

    results = products.iloc[top_indices].copy()
    results["Similarity"] = scores[top_indices]

    return results[results["Similarity"] > 0]


if __name__ == "__main__":
    while True:
        user_input = input(
            "Search for a product (type exit to stop): "
        )

        if user_input.lower() == "exit":
            break

        results = recommend_products(user_input)

        if results.empty:
            print("No matching products found.")
        else:
            print(results[
                ["ProductName", "Category", "Brand", "Price"]
            ].to_string(index=False))
