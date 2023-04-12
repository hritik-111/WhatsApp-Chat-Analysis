from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    #total messages
    num_message = df.shape[0]
    #total words and fetch number of links shared
    words = []
    links=[]
    for message in df['message']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))

    #fetch number of media messages
    num_media_msg = df[df['message'] == '<Media omitted>'].shape[0]
    
    #fetch number of links
    return num_message, len(words),num_media_msg,len(links)

def busiest_user(df):
    x= df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc