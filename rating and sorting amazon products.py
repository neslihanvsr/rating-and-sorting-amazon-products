# Amazon products- rating and sorting reviews

import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv(r'C:\Users\amazon_review.csv')
df.head()
df.shape

#average rating of the product:
df['overall'].mean()

#weighted average score by date:

df['reviewTime'] = pd.to_datetime(df['reviewTime'])
df.info()
current_date = df['reviewTime'].max()
df["recency_rating_review"] = (current_date - df["reviewTime"]).dt.days
df["recency_rating_review"].describe().T

df.loc[df["recency_rating_review"] <= 30, "overall"].mean() + \
df.loc[(df["recency_rating_review"] > 30) & (df["recency_rating_review"] <= 90), "overall"].mean() + \
df.loc[(df["recency_rating_review"] > 90) & (df["recency_rating_review"] <= 180), "overall"].mean() + \
df.loc[df["recency_rating_review"] > 180, "overall"].mean()

def time_based_weighted_averege(dataframe,w1=29, w2=27, w3=23, w4=21):
    return df.loc[df["recency_rating_review"] <= 30, "overall"].mean()*w1/100 + \
           df.loc[(df["recency_rating_review"] > 30) & (df["recency_rating_review"] <= 90), "overall"].mean()*w2/100 + \
           df.loc[(df["recency_rating_review"] > 90) & (df["recency_rating_review"] <= 180), "overall"].mean()*w3/100 + \
           df.loc[df["recency_rating_review"] > 180, "overall"].mean()*w4/100

time_based_weighted_averege(df)


#specify 20 reviews for the product to be displayed on the product detail page:
df['helpful_no'] = df['total_vote'] - df['helpful_yes']
df.head()


#up-down diff score:
def score_up_down_diff(up, down):
    return up - down

score_up_down_diff(5, 2)


def score_pos_neg_diff(pos, neg):
    return pos - neg
score_up_down_diff(5, 2)

df["score_pos_neg_diff"] = score_pos_neg_diff(df["helpful_yes"], df["helpful_no"])
df.head()
df.tail()


#average rating score:
def score_average_rating(pos, neg):
    if pos + neg == 0:
        return 0
    return pos / (pos + neg)

score_average_rating(5, 2)

df["score_average_rating"] = score_pos_neg_diff(df["helpful_yes"], df["helpful_no"])
df.head()


#Wilson Lower Bound score:
def wilson_lower_bound(pos, neg, confidence=0.95):
    n = pos + neg
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * pos / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)
df.head()

df.sort_values("wilson_lower_bound", ascending=False).head(20)