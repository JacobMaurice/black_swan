### Sentiment Analysis of the Coverage of Black Swan Events Compared to Current Day Discourse (WORK IN PROGRESS)
I’m curious to how financial institutions and pundits described the events leading to the 2008 financial crisis as they were happening compared to how they talked about them after the fact.

### 1. Gather Data
- Need articles leading up to and including the crash (roughly 2006-2008)
   - Currently have access to the NYT archive which has hundreds/thousands of relevant articles.
   - Articles were retrieved in a two step process; First, the links to relevant articles were stored in Article_Links/NYT_Article_Links.CSV, then the bodies of text were extracted as seen in Article_Bodies.
   - This method worked for some time and managed to extract over 2000 links but only 350 articles were successfully scraped the bodies of roughly 300 articles before getting blocked (woops).
 
To Do:
- Could also include some outlier sources of skeptics and the responses to them
- Need articles post-crash talking about the events and get opinions on why it happened and how it could have been prevented (if at all)
- Would be cool to keep track of the dates of the articles to see how sentiment changed over time.
  - Maybe highlight some keywords related to the sentiment of the markets for every month to see how it changes over time.
  - Also include one that shows article sentiment distribution (positive, neutral, negative) count for each month

### 2. Create Model
- Use [FinBERT](https://doi.org/10.48550/arXiv.1908.10063) as reference
- Try to recreate it using [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert#transformers.DistilBertConfig)
   - Pre-train DistilBERT on [unlabelled financial news](https://github.com/Kriyszig/financial-news-data) to create a finance-focused language model (SwanBERT)
   - Pre-train SwanBERT on labelled finance sentiment classification data ([Financial PhraseBank](https://huggingface.co/datasets/takala/financial_phrasebank))
     - Currently experimenting with custom training using methods from the FinBERT paper (SwanBERT_PhraseBank_Pretraining_Custom.ipynb)

### 3. Classify the Data
Once we have a working sentiment classification model, we need to actually use it on our data.

Considerations:
- As the name describes, Financial PhraseBank contains uses labelled phrases as training data.
- We could either use just the headlines of the articles (Pre-Crash_Headlines.csv) or the entire bodies of text.
   - I will likely use the headlines as they are more succinct and I have a larger sample size.
   - I may still use the bodies of the articles in the future for something else.

### Useful Links
- [Useful labelled corpus for arguing subjectivities and recognizing arguments](https://mpqa.cs.pitt.edu/corpora/arguing)
- [Financial Phrasebank - Labelled financial news dataset](https://huggingface.co/datasets/takala/financial_phrasebank)
