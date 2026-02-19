import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data
headlines_df = pd.read_csv("./Article_Links/Pre-Crash_Articles.csv")

# Combine all text into one string
text = ' '.join(headlines_df['Title'].tolist())

# Generate the word cloud
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    max_words=200,
    stopwords=None,  # Uses built-in stopwords by default
    collocations=False  # Avoids repeating word pairs
).generate(text)

# Display
plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Pre-Crash Headlines')
plt.tight_layout()
plt.savefig('./Outputs/PreCrash Wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()