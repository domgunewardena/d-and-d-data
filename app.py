import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta

def Navbar():
    navbar = dbc.NavbarSimple(children=[dbc.NavItem(dbc.NavLink("Daily Sales", href="/daily-sales")),
                                        dbc.NavItem(dbc.NavLink("WTD Sales", href="/wtd-sales")),
                                        dbc.NavItem(dbc.NavLink("MTD Sales", href="/mtd-sales")),
                                        dbc.NavItem(dbc.NavLink("Weekly Sales", href="/weekly-sales")),
                                        dbc.NavItem(dbc.NavLink("Monthly Sales", href="/monthly-sales")),
                                        dbc.NavItem(dbc.NavLink("Cover Tracker", href="/tracker")),
                                        dbc.NavItem(dbc.NavLink("Beverage Sales Mix", href="/sales-mix"))],
                               brand="D&D Data",
                               brand_href="/",
                               sticky="top")
    return navbar

nav = Navbar()

home_page = html.Div(children=[html.Div([html.H1(children = 'D&D Data',
                                                 style={'textAlign':"center",
                                                        'borderBottom': 'thin lightgrey solid',
                                                        'borderRight': 'thin lightgrey solid',
                                                        'backgroundColor': "rgb(250,250,250)"})])])

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.FLATLY])
server = app.server
app.config.suppress_callback_exceptions = True

import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {'dandd':'london123'}

auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([dcc.Location(id='url', refresh=False),
                       html.Div([nav]),
                       html.Div(id='page-content')])

color_rev_ly = "powderblue"
color_rev_ty = "steelblue"
color_cov_ly = "lightgrey"
color_cov_ty = "darkslategrey"
color_spe_ly = "pink"
color_spe_ty = "mediumvioletred"

header_background_colour = "rgb(250,250,250)"
dropdown_background_colour = "rgb(250,250,250)"

dropdown_row_style = {'borderBottom': 'thin lightgrey solid',
                       'borderRight': 'thin lightgrey solid',
                      'backgroundColor': dropdown_background_colour,
                      'padding': '10px 5px'}


available_restaurants = ['100 Wardour Street', '20 Stories', 'Aster', 'Avenue',
                       'Bluebird Chelsea', 'Blueprint Café', 'Butlers Wharf Chophouse',
                       'Cantina', "Coq d'Argent", 'East 59th', 'Fiume',
                       'German Gymnasium', 'Issho', 'Launceston Place',
                       'Le Pont de la Tour', 'Madison', 'New Street Warehouse', 'Orrery',
                       'Paternoster Chophouse', 'Plateau', 'Quaglinos', 'Radici',
                       'Sartoria', 'Skylon', 'South Place Hotel', 'The Modern Pantry',
                       'Trinity', 'White City']

available_restaurants_week = ['Group', '100 Wardour Street', '20 Stories', 'Aster', 'Avenue',
                               'Bluebird Chelsea', 'Blueprint Café', 'Butlers Wharf Chophouse',
                               'Cantina', "Coq d'Argent", 'East 59th', 'Fiume',
                               'German Gymnasium', 'Issho', 'Launceston Place',
                               'Le Pont de la Tour', 'Madison', 'New Street Warehouse', 'Orrery',
                               'Paternoster Chophouse', 'Plateau', 'Quaglinos', 'Radici',
                               'Sartoria', 'Skylon', 'South Place Hotel', 'The Modern Pantry',
                               'Trinity', 'White City']

available_shifts = ['All Shifts', 'Lunch', 'Dinner']

available_measures = ['Revenue', 'Covers', 'Spend']

available_areas = ["Full Site",
                  "Restaurant",
                  "Bar",
                  "PDR",
                  "Events & Ex Hires",
                  "Retail & Other"]

available_types = ["Total",
                  "Food",
                  "Beverage",
                  "Wine",
                  "Non-Wine"]

plus = lambda i: ("+" if i > 0 else "") + str(i)

lastyear = str(date.today().year-1)
thisyear = str(date.today().year)

LY = str(date.today().year-1)
TY = str(date.today().year)

main_height = 900
main_width = 600

mini_height = 300
mini_width = 600 

week_height = 450
week_width = 900

outer_div_width = 600
outer_dropdown_width = outer_div_width - 10
inner_div_width = 600
inner_dropdown_width = inner_div_width - 10

week_div_width = 450
week_dropdown_width = week_div_width - 10

week_dropdown_style = {'textAlign':'center',
                      'display': 'inline-block',
                      'width':week_div_width}

def div_style_simple(width):
    return {'textAlign':'center',
              'display': 'inline-block',
              'width':width}

def small_graph(graph_id):
    return dcc.Graph(id=graph_id,
                     style={'height':mini_height,
                            'width':mini_width},
                     config={'displayModeBar':False})

def week_graph(graph_id):
    return dcc.Graph(id=graph_id,
                    style={'height':week_height,
                          'width':week_width},
                    config={'displayModeBar':False})

def site_annotation(restaurant):
    return {'x': 0, 'y': 1.1, 'xanchor': 'left', 'yanchor': 'bottom','xref': 'paper', 'yref': 'paper', 'showarrow': False,'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)','text': restaurant}

def totals_graph(dff,
                 xcolumn,
                color_ty,
                color_ly,
                hovertemplate,
                title,
                measure):

    x = dff[xcolumn]
    y_ly = dff[lastyear]
    y_ty = dff[thisyear]
    customdata = dff["% Change"]
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'

    max_value = (y_ly.append(y_ty)).max()
    y_limit = max_value*1.3

    data = [{'x': x,
             'y': y_ly,
              'type': 'bar',
              'name': lastyear,
              'marker':{'color':color_ly},
             'hovertemplate':hovertemplate},
             {'x': x,
              'y': y_ty,
              'customdata': customdata,
              'marker':{'color':color_ty},
              'type': 'bar',
              'name': thisyear,
             'hovertemplate':hovertemplate,
             'text': customdata,
              'textposition':textposition,
              'texttemplate':texttemplate}]

    layout = {'title': title,
             'yaxis':{'title':measure,
                      'range':[0,y_limit]}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
           'config': config} 

def change_graph(dff,
                xcolumn,
                hovertemplate,
                title,
                measure):

    x = dff[xcolumn]
    y = dff["Year Change"]
    customdata = dff["% Change"]
    colour = dff["Colour"]
    textposition = 'auto'
    texttemplate = '%{customdata:+.0f}%'

    max_change = (dff["Year Change"].append(dff["Year Change"]*-1)).max()
    y_limit = max_change*1.2

    data = [{'x': x,
              'y': y,
              'customdata': customdata,
              'type': 'bar',
              'name': "vs. Last Year",
              'marker': {'color': colour},
             'text': customdata,
              'textposition':textposition,
              'texttemplate':texttemplate,
             'hovertemplate':hovertemplate}]

    layout = {'title': title,
              'yaxis':{'title':measure + ' vs. LY'}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
           'config': config}    


def create_sales_change(dff, 
                       title, 
                       template):

    x = dff["Year Change"]
    y = dff["SiteName"]
    customdata = dff["% Change"]
    colour = dff["Colour"]
    textposition = 'auto'
    texttemplate = '%{customdata:+.0f}%'

    max_change = (dff["Year Change"].append(dff["Year Change"]*-1)).max()
    x_limit = max_change*1.2

    data = [{'x': x,
              'y': y,
              'customdata': customdata,
              'type': 'bar',
              'name': "vs. Last Year",
             'orientation':'h',
              'marker': {'color': colour},
             'text': customdata,
              'textposition':textposition,
              'texttemplate':texttemplate,
             'hovertemplate':template}]

    layout = {'title': title,
               'height':900,
               'width':'49%',
               'yaxis':{'automargin':True},
              'xaxis':{'side':'top',
                       'range':[-x_limit, x_limit]}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
           'config': config} 


def create_sales_totals(dff, 
                       title,
                       template,
                       color_ly,
                       color_ty):

    x_ty = dff[thisyear]
    x_ly = dff[lastyear]
    y = dff["SiteName"]
    customdata_ty = (dff[thisyear]/1000)
    customdata_ly = (dff[lastyear]/1000)
    textposition = 'auto'
    texttemplate = '%{customdata:+.0f}%'

    data = [{'x': x_ty,
              'y': y,
              'customdata': customdata_ty,
              'type': 'bar',
              'name': thisyear,
              'orientation':'h',
              'marker': {'color': color_ty},
              'hovertemplate':template,
             'text':customdata_ty,
             'textposition':'textposition',
             'texttemplate':template},
             {'x': x_ly,
              'y': y,
              'customdata': customdata_ly,
              'type': 'bar',
              'name': lastyear,
              'orientation':'h',
              'marker': {'color': color_ly},
              'hovertemplate':template,
             'text':customdata_ly,
             'textposition':'textposition',
             'texttemplate':template}]

    layout = {'title': title,
              'showlegend':True,
               'height':900,
               'width':'49%',
               'yaxis':{'automargin':True},
              'xaxis':{'side':'top'}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
            'config': config}


def week_totals(dff,
                y_ly,
                y_ty,
                customdata,
                hovertemplate,
               title,
               measure):

    x = dff["DaySession"]
    colour_ly = dff["Colour_LY"]
    colour_ty = dff["Colour_TY"]
    textposition = 'auto'
    texttemplate = '%{customdata:+.0f}%'

    data = [{'x': x,
              'y': y_ly,
              'type': 'bar',
              'name': lastyear,
              'marker':{'color':colour_ly},
             'hovertemplate':hovertemplate},
            {'x': dff["DaySession"],
              'y': y_ty,
             'customdata': customdata,
              'type': 'bar',
              'name': thisyear,
              'marker':{'color':colour_ty},
              'text': y_ty,
              'textposition':textposition,
              'texttemplate':texttemplate,
             'hovertemplate':hovertemplate}]

    layout = {'title':title,
             'yaxis':{'title':measure}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
           'config': config} 

def week_change(dff,
                y,
                customdata,
                colour,
               hovertemplate,
                title,
               measure):

    x = dff["DaySession"]
    max_change = (y.append(y*-1)).max()
    y_limit = max_change*1.2

    data = [{'x': x,
              'y': y,
              'customdata': customdata,
              'type': 'bar',
              'name': "vs. Last Year",
              'marker':{'color':colour},
              'text': y,
              'textposition':'auto',
              'texttemplate':'%{customdata:+.0f}%',
              'hovertemplate':hovertemplate}]

    layout = {'title': title,
              'yaxis':{'title':measure + ' vs. LY',
                      'range':[-y_limit, y_limit]}}

    config = {'displayModeBar': False}

    return {'data': data,
            'layout': layout,
           'config': config} 

daily_dropdown_ids = ['daily day slider','daily shift dropdown', 'daily area dropdown', 'daily measure dropdown', 'daily metric dropdown', 'daily site dropdown']
daily_dropdown_dependencies = []

for x in daily_dropdown_ids:
    daily_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))
    
df = pd.read_csv("Daily.csv")
daily_totals = df[df["Table"] == "Totals"]
location = df[df["Table"] == "Location"]
group = df[df["Table"] == "Group"]
daily_revenue_location = location[location["Measure"] == "Revenue"]
daily_covers_location = location[location["Measure"] == "Covers"]
daily_spend_location = location[location["Measure"] == "Spend"]
daily_revenue_group = group[group["Measure"] == "Revenue"]
daily_covers_group = group[group["Measure"] == "Covers"]
daily_spend_group = group[group["Measure"] == "Spend"]

daily_date_nums = df["Daily Date Num"].unique()
daily_dates = df["Daily Date"].unique()

@app.callback(dash.dependencies.Output('daily sales total', 'figure'),
             daily_dropdown_dependencies)
