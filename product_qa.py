
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load product dataset
products = pd.read_csv("data/cleaned_products.csv")

# Prepare product information
products = products.fillna("")

products["details"] = (
    products.astype(str).agg(" ".join, axis=1)
)

# Create vectors
vectorizer = TfidfVectorizer()
product_vectors = vectorizer.fit_transform(products["details"])


def answer_question(question):
    query_vector = vectorizer.transform([question])

    scores = cosine_similarity(
        query_vector, product_vectors
    )[0]

    best_match = scores.argmax()

    if scores[best_match] < 0.1:
        return "Sorry, no relevant product information found."

    product = products.iloc[best_match]

    return (
        f"Product: {product.get('ProductName', 'N/A')}\n"
        f"Category: {product.get('Category', 'N/A')}\n"
        f"Brand: {product.get('Brand', 'N/A')}\n"
        f"Price: {product.get('Price', 'N/A')}\n"
        f"Description: {product.get('Description', 'Not available')}"
    )


# Terminal testing
if __name__ == "__main__":
    while True:
        question = input(
            "Ask about a product (type exit to stop): "
        )

        if question.lower() == "exit":
            break

        print("\nChatbot:", answer_question(question))
