import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_mapbox_events import plotly_mapbox_events


st.set_page_config(layout="wide")

if 'Plotly Mapbox' not in st.session_state:
    d = {'lat' : [1,2,3,4],'lon' : [1,2,3,4]}
    df = pd.DataFrame(data = d)

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", zoom=3, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    st.session_state['Plotly Mapbox'] = fig

mapbox_events = plotly_mapbox_events(st.session_state['Plotly Mapbox'],click_event=True,select_event=True,hover_event=True, override_height=600)

plot_name_holder_clicked = st.empty()
plot_name_holder_selected = st.empty()
plot_name_holder_hovered = st.empty()

plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")