def update_daily_sales_total(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    daymask = daily_totals["Daily Date Num"] == day 

    shift = shiftValue
    measure = measureValue
    area = areaValue
    metric = metricValue

    shiftmask = daily_totals["Shift"] == shift
    measuremask = daily_totals["Measure"] == measure
    areamask = daily_totals["Area"] == area

    dff = daily_totals[shiftmask & measuremask & areamask & daymask]

    if measure == "Spend":
        revmask = daily_totals["Measure"] == "Revenue"
        covmask = daily_totals["Measure"] == "Covers"
        rev = daily_totals[revmask & shiftmask & areamask & daymask]
        cov = daily_totals[covmask & shiftmask & areamask & daymask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    else:
        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = area + ' ' + measure + ': ' + pchange


    if metric == "Year Change":
        #dff = dff.sort_values(by="Year Change", ascending=False)
        if measure == 'Revenue':
            template = '£%{x:+.0f}'
        elif measure == 'Covers':
            template = '%{x:+.0f}'
        elif measure == 'Spend':
            template = '£%{x:+.0f}'
        return create_sales_change(dff, 
                                  title,
                                  template)

    elif metricValue == "Totals":
        if measure == 'Revenue':
            template = '£%{customdata:.0f}k'
            color_ly = color_rev_ly
            color_ty = color_rev_ty
        elif measure == 'Covers':
            template = '%{x:.0f}'
            color_ly = color_cov_ly
            color_ty = color_cov_ty
        elif measure == 'Spend':
            template = '£%{x:.0f}'
            color_ly = color_spe_ly
            color_ty = color_spe_ty
        return create_sales_totals(dff, 
                                   title,
                                   template,
                                   color_ly,
                                   color_ty)


@app.callback(dash.dependencies.Output('daily group revenue', 'figure'),
             daily_dropdown_dependencies)
def update_daily_group_revenue(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    shift = shiftValue
    metric = metricValue

    df = daily_revenue_group

    daymask = df["Daily Date Num"] == day
    mask2 = df["Shift"] == shift

    dff = df[mask2 & daymask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = 'Group Revenue: ' + pchange
    measure ="Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)

@app.callback(dash.dependencies.Output('daily group covers', 'figure'),
              daily_dropdown_dependencies)
def update_daily_group_covers(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = daily_covers_group

    daymask = df["Daily Date Num"] == day
    mask2 = df["Shift"] == shift

    dff = df[mask2 & daymask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = 'Group Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('daily group spend', 'figure'),
              daily_dropdown_dependencies)
def update_daily_group_spend(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = daily_spend_group
    daymask = df["Daily Date Num"] == day
    mask2 = df["Shift"] == shift
    dff = df[mask2 & daymask]

    df = daily_revenue_group
    daymask = df["Daily Date Num"] == day
    mask2 = df["Shift"] == shift
    rev_df = df[mask2 & daymask]   

    df = daily_covers_group
    daymask = df["Daily Date Num"] == day
    mask2 = df["Shift"] == shift
    cov_df = df[mask2 & daymask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = 'Group Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('daily site revenue', 'figure'),
             daily_dropdown_dependencies)
def update_daily_site_revenue(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = daily_revenue_location

    daymask = df["Daily Date Num"] == day
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & daymask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = restaurant + ' Revenue: ' + pchange
    measure = "Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('daily site covers', 'figure'),
             daily_dropdown_dependencies)
def update_daily_site_covers(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = daily_covers_location

    daymask = df["Daily Date Num"] == day
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & daymask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = restaurant + ' Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('daily site spend', 'figure'),
             daily_dropdown_dependencies)
def update_daily_site_spend(dayValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    day = dayValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = daily_spend_location
    daymask = df["Daily Date Num"] == day
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    dff = df[mask1 & mask2 & daymask]

    df = daily_revenue_location
    daymask = df["Daily Date Num"] == day
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    rev_df = df[mask1 & mask2 & daymask]   

    df = daily_covers_location
    daymask = df["Daily Date Num"] == day
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    cov_df = df[mask1 & mask2 & daymask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = restaurant + ' Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)
    
Daily_Layout =  html.Div(children=[html.Div([html.H1(children = 'Daily Sales',
                                                 style={'textAlign':"center",
                                                        'borderBottom': 'thin lightgrey solid',
                                                        'borderRight': 'thin lightgrey solid',
                                                       'backgroundColor': header_background_colour})]),

                                 # Day Slider

                                 html.Div([html.P(['Choose the day of the report:'],
                                                 style={'textAlign':"center",
                                                       'backgroundColor': header_background_colour}),

                                           dcc.Slider(id='daily day slider',
                                                      min = 0,
                                                      max = 29,
                                                      step = None,
                                                      marks = {int(i):daily_dates[i] for i in daily_date_nums},
#                                                      marks = {int(i):'{}'.format(daily_dates[i]) for i in daily_date_nums},
                                                      value = 29)],

                                          style={'borderRight': 'thin lightgrey solid',
                                              'backgroundColor': dropdown_background_colour,
                                              'padding': '10px 5px'}),

                                 # First Dropdown Row

                                 html.Div([html.Div([html.P(['Choose the metric and shift of the report:']),

                                                     dcc.Dropdown(id='daily metric dropdown',
                                                                  options = [{'label':i, 
                                                                              'value':i} for i in ["Totals", "Year Change"]],
                                                                  value="Year Change",
                                                                         style={'width':inner_dropdown_width}),

                                                     dcc.Dropdown(id='daily shift dropdown',
                                                                  options=[{'label':i, 
                                                                            'value':i} for i in available_shifts],
                                                                  value='All Shifts',
                                                                  style={'width':outer_dropdown_width,
                                                                         'padding':'2px 0px'})],

                                                    style = div_style_simple(outer_div_width)),

                                           html.Div([html.P(['Choose the area and measure of the group summary:']),

                                                    dcc.Dropdown(id='daily area dropdown',
                                                                 options = [{'label':i, 
                                                                              'value':i} for i in available_areas],
                                                                  value='Full Site',
                                                                         style={'width':inner_dropdown_width}),

                                                     dcc.Dropdown(id='daily measure dropdown',
                                                                  options = [{'label':i, 
                                                                              'value':i} for i in available_measures],
                                                                  value='Revenue',
                                                                  style={'width':inner_dropdown_width,
                                                                         'padding':'2px 0px'})],

                                                    style = div_style_simple(inner_div_width)),

                                           html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                    dcc.Dropdown(id='daily site dropdown',
                                                                options=[{'label':i, 
                                                                          'value':i} for i in available_restaurants],
                                                                value='100 Wardour Street',
                                                                 style={'width':outer_dropdown_width})],

                                                   style = div_style_simple(outer_div_width))],

                                          style = dropdown_row_style),

                                 # Graphs

                                 html.Div([html.Div([small_graph('daily group revenue'),
                                                    small_graph('daily group covers'),
                                                    small_graph('daily group spend')],
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'backgroundColor': 'rgb(200,200,200)'}),

                                           html.Div([dcc.Graph(id='daily sales total')],                                                    
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'width':600}),

                                           html.Div([small_graph('daily site revenue'),
                                                    small_graph('daily site covers'),
                                                    small_graph('daily site spend')],
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'backgroundColor': 'rgb(200,200,200)'})])


                                ])

WTD_dropdown_ids = ['wtd shift dropdown', 'wtd area dropdown', 'wtd measure dropdown', 'wtd metric dropdown', 'wtd site dropdown']
WTD_dropdown_dependencies = []

for x in WTD_dropdown_ids:
    WTD_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))
    
df = pd.read_csv("WTD.csv")
WTD_totals = df[df["Table"] == "Totals"]
location = df[df["Table"] == "Location"]
group = df[df["Table"] == "Group"]
WTD_daily = df[df["Table"] == "Daily"]
WTD_revenue_location = location[location["Measure"] == "Revenue"]
WTD_covers_location = location[location["Measure"] == "Covers"]
WTD_spend_location = location[location["Measure"] == "Spend"]
WTD_revenue_group = group[group["Measure"] == "Revenue"]
WTD_covers_group = group[group["Measure"] == "Covers"]
WTD_spend_group = group[group["Measure"] == "Spend"]

@app.callback(dash.dependencies.Output('wtd sales total', 'figure'),
             WTD_dropdown_dependencies)
def update_wtd_sales_total(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    shift = shiftValue
    measure = measureValue
    area = areaValue
    metric = metricValue

    shiftmask = WTD_totals["Shift"] == shift
    measuremask = WTD_totals["Measure"] == measure
    areamask = WTD_totals["Area"] == area

    dff = WTD_totals[shiftmask & measuremask & areamask]

    if measure == "Spend":
        revmask = WTD_totals["Measure"] == "Revenue"
        covmask = WTD_totals["Measure"] == "Covers"
        rev = WTD_totals[revmask & shiftmask & areamask]
        cov = WTD_totals[covmask & shiftmask & areamask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    else:
        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = area + ' ' + measure + ': ' + pchange


    if metric == "Year Change":
        #dff = dff.sort_values(by="Year Change", ascending=False)
        if measure == 'Revenue':
            template = '£%{x:+.0f}'
        elif measure == 'Covers':
            template = '%{x:+.0f}'
        elif measure == 'Spend':
            template = '£%{x:+.0f}'
        return create_sales_change(dff, 
                                  title,
                                  template)

    elif metricValue == "Totals":
        if measure == 'Revenue':
            template = '£%{customdata:.0f}k'
            color_ly = color_rev_ly
            color_ty = color_rev_ty
        elif measure == 'Covers':
            template = '%{x:.0f}'
            color_ly = color_cov_ly
            color_ty = color_cov_ty
        elif measure == 'Spend':
            template = '£%{x:.0f}'
            color_ly = color_spe_ly
            color_ty = color_spe_ty
        return create_sales_totals(dff, 
                                   title,
                                   template,
                                   color_ly,
                                   color_ty)


@app.callback(dash.dependencies.Output('wtd group revenue', 'figure'),
             WTD_dropdown_dependencies)
def update_wtd_group_revenue(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    shift = shiftValue
    metric = metricValue

    df = WTD_revenue_group

    mask2 = df["Shift"] == shift

    dff = df[mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = 'Group Revenue: ' + pchange
    measure ="Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)

@app.callback(dash.dependencies.Output('wtd group covers', 'figure'),
              WTD_dropdown_dependencies)
def update_wtd_group_covers(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = WTD_covers_group
    mask2 = df["Shift"] == shift

    dff = df[mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = 'Group Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('wtd group spend', 'figure'),
              WTD_dropdown_dependencies)
def update_wtd_group_spend(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = WTD_spend_group
    mask2 = df["Shift"] == shift
    dff = df[mask2]

    df = WTD_revenue_group
    mask2 = df["Shift"] == shift
    rev_df = df[mask2]   

    df = WTD_covers_group
    mask2 = df["Shift"] == shift
    cov_df = df[mask2]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = 'Group Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('wtd site revenue', 'figure'),
             WTD_dropdown_dependencies)
def update_wtd_site_revenue(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = WTD_revenue_location

    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = restaurant + ' Revenue: ' + pchange
    measure = "Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('wtd site covers', 'figure'),
             WTD_dropdown_dependencies)
def update_wtd_site_covers(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = WTD_covers_location

    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = restaurant + ' Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('wtd site spend', 'figure'),
             WTD_dropdown_dependencies)
def update_wtd_site_spend(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = WTD_spend_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    dff = df[mask1 & mask2]

    df = WTD_revenue_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    rev_df = df[mask1 & mask2]   

    df = WTD_covers_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    cov_df = df[mask1 & mask2]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = restaurant + ' Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('wtd week view', 'figure'),
             [dash.dependencies.Input('wtd site week', 'value'),
             dash.dependencies.Input('wtd area week', 'value'),
             dash.dependencies.Input('wtd category week', 'value'),
             dash.dependencies.Input('wtd measure week', 'value'),
             dash.dependencies.Input('wtd metric dropdown', 'value')])
def update_wtd_week_view(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                    metricValue):

    restaurant = siteValue
    area = areaValue
    category = categoryValue
    measure = measureValue
    metric = metricValue

    sitemask = WTD_daily["SiteName"] == restaurant
    measuremask = WTD_daily["Measure"] == measure
    areamask = WTD_daily["GenericLocation"] == area
    categorymask = WTD_daily["RevenueType"] == category

    dff = WTD_daily[sitemask & measuremask & areamask & categorymask]

    if measure == "Spend":

        revmask = WTD_daily["Measure"] == "Revenue"
        covmask = WTD_daily["Measure"] == "Covers"
        rev = WTD_daily[revmask & sitemask & areamask & categorymask]
        cov = WTD_daily[covmask & sitemask & areamask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    if measure == "Revenue":

        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " " + measure + ": " + pchange

    if metric == "Totals":

        y_ly = dff[lastyear]
        y_ty = dff[thisyear]
        customdata = dff["% Change"]

        if measure == 'Spend':
            hovertemplate = '£%{y:.2f}'
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]

        if measure == 'Revenue':

            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]

            hovertemplate = '£%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                           hovertemplate,
                           title,
                          measure)

    if metric == "Year Change":

        if measure == "Spend":
            hovertemplate = '£%{y:+.2f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]        

        if measure == "Revenue":
            hovertemplate = '£%{y:+.0f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          measure)


@app.callback(dash.dependencies.Output('wtd week covers', 'figure'),
             [dash.dependencies.Input('wtd site week', 'value'),
             dash.dependencies.Input('wtd area week', 'value'),
             dash.dependencies.Input('wtd category week', 'value'),
             dash.dependencies.Input('wtd measure week', 'value'),
             dash.dependencies.Input('wtd metric dropdown', 'value')])
def update_wtd_week_covers(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                     metricValue):

    restaurant = siteValue
    area = areaValue
    category = categoryValue
    metric = metricValue

    sitemask = WTD_daily["SiteName"] == restaurant
    measuremask = WTD_daily["Measure"] == "Covers"
    areamask = WTD_daily["GenericLocation"] == area

    dff = WTD_daily[sitemask & measuremask & areamask]

    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " Covers: " + pchange
    measure = "Covers"

    if metric == "Totals":

        y_ly = dff[lastyear]
        y_ty = dff[thisyear]
        customdata = dff["% Change"]
        hovertemplate = '%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                           hovertemplate,
                           title,
                          measure)

    if metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        y = dff["Year Change"]
        customdata = dff["% Change"]
        colour = dff["Colour_CHG"]

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          measure)
    
WTD_Layout =  html.Div(children=[html.Div([html.H1(children = 'WTD Sales',
                                                 style={'textAlign':"center",
                                                        'borderBottom': 'thin lightgrey solid',
                                                        'borderRight': 'thin lightgrey solid',
                                                       'backgroundColor': header_background_colour})]),

                                 # First Dropdown Row

                                 html.Div([html.Div([html.P(['Choose the metric and shift of the report:']),

                                                     dcc.Dropdown(id='wtd metric dropdown',
                                                                  options = [{'label':i, 
                                                                              'value':i} for i in ["Totals", "Year Change"]],
                                                                  value="Year Change",
                                                                         style={'width':inner_dropdown_width}),

                                                     dcc.Dropdown(id='wtd shift dropdown',
                                                                  options=[{'label':i, 
                                                                            'value':i} for i in available_shifts],
                                                                  value='All Shifts',
                                                                  style={'width':outer_dropdown_width,
                                                                         'padding':'2px 0px'})],

                                                    style = div_style_simple(outer_div_width)),

                                           html.Div([html.P(['Choose the area and measure of the group summary:']),

                                                    dcc.Dropdown(id='wtd area dropdown',
                                                                 options = [{'label':i, 
                                                                              'value':i} for i in available_areas],
                                                                  value='Full Site',
                                                                         style={'width':inner_dropdown_width}),

                                                     dcc.Dropdown(id='wtd measure dropdown',
                                                                  options = [{'label':i, 
                                                                              'value':i} for i in available_measures],
                                                                  value='Revenue',
                                                                  style={'width':inner_dropdown_width,
                                                                         'padding':'2px 0px'})],

                                                    style = div_style_simple(inner_div_width)),

                                           html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                    dcc.Dropdown(id='wtd site dropdown',
                                                                options=[{'label':i, 
                                                                          'value':i} for i in available_restaurants],
                                                                value='100 Wardour Street',
                                                                 style={'width':outer_dropdown_width})],

                                                   style = div_style_simple(outer_div_width))],

                                          style = dropdown_row_style),

                                 # Graphs

                                 html.Div([html.Div([small_graph('wtd group revenue'),
                                                    small_graph('wtd group covers'),
                                                    small_graph('wtd group spend')],
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'backgroundColor': 'rgb(200,200,200)'}),

                                           html.Div([dcc.Graph(id='wtd sales total')],                                                    
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'width':600}),

                                           html.Div([small_graph('wtd site revenue'),
                                                    small_graph('wtd site covers'),
                                                    small_graph('wtd site spend')],
                                                    style = {'display': 'inline-block',
                                                            'height':900,
                                                            'backgroundColor': 'rgb(200,200,200)'})]),

                                 # Second Dropdown Row

                                 html.Div([html.Div([html.P(['Choose the restaurant of the week view:']),

                                                     dcc.Dropdown(id='wtd site week',
                                                                  options=[{'label':i, 
                                                                            'value':i} for i in available_restaurants_week],
                                                                  value='Group',
                                                                 style={'width':week_dropdown_width})],

                                                    style=week_dropdown_style),

                                           html.Div([html.P(['Choose the area of the week view:']),

                                                    dcc.Dropdown(id='wtd area week',
                                                          options = [{'label':i, 
                                                                      'value':i} for i in available_areas],
                                                          value='Full Site',
                                                                 style={'width':week_dropdown_width})],

                                                    style=week_dropdown_style),

                                           html.Div([html.P(['Choose the revenue category of the week view:']),

                                                    dcc.Dropdown(id='wtd category week',
                                                          options = [{'label':i, 
                                                                      'value':i} for i in available_types],
                                                          value='Total',
                                                                 style={'width':week_dropdown_width})],

                                                    style=week_dropdown_style),

                                           html.Div([html.P(['Choose the measure of the week view:']),

                                                    dcc.Dropdown(id='wtd measure week',
                                                                 options = [{'label':i, 
                                                                             'value':i} for i in ["Revenue",
                                                                                                  "Spend"]],
                                                                 value='Revenue',
                                                                 style={'width':week_dropdown_width})],

                                                   style=week_dropdown_style ) ],

                                          style = {'borderBottom': 'thin lightgrey solid',
                                                   'borderRight': 'thin lightgrey solid',
                                                  'backgroundColor': dropdown_background_colour,
                                                  'padding': '10px 5px'}),

                                 # Second Graph Row

                                 html.Div([html.Div([week_graph('wtd week view')],

                                                    style = {'display': 'inline-block',
                                                            'height':week_height,
                                                            'width':week_width}),

                                           html.Div([week_graph('wtd week covers')],

                                                    style = {'display': 'inline-block',
                                                            'height':week_height,
                                                            'width':week_width}) ])

                                ])


