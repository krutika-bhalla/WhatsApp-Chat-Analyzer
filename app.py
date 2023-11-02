import streamlit as st
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
# import plotly.figure_factory as ff
import plotly.express as px
import preprocess
import helper
# import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocess.preprocess(data)
    
    # unique users
    
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt ", user_list)
    
    
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages, words, media_messages = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
            
        with col2:
            st.header("Total Words")
            st.title(words)
            
        with col3:
            st.header("Media Shared")
            st.title(media_messages)
            
        # with col4:
        #     st.header("Links Shared")
        #     st.title(links)
        
        # finding busiest user in group (Group Level)
        
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig = go.Figure(data=[go.Scatter(x=timeline['time'], y=timeline['messages'], mode='lines', line=dict(color='green'))])
        fig.update_layout(
            xaxis_tickangle=-90 
        )
        st.plotly_chart(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = go.Figure(data=[go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['messages'], mode='lines', line=dict(color='blue'))])
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig = go.Figure(data=[go.Bar(x=busy_day.index, y=busy_day.values, marker_color='purple')])
            fig.update_layout(xaxis_tickangle=-90, width=300, height=400)  # Adjust width and height as needed
            st.plotly_chart(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = go.Figure(data=[go.Bar(x=busy_month.index, y=busy_month.values, marker_color='orange')])
            fig.update_layout(xaxis_tickangle=-90, width=300, height=400)  # Adjust width and height as needed
            st.plotly_chart(fig)


        # st.title("Weekly Activity Map")
        # user_heatmap = helper.activity_heatmap(selected_user,df)
        # fig = ff.create_annotated_heatmap(z=user_heatmap.values, x=user_heatmap.columns, y=user_heatmap.index)
        # st.plotly_chart(fig)

        
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.fetch_most_busy_users(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=x.index, y=x.values)
                ])
                
                # Customize the layout
                fig.update_layout(
                    # title="Most Busy Users",
                    xaxis_title="Users",
                    yaxis_title="Count",
                    xaxis_tickangle=-45,  # This will rotate x-axis labels
                    width=300,  # Adjust width
                    height=500,   # Adjust height
                    margin=dict(t=0, b=0, l=0, r=0)  # Adjust margins to reduce space
        )
                
                st.plotly_chart(fig)
                
            with col2:
                st.dataframe(new_df)
        
        
        # Word Cloud
        
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        
        fig = px.imshow(df_wc)

        fig.update_layout(
            width=700, 
            height=700,
            margin=dict(t=0, b=0, l=0, r=0)  
        )
        st.plotly_chart(fig)
        
            
        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig = go.Figure(data=[
            go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h')
        ])

        # Customize the layout
        fig.update_layout(
            # title="Most Common Words",
            xaxis_title="Count",
            yaxis_title="Words",
            xaxis_tickangle=-45,
            width=800, 
            height=600,
            margin=dict(t=0, b=0, l=0, r=0)
        )

        st.title("Most Common Words")
        st.plotly_chart(fig)
        
        # st.dataframe(most_common_df)
        
        # emoji analysis
        
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)

        with col2:
            blue_palette_lighter = [
            '#AEDFF7',
            '#72C7E7',
            '#5BB4D9',
            '#3A9ACD',
            '#1E7FBC',
            ]
            fig = go.Figure(data=[go.Pie(labels=emoji_df[0].head(), values=emoji_df[1].head(), textinfo='percent+label', hoverinfo='label+value', marker=dict(colors=blue_palette_lighter))])
            fig.update_traces(texttemplate='%{percent:.2f}')
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),  # Reduce margins
                width=400,  # Increase width
                height=500   # Increase height
            )
            st.plotly_chart(fig)
            