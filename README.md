# Streamlit Plotly MapBox Events

![PyPI](https://img.shields.io/pypi/v/streamlit-plotly-mapbox-events)
![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-plotly-mapbox-events)

A Streamlit component that enables interactive event handling for Plotly mapbox scatter plots. Capture click, select, and hover events on map markers with ease.

![Example Image](https://github.com/reyemb/streamlit-plotly-mapbox-events/blob/main/example.gif)

## Overview

This component extends Plotly's mapbox functionality in Streamlit by providing real-time event capture for interactive map visualizations. Perfect for building interactive dashboards with geographic data.

**Inspired by:** [Null Jones - Plotly Events](https://github.com/null-jones/streamlit-plotly-events)

## Installation

```bash
pip install streamlit-plotly-mapbox-events
```

## Quick Start

```python
import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events
import plotly.express as px
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'lat': [49.058, 50.383, 49.599, 50.677, 53.036, 50.541, 51.524, 54.992, 49.88],
    'lon': [11.115, 12.528, 11.231, 10.408, 8.185, 8.055, 7.639, 11.636, 7.678],
    'city': ['Munich', 'Dresden', 'Nuremberg', 'Göttingen', 'Bremen', 'Cologne', 'Düsseldorf', 'Hamburg', 'Dortmund'],
    'population': [1500000, 550000, 520000, 120000, 570000, 1080000, 620000, 1900000, 590000]
})

# Create mapbox figure
fig = px.scatter_map(
    df, 
    lat="lat", 
    lon="lon", 
    hover_name="city",
    hover_data={"population": True},
    zoom=5.5, 
    height=600
)
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

# Add interactive events
mapbox_events = plotly_mapbox_events(
    fig,
    click_event=True,
    select_event=True,
    hover_event=True,
    override_height=600
)

# Display captured events
if mapbox_events[0]:  # Click events
    st.write("**Clicked Point:**", mapbox_events[0])
if mapbox_events[1]:  # Select events
    st.write("**Selected Points:**", mapbox_events[1])
if mapbox_events[2]:  # Hover events
    st.write("**Hovered Point:**", mapbox_events[2])
```

## API Reference

### `plotly_mapbox_events()`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plot_fig` | `plotly.graph_objects.Figure` | Required | Plotly mapbox figure to render |
| `click_event` | `bool` | `True` | Enable click event capture |
| `select_event` | `bool` | `False` | Enable selection event capture |
| `hover_event` | `bool` | `False` | Enable hover event capture |
| `relayout_event` | `bool` | `False` | **DEPRECATED** - No longer functional |
| `override_height` | `int` | `450` | Component height in pixels |
| `override_width` | `str\|int` | `"100%"` | Component width |
| `key` | `str\|None` | `None` | Unique component identifier |

**Returns:**

A tuple containing four lists: `(click_events, select_events, hover_events, relayout_events)`

### Event Data Format

Each event returns a list of dictionaries with the following structure:

```python
{
    'lat': float,        # Latitude of the point
    'lon': float,        # Longitude of the point  
    'pointNumber': int,  # Index of the point in the data
    'pointIndex': int    # Same as pointNumber
}
```

## Event Types

### Click Events (`click_event=True`)
Triggered when a user clicks on a map marker. Returns data for the clicked point.

### Select Events (`select_event=True`) 
Triggered when markers are selected (e.g., using box/lasso select tools). Returns data for all selected points.

### Hover Events (`hover_event=True`)
Triggered when a user hovers over a map marker. Returns data for the hovered point.

### Relayout Events (**DEPRECATED**)
The `relayout_event` parameter is deprecated and non-functional due to interference with Streamlit's rendering cycle.

## Advanced Usage

### Handling Multiple Events

```python
# Capture all event types
click_data, select_data, hover_data, _ = plotly_mapbox_events(
    fig,
    click_event=True,
    select_event=True, 
    hover_event=True
)

# Process click events
if click_data:
    clicked_point = click_data[0]  # First clicked point
    st.info(f"Clicked: Lat {clicked_point['lat']}, Lon {clicked_point['lon']}")

# Process selection events  
if select_data:
    st.success(f"Selected {len(select_data)} points")
    for point in select_data:
        st.write(f"- Point {point['pointNumber']}: ({point['lat']}, {point['lon']})")
```

### Custom Styling

```python
# Create a styled mapbox
fig = px.scatter_mapbox(df, lat="lat", lon="lon", 
                       color="category", size="value",
                       hover_name="name")

# Custom mapbox style
fig.update_layout(
    mapbox_style="open-street-map",  # or "carto-positron", "carto-darkmatter", etc.
    mapbox=dict(center=dict(lat=50, lon=10), zoom=6),
    margin={"r":0, "t":0, "l":0, "b":0}
)

mapbox_events = plotly_mapbox_events(fig, override_height=700)
```

## Troubleshooting

**Events not triggering?**
- Ensure your Plotly figure is a mapbox scatter plot (`px.scatter_mapbox`)
- Check that the event parameters are set to `True`
- Verify your data has valid `lat` and `lon` columns

**Component not displaying?**
- Make sure you have the latest version installed
- Check that your Plotly figure renders correctly with `st.plotly_chart()` first

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to [Null Jones](https://github.com/null-jones/streamlit-plotly-events) for the original Plotly events component that inspired this mapbox-specific version.