month_week_div_width = 360
month_week_dropdown_width = month_week_div_width - 10

month_week_dropdown_style = {'textAlign':'center',
                          'display': 'inline-block',
                          'width':month_week_div_width}

MTD_dropdown_ids = ['mtd shift dropdown', 'mtd area dropdown', 'mtd measure dropdown', 'mtd metric dropdown', 'mtd site dropdown']
MTD_dropdown_dependencies = []

for x in MTD_dropdown_ids:
    MTD_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))
    
df = pd.read_csv("MTD.csv")
MTD_totals = df[df["Table"] == "Totals"]
location = df[df["Table"] == "Location"]
group = df[df["Table"] == "Group"]
MTD_daily = df[df["Table"] == "Daily"]
MTD_revenue_location = location[location["Measure"] == "Revenue"]
MTD_covers_location = location[location["Measure"] == "Covers"]
MTD_spend_location = location[location["Measure"] == "Spend"]
MTD_revenue_group = group[group["Measure"] == "Revenue"]
MTD_covers_group = group[group["Measure"] == "Covers"]
MTD_spend_group = group[group["Measure"] == "Spend"]

    
@app.callback(dash.dependencies.Output('mtd sales total', 'figure'),
             MTD_dropdown_dependencies)
def update_mtd_sales_total(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    shift = shiftValue
    measure = measureValue
    area = areaValue
    metric = metricValue

    shiftmask = MTD_totals["Shift"] == shift
    measuremask = MTD_totals["Measure"] == measure
    areamask = MTD_totals["Area"] == area

    dff = MTD_totals[shiftmask & measuremask & areamask]

    if measure == "Spend":
        revmask = MTD_totals["Measure"] == "Revenue"
        covmask = MTD_totals["Measure"] == "Covers"
        rev = MTD_totals[revmask & shiftmask & areamask]
        cov = MTD_totals[covmask & shiftmask & areamask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    else:
        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = area + ' ' + measure + ': ' + pchange


    if metric == "Year Change":
        #dff = dff.sort_values(by="Year Change", ascending=False)
        if measure == 'Revenue':
            template = '£%{x:+.0f}'
        elif measure == 'Covers':
            template = '%{x:+.0f}'
        elif measure == 'Spend':
            template = '£%{x:+.0f}'
        return create_sales_change(dff, 
                                  title, 
                                  template)

    elif metricValue == "Totals":
        if measure == 'Revenue':
            template = '£%{customdata:.0f}k'
            color_ly = color_rev_ly
            color_ty = color_rev_ty
        elif measure == 'Covers':
            template = '%{x:.0f}'
            color_ly = color_cov_ly
            color_ty = color_cov_ty
        elif measure == 'Spend':
            template = '£%{x:.0f}'
            color_ly = color_spe_ly
            color_ty = color_spe_ty
        return create_sales_totals(dff, 
                                   title,
                                   template,
                                   color_ly,
                                   color_ty)


@app.callback(dash.dependencies.Output('mtd group revenue', 'figure'),
             MTD_dropdown_dependencies)
def update_mtd_group_revenue(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    shift = shiftValue
    metric = metricValue

    df = MTD_revenue_group

    mask2 = df["Shift"] == shift

    dff = df[mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = 'Group Revenue: ' + pchange
    measure ="Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)

@app.callback(dash.dependencies.Output('mtd group covers', 'figure'),
              MTD_dropdown_dependencies)
def update_mtd_group_covers(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = MTD_covers_group

    mask2 = df["Shift"] == shift

    dff = df[mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = 'Group Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('mtd group spend', 'figure'),MTD_dropdown_dependencies)
def update_mtd_group_spend(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = MTD_spend_group
    mask2 = df["Shift"] == shift
    dff = df[mask2]

    df = MTD_revenue_group
    mask2 = df["Shift"] == shift
    rev_df = df[mask2]   

    df = MTD_covers_group
    mask2 = df["Shift"] == shift
    cov_df = df[mask2]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = 'Group Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('mtd site revenue', 'figure'),
             MTD_dropdown_dependencies)
def update_mtd_site_revenue(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = MTD_revenue_location

    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = restaurant + ' Revenue: ' + pchange
    measure = "Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('mtd site covers', 'figure'),
             MTD_dropdown_dependencies)
def update_mtd_site_covers(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = MTD_covers_location

    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = restaurant + ' Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('mtd site spend', 'figure'),
             MTD_dropdown_dependencies)
def update_mtd_site_spend(shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = MTD_spend_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    dff = df[mask1 & mask2]

    df = MTD_revenue_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    rev_df = df[mask1 & mask2]   

    df = MTD_covers_location
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    cov_df = df[mask1 & mask2]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = restaurant + ' Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('mtd week view', 'figure'),
             [dash.dependencies.Input('mtd site week', 'value'),
             dash.dependencies.Input('mtd area week', 'value'),
             dash.dependencies.Input('mtd category week', 'value'),
             dash.dependencies.Input('mtd measure week', 'value'),
             dash.dependencies.Input('mtd metric week', 'value'),
             dash.dependencies.Input('mtd metric dropdown', 'value')])
def update_mtd_week_view(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                    weekmetricValue,
                    metricValue):

    restaurant = siteValue
    area = areaValue
    category = categoryValue
    measure = measureValue
    weekmetric = weekmetricValue
    metric = metricValue

    sitemask = MTD_daily["SiteName"] == restaurant
    measuremask = MTD_daily["Measure"] == measure
    areamask = MTD_daily["GenericLocation"] == area
    categorymask = MTD_daily["RevenueType"] == category

    dff = MTD_daily[sitemask & measuremask & areamask & categorymask]

    if measure == "Spend":

        revmask = MTD_daily["Measure"] == "Revenue"
        covmask = MTD_daily["Measure"] == "Covers"
        rev = MTD_daily[revmask & sitemask & areamask & categorymask]
        cov = MTD_daily[covmask & sitemask & areamask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    if measure == "Revenue":

        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " " + measure + ": " + pchange

    if metric == "Totals":

        if measure == 'Spend':
            hovertemplate = '£%{y:.2f}'
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]
            ytitle = measure

        if measure == 'Revenue':
            if weekmetric == "Actuals":
                y_ly = dff[lastyear]
                y_ty = dff[thisyear]
                customdata = dff["% Change"]
                ytitle = measure
            if weekmetric == "Averages":
                y_ly = dff["Average_LY"]
                y_ty = dff["Average_TY"]
                customdata = dff["Average_% Change"]
                ytitle = "Average " + measure

            hovertemplate = '£%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                            hovertemplate,
                           title,
                          ytitle)

    if metric == "Year Change":

        if measure == "Spend":
            hovertemplate = '£%{y:+.2f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]
            ytitle = measure + " vs. LY"

        if measure == "Revenue":
            hovertemplate = '£%{y:+.0f}'
            if weekmetric == "Actuals":
                y = dff["Year Change"]
                customdata = dff["% Change"]
                colour = dff["Colour_CHG"]
                ytitle = measure + " vs. LY"
            if weekmetric == "Averages":
                y = dff["Average_Year Change"]
                customdata = dff["Average_% Change"]
                colour = dff["Average_Colour"]
                ytitle = "Average " + measure + " vs. LY"

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          ytitle)


@app.callback(dash.dependencies.Output('mtd week covers', 'figure'),
             [dash.dependencies.Input('mtd site week', 'value'),
             dash.dependencies.Input('mtd area week', 'value'),
             dash.dependencies.Input('mtd category week', 'value'),
             dash.dependencies.Input('mtd measure week', 'value'),
             dash.dependencies.Input('mtd metric week', 'value'),
             dash.dependencies.Input('mtd metric dropdown', 'value')])
def update_mtd_week_covers(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                    weekmetricValue,
                    metricValue):

    restaurant = siteValue
    area = areaValue
    category = categoryValue
    weekmetric = weekmetricValue
    metric = metricValue

    sitemask = MTD_daily["SiteName"] == restaurant
    measuremask = MTD_daily["Measure"] == "Covers"
    areamask = MTD_daily["GenericLocation"] == area

    dff = MTD_daily[sitemask & measuremask & areamask]

    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " Covers: " + pchange
    measure = "Covers"

    if metric == "Totals":

        if weekmetric == "Actuals":
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]
            ytitle = measure

        if weekmetric == "Averages":
            y_ly = dff["Average_LY"]
            y_ty = dff["Average_TY"]
            customdata = dff["Average_% Change"]
            ytitle = "Average " + measure

        hovertemplate = '%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                            hovertemplate,
                           title,
                          ytitle)

    if metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        if weekmetric == "Actuals":
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]
            ytitle = measure + " vs. LY"
        if weekmetric == "Averages":
            y = dff["Average_Year Change"]
            customdata = dff["Average_% Change"]
            colour = dff["Average_Colour"]
            ytitle = "Average " + measure + " vs. LY"

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          ytitle)

