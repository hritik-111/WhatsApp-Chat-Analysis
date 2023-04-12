import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)
    #to extract users
    users_list=df['user'].unique().tolist()
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("show Analysis wrt",users_list)

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)
        num_message, words, num_media_msg,links = helper.fetch_stats(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media")
            st.title(num_media_msg)
        with col4:
            st.header("Links")
            st.title(links)

        #finding the busiest users in the group
        if selected_user == 'Overall':
            st.title('Busiest User')
            x, new_df =helper.busiest_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='yellow')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            
        #WordCloud
        st.title("Word Cloud")
        df_wc =helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

