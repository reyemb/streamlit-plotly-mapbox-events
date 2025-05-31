from pathlib import Path

import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit_plotly_mapbox_events",
    version="0.2.1",
    author="Reyemb",
    author_email="info@reyemb.io",
    description="A Streamlit component that integrates Plotly's interactive Mapbox visualizations, enabling bidirectional communication between the map and Streamlit. It allows for seamless rendering of Mapbox plots within Streamlit applications while supporting event handling, such as click, select, hover, and relayout events, to facilitate dynamic interactions and data updates.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 1.45.0",
        "plotly >=  6.1.2",
    ],
)