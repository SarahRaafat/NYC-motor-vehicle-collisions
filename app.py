from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import pandas as pd
import os
import requests
from io import BytesIO

#Search works for sample: BROOKLYN Sedan Passing or Lane Usage Improper
#Search thar works for sample: MANHATTAN Station Wagon/Sport Utility Vehicle Following Too Closely

url = "https://drive.google.com/uc?export=download&id=1m8y0uC3mcWmBl5o2o4YXs2NGVLM7WEi7"
response = requests.get(url)
df_dashData = pd.read_csv(BytesIO(response.content))
#df_dashDataSample = pd.read_csv("data/dashboard_ready_sample.csv")

app = Dash(__name__) #creating the app
server = app.server

app.layout = dmc.MantineProvider(
    children = dmc.Container(
        fluid = True,
        style = {
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom right, #F5B7B1, #AED6F1, #A9DFBF)",  # muted pink → muted blue → muted green
            "padding": "20px"
        },
        children = [
            dmc.Title("NYC Motor Vehicle Collisions Dashboard", ta="center", c="teal", style={"marginTop": 20, "marginBottom": 20}),

    #dmc.Select is basically a dropdown menus so user would be able to filter the data accordingly
    dmc.Select(
        label = "Select a Year", data = [{"label": str(y), "value": str(y)}
            for y in sorted(df_dashData['CRASH_YEAR'].unique())], id = "Year-select"),
                
    dmc.Select(
        label = "Select a Borough", data = [{"label": str(b), "value": str(b)}
            for b in sorted(df_dashData['BOROUGH'].dropna().unique())], id = "Borough-select"),
                        
    dmc.Select(
        label = "Select Vechile Type", data = [{"label": str(s), "value": str(s)}
            for s in sorted(df_dashData['VEHICLE TYPE CODE 1'].dropna().unique())], id = "Vehicle-type-select"),

    dmc.Select(
        label = "Select Contributing Factor", data = [{"label": str(f), "value": str(f)}
            for f in sorted(df_dashData['CONTRIBUTING FACTOR VEHICLE 1'].dropna().unique())], id = "Contributing-factor-select"
    ),

    dmc.Select( 
        label = "Select Weekday", data = [{"label": str(w), "value": str(w)}
            for w in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]], id = "Weekday-select"
    ), 

    #dcc.input is basically a search bar where users can type in their queries
    html.H1("NYC Motor Vehicle Collisions Search", style = {"color": "#F3662EFF", "textAlign": "left"}),
    dcc.Input(id = "Search-input", type = "text", placeholder = "Search...", 
              style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "10px"}),
    html.Div(id = "Search-results"),

    dmc.Button("Generate Report", id = "Generate-report-button", color = "grape", style={"marginTop": "20px", "marginBottom": "20px"}),
    html.Div(id = "Visualization-results")])) #basically an area for the visualizations to be displayed

#the callaback function to update the visualizations based on given input otherwise it will remian static
#so when something changes it tells the app to run which certain function and update the output
@app.callback(
    Output("Visualization-results", "children"),
    [
        Input("Generate-report-button", "n_clicks"),
        Input("Search-input", "n_submit"),
    ],
    [
        State("Year-select", "value"),
        State("Borough-select", "value"),
        State("Vehicle-type-select", "value"),
        State("Contributing-factor-select", "value"),
        State("Weekday-select", "value"),
        State("Search-input", "value"),
    ],
    prevent_initial_call=True
)