MTD_Layout =  html.Div(children=[html.Div([html.H1(children = 'MTD Sales',
                                                     style={'textAlign':"center",
                                                            'borderBottom': 'thin lightgrey solid',
                                                            'borderRight': 'thin lightgrey solid',
                                                           'backgroundColor': header_background_colour})]),

                                     # First Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the metric and shift of the report:']),

                                                         dcc.Dropdown(id='mtd metric dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in ["Totals", "Year Change"]],
                                                                      value="Year Change",
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='mtd shift dropdown',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_shifts],
                                                                      value='All Shifts',
                                                                      style={'width':outer_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(outer_div_width)),

                                               html.Div([html.P(['Choose the area and measure of the group summary:']),

                                                        dcc.Dropdown(id='mtd area dropdown',
                                                                     options = [{'label':i, 
                                                                                  'value':i} for i in available_areas],
                                                                      value='Full Site',
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='mtd measure dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in available_measures],
                                                                      value='Revenue',
                                                                      style={'width':inner_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(inner_div_width)),

                                               html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                        dcc.Dropdown(id='mtd site dropdown',
                                                                    options=[{'label':i, 
                                                                              'value':i} for i in available_restaurants],
                                                                    value='100 Wardour Street',
                                                                     style={'width':outer_dropdown_width})],

                                                       style = div_style_simple(outer_div_width))],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Graphs

                                     html.Div([html.Div([small_graph('mtd group revenue'),
                                                        small_graph('mtd group covers'),
                                                        small_graph('mtd group spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'}),

                                               html.Div([dcc.Graph(id='mtd sales total')],                                                    
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'width':600}),

                                               html.Div([small_graph('mtd site revenue'),
                                                        small_graph('mtd site covers'),
                                                        small_graph('mtd site spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'})]),

                                     # Second Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the restaurant of the week view:']),

                                                         dcc.Dropdown(id='mtd site week',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_restaurants_week],
                                                                      value='Group',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the area of the week view:']),

                                                        dcc.Dropdown(id='mtd area week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_areas],
                                                              value='Full Site',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the revenue category of the week view:']),

                                                        dcc.Dropdown(id='mtd category week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_types],
                                                              value='Total',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the measure of the week view:']),

                                                        dcc.Dropdown(id='mtd measure week',
                                                                     options = [{'label':i, 
                                                                                 'value':i} for i in ["Revenue",
                                                                                                      "Spend"]],
                                                                     value='Revenue',
                                                                     style={'width':month_week_dropdown_width})],

                                                       style=month_week_dropdown_style ),

                                               html.Div([html.P(['Choose the metric of the week view:']),

                                                        dcc.Dropdown(id='mtd metric week',
                                                                     options = [{'label':i, 
                                                                                 'value':i} for i in ["Actuals",
                                                                                                      "Averages"]],
                                                                     value='Actuals',
                                                                     style={'width':month_week_dropdown_width})],

                                                       style=month_week_dropdown_style ) ],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Second Graph Row

                                     html.Div([html.Div([week_graph('mtd week view')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}),

                                               html.Div([week_graph('mtd week covers')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}) ])

                                    ])


df = pd.read_csv("Week.csv")
Weekly_totals = df[df["Table"] == "Totals"]
location = df[df["Table"] == "Location"]
group = df[df["Table"] == "Group"]
Weekly_daily = df[df["Table"] == "Daily"]
Weekly_revenue_location = location[location["Measure"] == "Revenue"]
Weekly_covers_location = location[location["Measure"] == "Covers"]
Weekly_spend_location = location[location["Measure"] == "Spend"]
Weekly_revenue_group = group[group["Measure"] == "Revenue"]
Weekly_covers_group = group[group["Measure"] == "Covers"]
Weekly_spend_group = group[group["Measure"] == "Spend"]

available_weeks = df["Week Num"].unique()

Weekly_dropdown_ids = ['week slider','weekly shift dropdown', 'weekly area dropdown', 'weekly measure dropdown', 'weekly metric dropdown', 'weekly site dropdown']
Weekly_dropdown_dependencies = []

for x in Weekly_dropdown_ids:
    Weekly_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))
    
@app.callback(dash.dependencies.Output('weekly sales total', 'figure'),
             Weekly_dropdown_dependencies)
def update_weekly_sales_total(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    weekmask = Weekly_totals["Week Num"] == week 

    shift = shiftValue
    measure = measureValue
    area = areaValue
    metric = metricValue

    shiftmask = Weekly_totals["Shift"] == shift
    measuremask = Weekly_totals["Measure"] == measure
    areamask = Weekly_totals["Area"] == area

    dff = Weekly_totals[shiftmask & measuremask & areamask & weekmask]

    if measure == "Spend":
        revmask = Weekly_totals["Measure"] == "Revenue"
        covmask = Weekly_totals["Measure"] == "Covers"
        rev = Weekly_totals[revmask & shiftmask & areamask & weekmask]
        cov = Weekly_totals[covmask & shiftmask & areamask & weekmask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    else:
        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = area + ' ' + measure + ': ' + pchange


    if metric == "Year Change":
        #dff = dff.sort_values(by="Year Change", ascending=False)
        if measure == 'Revenue':
            template = '£%{x:+.0f}'
        elif measure == 'Covers':
            template = '%{x:+.0f}'
        elif measure == 'Spend':
            template = '£%{x:+.0f}'
        return create_sales_change(dff, 
                                  title,
                                  template)

    elif metricValue == "Totals":
        if measure == 'Revenue':
            template = '£%{customdata:.0f}k'
            color_ly = color_rev_ly
            color_ty = color_rev_ty
        elif measure == 'Covers':
            template = '%{x:.0f}'
            color_ly = color_cov_ly
            color_ty = color_cov_ty
        elif measure == 'Spend':
            template = '£%{x:.0f}'
            color_ly = color_spe_ly
            color_ty = color_spe_ty
        return create_sales_totals(dff, 
                                   title,
                                   template,
                                   color_ly,
                                   color_ty)


@app.callback(dash.dependencies.Output('weekly group revenue', 'figure'),
             Weekly_dropdown_dependencies)
def update_weekly_group_revenue(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_revenue_group

    weekmask = df["Week Num"] == week
    mask2 = df["Shift"] == shift

    dff = df[mask2 & weekmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = 'Group Revenue: ' + pchange
    measure ="Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)

@app.callback(dash.dependencies.Output('weekly group covers', 'figure'),
              Weekly_dropdown_dependencies)
def update_weekly_group_covers(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_covers_group

    weekmask = df["Week Num"] == week
    mask2 = df["Shift"] == shift

    dff = df[mask2 & weekmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = 'Group Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('weekly group spend', 'figure'),Weekly_dropdown_dependencies)
def update_weekly_group_spend(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_spend_group
    weekmask = df["Week Num"] == week
    mask2 = df["Shift"] == shift
    dff = df[mask2 & weekmask]

    df = Weekly_revenue_group
    weekmask = df["Week Num"] == week
    mask2 = df["Shift"] == shift
    rev_df = df[mask2 & weekmask]   

    df = Weekly_covers_group
    weekmask = df["Week Num"] == week
    mask2 = df["Shift"] == shift
    cov_df = df[mask2 & weekmask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = 'Group Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('weekly site revenue', 'figure'),
             Weekly_dropdown_dependencies)
def update_weekly_site_revenue(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_revenue_location

    weekmask = df["Week Num"] == week
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & weekmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = restaurant + ' Revenue: ' + pchange
    measure = "Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('weekly site covers', 'figure'),
             Weekly_dropdown_dependencies)
def update_weekly_site_covers(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_covers_location

    weekmask = df["Week Num"] == week
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & weekmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = restaurant + ' Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('weekly site spend', 'figure'),
             Weekly_dropdown_dependencies)
def update_weekly_site_spend(weekValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    week = weekValue
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Weekly_spend_location
    weekmask = df["Week Num"] == week
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    dff = df[mask1 & mask2 & weekmask]

    df = Weekly_revenue_location
    weekmask = df["Week Num"] == week
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    rev_df = df[mask1 & mask2 & weekmask]   

    df = Weekly_covers_location
    weekmask = df["Week Num"] == week
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    cov_df = df[mask1 & mask2 & weekmask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = restaurant + ' Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('weekly week view', 'figure'),
             [dash.dependencies.Input('weekly site week', 'value'),
             dash.dependencies.Input('weekly area week', 'value'),
             dash.dependencies.Input('weekly category week', 'value'),
             dash.dependencies.Input('weekly measure week', 'value'),
             dash.dependencies.Input('week slider', 'value'),
             dash.dependencies.Input('weekly metric dropdown', 'value')])
def update_weekly_week_view(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                     weekValue,
                    metricValue):

    week = weekValue    
    restaurant = siteValue
    area = areaValue
    category = categoryValue
    measure = measureValue
    metric = metricValue

    weekmask = Weekly_daily["Week Num"] == week    
    sitemask = Weekly_daily["SiteName"] == restaurant
    measuremask = Weekly_daily["Measure"] == measure
    areamask = Weekly_daily["GenericLocation"] == area
    categorymask = Weekly_daily["RevenueType"] == category

    dff = Weekly_daily[sitemask & measuremask & areamask & categorymask & weekmask]

    if measure == "Spend":

        revmask = Weekly_daily["Measure"] == "Revenue"
        covmask = Weekly_daily["Measure"] == "Covers"
        rev = Weekly_daily[revmask & sitemask & areamask & categorymask & weekmask]
        cov = Weekly_daily[covmask & sitemask & areamask & weekmask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    if measure == "Revenue":

        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " " + measure + ": " + pchange

    if metric == "Totals":

        y_ly = dff[lastyear]
        y_ty = dff[thisyear]
        customdata = dff["% Change"]

        if measure == 'Spend':
            hovertemplate = '£%{y:.2f}'
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]

        if measure == 'Revenue':

            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]

            hovertemplate = '£%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                           hovertemplate,
                           title,
                          measure)

    if metric == "Year Change":

        if measure == "Spend":
            hovertemplate = '£%{y:+.2f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]        

        if measure == "Revenue":
            hovertemplate = '£%{y:+.0f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          measure)


@app.callback(dash.dependencies.Output('weekly week covers', 'figure'),
             [dash.dependencies.Input('weekly site week', 'value'),
             dash.dependencies.Input('weekly area week', 'value'),
             dash.dependencies.Input('weekly category week', 'value'),
             dash.dependencies.Input('weekly measure week', 'value'),
             dash.dependencies.Input('week slider', 'value'),
             dash.dependencies.Input('weekly metric dropdown', 'value')])
def update_weekly_week_covers(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                     weekValue,
                    metricValue):

    week = weekValue    
    restaurant = siteValue
    area = areaValue
    category = categoryValue
    metric = metricValue

    weekmask = Weekly_daily["Week Num"] == week    
    sitemask = Weekly_daily["SiteName"] == restaurant
    measuremask = Weekly_daily["Measure"] == "Covers"
    areamask = Weekly_daily["GenericLocation"] == area

    dff = Weekly_daily[sitemask & measuremask & areamask & weekmask]

    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " Covers: " + pchange
    measure = "Covers"

    if metric == "Totals":

        y_ly = dff[lastyear]
        y_ty = dff[thisyear]
        customdata = dff["% Change"]
        hovertemplate = '%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                           hovertemplate,
                           title,
                          measure)

    if metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        y = dff["Year Change"]
        customdata = dff["% Change"]
        colour = dff["Colour_CHG"]

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          measure)
    
Week_Layout =  html.Div(children=[html.Div([html.H1(children = 'Weekly Sales',
                                                     style={'textAlign':"center",
                                                            'borderBottom': 'thin lightgrey solid',
                                                            'borderRight': 'thin lightgrey solid',
                                                           'backgroundColor': header_background_colour})]),

                                     # Week Slider

                                     html.Div([html.P(['Choose the week of the report:'],
                                                     style={'textAlign':"center",
                                                           'backgroundColor': header_background_colour}),

                                               dcc.Slider(id = 'week slider',
                                                          min = available_weeks[0],
                                                          max = available_weeks[-1],
                                                          step = None,
                                                          marks = {int(i):'Last Week' if i == available_weeks[-1]
                                                                   else 'Week {}'.format(i) if len(available_weeks) <= 40
                                                                   else 'Wk{}'.format(i) for i in range(1,52)},
                                                          value = available_weeks[-1])],

                                              style={'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # First Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the metric and shift of the report:']),

                                                         dcc.Dropdown(id='weekly metric dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in ["Totals", "Year Change"]],
                                                                      value="Year Change",
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='weekly shift dropdown',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_shifts],
                                                                      value='All Shifts',
                                                                      style={'width':outer_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(outer_div_width)),

                                               html.Div([html.P(['Choose the area and measure of the group summary:']),

                                                        dcc.Dropdown(id='weekly area dropdown',
                                                                     options = [{'label':i, 
                                                                                  'value':i} for i in available_areas],
                                                                      value='Full Site',
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='weekly measure dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in available_measures],
                                                                      value='Revenue',
                                                                      style={'width':inner_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(inner_div_width)),

                                               html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                        dcc.Dropdown(id='weekly site dropdown',
                                                                    options=[{'label':i, 
                                                                              'value':i} for i in available_restaurants],
                                                                    value='100 Wardour Street',
                                                                     style={'width':outer_dropdown_width})],

                                                       style = div_style_simple(outer_div_width))],

                                              style = dropdown_row_style),

                                     # Graphs

                                     html.Div([html.Div([small_graph('weekly group revenue'),
                                                        small_graph('weekly group covers'),
                                                        small_graph('weekly group spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'}),

                                               html.Div([dcc.Graph(id='weekly sales total')],                                                    
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'width':600}),

                                               html.Div([small_graph('weekly site revenue'),
                                                        small_graph('weekly site covers'),
                                                        small_graph('weekly site spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'})]),

                                     # Second Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the restaurant of the week view:']),

                                                         dcc.Dropdown(id='weekly site week',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_restaurants_week],
                                                                      value='Group',
                                                                     style={'width':week_dropdown_width})],

                                                        style=week_dropdown_style),

                                               html.Div([html.P(['Choose the area of the week view:']),

                                                        dcc.Dropdown(id='weekly area week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_areas],
                                                              value='Full Site',
                                                                     style={'width':week_dropdown_width})],

                                                        style=week_dropdown_style),

                                               html.Div([html.P(['Choose the revenue category of the week view:']),

                                                        dcc.Dropdown(id='weekly category week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_types],
                                                              value='Total',
                                                                     style={'width':week_dropdown_width})],

                                                        style=week_dropdown_style),

                                               html.Div([html.P(['Choose the measure of the week view:']),

                                                        dcc.Dropdown(id='weekly measure week',
                                                                     options = [{'label':i, 
                                                                                 'value':i} for i in ["Revenue",
                                                                                                      "Spend"]],
                                                                     value='Revenue',
                                                                     style={'width':week_dropdown_width})],

                                                       style=week_dropdown_style ) ],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Second Graph Row

                                     html.Div([html.Div([week_graph('weekly week view')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}),

                                               html.Div([week_graph('weekly week covers')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}) ])

                                    ])


