import streamlit as st


channel_id=str(st.text_input("ENTER CHANNEL ID harshini👉: "))
options = ['select option','show channel details','show video details','show comments']
with st.sidebar:
  selected = st.selectbox("Select table to show", options=options)
 
if selected==options[0]:
    None
 
if selected==options[1]:
    data=channel_table(channel_id)
    st.dataframe(data)
 
if selected==options[2]:
    data=video_tables(channel_id)
    st.dataframe(data)    
 
if selected==options[3]:
    data=comment_tables()
    st.dataframe(data)