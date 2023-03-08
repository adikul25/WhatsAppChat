import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS


def whatsapp_parser16(text):
    # Split the text into messages
    messages = text.split('\n')

    # Create empty lists to store the data
    dates = []
    times = []
    authors = []
    messages_list = []

    # Loop through the messages
    for message in messages:
        # Split the message into date, time, author, and message
        try:
            datetime, text = message.split(' - ')
            date, time = datetime.split(', ')
            author, message = text.split(': ', 1)
        except ValueError:
            continue

        # Append the data to the lists
        dates.append(date)
        times.append(time)
        authors.append(author)
        messages_list.append(message)

    # Create a dictionary with the data
    data = {
        'date': dates,
        'time': times,
        'author': authors,
        'message': messages_list
    }

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(data)

    # Return the DataFrame
    return df

def generate_wordcloud(author_messages):
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = set(STOPWORDS),
                min_font_size = 10).generate(author_messages)
    return wordcloud

def main():
    st.title("WhatsApp Chat Parser")

    # Upload file
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])

    if uploaded_file is not None:
        # Read file contents
        text = uploaded_file.read().decode("utf-8")

        # Parse the text and get the DataFrame
        df = whatsapp_parser16(text)
        df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

        # Display the DataFrame
        st.write(df.head(10))


        options = ['Total messages', 'Media messages', 'Links shared', 'Most active hours', 'Most active days', 'Author value counts', 'Media messages by author', 'Message count by Date', 'wordcloud']
        selected_options = st.multiselect('Select analytics to display', options)

        if 'Total messages' in selected_options:
            total_messages = df.shape[0]
            st.write('Total messages:', total_messages)


        if 'Media messages' in selected_options:
            media_messages = df[df['message'] == '<Media omitted>'].shape[0]
            st.write('Media messages:', media_messages)

        if 'Links shared' in selected_options:
            links_regex = r'http\S+|www\S+'
            links = df['message'].str.findall(links_regex).sum()
            links_count = len(links)
            st.write('Links shared:', links_count)

        if 'Most active hours' in selected_options:
            df['Hour'] = pd.to_datetime(df['time']).dt.hour
            active_hours = df.groupby('Hour').size().reset_index(name='Counts')
            st.write('Most active hours:')
            st.bar_chart(active_hours)

        # if 'Most active days' in selected_options:
        #          df['Day'] = df['date'].dt.day_name()
        #          active_days = df.groupby('Day').size().reset_index(name='Counts')
        #          st.write('Most active days:')
        #          st.bar_chart(active_days)

        if 'Author value counts' in selected_options:
                author_value_counts = df['author'].value_counts()
                st.write('Author value counts:')
                st.bar_chart(author_value_counts)

        if 'Media messages by author' in selected_options:
            media_messages_by_author = df[df['message'] == '<Media omitted>']['author'].value_counts()
            sns.set_style("darkgrid")

            # Create the bar chart with Seaborn
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x=media_messages_by_author.index, y=media_messages_by_author.values, ax=ax)
            plt.xticks(rotation=270)
            ax.set_title("Media messages by author")
            ax.set_xlabel("Author")
            ax.set_ylabel("Count")

            # Show the plot using Streamlit
            st.pyplot(fig)

        if "Message count by Date" in selected_options:
            date_df = df.groupby('date')
            Message_count = date_df['message'].count()
            df_Message_count = pd.DataFrame(Message_count)
            df_Message_count.index = pd.to_datetime(df_Message_count.index, format = '%d/%m/%Y')
            df_Message_count = df_Message_count.sort_index()
            sns.set_style("whitegrid")
            plt.figure(figsize=(15,10))
            sns.lineplot(data=df_Message_count, x="date", y="message")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.xticks(rotation=270)
            plt.title("WhatsApp Message Count Over Time")
            plt.xlabel("Date")
            plt.ylabel("Message Count")
            st.pyplot()

            # Display the plot
            #st.pyplot(plt.gcf())

        if "wordcloud" in selected_options:
            authors = df["author"].unique()

            # Create a selectbox to choose the author
            selected_author = st.selectbox("Select an author:", authors)

            # Filter the DataFrame by the selected author
            author_df = df[df["author"] == selected_author]

            # Generate the word cloud
            author_messages = " ".join(author_df["message"])
            wordcloud = generate_wordcloud(author_messages)

            # Display the word cloud
            st.markdown(f"## Word cloud for {selected_author}")
            plt.imshow(wordcloud, interpolation='bilinear')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.axis("off")
            st.pyplot()


if __name__ == '__main__':
    main()