df = pd.read_csv("Month.csv")
Monthly_totals = df[df["Table"] == "Totals"]
location = df[df["Table"] == "Location"]
group = df[df["Table"] == "Group"]
Monthly_daily = df[df["Table"] == "Daily"]
Monthly_revenue_location = location[location["Measure"] == "Revenue"]
Monthly_covers_location = location[location["Measure"] == "Covers"]
Monthly_spend_location = location[location["Measure"] == "Spend"]
Monthly_revenue_group = group[group["Measure"] == "Revenue"]
Monthly_covers_group = group[group["Measure"] == "Covers"]
Monthly_spend_group = group[group["Measure"] == "Spend"]

# today = date.today()
mar_13 = '06/03/20'
today = datetime.strptime(mar_13, '%d/%m/%y').date()
currentmonth = today.month
monthfetch = currentmonth - 2

all_months = ['January',
             'February',
             'March',
             'April',
             'May',
             'June',
             'July',
             'August',
             'September',
             'October',
             'November',
             'December']

Monthly_dropdown_ids = ['month slider','monthly shift dropdown', 'monthly area dropdown', 'monthly measure dropdown', 'monthly metric dropdown', 'monthly site dropdown']
Monthly_dropdown_dependencies = []

for x in Monthly_dropdown_ids:
    Monthly_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))
    
@app.callback(dash.dependencies.Output('monthly sales total', 'figure'),
             Monthly_dropdown_dependencies)
def update_monthly_sales_total(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    monthmask = Monthly_totals["Month Num"] == month 

    shift = shiftValue
    measure = measureValue
    area = areaValue
    metric = metricValue

    shiftmask = Monthly_totals["Shift"] == shift
    measuremask = Monthly_totals["Measure"] == measure
    areamask = Monthly_totals["Area"] == area

    dff = Monthly_totals[shiftmask & measuremask & areamask & monthmask]

    if measure == "Spend":
        revmask = Monthly_totals["Measure"] == "Revenue"
        covmask = Monthly_totals["Measure"] == "Covers"
        rev = Monthly_totals[revmask & shiftmask & areamask & monthmask]
        cov = Monthly_totals[covmask & shiftmask & areamask & monthmask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    else:
        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = area + ' ' + measure + ': ' + pchange


    if metric == "Year Change":
        #dff = dff.sort_values(by="Year Change", ascending=False)
        if measure == 'Revenue':
            template = '£%{x:+.0f}'
        elif measure == 'Covers':
            template = '%{x:+.0f}'
        elif measure == 'Spend':
            template = '£%{x:+.0f}'
        return create_sales_change(dff, 
                                  title, 
                                  template)

    elif metricValue == "Totals":
        if measure == 'Revenue':
            template = '£%{customdata:.0f}k'
            color_ly = color_rev_ly
            color_ty = color_rev_ty
        elif measure == 'Covers':
            template = '%{x:.0f}'
            color_ly = color_cov_ly
            color_ty = color_cov_ty
        elif measure == 'Spend':
            template = '£%{x:.0f}'
            color_ly = color_spe_ly
            color_ty = color_spe_ty
        return create_sales_totals(dff, 
                                   title,
                                   template,
                                   color_ly,
                                   color_ty)


@app.callback(dash.dependencies.Output('monthly group revenue', 'figure'),
             Monthly_dropdown_dependencies)
def update_monthly_group_revenue(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    shift = shiftValue
    metric = metricValue

    df = Monthly_revenue_group

    monthmask = df["Month Num"] == month
    mask2 = df["Shift"] == shift

    dff = df[mask2 & monthmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = 'Group Revenue: ' + pchange
    measure ="Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)

@app.callback(dash.dependencies.Output('monthly group covers', 'figure'),
              Monthly_dropdown_dependencies)
def update_monthly_group_covers(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Monthly_covers_group

    monthmask = df["Month Num"] == month
    mask2 = df["Shift"] == shift

    dff = df[mask2 & monthmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "GenericLocation"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = 'Group Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('monthly group spend', 'figure'),Monthly_dropdown_dependencies)
def update_monthly_group_spend(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Monthly_spend_group
    monthmask = df["Month Num"] == month
    mask2 = df["Shift"] == shift
    dff = df[mask2 & monthmask]

    df = Monthly_revenue_group
    monthmask = df["Month Num"] == month
    mask2 = df["Shift"] == shift
    rev_df = df[mask2 & monthmask]   

    df = Monthly_covers_group
    monthmask = df["Month Num"] == month
    mask2 = df["Shift"] == shift
    cov_df = df[mask2 & monthmask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = 'Group Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('monthly site revenue', 'figure'),
             Monthly_dropdown_dependencies)
def update_monthly_site_revenue(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Monthly_revenue_location

    monthmask = df["Month Num"] == month
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & monthmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_rev_ty
    color_ly = color_rev_ly
    title = restaurant + ' Revenue: ' + pchange
    measure = "Revenue"

    if metric == "Totals":
        hovertemplate = '£%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)



@app.callback(dash.dependencies.Output('monthly site covers', 'figure'),
             Monthly_dropdown_dependencies)
def update_monthly_site_covers(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Monthly_covers_location

    monthmask = df["Month Num"] == month
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift

    dff = df[mask1 & mask2 & monthmask]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    xcolumn = "LocationName"
    color_ty = color_cov_ty
    color_ly = color_cov_ly
    title = restaurant + ' Covers: ' + pchange
    measure = "Covers"

    if metric == "Totals":
        hovertemplate = '%{y:.0f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('monthly site spend', 'figure'),
             Monthly_dropdown_dependencies)
def update_monthly_site_spend(monthValue,
                        shiftValue,
                       areaValue,
                       measureValue,
                      metricValue,
                       siteValue):

    month = monthValue + 1
    restaurant = siteValue
    shift = shiftValue
    metric = metricValue

    df = Monthly_spend_location
    monthmask = df["Month Num"] == month
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    dff = df[mask1 & mask2 & monthmask]

    df = Monthly_revenue_location
    monthmask = df["Month Num"] == month
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    rev_df = df[mask1 & mask2 & monthmask]   

    df = Monthly_covers_location
    monthmask = df["Month Num"] == month
    mask1 = df["SiteName"] == restaurant
    mask2 = df["Shift"] == shift
    cov_df = df[mask1 & mask2 & monthmask]

    spend_ly = rev_df[lastyear].sum()/cov_df[lastyear].sum()
    spend_ty = rev_df[thisyear].sum()/cov_df[thisyear].sum()
    pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%" 

    xcolumn = "RevenueType"
    color_ty = color_spe_ty
    color_ly = color_spe_ly
    title = restaurant + ' Restaurant Spend (Site: ' + pchange + ')'
    measure = "Spend"

    if metric == "Totals":
        hovertemplate = '£%{y:.2f}'
        return totals_graph(dff,
                            xcolumn,
                            color_ty,
                            color_ly,
                            hovertemplate,
                            title,
                           measure)

    elif metric == "Year Change":
        hovertemplate = '£%{y:+.2f}'
        return change_graph(dff,
                            xcolumn,
                            hovertemplate,
                            title,
                           measure)


@app.callback(dash.dependencies.Output('monthly week view', 'figure'),
             [dash.dependencies.Input('monthly site week', 'value'),
             dash.dependencies.Input('monthly area week', 'value'),
             dash.dependencies.Input('monthly category week', 'value'),
             dash.dependencies.Input('monthly measure week', 'value'),
             dash.dependencies.Input('month slider', 'value'),
             dash.dependencies.Input('monthly metric week', 'value'),
             dash.dependencies.Input('monthly metric dropdown', 'value')])
def update_monthly_week_view(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                     monthValue,
                    weekmetricValue,
                    metricValue):

    month = monthValue + 1    
    restaurant = siteValue
    area = areaValue
    category = categoryValue
    measure = measureValue
    weekmetric = weekmetricValue
    metric = metricValue

    monthmask = Monthly_daily["Month Num"] == month    
    sitemask = Monthly_daily["SiteName"] == restaurant
    measuremask = Monthly_daily["Measure"] == measure
    areamask = Monthly_daily["GenericLocation"] == area
    categorymask = Monthly_daily["RevenueType"] == category

    dff = Monthly_daily[sitemask & measuremask & areamask & categorymask & monthmask]

    if measure == "Spend":

        revmask = Monthly_daily["Measure"] == "Revenue"
        covmask = Monthly_daily["Measure"] == "Covers"
        rev = Monthly_daily[revmask & sitemask & areamask & categorymask & monthmask]
        cov = Monthly_daily[covmask & sitemask & areamask & monthmask]

        spend_ly = rev[lastyear].sum()/cov[lastyear].sum()
        spend_ty = rev[thisyear].sum()/cov[thisyear].sum()

        pchange = plus(round(((spend_ty - spend_ly)/spend_ly)*100)) + "%"

    if measure == "Revenue":

        pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " " + measure + ": " + pchange

    if metric == "Totals":

        if measure == 'Spend':
            hovertemplate = '£%{y:.2f}'
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]
            ytitle = measure

        if measure == 'Revenue':
            if weekmetric == "Actuals":
                y_ly = dff[lastyear]
                y_ty = dff[thisyear]
                customdata = dff["% Change"]
                ytitle = measure
            if weekmetric == "Averages":
                y_ly = dff["Average_LY"]
                y_ty = dff["Average_TY"]
                customdata = dff["Average_% Change"]
                ytitle = "Average " + measure

            hovertemplate = '£%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                            hovertemplate,
                           title,
                          ytitle)

    if metric == "Year Change":

        if measure == "Spend":
            hovertemplate = '£%{y:+.2f}'
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]
            ytitle = measure + " vs. LY"

        if measure == "Revenue":
            hovertemplate = '£%{y:+.0f}'
            if weekmetric == "Actuals":
                y = dff["Year Change"]
                customdata = dff["% Change"]
                colour = dff["Colour_CHG"]
                ytitle = measure + " vs. LY"
            if weekmetric == "Averages":
                y = dff["Average_Year Change"]
                customdata = dff["Average_% Change"]
                colour = dff["Average_Colour"]
                ytitle = "Average " + measure + " vs. LY"

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          ytitle)


@app.callback(dash.dependencies.Output('monthly week covers', 'figure'),
             [dash.dependencies.Input('monthly site week', 'value'),
             dash.dependencies.Input('monthly area week', 'value'),
             dash.dependencies.Input('monthly category week', 'value'),
             dash.dependencies.Input('monthly measure week', 'value'),
             dash.dependencies.Input('month slider', 'value'),
             dash.dependencies.Input('monthly metric week', 'value'),
             dash.dependencies.Input('monthly metric dropdown', 'value')])
def update_monthly_week_covers(siteValue, 
                     areaValue, 
                     categoryValue, 
                     measureValue,
                     monthValue,
                    weekmetricValue,
                    metricValue):

    month = monthValue + 1    
    restaurant = siteValue
    area = areaValue
    category = categoryValue
    weekmetric = weekmetricValue
    metric = metricValue

    monthmask = Monthly_daily["Month Num"] == month    
    sitemask = Monthly_daily["SiteName"] == restaurant
    measuremask = Monthly_daily["Measure"] == "Covers"
    areamask = Monthly_daily["GenericLocation"] == area

    dff = Monthly_daily[sitemask & measuremask & areamask & monthmask]

    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[lastyear])*100)) + "%"

    title = restaurant + " " + area + " " + category + " Covers: " + pchange
    measure = "Covers"

    if metric == "Totals":

        if weekmetric == "Actuals":
            y_ly = dff[lastyear]
            y_ty = dff[thisyear]
            customdata = dff["% Change"]
            ytitle = measure

        if weekmetric == "Averages":
            y_ly = dff["Average_LY"]
            y_ty = dff["Average_TY"]
            customdata = dff["Average_% Change"]
            ytitle = "Average " + measure

        hovertemplate = '%{y:.0f}'

        return week_totals(dff,
                            y_ly,
                            y_ty,
                           customdata,
                            hovertemplate,
                           title,
                          ytitle)

    if metric == "Year Change":
        hovertemplate = '%{y:+.0f}'
        if weekmetric == "Actuals":
            y = dff["Year Change"]
            customdata = dff["% Change"]
            colour = dff["Colour_CHG"]
            ytitle = measure + " vs. LY"
        if weekmetric == "Averages":
            y = dff["Average_Year Change"]
            customdata = dff["Average_% Change"]
            colour = dff["Average_Colour"]
            ytitle = "Average " + measure + " vs. LY"

        return week_change(dff,
                            y,
                           customdata,
                           colour,
                           hovertemplate,
                            title,
                          ytitle)


Month_Layout =  html.Div(children=[html.Div([html.H1(children = 'Monthly Sales',
                                                     style={'textAlign':"center",
                                                            'borderBottom': 'thin lightgrey solid',
                                                            'borderRight': 'thin lightgrey solid',
                                                           'backgroundColor': header_background_colour})]),

                                     # Month Slider

                                     html.Div([html.P(['Choose the month of the report:'],
                                                     style={'textAlign':"center",
                                                           'backgroundColor': header_background_colour}),

                                               dcc.Slider(id = 'month slider',
                                                          min = 0,
                                                          max = 11,
                                                          step = None,
                                                          marks = {int(i):all_months[i] for i in range(0,12)},
                                                          value = monthfetch)],

                                              style={'textAlign':"center",
                                                     'borderRight': 'thin lightgrey solid',
                                                     'backgroundColor': header_background_colour,
                                                      'padding': '10px 5px'}),

                                     # First Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the metric and shift of the report:']),

                                                         dcc.Dropdown(id='monthly metric dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in ["Totals", "Year Change"]],
                                                                      value="Year Change",
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='monthly shift dropdown',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_shifts],
                                                                      value='All Shifts',
                                                                      style={'width':outer_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(outer_div_width)),

                                               html.Div([html.P(['Choose the area and measure of the group summary:']),

                                                        dcc.Dropdown(id='monthly area dropdown',
                                                                     options = [{'label':i, 
                                                                                  'value':i} for i in available_areas],
                                                                      value='Full Site',
                                                                             style={'width':inner_dropdown_width}),

                                                         dcc.Dropdown(id='monthly measure dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in available_measures],
                                                                      value='Revenue',
                                                                      style={'width':inner_dropdown_width,
                                                                             'padding':'2px 0px'})],

                                                        style = div_style_simple(inner_div_width)),

                                               html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                        dcc.Dropdown(id='monthly site dropdown',
                                                                    options=[{'label':i, 
                                                                              'value':i} for i in available_restaurants],
                                                                    value='100 Wardour Street',
                                                                     style={'width':outer_dropdown_width})],

                                                       style = div_style_simple(outer_div_width))],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Graphs

                                     html.Div([html.Div([small_graph('monthly group revenue'),
                                                        small_graph('monthly group covers'),
                                                        small_graph('monthly group spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'}),

                                               html.Div([dcc.Graph(id='monthly sales total')],                                                    
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'width':600}),

                                               html.Div([small_graph('monthly site revenue'),
                                                        small_graph('monthly site covers'),
                                                        small_graph('monthly site spend')],
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'backgroundColor': 'rgb(200,200,200)'})]),

                                     # Second Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the restaurant of the week view:']),

                                                         dcc.Dropdown(id='monthly site week',
                                                                      options=[{'label':i, 
                                                                                'value':i} for i in available_restaurants_week],
                                                                      value='Group',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the area of the week view:']),

                                                        dcc.Dropdown(id='monthly area week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_areas],
                                                              value='Full Site',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the revenue category of the week view:']),

                                                        dcc.Dropdown(id='monthly category week',
                                                              options = [{'label':i, 
                                                                          'value':i} for i in available_types],
                                                              value='Total',
                                                                     style={'width':month_week_dropdown_width})],

                                                        style=month_week_dropdown_style),

                                               html.Div([html.P(['Choose the measure of the week view:']),

                                                        dcc.Dropdown(id='monthly measure week',
                                                                     options = [{'label':i, 
                                                                                 'value':i} for i in ["Revenue",
                                                                                                      "Spend"]],
                                                                     value='Revenue',
                                                                     style={'width':month_week_dropdown_width})],

                                                       style=month_week_dropdown_style ),

                                               html.Div([html.P(['Choose the metric of the week view:']),

                                                        dcc.Dropdown(id='monthly metric week',
                                                                     options = [{'label':i, 
                                                                                 'value':i} for i in ["Actuals",
                                                                                                      "Averages"]],
                                                                     value='Actuals',
                                                                     style={'width':month_week_dropdown_width})],

                                                       style=month_week_dropdown_style ) ],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Second Graph Row

                                     html.Div([html.Div([week_graph('monthly week view')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}),

                                               html.Div([week_graph('monthly week covers')],

                                                        style = {'display': 'inline-block',
                                                                'height':week_height,
                                                                'width':week_width}) ])

                                    ])


