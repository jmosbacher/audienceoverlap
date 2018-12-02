from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout, column, row, widgetbox
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker,
                          Slider, Button, Label, CategoricalColorMapper)
from bokeh.palettes import Spectral6, Category20
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, Paragraph, Div
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
import pandas as pd

from pages import Page, DataImport, OverlapVisualization
import itertools


doc = curdoc()

data_store = {
    "audiences": pd.DataFrame(),
    "overlaps": pd.DataFrame(),
}

adata = {k:[] for k in Page.AUD_COLUMNS}
odata = {k:[] for k in Page.OVERLAP_COLUMNS}

sources ={
    "audiences": ColumnDataSource(adata),
    "overlaps": ColumnDataSource(odata),
}

warning = Div(text='''<p><font color="red">WARNING! </font> This is a proof of concept hacked together over a couple of days.
 There will be bugs! Please report them on github.com/jmosbacher/audienceoverlap. Tested only with chrome on Linux.</p>''', width=700)
p1 = DataImport(doc, sources, data_store).build_layout()
tab1 = Panel(child=p1, title="Data Import")

p2 = OverlapVisualization(doc, sources, data_store).build_layout()
tab2 = Panel(child=p2, title="Visualization")

# p3 = HeatmapOverlaps(doc, sources, data_store).build_layout()
# tab3 = Panel(child=p3, title="Heatmap Overlaps")
tabs1 = Tabs(tabs=[ tab1], width=800, height=350)
tabs2 = Tabs(tabs=[  tab2 ], width=800)
# tabs3 = Tabs(tabs=[ tab3 ], width=800)
c = column(warning,tabs1,tabs2, width=800)
doc.add_root(c)
