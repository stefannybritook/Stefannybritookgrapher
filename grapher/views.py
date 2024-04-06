from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render
import json

import sympy
import sympy.plotting
from sympy import symbols, E
from sympy.parsing.latex import parse_latex
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.models import HoverTool, Range1d, WheelZoomTool

def plot(request):
    if request.method == "POST":
        x = symbols('x')
        TOOLTIPS = [
            ("(x,y)", "($x, $y)"),
        ]
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        latex = body['latex_string']
        # latex = "\\csc\\left(x+3\\right)"
        # latex = "\\frac{1}{x}"
        equation = parse_latex(rf"{latex}")
        print(equation)
        plot = sympy.plot(
            equation,
            ("x", -15, 15),
            show=False,
        )
        x, y = plot[0].get_data()
        x_points = np.asarray(x) 
        y_points = np.asarray(y) 
        for i in y_points:
            if (i != None):
                if not (-100 < i < 100):
                    y_points[y_points>100] = np.inf
                    y_points[y_points<-100] = -np.inf
        p = figure(
            toolbar_location="below", 
            title=f"f(x) = {equation}", 
            tooltips=TOOLTIPS,
        )
        p.y_range = Range1d(-5, 5)
        p.line(x_points, y_points, line_width=2, color="firebrick", alpha=.8)
        
        hover = HoverTool(tooltips=TOOLTIPS, mode='vline')
        p.add_tools(hover)
        p.toolbar.active_scroll = p.select_one(WheelZoomTool)
        item_text = json_item(p, "myplot")
        return JsonResponse(item_text)

def index(request):
    return render(request, 'index.html', {"points": ""})
