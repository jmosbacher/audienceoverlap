import sys
import time
import random
import requests
# sys.path.append("/home/yossi/anaconda3/lib/python3.6/site-packages/") # Replace this with the place you installed facebookads using pip
# sys.path.append("/home/yossi/anaconda3/lib/python3.6/site-packages/facebook_business") # same as above
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
import json
import gspread
from collections import defaultdict
from bokeh.palettes import Spectral6,Category20



scope = ['https://spreadsheets.google.com/feeds']
KEY_FILE = "audienceoverlap/credentials/google.json"
with open(KEY_FILE, 'r') as f:
    d = json.load(f)
gsheet_email = d.get('client_email', 'ERROR: No credentiald file.')
spreadsheet_key = '1MmfJr8blGKVMbH7lVoSq7GIPqVqq3q3BYGoEJj9cYdw'

def read_google_sheet(key):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scope)
    gc = gspread.authorize(credentials)
    book = gc.open_by_key(key)
    aud_ws = book.worksheet("audiences")
    aud_table = aud_ws.get_all_values()
    aud_df = pd.DataFrame(aud_table[1:], columns=aud_table[0])
    ov_ws = book.worksheet("overlaps")
    ov_table = ov_ws.get_all_values()
    d = np.array(ov_table)
    ov_df = pd.DataFrame(d[1:,1:], columns=d[0,1:], index=d[1:,0]).astype(int)
    return aud_df, ov_df

def read_audience_list(acctid, appid, appsec, token):
    FacebookAdsApi.init(appid, appsec, token)
    my_account = AdAccount(f'act_{acctid}')
    fs = ['name', 'account_id', 'id', 'approximate_count']
    cauds = my_account.get_custom_audiences()
    data = {k:[] for k in fs}
    for ca in cauds:
        try:
            ca.remote_read(fields=fs)
            for f in fs:
                data[f].append(ca[f])
            time.sleep(0.2*random.random())
        except:
            pass
    df = pd.DataFrame(data)
    data = add_audience_columns(df)
    return data

def fetch_overlaps_fbapi(cmp_auds, acctid, token):
    overlaps = {}
    for aid in cmp_auds:
        params = {
        "access_token": token,
        "comparison_ids[]": cmp_auds,
        "pivot_id": f"{aid}",
        }
        resp = requests.get(f'https://graph.facebook.com/v3.2/act_{acctid}/audienceoverlap', params=params)
        if resp.status_code==200:
            data = resp.json()["data"]
            overlaps[aid] = {d["id"]:int(d["overlap"]) for d in data}
        else:
            overlaps[aid] =  {}
        time.sleep(0.2*random.random())
    return overlaps
    
def add_audience_columns(aud_df):
    aud_df["approximate_count"] = aud_df["approximate_count"].astype(int)
    aud_df["approximate_count_txt"] = (aud_df["approximate_count"]/1000).astype(str)+"K"
    aud_df["r"] = np.sqrt(aud_df["approximate_count"]/aud_df["approximate_count"].max())
    aud_df['x'] = 0.
    aud_df['y'] = 0.
    aud_df['c'] = np.random.choice(Category20[20], len(aud_df.index))
    return aud_df #.to_dict(orient='list')

def best_dist(r1,r2, overlap):
    def overlap_1d(d,R,r):
        a = (d**2 +r**2 -R**2)/(2*d*r)
        b = (d**2 + R**2 -r**2)/(2*d*R)
        c = (-d+r+R)*(d-r+R)*(d+r-R)*(d+r+R)
        if all([0<a<np.pi,0<b<np.pi, 0<c ]):
            return r**2*np.arccos(a) + R**2*np.arccos(b) - 0.5*np.sqrt(c)
        else:
            return 999
    def pen(d):
        return (overlap - overlap_1d(d,r1,r2))**2
    
    res = minimize(pen, [max(r1,r2)])
    return res.x[0]

def best_angle(r01,r02,r12):
    arg = (r01**2 + r02**2 - r12**2)/(2*r01*r02)
    if -1< arg <1:
        a = np.arccos(arg)
    else:
        a = 0.
    return a


def place_circles(rs, os, thresh=0.1, method="pivot"):
    
    rs = np.array(rs)
    os = np.pi*np.array(os)
    
    N = rs.size
    d01 = best_dist(rs[0], rs[1], os[0,1])
    ds = [0, d01]
    thetas = [0, 0]
    xs = [0, d01]
    ys = [0, 0]
    
    for i in range(2, N):
        if method=='chain':
            frst = i-2
        else:
            frst = 0
        if os[frst,i]<thresh*np.pi*rs[i]**2:
            d02 = 2*(rs[frst] + rs[i])
        else:
            d02 = best_dist(rs[frst], rs[i], os[frst,i])
        if os[i-1,i]<thresh*np.pi*rs[i]**2:
            d12 = 2*(rs[i-1] + rs[i])
        else:
            d12 = best_dist(rs[i-1], rs[i], os[i-1,i])
        d01 = ds[i-1]
        
        theta = thetas[i-1]+best_angle(d01,d02,d12)
        ds.append(d02)
        thetas.append(theta)
        xs.append(xs[frst] + d02*np.cos(theta))
        ys.append(ys[frst] + d02*np.sin(theta))
    return np.array(xs), np.array(ys)

def random_data(mn_ov=1,mxaud=10000, N=200):
    # mxaud = 10000
    # N = np.random.uniform(mnN,mxN)
    rs = 0.1+0.5*np.random.random(N)
    rs = np.sort(rs)[-1::-1]
    overlaps = {}#np.empty((N,N), dtype=np.float)

    for i in range(1,N+1):
        overlaps[f'{i}'] = {}
        for j in range(1,i+1):
            s = int(np.random.uniform(mn_ov, mxaud*np.min(rs[[i-1,j-1]])**2))
            overlaps[f'{i}'][f'{j}'] = s
            overlaps[f'{j}'][f'{i}'] = s
        overlaps[f'{i}'][f'{i}'] = int(mxaud*rs[i-1]**2)

    ids = [f'{i+1}' for i in range(N)]
    names = [f'fake_audience_{i}' for i in ids]
    sizes = [int(mxaud*r**2) for r in rs]
    # x, y = place_circles(rs, overlaps)
    
    data = {
        "name": names, 
        'account_id': ['42' for _ in rs],
        'id': ids,
        "approximate_count": sizes,

    }
    aud_df = pd.DataFrame(data)
    ov_df = pd.DataFrame(overlaps)
    return aud_df, ov_df