df = pd.read_csv("Tracker.csv")
tracker_daily = df[df["Table"] == "Daily"]
tracker_weekly = df[df["Table"] == "Weekly"]

tracker_available_restaurants = df["Restaurant Name"].unique()
tracker_available_weeks = df["Week Sort"].unique()
tracker_available_week_nums = df["Week Number"].unique()


templates = {'pound_total_0dec' : '£%{y:.0f}',
            'pound_change_0dec' : '£%{y:+.0f}',
             'x_pound_total_0dec': '£%{x:.0f}',
             'x_pound_change_0dec': '£%{x:+.0f}',
            'pound_total_2dec' : '£%{y:.2f}',
            'pound_change_2dec': '£%{y:+.2f}',
            'number_total_0dec': '%{y:.0f}',
            'number_change_0dec' : '%{y:+.0f}',
            'x_number_total_0dec': '%{x:.0f}',
             'x_number_change_0dec':'%{x:+.0f}',
            'custom_k' : '£%{customdata:.0f}k',
            'custom_percent_total' : '%{customdata:.0f}%',
            'custom_percent_total_1dec' : '%{customdata:.1f}%',
            'custom_percent_change' : '%{customdata:+.0f}%',
            'custom_percent_change_1dec' : '%{customdata:+.1f}%',
             'percent_total' : '%{y:.0f}%',
             'percent_total_1dec' : '%{y:.1f}%',
            'percent_change' : '%{y:+.0f}%',
            'percent_change_1dec' : '%{y:+.1f}%',
            'x_percent_total' : '%{x:.0f}%',
            'x_percent_total_1dec' : '%{x:.1f}%',
            'x_percent_change' : '%{x:+.0f}%',
            'x_percent_change_1dec' : '%{x:+.1f}%'}


tracker_mini_height = 450
tracker_mini_width = 600 

tracker_outer_div_width = 900
tracker_outer_dropdown_width = tracker_outer_div_width - 10

tracker_week_div_width = 360
tracker_week_dropdown_width = 350

tracker_week_dropdown_style = {'textAlign':'center',
                      'display': 'inline-block',
                      'width':tracker_week_div_width}

def main_graph():
    return dcc.Graph(id='tracker total',
                     style={'display': 'inline-block',
                              'height':main_height,
                              'width':main_width},
                    config={'displayModeBar':False})

def tracker_small_graph(graph_id):
    return dcc.Graph(id=graph_id,
                     style={'height':tracker_mini_height,
                            'width':tracker_mini_width},
                     config={'displayModeBar':False})

tracker_dropdowns = ['tracker week slider', 'tracker metric dropdown', 'tracker site dropdown']
tracker_dropdown_dependencies = []

for x in tracker_dropdowns:
    tracker_dropdown_dependencies.append(dash.dependencies.Input(x, 'value'))

def tracker_totals_graphs(dff,
                   xcolumn,
                   title,
                 restaurant):

    x = dff[xcolumn]
    y_ly = dff[str(lastyear)]
    y_ty = dff[str(thisyear)]
    customdata = dff["% Change"]
    colours = dff["Week Colours"]
    hovertemplate = templates["number_total_0dec"]
    texttemplate = templates["custom_percent_change"]

    data = [{'x': x,
            'y': y_ly,
            'type': 'bar',
            'name': lastyear,
            'marker':{'color':colours},
             'opacity':0.5,
            'hovertemplate':hovertemplate},

           {'x': x,
            'y': y_ty,
            'customdata':customdata,
            'type': 'bar',
            'name': thisyear,
            'marker':{'color':colours},
            'hovertemplate':hovertemplate,
            'text': customdata,
            'textposition':'outside',
            'textfont':{'size':'20'},
            'textfont_size':'20',
            'textsize':'20',
            'fontsize':'20',
            'font':{'size':'20'},
            'sizemax':'20',
            'texttemplate':texttemplate}]

    layout = {'title': title,
              'yaxis':{'title':"Covers"},
              'showlegend':False,
             'uniformtext_minsize':20}

    return {'data': data,
            'layout': layout,
           'config': {'displayModeBar': False}} 


def tracker_change_graphs(dff,
                  xcolumn,
                  title,
                 restaurant):

    x = dff[xcolumn]
    y = dff["Year Change"]
    colours = dff["Colour"]
    customdata = dff["% Change"]
    hovertemplate = templates["number_change_0dec"]
    texttemplate = templates["custom_percent_change"]

    max_change = (dff["Year Change"].append(dff["Year Change"]*-1)).max()
    y_limit = max_change*1.2

    data = [{'x': x,
            'y': y,
             'customdata': customdata,
            'type': 'bar',
            'name': "vs. Last Year",
            'marker':{'color':colours},
            'hovertemplate':hovertemplate,
            'text': customdata,
            'textposition':'outside',
            'texttemplate':texttemplate}]

    layout = {'title': title,
              'yaxis':{'title':'Covers vs. LY',
                      'range':[-y_limit, y_limit]}}

    return {'data': data,
            'layout': layout,
           'config': {'displayModeBar': False}} 



def tracker_summary_change_graph(dff,title):

    x = dff["Year Change"]
    y = dff["Restaurant Name"]
    customdata = dff["% Change"]
    colours = dff["Colour"]
    texttemplate = templates['custom_percent_change']
    hovertemplate = templates['x_number_change_0dec']

    max_change = (dff["Year Change"].append(dff["Year Change"]*-1)).max()
    x_limit = max_change*1.2

    return {'data': [{'x': x,
                      'y': y,
                      'customdata': customdata,
                      'type': 'bar',
                      'name': 'vs. Last Year',
                      'orientation':'h',
                      'marker': {'color': colours},
                      'text':customdata,
                      'textposition':'outside',
                      'texttemplate':texttemplate,
                      'hovertemplate':hovertemplate}],
            'layout': {'title': title,
                       'yaxis':{'automargin':True},
                       'xaxis':{'side':'top',
                      'range':[-x_limit, x_limit]}}}

