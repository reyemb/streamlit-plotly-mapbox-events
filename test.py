import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_mapbox_events import plotly_mapbox_events


st.set_page_config(layout="wide")

if 'Plotly Mapbox' not in st.session_state:
    df = pd.DataFrame({'lat': {0: 49.058, 1: 50.383, 2: 49.599000000000004, 3: 50.677, 4: 53.036, 5: 50.541, 6: 51.524,
                               7: 54.992, 8: 49.88},
                       'lon': {0: 11.115, 1: 12.528, 2: 11.231, 3: 10.408, 4: 8.185, 5: 8.055, 6: 7.638999999999999,
                               7: 11.636, 8: 7.678}, 'hover': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9},
                       'color_1': {0: 3, 1: 3, 2: 4, 3: 3, 4: 5, 5: 5, 6: 5, 7: 4, 8: 2},
                       'color_2': {0: 5, 1: 5, 2: 3, 3: 1, 4: 1, 5: 2, 6: 5, 7: 2, 8: 2}, 'color_3':
                           {0: 3, 1: 2, 2: 1, 3: 5, 4: 3, 5: 2, 6: 5, 7: 2, 8: 2}})

    mapbox = px.scatter_map(df, lat="lat", lon="lon", hover_name="hover", zoom=5.5, height=600)

    mapbox.update_layout(mapbox_style="carto-positron")
    mapbox.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.session_state['Plotly Mapbox'] = mapbox

mapbox_events = plotly_mapbox_events(st.session_state['Plotly Mapbox'], click_event=True, select_event=True,
                                     hover_event=True, override_height=600)

plot_name_holder_clicked = st.empty()
plot_name_holder_selected = st.empty()
plot_name_holder_hovered = st.empty()

plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")