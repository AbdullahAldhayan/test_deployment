from fastapi import FastAPI, Query
import pandas as pd
import folium
import osmnx as ox
from pydantic import BaseModel


class rent_index(BaseModel):
    average_rent: int
    coordinations: list

df = pd.read_csv('all_data_PoC.csv')


app = FastAPI()

@app.get("/avg_rent")
def avg_rent(city: str = Query(default='الرياض'),
             district: str = Query(default=...,)):
    district_gdf = ox.geocode_to_gdf(district.lower().strip()+' '+city.lower().strip())
    district_center = [
        district_gdf.geometry.centroid.y.iloc[0],
        district_gdf.geometry.centroid.x.iloc[0],
    ]
    average_rent = round(df[(df['district'].str.contains(district.strip())) &
        (df['city'].str.contains(city.strip())) &
        (df['apartment'] == 'شقة')]['price'].mean())
    return rent_index(average_rent=average_rent, coordinations=district_center)
    
    # # Add a marker at the district center
    # folium.Marker(
    #     location=district_center,
    #     popup=district.lower().strip()+' '+city.lower().strip(),
    #     tooltip=f"Avg rent in {district.lower().strip()+' '+city.lower().strip()} is: {round(df[(df['district'].str.contains(district.split()[0].strip())) &
    #     (df['city'].str.contains(district.split()[1].strip())) &
    #     (df['apartment'] == 'شقة')]['price'].mean())}",
    #     icon=folium.Icon(color="green", icon="info-sign")
    # )