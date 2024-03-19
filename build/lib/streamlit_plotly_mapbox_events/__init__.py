import os
import streamlit.components.v1 as components
import warnings

from json import loads

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "scattermap_events",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_plotly_mapbox_events", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def plotly_mapbox_events(
    plot_fig,
    click_event=True,
    select_event=False,
    hover_event=False,
    relayout_event=False,
    override_height=450,
    override_width="100%",
    key=None,
):
    """Create a new instance of "plotly_mapbox_events".

    Parameters
    ----------
    plot_fig: Plotly Figure
        Plotly figure that we want to render in Streamlit
    click_event: boolean, default: True
        Watch for click events on plot and return point data when triggered
    select_event: boolean, default: False
        Watch for select events on plot and return point data when triggered
    hover_event: boolean, default: False
        Watch for hover events on plot and return point data when triggered
    relayout_event: boolean, default: False
        Watch for relayout events and returns the raw data and lat,lon,zoom
    override_height: int, default: 450
        Integer to override component height.  Defaults to 450 (px)
    override_width: string, default: '100%'
        String (or integer) to override width.  Defaults to 100% (whole width of iframe)
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    tuple consisting of list or dictionary

        events will be returned ordered
            1. Click Event
            2. Select Event
            3. Hover Event
            4. Relayout Event

        For selected, click and hoverevents:
        List of dictionaries containing marker details (in case multiple overlapping
        marker have been clicked/selected/hovereed).

        Details can be found here:
            https://plotly.com/javascript/plotlyjs-events/#event-data

        Format of dict:
            {
                lat: int (lat value of point),
                lon: int (lon value of point),
                pointNumber: (index of selected point),
                pointIndex: (index of selected point)
            }

        For relayout event

        Only a dictionary will be returned

        Format of dict:
            {
                raw: containing the raw information about the relayout event
                lat: new lat position
                lon: new lon position
                zoom: new zoom level
            }
    """
    if relayout_event:
        warnings.warn(
            "The 'relayout_event' parameter is deprecated and will have no effect. "
            "Relayout events have been removed due to interferences with Streamlit.",
            DeprecationWarning,
        )
    # kwargs will be exposed to frontend in "args"
    component_value = _component_func(
        plot_obj=plot_fig.to_json(),
        override_height=override_height,
        override_width=override_width,
        key=key,
        click_event=click_event,
        select_event=select_event,
        hover_event=hover_event,
        relayout_event=relayout_event,
        default="[]",  # Default return empty JSON list
    )

    # Parse component_value since it's JSON and return to Streamlit
    events = loads(component_value)
    if not events:
        return [], [], [], []
    return tuple(loads(component_value))

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run src/streamlit_plotly_events/__init__.py`
if not _RELEASE:
    import streamlit as st
    import plotly.express as px
    import pandas as pd
    
    st.set_page_config(layout="wide")

    if 'Plotly Mapbox' not in st.session_state:
        df = pd.DataFrame({'lat': {0: 49.058, 1: 50.383, 2: 49.599000000000004, 3: 50.677, 4: 53.036, 5: 50.541, 6: 51.524,
                        7: 54.992, 8: 49.88},
                'lon': {0: 11.115, 1: 12.528, 2: 11.231, 3: 10.408, 4: 8.185, 5: 8.055, 6: 7.638999999999999,
                        7: 11.636, 8: 7.678}, 'hover': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9},
                'color_1': {0: 3, 1: 3, 2: 4, 3: 3, 4: 5, 5: 5, 6: 5, 7: 4, 8: 2},
                'color_2': {0: 5, 1: 5, 2: 3, 3: 1, 4: 1, 5: 2, 6: 5, 7: 2, 8: 2}, 'color_3':
                    {0: 3, 1: 2, 2: 1, 3: 5, 4: 3, 5: 2, 6: 5, 7: 2, 8: 2}})


        mapbox = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="hover", zoom=5.5, height=600)

        mapbox.update_layout(mapbox_style="carto-positron")
        mapbox.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        st.session_state['Plotly Mapbox'] = mapbox

    mapbox_events = plotly_mapbox_events(st.session_state['Plotly Mapbox'],click_event=True,select_event=True,hover_event=True, override_height=600)

    plot_name_holder_clicked = st.empty()
    plot_name_holder_selected = st.empty()
    plot_name_holder_hovered = st.empty()

    plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
    plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
    plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")