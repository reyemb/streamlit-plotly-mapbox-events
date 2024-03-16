from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-plotly-mapboxEvents",
    version="0.1.0",
    author="Reyemb",
    author_email="info@reyemb.io",
    description="A Streamlit component that integrates Plotly's interactive Mapbox visualizations, enabling bidirectional communication between the map and Streamlit. It allows for seamless rendering of Mapbox plots within Streamlit applications while supporting event handling, such as click, select, hover, and relayout events, to facilitate dynamic interactions and data updates.",
    long_description="The Plotly Mapbox component for Streamlit is a powerful tool that brings the rich functionality of Plotly's Mapbox visualizations to Streamlit applications. It provides a seamless integration between Plotly's interactive Mapbox plots and Streamlit's intuitive app development framework. With this component, you can effortlessly render Mapbox visualizations within your Streamlit app, enabling users to explore and interact with geospatial data in a highly engaging manner.\n\nOne of the key features of this component is its ability to handle various events triggered by user interactions with the Mapbox plot. It supports click, select, hover, and relayout events, allowing you to capture and respond to user actions in real-time. When an event occurs, such as clicking on a marker or selecting a region, the component communicates the event data back to Streamlit, enabling you to update other elements of your app or perform further data analysis based on the user's interactions.\n\nThe component offers flexibility in customizing the appearance and behavior of the Mapbox plot. You can easily control the plot's height, width, and initial zoom level to suit your app's layout and requirements. Additionally, you can enable or disable specific event types depending on your use case, giving you fine-grained control over the interactivity of the plot.\n\nBy leveraging the power of Plotly's Mapbox visualizations and the simplicity of Streamlit's app development framework, this component empowers you to create stunning and interactive geospatial applications with ease. Whether you're building dashboards, data exploration tools, or location-based services, the Plotly Mapbox component for Streamlit provides a seamless and efficient way to integrate interactive maps into your Streamlit apps, enhancing the user experience and facilitating data-driven decision-making.",
    long_description_content_type="text/plain",
    url="https://github.com/reyemb/streamlit-plotly-mapbox-events",
    package_dir={"": "streamlit-plotly-mapbox-events"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
        "plotly >= 4.14.3",
    ],
)