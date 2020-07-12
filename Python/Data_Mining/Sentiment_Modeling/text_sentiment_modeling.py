import pandas as pd

data = pd.read_csv('train.tsv', sep='\t')
data.head()
data.info()
print('\n', data.Sentiment.value_counts())

