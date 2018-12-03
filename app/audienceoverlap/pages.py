


from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout, column, row, widgetbox
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker, CDSView,LinearColorMapper,
                          Slider, Button, Label, CategoricalColorMapper, IndexFilter)
from bokeh.palettes import Spectral6, Category20, Magma, Viridis,Plasma,Inferno
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, TextInput, PasswordInput, Paragraph
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Select, PreText

import pandas as pd
import numpy as np
from data import (read_google_sheet, add_audience_columns, random_data,
 read_audience_list,fetch_overlaps_fbapi, place_circles, gsheet_email)


class Page:
    AUD_COLUMNS = ["name", "account_id","id","approximate_count",
        "approximate_count_txt","c", "r", "x", "y"]

    OVERLAP_COLUMNS = ["xid", "yid", "xname", "yname", "xsize", 'ysize', 
        "overlap","overlap_perc", "overlap_perc_txt", "color"]

    def __init__(self, doc,sources, data, trigger_update=None):
        self.doc = doc
        self.asource = sources["audiences"]
        self.osource = sources["overlaps"]
        self.data = data

        # self.trigger_update = trigger_update

    def build_layout(self):
        pass

    def data_changed(self):
        pass


class DataImport(Page):

    def load_random(self):
        try:
            self.load_random_btn.disabled = True
            n = self.random_n.value
            aud_df, ov_df = random_data(N=n)
            adata = add_audience_columns(aud_df)
            self.data["audiences"] = adata
            self.data["overlaps"] = ov_df
            self.asource.data = adata.to_dict(orient='list')
        finally:
            self.load_random_btn.disabled = False

    def load_gsheet_auds(self):
        try:
            self.load_gsheet_btn.disabled = True
            gsheet_key = self.gsheet_key_inp.value
            aud_df, ov_df = read_google_sheet(gsheet_key)
            
            self.data["overlaps"] = ov_df
            data = add_audience_columns(aud_df)
            self.asource.data = data.to_dict(orient='list')
            
        finally:
            self.load_gsheet_btn.disabled = False

    def load_auds(self):
        try:
            self.load_btn.disabled = True
            acctid = self.acctid_inp.value
            appid = self.appid_inp.value
            appsec = self.appsec_inp.value
            token = self.token_inp.value
            data = read_audience_list(acctid, appid, appsec, token)
            overlaps = fetch_overlaps_fbapi(data["id"] ,acctid, token)
            self.data["overlaps"] = overlaps
            self.asource.data = data.to_dict(orient='list')
        finally:
            self.load_btn.disabled = False

    def build_layout(self):
        self.appid_inp = TextInput(title='App ID', placeholder='App ID', width=350)
        self.acctid_inp = TextInput(title='Account ID', placeholder='Account ID', width=350)
        self.appsec_inp = PasswordInput(title='App secret', placeholder='App secret', width=350)
        self.token_inp = TextInput(title='FB Token', placeholder='FB Token',  width=350)

        self.load_btn = Button(label='Load from Facebook', button_type="primary", width=700)
        self.load_btn.on_click(self.load_auds)

        self.gsheet_key_inp = TextInput(title=f'Google Sheet ID (shared with {gsheet_email})',
                         value="1MmfJr8blGKVMbH7lVoSq7GIPqVqq3q3BYGoEJj9cYdw", width=700)

        # gsheet_text = Paragraph(text=f"* Must be a correctly formatted google sheet ", width=700)
        self.load_gsheet_btn = Button(label='Load from Google Sheet', button_type="success", width=700)
        self.load_gsheet_btn.on_click(self.load_gsheet_auds)


        self.random_n =  self.maxaud_inp = Slider(start=2, end=100, value=20, 
                step=1, title="Number of audiences", disabled=False)
        self.load_random_btn = Button(label='Load Random Data', button_type="default", width=700)
        self.load_random_btn.on_click(self.load_random)

        cols = [
            TableColumn(field="name", title="Name", width=200),
            TableColumn(field="account_id", title="Account ID",),
            TableColumn(field="id", title="Audience ID",),
            TableColumn(field="approximate_count", title="Est. size",),
        ]
        #self.asource = ColumnDataSource()
        self.aud_list = DataTable(source=self.asource ,columns=cols, width=700, height=280)
        ids = row(self.appid_inp, self.acctid_inp)
        creds = row(self.token_inp, self.appsec_inp, )
        fb = Panel(title='Facebook', child=column(ids, creds, self.load_btn))
        gsheets = Panel(title='GSheet', child=column(self.gsheet_key_inp,self.load_gsheet_btn) )
        rndm = Panel(title='Random',child=column(self.random_n, self.load_random_btn)  )
        aud =  Panel(child=self.aud_list)
        lo = Tabs(tabs=[fb, gsheets, rndm],width=800)
        return lo
        

