import pandas as pd

def (path,gauge_index):
    gauge_val = pd.read_csv(path,encoding="ISO-8859-1")
    min_angle,max_angle,min_val,max_val,unit = gauge_val.iloc[gauge_index,1:]

    return min_angle,max_angle,min_val,max_val,unit