#this is for the dropdown filters and search bar
def update_visualizations(n_clicks, n_submit, year, borough, vehicle_type, factor, weekday, search_text):
    if not n_clicks and not n_submit:
        raise PreventUpdate
    
    df = df_dashData.copy()

    #to make sure zip codes are strings
    df["ZIP CODE"] = (df["ZIP CODE"].astype(str).str.replace(".0", "", regex=False).fillna(""))
    df = df[df["ZIP CODE"].str.isdigit()]

    if year and "CRASH_YEAR" in df.columns:
        df["CRASH_YEAR"] = df["CRASH_YEAR"].astype(str).str.strip()
        df = df[df["CRASH_YEAR"] == str(year)]

    if borough and "BOROUGH" in df.columns:
        df["BOROUGH"] = df["BOROUGH"].astype(str).str.upper().str.strip()
        borough = borough.upper().strip()
        df = df[df["BOROUGH"] == borough]

    if vehicle_type and "VEHICLE TYPE CODE 1" in df.columns:
        df["VEHICLE TYPE CODE 1"] = df["VEHICLE TYPE CODE 1"].astype(str).str.upper().str.strip()
        vehicle_type = vehicle_type.upper().strip()
        df = df[df["VEHICLE TYPE CODE 1"] == vehicle_type]

    if factor and "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
        df["CONTRIBUTING FACTOR VEHICLE 1"] = df["CONTRIBUTING FACTOR VEHICLE 1"].astype(str).str.upper().str.strip()
        factor = factor.upper().strip()
        df = df[df["CONTRIBUTING FACTOR VEHICLE 1"] == factor]

    if weekday and "CRASH_WEEKDAY" in df.columns:
        df["CRASH_WEEKDAY"] = df["CRASH_WEEKDAY"].astype(str).str.capitalize().str.strip()
        weekday = weekday.capitalize().strip()
        df = df[df["CRASH_WEEKDAY"] == weekday]

    #we're doint it word word because in the search when you write "BRONX Sedan Driver Inexperience" it will bring up no data found
    #but if we split it into words and search for each word separately it will bring up the relevant data
    if search_text and search_text.strip():
        search_words = search_text.lower().strip().split()

        search_columns = [col for col in ["BOROUGH", "VEHICLE TYPE CODE 1", "CONTRIBUTING FACTOR VEHICLE 1"] if col in df.columns]

        for word in search_words:
            df = df[df[search_columns].fillna('').apply(lambda x: x.str.lower().str.contains(word)).any(axis = 1)]

    #for the visualizations based on the filtered data
    if df.empty:
        return html.Div([
        html.H3("No data matches the selected filters T_T", style={"color": "red"})
    ])

    #group by month and contributing factor
    line_data = (
        df.groupby(["CRASH_MONTH", "CONTRIBUTING FACTOR VEHICLE 1"])["NUMBER OF PERSONS INJURED"]
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        line_data,
        x="CRASH_MONTH",
        y="NUMBER OF PERSONS INJURED",
        color="CONTRIBUTING FACTOR VEHICLE 1",
        markers=True,
        title="Injuries Over the Year by Contributing Factor"
    )

    #set's layout
    fig_line.update_layout( 
        xaxis_title="Crash Month",
        yaxis_title="Number of Persons Injured",
        legend_title="Contributing Factor"
    )

    heatmap_data = df.groupby(["BOROUGH", "CRASH_MONTH"])["NUMBER OF PERSONS INJURED"].sum().reset_index()
    heatmap_data = heatmap_data.pivot(index = "BOROUGH", columns = "CRASH_MONTH", values = "NUMBER OF PERSONS INJURED").fillna(0)

    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Month", y="Borough", color="Number of Injured"),
        aspect="auto",
        color_continuous_scale='Oranges' 
)

    scatter_df = df.copy()

    fig_zip_scatter = px.scatter(
        scatter_df,
        x="ZIP CODE",
        y="NUMBER OF PERSONS INJURED",
        color="CONTRIBUTING FACTOR VEHICLE 1", #color when used here means each factor will have a different color
        size="NUMBER OF PERSONS INJURED",
        title="Injuries by ZIP Code and Contributing Factor",
        hover_data=["BOROUGH", "VEHICLE TYPE CODE 1"]
    )

    fig_zip_scatter.update_layout(
        xaxis_title="ZIP Code",
        yaxis_title="Number of Persons Injured",
        legend_title="Contributing Factor"
    )

    #this is basically so we wouldn't get a callback error if no coordinates are available    
    df = df.dropna(subset = ["LATITUDE","LONGITUDE"])
    if df.empty:
        return html.Div([
            html.H3("No mappable coordinates available for this filter.", style = {"color":"red"})
        ])

    fig_geomap = px.scatter_mapbox(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="NUMBER OF PERSONS INJURED",
        size="NUMBER OF PERSONS INJURED",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10,
        mapbox_style="carto-positron",
        title="Crash Locations by Number of Injuries"
    )

    hourly_data = (
        df.groupby(["CRASH_HOUR", "BOROUGH"])["NUMBER OF PERSONS INJURED"]
        .sum()
        .reset_index()
    )

    #making sure the hours are intergers not strings
    hourly_data["CRASH_HOUR"] = hourly_data["CRASH_HOUR"].astype(int)

    fig_hour_line = px.line(
        hourly_data,
        x="CRASH_HOUR",
        y="NUMBER OF PERSONS INJURED",
        color="BOROUGH",
        markers=True,
        title="Number of Injuries by Hour of Day (by Borough)"
    )

    fig_hour_line.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Number of Persons Injured",
        legend_title="Borough"
    )

    #return tne visualizatiosn that should be displayed on the dashboard
    return html.Div([
        dcc.Graph(figure=fig_line),
        dcc.Graph(figure=fig_heatmap),
        dcc.Graph(figure=fig_geomap),
        dcc.Graph(figure=fig_zip_scatter),
        dcc.Graph(figure=fig_hour_line)
    ])

#run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port, fallback to 5000
    app.run(host="0.0.0.0", port=port)      

#Searh1: BRONX Sedan Driver Inexperience
#Search2: QUEENS Bike Unsafe Speed
#Search3: BROOKLYN Sedan Passing or Lane Usage Improper
#Filter1: 2021, BRONX, Sedan, Driver Inexperince, Tuesday
#Filter2: 2021, MANHATTAN, Station Wagon/Sport Utility Vehicle, Following Too Closely, Saturday
#Filter3: 2022, QUEENS, Sedan, Unsafe Speed, Saturday
#If a second re-run happens without refreshing, dashboard may freeze/crash because the data is too large
#in addition that the search goes word by word because otherwise it's difficult to get results so yeah preferable to refresh
#ALSO if dropdown filters are chosen first then search won't work correctly unless we refresh

