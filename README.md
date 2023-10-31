# WhatsApp Chat Analyzer

Analyze your WhatsApp chats with precision and gain insights into your conversations, both in groups and individual chats.

## 🌟 Features

- **Group and Individual Analysis**: Dive deep into both group chats and individual conversations.
- **Participant Analysis**: Get a detailed breakdown of each participant's activity in group chats.
- **Message Metrics**: View the total number of messages, words, and media shared.
- **Monthly Timeline**: Visualize the activity of participants with a line plot showcasing monthly activity.
- **Daily Activity**: Discover the most to least active days.
- **Activity Map**: Identify the busiest day and month of the year with intuitive bar plots.
- **Top User Analysis**: Find out the most active user with a clear bar plot representation.
- **Word Cloud**: Visualize the most commonly used words by each participant and overall in the chat.
- **Common Words**: Get a list of the most frequently used words.
- **Emoji Analysis**: Understand emoji usage patterns with a comprehensive pie chart.

## 🚀 How to Use

1. Export your WhatsApp chat from the app.
2. Upload the exported chat file to the "WhatsApp Chat Analyzer".
3. Wait for the analysis to complete and explore the insights!

## 🔧 Requirements

- A chat export from WhatsApp (`.txt` format).
- Go to a particular chat group or individual --> click on 3 dots at top right corner --> More --> Export Chat --> without using media.
- Ensure to exclude media.
- Use Python version 2.7 and install requirements.txt

## 🗺️ Instructions
- Run `streamlit run app.py`
- Upload the WhatsApp `.txt` file and hit Show Analysis.
- In case of group chats you'll find a dropdown that shows each participant, you can click on them for individual analysis.
