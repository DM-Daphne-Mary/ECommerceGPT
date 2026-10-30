
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load FAQ dataset
faqs = pd.read_csv("data/cleaned_faqs.csv")

# Clean text columns
faqs["Question"] = faqs["Question"].fillna("").astype(str)
faqs["Answer"] = faqs["Answer"].fillna("").astype(str)

# Convert questions into vectors
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faqs["Question"])


def search_faq(user_question):
    question_vector = vectorizer.transform([user_question])

    scores = cosine_similarity(question_vector, faq_vectors)[0]

    best_match = scores.argmax()

    if scores[best_match] < 0.1:
        return "Sorry, I couldn't find a suitable answer."

    return faqs.iloc[best_match]["Answer"]


# Terminal testing
if __name__ == "__main__":
    while True:
        question = input("Ask your question (type exit to stop): ")

        if question.lower() == "exit":
            break

        print("Chatbot:", search_faq(question))
