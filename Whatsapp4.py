import pandas as pd
import streamlit as st

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

def main():
    st.title("WhatsApp Chat Parser")

    # Upload file
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])

    if uploaded_file is not None:
        # Read file contents
        text = uploaded_file.read().decode("utf-8")

        # Parse the text and get the DataFrame
        df = whatsapp_parser16(text)
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

        # Display the DataFrame
        st.write(df)


        options = ['Total messages', 'Media messages', 'Links shared', 'Most active hours', 'Most active days', 'Author value counts', 'Media messages by author']
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
        #         df['Day'] = df['date'].dt.day_name()
        #         active_days = df.groupby('Day').size().reset_index(name='Counts')
        #         st.write('Most active days:')
        #         st.bar_chart(active_days)

        if 'Author value counts' in selected_options:
                author_value_counts = df['author'].value_counts()
                st.write('Author value counts:')
                st.bar_chart(author_value_counts)

        if 'Media messages by author' in selected_options:
            media_messages_by_author = df[df['message'] == '<Media omitted>']['author'].value_counts()
            st.write('Media messages by author:')
            st.bar_chart(media_messages_by_author)

if __name__ == '__main__':
    main()
