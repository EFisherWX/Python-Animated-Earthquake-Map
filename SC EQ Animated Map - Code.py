# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:05:33 2022

@author: evanw
"""

from datetime import timedelta, date
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

#Function for calculating the range between two dates, needed for loop on line 92
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
    
#Coordinates that bound the map, here bounding central SC
lon_min = -81.8842
lat_min = 33.5003
lon_max = -80.1846
lat_max = 34.5172

#Create basic figure without a plot of the earthquake locations. This will be used as a base map onto which the earthquakes will be plotted.
fig=plt.figure(figsize=(14, 16))
ax=plt.subplot(111, projection=ccrs.PlateCarree())
fig.tight_layout()
ax.set_extent([lon_min, lon_max, lat_min, lat_max],ccrs.PlateCarree())

#Add three shapefiles to the map: SC.shp, SC Counties.shp, and SC Interstate.shp
reader = shpreader.Reader('./SC.shp')
shpHold1 = list(reader.geometries())
shpHold2 = cfeature.ShapelyFeature(shpHold1, ccrs.PlateCarree())
ax.add_feature(shpHold2, facecolor='none', edgecolor='black', linewidth=0.35)

reader = shpreader.Reader('./SC Counties.shp')
shpHold1 = list(reader.geometries())
shpHold2 = cfeature.ShapelyFeature(shpHold1, ccrs.PlateCarree())
ax.add_feature(shpHold2, facecolor='none', edgecolor='black', linewidth=0.35)

reader = shpreader.Reader('./SC Interstate.shp')
shpHold1 = list(reader.geometries())
shpHold2 = cfeature.ShapelyFeature(shpHold1, ccrs.PlateCarree())
ax.add_feature(shpHold2, facecolor='none', edgecolor='red', linewidth=0.55)

#Add city labels at their respective latitudes and longitudes
plt.text(-81.0348,34.0007,'Columbia',fontweight='bold',fontsize=20,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-80.6070,34.2465,'Camden',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.2362,33.9815,'Lexington',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-80.9740,34.2143,'Blythewood',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.3498,34.1660,'Chapin',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.1009,33.8171,'Gaston',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-80.3415,33.9204,'Sumter',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.7196,33.5604,'Aiken',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.6187,34.2746,'Newberry',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-80.7779,33.6649,'St. Matthews',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)
plt.text(-81.0865,34.3807,'Winnsboro',fontweight='bold',fontsize=14,ha='center',color='white',path_effects=[pe.withStroke(linewidth=3, foreground="black")],zorder=2)

#Initialize a few lists in which the earthquake date will be stored. Data for each earthquake is stored at the same time, so they can be referenced with a singular index value later on
latList = []
lonList = []
magList = []
dateList = []
for line in open('./ScEqs1980Revised.csv'):
    fullSplit = line[0:-1].split(',')
    
    if fullSplit[0] != 'time':
        dateSplit = fullSplit[0].split('-')
        day = int(dateSplit[0])
        month = dateSplit[1]
        year = int(dateSplit[2])
        
        lat = eval(fullSplit[1])
        lon = eval(fullSplit[2])
        
        mag = eval(fullSplit[4])
        
        latList.append(lat)
        lonList.append(lon)
        magList.append(mag)
        dateList.append(fullSplit[0])
        
#Set start date and end date for looping  
start_date = date(2020, 1, 1)
end_date = date(2022, 6, 30)

'''Initialize lists for the scatter plot. count is simply a method for naming each file something unique with increasing numerical order.
---
Iterate through desired dates. This dataset extends back to 1980, however, I've chosen to only iterate through the last two and a half years. This keeps total # of figures from getting too large and keeps the focus on the recent earthquake swarm.
---
As the loop iterates through each day between the start and end dates, an if statement checks if an earthquake occured on that day (line 101).
---
For each earthquake event, the epicenter coordinates are appended to the runningLatList/runningLonList lists. The magnitude of each event is used to determine the earthquake marker size and color.
'''

runningLatList = []
runningLonList = []
sList = []
cList = []
count = 100
for single_date in daterange(start_date, end_date):
    #If an earthquake occured on single_date
    if single_date.strftime("%d-%b-%Y") in dateList:
        #Identify the index of the earthquake in the original dateList. This index will be used to find the lat, lon, and magnitude of the earthquake even though they're split into separate lists.
        startIndex = dateList.index(single_date.strftime("%d-%b-%Y"))
        #Identify how many earthquakes happened on single_date
        dailyCount = dateList.count(single_date.strftime("%d-%b-%Y"))
        
        #Loop through all earthquakes that occured on single_day (often just one earthquake and one loop)
        for i in range(dailyCount):
            #Append lat and lon to of earthquake to the list of earthquakes-to-date
            runningLatList.append(latList[startIndex + i])
            runningLonList.append(lonList[startIndex + i])
            
            #If statement for determining size and color of earthquake marker
            if magList[startIndex + i] < 1:
                sList.append(450)
                cList.append('#BECFFD')
            elif magList[startIndex + i] >= 1 and magList[startIndex + i] < 2:
                sList.append(650)
                cList.append('#87F7FE')
            elif magList[startIndex + i] >= 2 and magList[startIndex + i] < 3:
                sList.append(900)
                cList.append('#7BFBA0')
            elif magList[startIndex + i] >= 3:
                sList.append(1200) 
                cList.append('#FFF735')
                
    #Create scatter plot using the lat/lon lists of earthquakes to-date    
    scat = plt.scatter(runningLonList,runningLatList,c=cList,s=sList,zorder=3)
    plt.title(single_date.strftime("%d-%b-%Y"),fontsize=20)
    
    #Junk for making sure there is no extra whitespace on the saved map
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    #Save the map
    plt.savefig(f'./SCEQ/{count}.png',bbox_inches = 'tight',pad_inches = 0)
    
    #Iterate through all marker sizes (sList) and reduce their size since the earthquakes have now happened in the past. The larger the marker, the quicker its size is reduced.
    sCount = 0
    for b in sList:
        if b > 500:
            sList[sCount] = b - 50
        elif b > 300:
            sList[sCount] = b - 35
        elif b > 100:
            sList[sCount] = b - 20
        elif b > 60:
           sList[sCount] = b - 5 
        
        sCount += 1
    
    #Clear only scatter plot, not entire figure. This ensures that the scatter plots don't stack on top of each other and the base map doesn't have to be rebuilt every time
    scat.remove()
    
    count += 1