def tracker_summary_totals_graph(dff,title):

    y = dff["Restaurant Name"]
    x_ly = dff[str(lastyear)]
    x_ty = dff[str(thisyear)]
    colours = dff["Week Colours"]
    hovertemplate = templates['x_number_total_0dec']

    return {'data': [{'x': x_ty,
                      'y': y,
                      'type': 'bar',
                      'name': str(thisyear),
                      'orientation':'h',
                      'marker': {'color': colours},
                      'hovertemplate':hovertemplate},
                    {'x': x_ly,
                      'y': y,
                      'type': 'bar',
                      'name': str(lastyear),
                     'opacity':0.5,
                      'orientation':'h',
                      'marker': {'color': colours},
                      'hovertemplate':hovertemplate}],
            'layout': {'title': title,
                       'yaxis':{'automargin':True},
                      'xaxis':{'side':'top'}}}

@app.callback(dash.dependencies.Output('tracker total', 'figure'),
              tracker_dropdown_dependencies)

def update_tracker_total(weekValue,metricValue,siteValue):

    week = tracker_available_weeks[weekValue]
    #week = weekValue
    metric = metricValue
    site = siteValue

    df = tracker_weekly
    mask1 = df["Week Sort"] == week
    mask2 = df["Restaurant Name"] != "Group"
    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[str(lastyear)])*100)) + "%"


    if metric == "Year Change":
        title = week + ": " + pchange
        return tracker_summary_change_graph(dff,title)

    elif metric == "Totals":
        title = week + ": " + pchange
        return tracker_summary_totals_graph(dff, title)


@app.callback(dash.dependencies.Output('tracker_group_eight_week', 'figure'),
              tracker_dropdown_dependencies)

def update_tracker_group_eight_week(weekValue,metricValue,siteValue):

    week = tracker_available_weeks[weekValue]
    #week = weekValue
    metric = metricValue
    site = siteValue

    df = tracker_weekly
    dff = df[df["Restaurant Name"] == "Group"]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[str(lastyear)])*100)) + "%"
    restaurant = "Group"
    xcolumn = "Week Sort"
    title = "Next 8 Weeks - Group"

    if metric == "Year Change":
        return tracker_change_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)

    elif metric == "Totals":
        return tracker_totals_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)


@app.callback(dash.dependencies.Output('tracker_group_week', 'figure'),
              tracker_dropdown_dependencies)

def update_tracker_group_week(weekValue,metricValue,siteValue):

    week = tracker_available_weeks[weekValue]
    #week = weekValue
    metric = metricValue
    site = siteValue

    df = tracker_daily
    mask1 = df["Restaurant Name"] == "Group"
    mask2 = df["Week Sort"] == week
    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[str(lastyear)])*100)) + "%"
    restaurant = "Group"
    xcolumn = "Day of Week"
    title = week + " - Group: " + pchange

    if metric == "Year Change":
        return tracker_change_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)

    elif metric == "Totals":
        return tracker_totals_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)

@app.callback(dash.dependencies.Output('tracker_site_eight_week', 'figure'),
              tracker_dropdown_dependencies)

def update_tracker_site_eight_week(weekValue,metricValue,siteValue):

    week = tracker_available_weeks[weekValue]
    #week = weekValue
    metric = metricValue
    site = siteValue

    df = tracker_weekly
    dff = df[df["Restaurant Name"] == site]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[str(lastyear)])*100)) + "%"
    restaurant = site
    xcolumn = "Week Sort"
    title = "Next 8 Weeks - " + site

    if metric == "Year Change":
        return tracker_change_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)

    elif metric == "Totals":
        return tracker_totals_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)


@app.callback(dash.dependencies.Output('tracker_site_week', 'figure'),
              tracker_dropdown_dependencies)

def update_tracker_site_week(weekValue,metricValue,siteValue):

    week = tracker_available_weeks[weekValue]
    #week = weekValue
    metric = metricValue
    site = siteValue

    df = tracker_daily
    mask1 = df["Restaurant Name"] == site
    mask2 = df["Week Sort"] == week
    dff = df[mask1 & mask2]
    pchange = plus(round((dff.sum()["Year Change"] / dff.sum()[str(lastyear)])*100)) + "%"
    restaurant = site
    xcolumn = "Day of Week"
    title = week + " - " + site + ": " + pchange

    if metric == "Year Change":
        return tracker_change_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)

    elif metric == "Totals":
        return tracker_totals_graphs(dff,
                             xcolumn,
                             title,
                             restaurant)
    
Tracker_Layout =  html.Div(children=[html.Div([html.H1(children = 'Cover Tracker',
                                                     style={'textAlign':"center",
                                                            'borderBottom': 'thin lightgrey solid',
                                                            'borderRight': 'thin lightgrey solid',
                                                           'backgroundColor': header_background_colour})]),

                                     # Week Slider

                                     html.Div([html.P(['Choose the week of the report:'],
                                                     style={'textAlign':"center",
                                                            'borderRight': 'thin lightgrey solid',
                                                           'backgroundColor': header_background_colour}),

                                               dcc.Slider(id = 'tracker week slider',
                                                          min = 0,
                                                          max = 8,
                                                          step = None,
                                                          marks = {int(i):tracker_available_weeks[i] for i in range(0,9)},
                                                          value = 0)],

                                              style={'textAlign':"center",
                                                     'borderRight': 'thin lightgrey solid',
                                                     'backgroundColor': header_background_colour,
                                                      'padding': '10px 5px'}),

                                     # First Dropdown Row

                                     html.Div([html.Div([html.P(['Choose the metric of the report:']),

                                                         dcc.Dropdown(id='tracker metric dropdown',
                                                                      options = [{'label':i, 
                                                                                  'value':i} for i in ["Totals", "Year Change"]],
                                                                      value="Year Change",
                                                                             style={'width':tracker_outer_dropdown_width,
                                                                                   'padding':'2px 0px'})],

                                                        style = div_style_simple(tracker_outer_div_width)),

                                                html.Div([html.P(['Choose the restaurant of the site analysis:']),

                                                        dcc.Dropdown(id='tracker site dropdown',
                                                                    options=[{'label':i, 
                                                                              'value':i} for i in tracker_available_restaurants],
                                                                    value='100 WDST Club',
                                                                     style={'width':tracker_outer_dropdown_width})],

                                                       style = div_style_simple(tracker_outer_div_width))],

                                              style = {'borderBottom': 'thin lightgrey solid',
                                                       'borderRight': 'thin lightgrey solid',
                                                      'backgroundColor': dropdown_background_colour,
                                                      'padding': '10px 5px'}),

                                     # Graphs

                                     html.Div([html.Div([tracker_small_graph('tracker_group_eight_week'),
                                                        tracker_small_graph('tracker_group_week')],
                                                        style = {'display': 'inline-block',
                                                                'height':900}),

                                               html.Div([main_graph()],                                                    
                                                        style = {'display': 'inline-block',
                                                                'height':900,
                                                                'width':600}),

                                               html.Div([tracker_small_graph('tracker_site_eight_week'),
                                                         tracker_small_graph('tracker_site_week')],
                                                        style = {'display': 'inline-block',
                                                                'height':900})]) ])

df = pd.read_csv("Sales Mix.csv")
summary_df = df[df["Table Type"] == "Summary"]
category_df = df[df["Table Type"] == "Category"]
price_df = df[df["Table Type"] == "Price Bracket"]

available_summary_categories = df["Summary Category"].unique()
available_summary_measures = ["Sales", "Profit", "Margin"]
sales_mix_available_restaurants = df["Restaurant"].unique()
sales_mix_available_months = df["Month"].unique()
available_metrics = ["Totals", "Year Change"]
available_categories = price_df["Table"].unique()

grey_background_colour = "rgb(250,250,250)"

restaurant_height = 1000
restaurant_width = 600

graph_height = restaurant_height/3
graph_width = 400

dropdown_width = 600
top_dropdown_width = 900

intro_text = ['Summary category:',
              'Summary measure:',
              'Choose the restaurant of the site analysis:',
              'Choose the month of the report:',
              'Choose the metric of the report:',
             'Choose the category of the site analysis:']  

dropdown_id = ['sales mix summary category dropdown','sales mix summary measure dropdown','sales mix site dropdown', 'sales mix month dropdown', 'sales mix metric dropdown', 'sales mix category dropdown']

available_values = [available_summary_categories, available_summary_measures, sales_mix_available_restaurants, sales_mix_available_months, available_metrics, available_categories]

initial_value = ['Beverage',"Sales",'Group', sales_mix_available_months[-1], 'Year Change', available_categories[0]] 

def dropdown(intro_text,
             dropdown_id,
            available_values,
            initial_value,
            width):
    return html.Div([html.P([intro_text]),
                     dcc.Dropdown(id=dropdown_id,
                                  options=[{'label':i, 
                                            'value':i} for i in available_values],
                                  value=initial_value,
                                  style={'width':(width-10)})],
                    style={'display':'inline-block',
                           'width':width,
                           'padding': '10px 5px'})

def small_dropdown(dropdown_id,
                    available_values,
                    initial_value,
                    width):
    return dcc.Dropdown(id=dropdown_id,
                          options=[{'label':i, 
                                    'value':i} for i in available_values],
                          value=initial_value,
                          style={'width':(width)})

def graph(graph_id, height, width):
    return dcc.Graph(id=graph_id,
                     style={'height':height,
                          'width':width},
                    config={'displayModeBar':False})

def standard_graph(graph_id):
    return dcc.Graph(id=graph_id,
                     style={'height':graph_height,
                          'width':graph_width},
                    config={'displayModeBar':False})

def graph_div(graph_id):
    return html.Div([dcc.Graph(id=graph_id,
                                style={'height':graph_height,
                                      'width':graph_width},
                                config={'displayModeBar':False})],

                    style = {'height':graph_height,
                             'width':graph_width})

sales_mix_dropdown_dependencies = []

for i in dropdown_id:
    sales_mix_dropdown_dependencies.append(dash.dependencies.Input(i, 'value'))

def sales_mix_totals_graph(siteValue,
                monthValue,
                measureValue,
                 dff,
                 xcolumn,
                 table):

    site = siteValue
    month = monthValue
    measure = measureValue

    df = dff
    mask1 = df["Restaurant"] == site
    mask2 = df["Month"] == month
    dff = df[mask1 & mask2]

    x = dff[xcolumn]
    y_ly = dff[measure + " " + lastyear]
    y_ty = dff[measure + " " + thisyear]
    colours = dff["Drink Colour"]

    if measure == "Sales" or measure == "Profit":
        customdata_ly = y_ly/1000
        customdata_ty = y_ty/1000
        hovertemplate = templates['custom_k']
    if measure == "Margin":
        customdata_ly = y_ly
        customdata_ty = y_ty
        hovertemplate = templates['custom_percent_total_1dec']

    if xcolumn == "Summary Category":
        title = table + " " + measure  
    elif xcolumn == "Category":
        title = "Category Analysis: " + table + " " + measure  
    elif xcolumn == "Price Bracket":
        title = "Price Analysis: " + table + " " + measure

    restaurant = site

    data = [{'x': x,
            'y': y_ly,
             'customdata': customdata_ly,
            'type': 'bar',
            'name': lastyear,
            'marker':{'color':colours},
             'opacity':0.5,
            'hovertemplate':hovertemplate},

            {'x': x,
            'y': y_ty,
             'customdata': customdata_ty,
            'type': 'bar',
            'name': thisyear,
            'marker':{'color':colours},
            'hovertemplate':hovertemplate}]

    if title[:5] == "Price":
        layout = {'title': title,
                  'yaxis':{'title':measure},
                  'xaxis':{'title':"Cost Price"},
                   'annotations': [site_annotation(restaurant)],
                  'showlegend':False}
    else:
        layout = {'title': title,
                  'yaxis':{'title':measure},
                   'annotations': [site_annotation(restaurant)],
                  'showlegend':False}

    return {'data': data,
            'layout': layout,
           'config': {'displayModeBar': False}}


def sales_mix_change_graph(siteValue,
                monthValue,
                measureValue,
               dff,
               xcolumn,
               table):

    site = siteValue
    month = monthValue
    measure = measureValue

    df = dff
    mask1 = df["Restaurant"] == site
    mask2 = df["Month"] == month
    dff = df[mask1 & mask2]

    x = dff[xcolumn]
    y = dff[measure + " Year Change"]
    colours = dff[measure + " Colour"]

    if measure == "Sales" or measure == "Profit":
        customdata = dff[measure + " % Change"]
        texttemplate = templates['custom_percent_change']
        hovertemplate = templates['pound_change_0dec']
    else:
        customdata = dff[measure + " Year Change"]
        texttemplate = templates['custom_percent_change_1dec']
        hovertemplate = templates['percent_change_1dec']

    if xcolumn == "Summary Category":
        title = table + " " + measure  
    elif xcolumn == "Category":
        title = "Category Analysis: " + table + " " + measure  
    elif xcolumn == "Price Bracket":
        title = "Price Analysis: " + table + " " + measure  

    restaurant = site

    data = [{'x': x,
            'y': y,
             'customdata': customdata,
            'type': 'bar',
            'name': "vs. Last Year",
            'marker':{'color':colours},
            'hovertemplate':hovertemplate,
            'text': customdata,
            'textposition':'auto',
            'texttemplate':texttemplate}]

    if title[:5] == "Price":
        layout = {'title': title,
                  'yaxis':{'title':measure + ' vs. LY'},
                  'xaxis':{'title':"Cost Price"},
                   'annotations': [site_annotation(restaurant)]}
    else:
        layout = {'title': title,
                  'yaxis':{'title':measure + ' vs. LY'},
                   'annotations': [site_annotation(restaurant)]}

    return {'data': data,
            'layout': layout,
           'config': {'displayModeBar': False}} 

