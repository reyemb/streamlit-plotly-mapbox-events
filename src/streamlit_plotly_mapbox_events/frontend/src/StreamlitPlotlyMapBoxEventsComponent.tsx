import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Plot from 'react-plotly.js';

interface layout {
  raw: object,
  lat: number,
  lon: number,
  zoom: number,
}

class StreamlitPlotlyMapBoxEvents extends StreamlitComponentBase {
  private clickedElements: Array<any>
  private hoveredElements: Array<any>
  private selectedElements: Array<any>
  private relayoutinfo: Object
    constructor(props: any) {
      super(props)
      this.clickedElements = []
      this.hoveredElements = []
      this.selectedElements = []
      this.relayoutinfo = {}
    }
    render = (): ReactNode => {
    // Pull Plotly object from args and parse
    const plot_obj = JSON.parse(this.props.args["plot_obj"]);
    const override_height = this.props.args["override_height"];
    const override_width = this.props.args["override_width"];

    // Event booleans
    const click_event = this.props.args["click_event"];
    const select_event = this.props.args["select_event"];
    const hover_event = this.props.args["hover_event"];
    const relayout_event = this.props.args["relayout_event"]

    Streamlit.setFrameHeight(override_height);
    return (
      <Plot
        data={plot_obj.data}
        layout={plot_obj.layout}
        config={plot_obj.config}
        frames={plot_obj.frames}
        onClick={click_event ? this.plotlyClickHandler : function() { }}
        onSelected={select_event ? this.plotlySelectHandler : function() { }}
        onHover={hover_event ? this.plotlyHoverHandler : function() { }}
        onRelayout={relayout_event ? this.plotlyReLayoutEventHandler: function() { } }
        style={{ width: override_width, height: override_height }}
        className="stPlotlyChart"
      />
    )
  }
  /** send value back to python backend */
  private sendData() {
    const returnArr: Array<any> = []
    const arrayOfInterest: Array<any> = [
      [this.props.args["click_event"], this.clickedElements],
      [this.props.args["select_event"], this.selectedElements],
      [this.props.args["hover_event"], this.hoveredElements],
      [this.props.args["relayout_event"], this.relayoutinfo],
    ]
    arrayOfInterest.forEach(element => {
      if (element[0]) {
        returnArr.push(element[1])
      }
    });
    Streamlit.setComponentValue(JSON.stringify(returnArr))
  }
  private plotlySelectHandler = (data: any) => {
    this.selectedElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }
  private plotlyClickHandler = (data: any) => {
    this.clickedElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }
  private plotlyHoverHandler = (data: any) => {
    this.hoveredElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }

  /** Click handler for plot. */
  private plotlyMarkerHandler = (data: any) => {
    // Build array of points to return
    var marker: Array<any> = [];
    data.points.forEach(function (arrayItem: any) {
      marker.push({
        lat: arrayItem.lat,
        lon: arrayItem.lon,
        pointNumber: arrayItem.pointNumber,
        pointIndex: arrayItem.pointIndex
      })
    });
    return marker
  }

  /** Relayout Eventhandler */
  private plotlyReLayoutEventHandler = (data: any) => {
    // Build array of points to return
    if (data['mapbox.center']){
      const relayout: layout = {
        raw: data,
        lat: data['mapbox.center'].lat,
        lon: data['mapbox.center'].lon,
        zoom: data['mapbox.zoom'],
      }
      this.relayoutinfo = relayout
      this.sendData()
    }
  }
}

export default withStreamlitConnection(StreamlitPlotlyMapBoxEvents)