class OverlapVisualization(Page):
    
    def data_changed(self,attr,old,new):
        self.pivot_inp.options = [n for n in self.asource.data.get("name",[])]

    def selected_changed(self,attr,old,new):
        if len(self.asource.selected.indices):
            self.show_btn.disabled = False
        else:
            self.show_btn.disabled = True

    def show_overlaps(self):
        try:
            self.show_btn.disabled = True
            maxaud = self.maxaud_inp.value
            thresh = self.thresh_inp.value
            rankby = self.rankby_inp.value
            method = self.method_inp.value
            substrings = self.substring_inp.value.split(',')
            pivot = self.pivot_inp.value
            pividx = 0
            idxs = []
            for idx, name in enumerate(self.asource.data["name"]):
                if name==pivot: 
                    pividx = idx
                elif any([s in name for s in substrings]+['' in substrings]):
                    idxs.append(idx)
                elif idx in self.asource.selected.indices:
                    idxs.append(idx)

            # print(pividx)
            # idxs = self.asource.selected.indices
            if len(idxs)<1:
                raise RuntimeError('Nothing selected')

            if pividx in idxs:
                idxs.remove(pividx)

            data = {k:[vs[idx] for idx in idxs] for k, vs in self.asource.data.items()}
            
            overlaps = self.data["overlaps"].to_dict()
            # print(overlaps)
            df = pd.DataFrame(data)
            pivid = self.asource.data["id"][pividx]
            df["overlap"] = [overlaps[pivid][aid] for aid in df["id"]]
            sortby = {'size':'approximate_count', "overlap": "overlap"}[rankby]
            df["idx"] = idxs
            df = df.sort_values(sortby, ascending=False)

            data = df.to_dict(orient='list')
            for k, vs in self.asource.data.items():
                data[k] = [vs[pividx]] + data[k]
            data["idx"] = [pividx] + data["idx"]
            data["overlap"] = [data["approximate_count"][0]] + data["overlap"]
            
            norm = np.max(data["approximate_count"])
            # sizes = {aid:size for aid, size in zip(self.asource.data["id"], self.asource.data["approximate_count"])}
            os = [[overlaps[audid1][audid2]/norm for audid2 in data['id']] for audid1 in data['id']]
            rs = np.sqrt(np.array(data["approximate_count"])/norm)
        
            xs, ys = place_circles(rs, os, thresh, method=method)
      
  
            p = { 'x' : [(idx, x)  for idx, x in zip(data["idx"], xs)], 
                    'y' : [(idx, y) for idx, y in zip(data["idx"], ys)],
                    'r': [(idx, r) for idx, r in zip(data["idx"], rs)]}
            
            self.asource.patch(p)
          
            self.update_heatmap(data["idx"])
            self.view.filters = [IndexFilter(data["idx"])]
            self.tabs.active = 1
            self.asource.selected.update(indices = [])
        except Exception as e:
            # raise e
            print(e)
        finally:
            self.show_btn.disabled = False

    def build_options(self):
        self.maxaud_inp = Slider(start=0, end=10, value=4, 
                step=1, title="Max audiences per group", disabled=False)
        self.thresh_inp = Slider(start=0, end=1, value=0.1, step=0.05, title="Overlap threshold")
        self.rankby_inp = Select(title='Order by',options=['size', 'overlap'], value='overlap')
        self.pivot_inp = Select(title='Pivot Audience',
                                options=[n for n in self.asource.data.get("name",[])])
        self.method_inp = Select(title='Preserve overlap',options=[('pivot','previous + pivot' ), ('chain','previous two')], value='pivot', )
        self.asource.on_change("data", self.data_changed)
        # self.asource.selected.on_change("indices", self.selected_changed)
        self.substring_inp = TextInput(title='Match substrings (, seperated)', placeholder='*', width=700)

        cols = [
            TableColumn(field="name", title="Name", width=200),
            TableColumn(field="account_id", title="Account ID",),
            TableColumn(field="id", title="Audience ID",),
            TableColumn(field="approximate_count", title="Est. size",),
        ]
        #self.source = ColumnDataSource()
        self.aud_list_title = Paragraph(text="Manual Selection")
        self.aud_list = DataTable(source=self.asource ,columns=cols, width=700, height=280)
        self.show_btn = Button(label='Show Overlaps', button_type="success", width=500, disabled=False)
        self.show_btn.on_click(self.show_overlaps)
        first = row(self.pivot_inp, )
        second = row(self.method_inp, self.rankby_inp)
        third = row(self.thresh_inp)
        options = column(self.substring_inp,self.aud_list_title, self.aud_list, first, second, third, self.show_btn)
        return options


    def build_venn_figure(self):
        TOOLS = "hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save,"
        TOOLTIPS = [
        ("index", "$index"),
        ("Name", "@name"),
        ("Size", "@approximate_count"),
        ]
        self.view = CDSView(source=self.asource, filters=[IndexFilter([0])])

        p = figure(tools=TOOLS, y_range=[-2,2], x_range=[-2,2], plot_width=700, plot_height=600,
        tooltips=TOOLTIPS)
        # self.osource = ColumnDataSource(self.source.data)
        p.circle(x='x', y='y', radius='r',line_color='c', source=self.asource, view=self.view,
                fill_alpha=0.2, selection_line_color="firebrick",
                nonselection_fill_color=None, selection_fill_color=None,
                fill_color=None)
        p.text(x='x', y='y',text='approximate_count_txt',source=self.asource, text_font_size='12px',
         text_align='center', text_baseline='middle',text_color='c', view=self.view,selection_text_color="firebrick",)
        # l = column(s, p)
        p.xgrid.visible = False
        p.ygrid.visible = False
        p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

        p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        # output_file("color_scatter.html", title="color_scatter.py example")
        p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
        p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
        return p

    def build_layout(self):
        options = self.build_options()
        venn_fig = self.build_venn_figure()
        heatmap_fig = self.build_heatmap_figure()
        tab1 = Panel(title='Audience Selection',child=options)
        tab2 = Panel(title='Venn Diagrams',child=venn_fig)
        tab3 = Panel(title='Heatmap',child=heatmap_fig)
        self.tabs = Tabs(tabs=[tab1, tab2, tab3], width=800)
        return self.tabs

    def update_heatmap(self, idxs):
        color_map = Inferno[256]
        all_ovs = self.data["overlaps"].to_dict()
        ids = [self.asource.data["id"][idx] for idx in idxs]
        overlaps = {audid1: {audid2: all_ovs[audid1][audid2] for audid2 in ids} for audid1 in ids}
        
        data = {k:[] for k in self.OVERLAP_COLUMNS}

        all_vals = np.unique([[x for x in col.values()] for col in overlaps.values()])
        mn = np.min(all_vals)
        mx = np.max(all_vals)
        # ids = self.asource.data["id"]
        names = [self.asource.data["name"][idx] for idx in idxs]
        sizes = [self.asource.data["approximate_count"][idx] for idx in idxs]

        for xid, xname, xsize in zip(ids, names, sizes):
            for yid,yname, ysize in zip(ids, names,sizes):
                data['xid'].append(xid)
                data['yid'].append(yid)
                data["xname"].append(xname)
                data["yname"].append(yname) 
                data["xsize"].append(xsize)
                data["ysize"].append(ysize) 
                ov = overlaps[xid][yid]
                data["overlap"].append(ov)
                op = min(int(100*ov/ysize),100)
                
                data["overlap_perc"].append(op)
                data["overlap_perc_txt"].append(f"{op}%")

        cvals = np.clip(256*np.array(data["overlap_perc"])/100, a_min=0, a_max=255)
        data['color'] = [color_map[int(cval)] for cval in cvals]
        
        names = list(names)
        self.heatmap_fig.x_range.factors = list(reversed(names))
        self.heatmap_fig.y_range.factors = names
        
        #self.rect.color_mapper = mapper
        # cm = self.fig.select_one(LinearColorMapper)
        # cm.update(low=mn, high=mx)
        # self.fig. = mapper
        self.osource.data = data

    def build_heatmap_figure(self):
        names = ["1", "2", "3"]
        p = figure(title="",x_axis_location="below",
        y_axis_location="right",
           tools="hover,save", toolbar_location="above",
           x_range=list(reversed(names)), y_range=names,
           tooltips = [
                ('IDs', '@yid, @xid'),  
                # ('names', '@yname, @xname'), 
                ('Sizes', '@ysize, @xsize'),
                ('Overlap', '@overlap')])

        p.plot_width = 700
        p.plot_height = 550
        p.min_border_left = 100
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "5pt"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_orientation = np.pi/3
        
        # self.dsources["audiences"].on_change("data", self.data_changed)
        # color_mapper = LinearColorMapper(palette="Magma256", low=0, high=1)
        self.rect = p.rect('xname', 'yname', 0.9, 0.9, source=self.osource,
            fill_color='color', alpha=0.4, line_color=None,
                hover_line_color='black', hover_color='color')
        self.text = p.text(x='xname', y='yname', text='overlap_perc_txt', text_font_size='0.4em',
         text_align='center', text_baseline='middle',color='color', source=self.osource)

        title = Paragraph(text=""" Overlap percentages are relative to y-axis audience""",
        width=600)

        self.heatmap_fig = p


        return column(title,p)