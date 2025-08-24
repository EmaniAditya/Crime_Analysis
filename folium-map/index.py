import folium
try:
    from scrapper4 import news_list
except Exception:
    # If scraper import fails (e.g., selenium/chrome not available), continue with no data
    news_list = []
from folium.plugins import HeatMap
import re
from geopy.geocoders import Nominatim
import sys
import os
import pickle


geolocator = Nominatim(user_agent="crime-analysis-app")



cities=["Andhra Pradesh","Seoni","Ajmer","Hoogly","Begusarai","Farrukhabad","Mansa","Sonipat","Borivali","Mathura", "Jubilee Hills","Guntur", "Amaravati","Burhanpur", "Visakhapatnam","Cuttak","Kalyanpuri","Ajmer","Patiala", "Sitamarhi","Tirupati", "Arunachal Pradesh", "Itanagar", "Assam", "Dispur", "Guwahati", "Bihar", "Patna", "Gaya", "Purulia","Fatehpur", "Muzaffarpur", "Chandigarh", "Chhattisgarh", "Raipur", "Bhilai", "Goa", "Panaji", "Gujarat", "Gandhinagar", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Haryana", "Chandigarh","Kanpur", "Faridabad", "Gurugram", "Hisar", "Karnal", "Ambala", "Jammu and Kashmir", "Jammu", "Srinagar", "Jharkhand", "Ranchi", "Jamshedpur", "Bokaro Steel City", "Karnataka", "Bengaluru", "Mangalore", "Hubli", "Belgaum", "Gulbarga", "Shimoga", "Udupi", "Kerala", "Thiruvananthapuram", "Kochi", "Calicut", "Madhya Pradesh", "Bhopal", "Indore", "Jabalpur", "Maharashtra", "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane", "Manipur", "Imphal", "Meghalaya", "Shillong", "Mizoram", "Aizawl", "Nagaland", "Kohima", "Odisha", "Bhubaneswar", "Cuttack", "Punjab", "Chandigarh", "Ludhiana", "Amritsar", "Rajasthan", "Jaipur", "Jodhpur", "Udaipur", "Bikaner", "Ajmer","Dwarka","Mathura","Gurdaspur","Sonipat", "Sikkim", "Gangtok", "Tamil Nadu", "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Telangana", "Hyderabad", "Warangal", "Tripura", "Agartala", "Uttar Pradesh", "Lucknow", "Kanpur", "Agra", "Noida", "Varanasi", "Prayagraj", "Uttarakhand", "Dehradun", "West Bengal", "Kolkata", "Howrah", "Asansol", "Siliguri"]

# Proceed even with few items; if none, we'll still produce a base map
if not news_list:
    print("No news scraped; generating base map without heat layer.")

city_list = []
for string in news_list:
        for city in cities:
            if city in string:
                city_list.append(city)
            elif "Uttar Pradesh's" in string:
                city_list.append('Uttar Pradesh')
            elif "UP's" in string:
                city_list.append('Uttar Pradesh')
            elif "UP" in string:
                city_list.append('Uttar Pradesh')
            elif 'Bangalore' in string:
                city_list.append('Bengaluru')
            elif 'Mangalore' in string:
                city_list.append('Mangaluru')
            elif 'MP' in string:
                city_list.append('Madhya Pradesh')
            elif "MP's" in string:
                city_list.append('Madhya Pradesh')
            elif "Andhra" in string:
                city_list.append('Andhra Pradesh')
            elif "Andhra Pradesh's" in string:
                city_list.append('Andhra Pradesh')
            elif "Delhi" in string:
                city_list.append('New Delhi')
                
            
                
if "Surat" in city_list:
    city_list.remove("Surat")

print(len(news_list))


    # Create a dictionary to store the frequency of each city
city_freq = {}
for city in city_list:
        if city not in city_freq:
            city_freq[city] = 1
        else:
            city_freq[city] += 1
print(city_freq)
    # Create a list of tuples with latitude, longitude and frequency of each city
city_coords_freq = []
# Geocode only the top-N most frequent cities to keep runtime reasonable
top_cities = sorted(city_freq.items(), key=lambda kv: kv[1], reverse=True)[:60]
for city, freq in top_cities:
        try:
            loc = geolocator.geocode(city, country_codes='in', timeout=5)
            if not loc:
                continue
            lat, lon = float(getattr(loc, 'latitude', None)), float(getattr(loc, 'longitude', None))
            if lat is None or lon is None:
                continue
            city_coords_freq.append((lat, lon, freq))
        except Exception:
            # Skip cities we can't geocode
            continue

    # Create a folium map centered at India
india_coords = [20.5937, 78.9629]
m = folium.Map(location=india_coords, zoom_start=5)


    # Create a heatmap layer using the list of tuples
# Fallback: if no coordinates computed, try using cached data from previous run
if not city_coords_freq:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'previous_array.pickle'), 'rb') as f:
            fallback = pickle.load(f)
            if isinstance(fallback, (list, tuple)) and fallback:
                city_coords_freq = list(fallback)
    except Exception:
        pass

if city_coords_freq:
    HeatMap(city_coords_freq, radius=15, blur=10).add_to(m)

    # Display the map



base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
templates_path = os.path.join(project_dir, 'templates', 'final.html')
m.save(templates_path) 
print(f"Heat Map generated with {len(city_coords_freq)} points. Refresh to see the results.")
    #HeatMap(data).add_to(mapObj)




