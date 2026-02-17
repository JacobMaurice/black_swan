# Import libraries
import pandas as pd
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from tqdm import tqdm

# Load the model and tokenizer
print("Loading model and tokenizer...")
model = DistilBertForSequenceClassification.from_pretrained("./sentiment_model_custom")
tokenizer = DistilBertTokenizer.from_pretrained("./sentiment_model_custom")
label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}

# Set model to evaluation mode
model.eval()

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
print(f"Using device: {device}")

# Load the CSV file
print("\nLoading CSV file...")
precrash_sentiments_df = pd.read_csv('./Article_Links/Pre-Crash_Articles.csv')
print(f"Loaded {len(precrash_sentiments_df)} articles")

# Function to predict sentiment for a single title
def predict_sentiment(title):
    """
    Predict sentiment for a single title.
    Returns: (sentiment_label, confidence_score)
    """
    # Tokenize the title
    inputs = tokenizer(
        title,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )
    
    # Move inputs to device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    sentiment_label = label_map[predicted_class]
    return sentiment_label, confidence

# Apply sentiment analysis to all titles
print("\nAnalyzing sentiments...")
sentiments = []
confidences = []

for title in tqdm(precrash_sentiments_df['Title'], desc="Processing titles"):
    sentiment, confidence = predict_sentiment(title)
    sentiments.append(sentiment)
    confidences.append(confidence)

# Add results to dataframe
precrash_sentiments_df['Sentiment'] = sentiments
precrash_sentiments_df['Confidence'] = confidences

# Save results
output_path = './Outputs/PreCrash_Articles_with_sentiment.csv'
precrash_sentiments_df.to_csv(output_path, index=False)
print(f"\nResults saved to: {output_path}")

# Display summary statistics
print("\n" + "="*50)
print("SENTIMENT ANALYSIS SUMMARY")
print("="*50)
print(f"\nTotal articles analyzed: {len(precrash_sentiments_df)}")
print(f"\nSentiment distribution:")
print(precrash_sentiments_df['Sentiment'].value_counts())
print(f"\nSentiment percentages:")
print(precrash_sentiments_df['Sentiment'].value_counts(normalize=True) * 100)
print(f"\nAverage confidence: {precrash_sentiments_df['Confidence'].mean():.4f}")
print(f"Median confidence: {precrash_sentiments_df['Confidence'].median():.4f}")

# Show some examples
print("\n" + "="*50)
print("SAMPLE RESULTS")
print("="*50)
for sentiment in ['negative', 'neutral', 'positive']:
    print(f"\nExample {sentiment.upper()} titles:")
    examples = precrash_sentiments_df[precrash_sentiments_df['Sentiment'] == sentiment].head(3)
    for idx, row in examples.iterrows():
        print(f"  - {row['Title']} (confidence: {row['Confidence']:.3f})")