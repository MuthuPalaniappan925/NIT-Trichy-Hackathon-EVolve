import streamlit as st
import googlemaps
import urllib.request,json
import pandas as pd
import numpy as np
from datetime import datetime
@st.cache

def calc_tots(directions):
    total_dist=0
    total_time=0
   
    for i in directions[0]["legs"][0]["steps"]:
        total_dist += int(i["distance"]["value"])
        total_time += int(i['duration']['value'])
       
    total_dist /= 1000
    total_time /= 60
    
    return total_dist,total_time

def get_end_lat_lng(directions):
    end_lat = directions['routes'][0]['legs'][0]['end_location']['lat']
    end_lng = directions['routes'][0]['legs'][0]['end_location']['lng']
    
    return end_lat,end_lng
def get_start_lat_lng(directions):
    start_lat = directions['routes'][0]['legs'][0]['start_location']['lat']
    start_lng = directions['routes'][0]['legs'][0]['start_location']['lng']
    
    return end_lat,end_lng

def break_coordinates(orgin,destination,threshold,gmaps):
    route = gmaps.directions(origin=origin,destination=destination,mode="driving")
    total_dist,total_time = calc_tots(route)
   
    travellable_dist = threshold

    travellable_dist *= 1000
   
    cum_dist = 0
    prev_cum = 0
   
    fail = False
   
    count=0
    for i in route[0]["legs"][0]["steps"]:
        prev_cum = cum_dist
        cum_dist+=int(i['distance']['value'])
        if cum_dist>travellable_dist:
            break_coords = i["start_location"]
            #print(break_coords)
            remaining_dist = travellable_dist-prev_cum
            fail = True
            break
        count+=1
    return remaining_dist,break_coords    
    
def break_coords_dist_final(data,origin,destination):
    list_1 = [0]
    for (i1, row1), (i2, row2) in pairwise(data.iterrows()):
        latest_orgin,longit_orgin = break_coordinates(origin,destination)
        origins = (latest_orgin,longit_orgin)
    
        lat_dest = row1['Lat']
        longitude_des = row1['Long']
        destinations = (lat_dest,longitude_des)
        
        result = gmaps.distance_matrix(origins, destinations)
        list_1.append(result)
        dist_final = []
        for i in range(1,len(list_1)):
            if "distance" in list_1[i]["rows"][0]["elements"][0].keys():
                dist_final.append(list_1[i]['rows'][0]['elements'][0]['distance']['value'])
            else:
                dist_final.append(1000000000000)
        data['break_ev_distance'] = pd.DataFrame(dist_final)
        return data

def read_dataset():
    data = pd.read_csv("Indian Cities Database.csv")
    data = data[['Lat','Long']]
    return data

def get_new_dataframe(data,remaining_dist):
    new_data = data[data['break_ev_distance'] < remaining_dist]
    return new_data

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def dist_ev_distance(directions,new_data):
    list_2 = [0]
    
    for i in range(len(new_data)):
        latest_orgin,longit_orgin = get_end_lat_lng(directions)
        origins = (latest_orgin,longit_orgin)

        lat_dest = new_data.iloc[i]['Lat']
        longitude_des = new_data.iloc[i]['Long']
        #print(lat_dest,longitude_des)
        destinations = (lat_dest,longitude_des)
    
        result = gmaps.distance_matrix(origins, destinations)
        list_2.append(result)
        dist_final_2 = []
        for i in range(1,len(list_2)):
    #print(i)
    #abx = list_1[i]["rows"][0]["elements"][0]["distance"]['text']
            if "distance" in list_2[i]["rows"][0]["elements"][0].keys():
                dist_final_2.append(list_2[i]['rows'][0]['elements'][0]['distance']['value'])
            else:
                dist_final_2.append(1000000000000)
        new_data['dest_ev_dist'] = dist_final_2
        return new_data


def get_mini_ev_lat_lng(new_data):
    new_data['min_ev_distance'] = new_data['break_ev_distance'] + new_data['dest_ev_dist']
    mini_ev_lat = new_data.nsmallest(1,'min_ev_distance')['Lat']
    mini_ev_lng = new_data.nsmallest(1,'min_ev_distance')['Long']
    li = []
    li.append(mini_ev_lat.values,mini_ev_lng.values)
    return li     


def fn(origin,destination):
    gmaps = googlemaps.Client(key='AIzaSyD6fq8uvE15O56YLG-C5k1oYnedFLL4PNs')
    key='AIzaSyD6fq8uvE15O56YLG-C5k1oYnedFLL4PNs'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,key)
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    remaining_dist,break_coords=break_coordinates(origin, destination,400,gmaps)
    st.write("You need to look for a charging station from ",break_coords)
    st.write("Looking for a charging station....")
    data=read_dataset()
    data=break_coords_dist_final(data,origin,destination)
    data=get_new_dataframe(data,remaining_dist)
    data=dist_ev_distance(directions,data)
    ev_coords=get_mini_ev_lat_lng(data)
    origin_coords=get_start_lat_lng(directions)
    #visualizer(origin_coords,ev_coords)
    st.write("Found you an EV charging station at: ",ev_coords)




st.title("Path Generator")
origin=st.text_input("Enter the start location:","Chennai")
destn=st.text_input("Enter destination:","Kashmir")


st.button("Generate Path",on_click=fn(origin,destn))
