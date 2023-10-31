# from urlextract import URLExtract
# extractor = URLExtract()
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    
        
    # fetch number of messages
    num_messages = df.shape[0]
        
    # fetch number of words
    words = []
    for m in df['messages']:
        words.extend(m.split())
        
        
    # fetch number of media messages
    media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]
    
    # fetch links
    # links = []
    # for m in df['message']:
    #     c = extractor.find_urls(m)
    #     links.extend(c)
    
    return num_messages, len(words), media_messages

def fetch_most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'users':'Name', 'count': 'Percent'})
    return x, df
    
# Wordcloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    stopwords = set(STOPWORDS)
    stopwords.update(["Media omitted", "media omitted", "Group_notifications", "group notifications","Media", "omitted"])
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=stopwords)
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    
    return df_wc
    

    
# words used most
def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    
    words = []
    for m in temp['messages']:
        for w in m.lower().split():
            if w not in stop_words:
                words.append(w)
                
                
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    emojis = []
    for m in df['messages']:
        emojis.extend([c for c in m if c in emoji.UNICODE_EMOJI['en']])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

# def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap