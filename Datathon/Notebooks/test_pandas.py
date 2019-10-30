import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPoint

ny_shp = gpd.read_file("/home/shade/DS4A/Data/Dataset/Shapes/nta_map.shp")
yellow_taxi = pd.read_csv('/home/shade/DS4A/Data/Dataset/Dataset/yellow_trips.csv')

df_Points = []

for i in range(196):
    bounds = ny_shp.loc[i, 'geometry'].bounds
    #bounds = ny_shp.loc[28, 'geometry'].bounds
    #bounds = ny_shp.loc[0,'geometry'].bounds
    #bounds = ny_shp.geometry.total_bounds
    df_filtered = yellow_taxi

    df_filtered = df_filtered[df_filtered['pickup_longitude'] > bounds[0]]
    df_filtered = df_filtered[df_filtered['pickup_longitude'] < bounds[2]]
    df_filtered = df_filtered[df_filtered['pickup_latitude'] > bounds[1]]
    df_filtered = df_filtered[df_filtered['pickup_latitude'] < bounds[3]]

    Points = [Point(x, y) for x, y in zip(df_filtered['pickup_longitude'], df_filtered['pickup_latitude'])]
    df_Points.append(gpd.GeoDataFrame(df_filtered, geometry=Points))
    print(i)

fig, ax = plt.subplots(figsize = (20,16))
ny_shp.plot(figsize=(20,16), alpha=0.1, edgecolor='k', ax=ax)

for i in df_Points:
    i.plot(figsize=(20,16), edgecolor='green', color='green', ax=ax)

plt.savefig('plot')