# Streamlit Plotly MapBox Events


![Example Image](https://github.com/reyemb/streamlit-plotly-mapbox-events/blob/main/example.gif)


## First things first

This Repository is heavily inspired my [Null Jones - Plotly Events](https://github.com/null-jones/streamlit-plotly-events)

Since it didn't cover scattermaps in a way I need. I decided to reuse her repository and fit it to the needs of a scattermap

### Installation

Install via Pip!

```pip install streamlit-plotly-mapbox-events```

### Usage

Import the component, and use it like any other Streamlit custom component!
```python
import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events
import plotly.express as px
import pandas as pd

# Create a sample dataframe
df = pd.DataFrame({
    'lat': [49.058, 50.383, 49.599, 50.677, 53.036, 50.541, 51.524, 54.992, 49.88],
    'lon': [11.115, 12.528, 11.231, 10.408, 8.185, 8.055, 7.639, 11.636, 7.678],
    'hover': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'color_1': [3, 3, 4, 3, 5, 5, 5, 4, 2],
    'color_2': [5, 5, 3, 1, 1, 2, 5, 2, 2],
    'color_3': [3, 2, 1, 5, 3, 2, 5, 2, 2]
})

# Create a Plotly Mapbox figure
mapbox = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="hover", zoom=5.5, height=600)
mapbox.update_layout(mapbox_style="carto-positron")
mapbox.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

# Create an instance of the plotly_mapbox_events component
mapbox_events = plotly_mapbox_events(
    mapbox,
    click_event=True,
    select_event=True,
    hover_event=True,
    override_height=600
)

# Display the captured events
plot_name_holder_clicked = st.empty()
plot_name_holder_selected = st.empty()
plot_name_holder_hovered = st.empty()

plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")
```

## Parameters
- plot_fig (Plotly Figure): Plotly figure that we want to render in Streamlit.
- click_event (boolean, default: True): Watch for click events on plot and return point data when triggered.
- select_event (boolean, default: False): Watch for select events on plot and return point data when triggered.
- hover_event (boolean, default: False): Watch for hover events on plot and return point data when triggered.
- override_height (int, default: 450): Integer to override component height. Defaults to 450 (px).
- override_width (string, default: '100%'): String (or integer) to override width. Defaults to 100% (whole width of iframe).
- key (str or None): An optional key that uniquely identifies this component. If this is None, and the component's arguments are changed, the component will be re-mounted in the Streamlit frontend and lose its current state.


## Return Value

A tuple consisting of lists or dictionaries for the captured events:

Click Event
Select Event
Hover Event
For selected, click, and hover events, a list of dictionaries containing marker details is returned (in case multiple overlapping markers have been clicked/selected/hovered). The dictionary format is as follows:
```python
{
    'lat': int (lat value of point),
    'lon': int (lon value of point),
    'pointNumber': (index of selected point),
    'pointIndex': (index of selected point)
}
```

## Events
Currently, a number of plotly events can be enabled.  They can be enabled/disabled using kwargs on the `plotly_event()` function.
- **Click** `click_event` (defaults to `True`): Triggers event on mouse click of marker
- **Select** `select_event`: Triggers event when markers have been selected
- **Hover** `hover_event`: Triggers event on mouse hover of marker
- **Relayout** `relayout_event`: Triggers if the layout has changed. Occurs on Zoom and Moving

## Deprecation Warning
The relayout_event parameter is deprecated and will have no effect. Relayout events have been removed due to interferences with Streamlit.