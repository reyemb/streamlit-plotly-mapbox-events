import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Plot from 'react-plotly.js';

interface State {
  numClicks: number
  isFocused: boolean
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class MyComponent extends StreamlitComponentBase<State> {
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

  public state = { numClicks: 0, isFocused: false }

  public render = (): ReactNode => {
    const plot_obj = JSON.parse(this.props.args["plot_obj"]);
    const override_width = this.props.args["override_width"];

    // Event booleans
    const click_event = this.props.args["click_event"];
    const select_event = this.props.args["select_event"];
    const hover_event = this.props.args["hover_event"];

    this.sendData()

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.state.isFocused ? theme.primaryColor : "gray"
      }`
      style.border = borderStyling
      style.outline = borderStyling
    }

    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    return (
      <Plot
        data={plot_obj.data}
        layout={plot_obj.layout}
        config={plot_obj.config}
        frames={plot_obj.frames}
        onClick={click_event ? this.plotlyClickHandler : function() { }}
        onSelected={select_event ? this.plotlySelectHandler : function() { }}
        onHover={hover_event ? this.plotlyHoverHandler : function() { }}
        style={{ width: override_width, height: this.props.args["override_height"] }}
        className="stPlotlyChart"
      />
    )
  }

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

  private plotlyClickHandler = (data: any) => {
    this.clickedElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }

  private plotlySelectHandler = (data: any) => {
    this.selectedElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }

  private plotlyHoverHandler = (data: any) => {
    this.hoveredElements = this.plotlyMarkerHandler(data)
    this.sendData()
  }

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

  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)