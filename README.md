# WhatsApp Chat Parser

This Python script allows you to parse WhatsApp chat data from a text file and visualize various analytics using Streamlit.

## Installation

1. **Clone the repository:**
    ```
    git clone <repository_url>
    ```

2. **Install the required libraries:**
    ```
    pip install pandas streamlit matplotlib seaborn plotly wordcloud
    ```

3. **Run the script:**
    ```
    streamlit run whatsapp_chat_parser.py
    ```

## Usage

1. Choose a WhatsApp chat text file.
2. Upload the file using the file uploader.
3. Select the analytics to display from the available options.
4. Visualize the selected analytics.

## Functions

### `whatsapp_parser16(text)`

Parses the WhatsApp chat text and returns a pandas DataFrame containing date, time, author, and message columns.

### `generate_wordcloud(author_messages)`

Generates a word cloud from the messages of a specific author.

### `main()`

Main function to run the Streamlit application. It displays the uploaded chat data and various analytics options.

## Analytics Options

- **Total messages**: Displays the total number of messages in the chat.
- **Media messages**: Shows the count of media messages (images, videos, etc.).
- **Links shared**: Counts the number of shared links in the chat.
- **Most active hours**: Visualizes the distribution of messages over different hours of the day.
- **Author value counts**: Displays the count of messages sent by each author.
- **Media messages by author**: Shows the count of media messages sent by each author.
- **Message count by Date**: Displays the message count over time with a line plot.
- **Word cloud**: Generates a word cloud for the messages of a selected author.

## Example

To visualize the word cloud for a specific author, select the author from the dropdown list and view the generated word cloud.


