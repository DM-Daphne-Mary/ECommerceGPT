import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load review dataset
reviews = pd.read_csv("data/cleaned_reviews.csv")

# Create sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze customer reviews
def analyze_review(review):

    score = analyzer.polarity_scores(str(review))["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# Apply sentiment analysis
reviews["Sentiment"] = reviews["Review"].apply(analyze_review)

# Display results
print("CUSTOMER REVIEW ANALYSIS")
print(reviews[["ProductName", "Review", "Rating", "Sentiment"]].head(10))

# Sentiment summary
print("\nSENTIMENT SUMMARY")
print(reviews["Sentiment"].value_counts())

# Save results
reviews.to_csv("data/analyzed_reviews.csv", index=False)

print("\nReview analysis completed successfully!")