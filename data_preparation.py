import pandas as pd

# Load datasets
products = pd.read_csv("data/products.csv")
faqs = pd.read_csv("data/faqs.csv")
reviews = pd.read_csv("data/reviews.csv")

# Remove duplicate records
products = products.drop_duplicates()
faqs = faqs.drop_duplicates()
reviews = reviews.drop_duplicates()

# Handle missing values
products = products.dropna()
faqs = faqs.dropna()
reviews = reviews.dropna()

# Save cleaned datasets
products.to_csv("data/cleaned_products.csv", index=False)
faqs.to_csv("data/cleaned_faqs.csv", index=False)
reviews.to_csv("data/cleaned_reviews.csv", index=False)

print("Data cleaning completed successfully!")

print("Products:", products.shape)
print("FAQs:", faqs.shape)
print("Reviews:", reviews.shape)