@app.callback(dash.dependencies.Output('sales mix restaurant breakdown', 'figure'),
            sales_mix_dropdown_dependencies)    

def update_sales_mix_restaurant_breakdown(summarycategoryValue,
                                        summarymeasureValue,
                                        siteValue,
                                        monthValue,
                                        metricValue,
                                       categoryValue):

    summarycategory = summarycategoryValue
    measure = summarymeasureValue
    site = siteValue
    month = monthValue
    metric = metricValue
    category = categoryValue

    df = summary_df

    mask1 = df["Summary Category"] == summarycategory
    mask2 = df["Restaurant"] != "Group"
    mask3 = df["Month"] == month

    dff = df[mask1 & mask2 & mask3].sort_values(by="Restaurant", ascending=False)

    if metric == "Totals":

        y = dff["Restaurant"]
        x_ty = dff[measure + " " + thisyear]
        x_ly = dff[measure + " " + lastyear]
        colours = dff["Drink Colour"]

        if measure == "Sales" or measure == "Profit":
            customdata_ty = x_ty/1000
            customdata_ly = x_ly/1000
            hovertemplate = templates['custom_k']
            pchange = plus(round((dff.sum()[measure +" Year Change"] / dff.sum()[measure + " " + lastyear])*100)) + "%"
        else:
            customdata_ty = x_ty
            customdata_ly = x_ly
            hovertemplate = templates['x_percent_total_1dec']

            sales_ly = dff.sum()["Sales " + lastyear]
            sales_ty = dff.sum()["Sales " + thisyear]
            profit_ly = dff.sum()["Profit " + lastyear]
            profit_ty = dff.sum()["Profit " + thisyear]
            margin_ly = profit_ly / sales_ly
            margin_ty = profit_ty / sales_ty

            pchange = plus(round((((margin_ty - margin_ly)/margin_ly)*100),1)) + "%"

        title = summarycategory + " " + measure + ": " + pchange

        max_change = (dff[measure + " Year Change"].append(dff[measure + " Year Change"]*-1)).max()
        x_limit = max_change*1.2

        data = [{'x': x_ty,
                'y': y,
                 'customdata': customdata_ty,
                'type': 'bar',
                 'orientation':'h',
                'name': thisyear,
                'marker':{'color':colours},
                'hovertemplate':hovertemplate},
               {'x': x_ly,
                'y': y,
                 'customdata': customdata_ly,
                'type': 'bar',
                 'orientation':'h',
                'opacity':0.5,
                'name': lastyear,
                'marker':{'color':colours},
                'hovertemplate':hovertemplate}]

        layout = {'title': title,
                  'yaxis':{'automargin':True},
                  'xaxis':{'side':'top'}}

        config = {'displayModeBar': False}

        return {'data': data,
                'layout': layout,
               'config': config}

    if metric == "Year Change":

        y = dff["Restaurant"]
        x = dff[measure + " Year Change"]
        colours = dff[measure + " Colour"]

        if measure == "Sales" or measure == "Profit":
            customdata = dff[measure + " % Change"]
            texttemplate = templates['custom_percent_change']
            hovertemplate = templates['x_pound_change_0dec']
            pchange = plus(round((dff.sum()[measure +" Year Change"] / dff.sum()[measure + " " + lastyear])*100)) + "%"
        else:
            customdata = dff[measure + " Year Change"]
            texttemplate = templates['custom_percent_change_1dec']
            hovertemplate = templates['x_percent_change_1dec']

            sales_ly = dff.sum()["Sales " + lastyear]
            sales_ty = dff.sum()["Sales " + thisyear]
            profit_ly = dff.sum()["Profit " + lastyear]
            profit_ty = dff.sum()["Profit " + thisyear]
            margin_ly = profit_ly / sales_ly
            margin_ty = profit_ty / sales_ty

            pchange = plus(round((((margin_ty - margin_ly)/margin_ly)*100),1)) + "%"

        title = summarycategory + " " + measure + ": " + pchange

        max_change = (dff[measure + " Year Change"].append(dff[measure + " Year Change"]*-1)).max()
        x_limit = max_change*1.2

        data = [{'x': x,
                'y': y,
                 'customdata': customdata,
                'type': 'bar',
                 'orientation':'h',
                'name': "vs. Last Year",
                'marker':{'color':colours},
                'hovertemplate':hovertemplate,
                'text': customdata,
                'textposition':'auto',
                'texttemplate':texttemplate}]

        layout = {'title': title,
                  'yaxis':{'automargin':True},
                  'xaxis':{'side':'top',
                           'range':[-x_limit, x_limit]}}

        config = {'displayModeBar': False}

        return {'data': data,
                'layout': layout,
               'config': config}


@app.callback(dash.dependencies.Output('sales mix summary sales', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_summary_sales(summarycategoryValue,
                        summarymeasureValue,
                        siteValue,
                        monthValue,
                        metricValue,
                       categoryValue):

    measureValue = "Sales"
    metric = metricValue
    dff = summary_df
    xcolumn = "Summary Category"
    table = "Beverage"

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix summary profit', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_summary_profit(summarycategoryValue,
                        summarymeasureValue,
                        siteValue,
                        monthValue,
                        metricValue,
                       categoryValue):

    measureValue = "Profit"
    metric = metricValue
    dff = summary_df
    xcolumn = "Summary Category"
    table = "Beverage"

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix summary margin', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_summary_margin(summarycategoryValue,
                            summarymeasureValue,
                            siteValue,
                            monthValue,
                            metricValue,
                           categoryValue):

    measureValue = "Margin"
    metric = metricValue
    dff = summary_df
    xcolumn = "Summary Category"
    table = "Beverage"

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)


@app.callback(dash.dependencies.Output('sales mix category sales', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_category_sales(summarycategoryValue,
                            summarymeasureValue,
                            siteValue,
                            monthValue,
                            metricValue,
                           categoryValue):

    measureValue = "Sales"
    metric = metricValue

    wines = ["White Wine",
             "Red Wine",
             "Sparkling Wine", 
             "Rose Wine", 
             "Fortified Wine", 
             "Sweet Wine", 
             "Fine Wine"]

    if categoryValue in wines:
        classValue = "Wine"
    else:
        classValue = categoryValue

    df = category_df
    dff = df[df["Table"] == classValue]
    xcolumn = "Category"
    table = classValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix category profit', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_category_profit(summarycategoryValue,
                            summarymeasureValue,
                            siteValue,
                            monthValue,
                            metricValue,
                           categoryValue):

    measureValue = "Profit"
    metric = metricValue

    wines = ["White Wine",
             "Red Wine",
             "Sparkling Wine", 
             "Rose Wine", 
             "Fortified Wine", 
             "Sweet Wine", 
             "Fine Wine"]

    if categoryValue in wines:
        classValue = "Wine"
    else:
        classValue = categoryValue

    df = category_df
    dff = df[df["Table"] == classValue]
    xcolumn = "Category"
    table = classValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix category margin', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_category_margin(summarycategoryValue,
                            summarymeasureValue,
                            siteValue,
                            monthValue,
                            metricValue,
                           categoryValue):

    measureValue = "Margin"
    metric = metricValue

    wines = ["White Wine",
             "Red Wine",
             "Sparkling Wine", 
             "Rose Wine", 
             "Fortified Wine", 
             "Sweet Wine", 
             "Fine Wine"]

    if categoryValue in wines:
        classValue = "Wine"
    else:
        classValue = categoryValue

    df = category_df
    dff = df[df["Table"] == classValue]
    xcolumn = "Category"
    table = classValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)


@app.callback(dash.dependencies.Output('sales mix price sales', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_price_sales(summarycategoryValue,
                        summarymeasureValue,
                        siteValue,
                        monthValue,
                        metricValue,
                       categoryValue):

    measureValue = "Sales"
    metric = metricValue
    df = price_df
    dff = df[df["Table"] == categoryValue]
    xcolumn = "Price Bracket"
    table = categoryValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix price profit', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_price_profit(summarycategoryValue,
                        summarymeasureValue,
                        siteValue,
                        monthValue,
                        metricValue,
                       categoryValue):

    measureValue = "Profit"
    metric = metricValue
    df = price_df
    dff = df[df["Table"] == categoryValue]
    xcolumn = "Price Bracket"
    table = categoryValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

@app.callback(dash.dependencies.Output('sales mix price margin', 'figure'),
             sales_mix_dropdown_dependencies)    

def update_sales_mix_price_margin(summarycategoryValue,
                        summarymeasureValue,
                        siteValue,
                        monthValue,
                        metricValue,
                       categoryValue):

    measureValue = "Margin"
    metric = metricValue
    df = price_df
    dff = df[df["Table"] == categoryValue]
    xcolumn = "Price Bracket"
    table = categoryValue

    if metric == "Totals":
        return sales_mix_totals_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)

    if metric == "Year Change":
        return sales_mix_change_graph(siteValue,
                            monthValue,
                            measureValue,
                           dff,
                           xcolumn,
                           table)


Sales_Mix_Layout =  html.Div(children=[html.Div([html.H1(children = 'Beverage Sales Mix',
                                                         style={'textAlign':"center",
                                                               'borderBottom': 'thin lightgrey solid',
                                                                'borderRight': 'thin lightgrey solid',
                                                               'backgroundColor': grey_background_colour})]),

                                         # Dropdown Row

                                        html.Div([dropdown(intro_text[3],dropdown_id[3],available_values[3],initial_value[3], top_dropdown_width),
                                                   dropdown(intro_text[4],dropdown_id[4],available_values[4],initial_value[4], top_dropdown_width)],

                                                style={'textAlign':"center",
                                                        'borderRight': 'thin lightgrey solid',
                                                       'backgroundColor': grey_background_colour}),   

                                         # Dropdown Row 2

                                         html.Div([html.Div([html.P([intro_text[0]]),
                                                             small_dropdown(dropdown_id[0],available_values[0],initial_value[0], (restaurant_width/2))],                                                                                                        

                                                    style = {'display': 'inline-block',
                                                           'padding': '10px 5px'}),

                                                   html.Div([html.P([intro_text[1]]),
                                                             small_dropdown(dropdown_id[1],available_values[1],initial_value[1], (restaurant_width/2))],                                                                                                        

                                                    style = {'display': 'inline-block',
                                                           'padding': '10px 5px'}),


                                                   dropdown(intro_text[2],dropdown_id[2],available_values[2],initial_value[2], dropdown_width),
                                                   dropdown(intro_text[5],dropdown_id[5],available_values[5],initial_value[5], dropdown_width)],

                                                 style={'textAlign':"center",
                                                       'borderBottom': 'thin lightgrey solid',
                                                        'borderRight': 'thin lightgrey solid',
                                                       'backgroundColor': grey_background_colour}),


                                         # Graph Row

                                         html.Div([html.Div([graph('sales mix restaurant breakdown',
                                                                  restaurant_height, 
                                                                  restaurant_width)],

                                                           style = {'display': 'inline-block'}),

                                                   html.Div([standard_graph('sales mix summary sales'),
                                                             standard_graph('sales mix category sales'),
                                                             standard_graph('sales mix price sales')],

                                                           style = {'display': 'inline-block'}),

                                                   html.Div([standard_graph('sales mix summary profit'),
                                                             standard_graph('sales mix category profit'),
                                                             standard_graph('sales mix price profit')],

                                                           style = {'display': 'inline-block'}),

                                                   html.Div([standard_graph('sales mix summary margin'),
                                                             standard_graph('sales mix category margin'),
                                                             standard_graph('sales mix price margin')],

                                                           style = {'display': 'inline-block'})

                                                  ])                                
                                        ])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/daily-sales':
        return Daily_Layout
    if pathname == '/wtd-sales':
        return WTD_Layout
    if pathname == '/mtd-sales':
        return MTD_Layout
    if pathname == '/weekly-sales':
        return Week_Layout
    if pathname == '/monthly-sales':
        return Month_Layout
    if pathname == '/tracker':
        return Tracker_Layout
    if pathname == '/sales-mix':
        return Sales_Mix_Layout
    else:
        return home_page
    
if __name__ == '__main__':
    app.run_server(debug=False)
