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
import logging


geolocator = Nominatim(user_agent="crime-analysis-app")



c_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heatmap_generation.log')
logging.basicConfig(filename=c_log_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
cities=["Andhra Pradesh","Seoni","Ajmer","Hoogly","Begusarai","Farrukhabad","Mansa","Sonipat","Borivali","Mathura", "Jubilee Hills","Guntur", "Amaravati","Burhanpur", "Visakhapatnam","Cuttak","Kalyanpuri","Ajmer","Patiala", "Sitamarhi","Tirupati", "Arunachal Pradesh", "Itanagar", "Assam", "Dispur", "Guwahati", "Bihar", "Patna", "Gaya", "Purulia","Fatehpur", "Muzaffarpur", "Chandigarh", "Chhattisgarh", "Raipur", "Bhilai", "Goa", "Panaji", "Gujarat", "Gandhinagar", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Haryana", "Chandigarh","Kanpur", "Faridabad", "Gurugram", "Hisar", "Karnal", "Ambala", "Jammu and Kashmir", "Jammu", "Srinagar", "Jharkhand", "Ranchi", "Jamshedpur", "Bokaro Steel City", "Karnataka", "Bengaluru", "Mangalore", "Hubli", "Belgaum", "Gulbarga", "Shimoga", "Udupi", "Kerala", "Thiruvananthapuram", "Kochi", "Calicut", "Madhya Pradesh", "Bhopal", "Indore", "Jabalpur", "Maharashtra", "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane", "Manipur", "Imphal", "Meghalaya", "Shillong", "Mizoram", "Aizawl", "Nagaland", "Kohima", "Odisha", "Bhubaneswar", "Cuttack", "Punjab", "Chandigarh", "Ludhiana", "Amritsar", "Rajasthan", "Jaipur", "Jodhpur", "Udaipur", "Bikaner", "Ajmer","Dwarka","Mathura","Gurdaspur","Sonipat", "Sikkim", "Gangtok", "Tamil Nadu", "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Telangana", "Hyderabad", "Warangal", "Tripura", "Agartala", "Uttar Pradesh", "Lucknow", "Kanpur", "Agra", "Noida", "Varanasi", "Prayagraj", "Uttarakhand", "Dehradun", "West Bengal", "Kolkata", "Howrah", "Asansol", "Siliguri"]

# Static coordinates fallback for common cities/states
CITY_COORDS_STATIC = {
    "New Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Bengaluru": (12.9716, 77.5946),
    "Mangaluru": (12.9141, 74.8560), "Chennai": (13.0827, 80.2707), "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639), "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873), "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319),
    "Noida": (28.5355, 77.3910), "Varanasi": (25.3176, 82.9739), "Prayagraj": (25.4358, 81.8463),
    "Nagpur": (21.1458, 79.0882), "Nashik": (19.9975, 73.7898), "Aurangabad": (19.8762, 75.3433),
    "Thane": (19.2183, 72.9781), "Patna": (25.5941, 85.1376), "Ranchi": (23.3441, 85.3096),
    "Bhopal": (23.2599, 77.4126), "Indore": (22.7196, 75.8577), "Jabalpur": (23.1815, 79.9864),
    "Raipur": (21.2514, 81.6296), "Bhilai": (21.1938, 81.3509), "Guwahati": (26.1445, 91.7362),
    "Chandigarh": (30.7333, 76.7794), "Srinagar": (34.0837, 74.7973), "Jammu": (32.7266, 74.8570),
    "Bhubaneswar": (20.2961, 85.8245), "Cuttack": (20.4625, 85.8828), "Udaipur": (24.5854, 73.7125),
    "Jodhpur": (26.2389, 73.0243), "Agra": (27.1767, 78.0081), "Dehradun": (30.3165, 78.0322),
    "Howrah": (22.5958, 88.2636), "Asansol": (23.6880, 86.9661), "Siliguri": (26.7271, 88.3953),
    "Gaya": (24.7794, 84.9819), "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812),
    "Rajkot": (22.3039, 70.8022), "Faridabad": (28.4089, 77.3178), "Gurugram": (28.4595, 77.0266),
    "Hisar": (29.1492, 75.7217), "Karnal": (29.6857, 76.9905), "Ambala": (30.3782, 76.7767),
    "Gangtok": (27.3389, 88.6065), "Warangal": (17.9689, 79.5941), "Agartala": (23.8315, 91.2868),
    "Imphal": (24.8170, 93.9368), "Shillong": (25.5788, 91.8933), "Aizawl": (23.7271, 92.7176),
    "Kohima": (25.6591, 94.1086), "Panaji": (15.4909, 73.8278), "Ajmer": (26.4499, 74.6399),
    "Mathura": (27.4924, 77.6737), "Sonipat": (28.9931, 77.0151), "Begusarai": (25.4186, 86.1294),
    "Mansa": (29.9970, 75.4018), "Farrukhabad": (27.3900, 79.5800), "Seoni": (22.0850, 79.5500),
    "Hoogly": (22.8948, 88.4021), "Guntur": (16.3067, 80.4365), "Amaravati": (16.5417, 80.5150),
    "Visakhapatnam": (17.6868, 83.2185), "Cuttak": (20.4625, 85.8828), "Kalyanpuri": (28.6141, 77.3139),
    "Patiala": (30.3398, 76.3869), "Sitamarhi": (26.5953, 85.4892), "Tirupati": (13.6288, 79.4192),
    "Burhanpur": (21.3120, 76.2220), "Dwarka": (28.5973, 77.0560), "Borivali": (19.2330, 72.8590),
    "Jubilee Hills": (17.4307, 78.4074),
    # States approximate to capitals
    "Uttar Pradesh": (26.8467, 80.9462), "Madhya Pradesh": (23.2599, 77.4126), "Andhra Pradesh": (16.5417, 80.5150),
    "Telangana": (17.3850, 78.4867), "Punjab": (30.7333, 76.7794), "Rajasthan": (26.9124, 75.7873),
    "Haryana": (30.7333, 76.7794), "Odisha": (20.2961, 85.8245), "Jharkhand": (23.3441, 85.3096),
    "Goa": (15.4909, 73.8278), "Gujarat": (23.2156, 72.6369), "West Bengal": (22.5726, 88.3639),
    "Uttarakhand": (30.3165, 78.0322), "Assam": (26.1408, 91.7902), "Jammu and Kashmir": (34.0837, 74.7973),
    "Manipur": (24.8170, 93.9368), "Meghalaya": (25.5788, 91.8933), "Mizoram": (23.7271, 92.7176),
    "Nagaland": (25.6591, 94.1086), "Sikkim": (27.3389, 88.6065), "Tripura": (23.8315, 91.2868),
    "Kerala": (8.5241, 76.9366), "Karnataka": (12.9716, 77.5946), "Bihar": (25.5941, 85.1376),
    "Chhattisgarh": (21.2514, 81.6296), "Maharashtra": (19.0760, 72.8777)
}

def _normalize_points(data):
    points = []
    try:
        for item in data:
            if item is None:
                continue
            # allow numpy arrays or other objects providing tolist()
            if hasattr(item, 'tolist'):
                try:
                    item = item.tolist()
                except Exception:
                    pass
            if isinstance(item, (list, tuple)):
                if len(item) >= 3:
                    lat, lon, w = item[0], item[1], item[2]
                elif len(item) == 2:
                    lat, lon = item[0], item[1]
                    w = 1
                else:
                    continue
                try:
                    lat = float(lat); lon = float(lon); w = float(w)
                except Exception:
                    continue
                points.append([lat, lon, w])
    except Exception:
        return []
    return points

# Proceed even with few items; if none, we'll still produce a base map
if not news_list:
    logging.warning("No news scraped; attempting fallback headlines...")
    # Fallback: try to load previously scraped headlines
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'previous_array.pickle'), 'rb') as f:
            t = pickle.load(f)
        it = iter(t)
        first = next(it)
        if isinstance(first, str):
            news_list = list(t)
            logging.info(f"Loaded fallback headlines: {len(news_list)}")
        else:
            logging.info("previous_array.pickle did not contain headlines list")
    except Exception as e:
        logging.info(f"No fallback headlines available: {e}")
else:
    logging.info(f"Scraped news items: {len(news_list)}")

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

logging.info(f"news_list length: {len(news_list)}")


    # Create a dictionary to store the frequency of each city
city_freq = {}
for city in city_list:
        if city not in city_freq:
            city_freq[city] = 1
        else:
            city_freq[city] += 1
logging.info(f"Unique extracted cities: {len(city_freq)}")
    # Create a list of tuples with latitude, longitude and frequency of each city
city_coords_freq = []
# Geocode only the top-N most frequent cities to keep runtime reasonable
top_cities = sorted(city_freq.items(), key=lambda kv: kv[1], reverse=True)[:60]
logging.info(f"Top cities considered for geocoding: {len(top_cities)}")
used_static = used_geopy = 0
for city, freq in top_cities:
        # Prefer static coords when available
        coords = CITY_COORDS_STATIC.get(city)
        if coords:
            lat, lon = coords
            city_coords_freq.append((lat, lon, freq))
            used_static += 1
            continue
        try:
            loc = geolocator.geocode(city, country_codes='in', timeout=5)
            if not loc:
                continue
            lat, lon = float(getattr(loc, 'latitude', None)), float(getattr(loc, 'longitude', None))
            if lat is None or lon is None:
                continue
            city_coords_freq.append((lat, lon, freq))
            used_geopy += 1
        except Exception:
            continue
logging.info(f"Points from static: {used_static}, from geopy: {used_geopy}")

    # Create a folium map centered at India
india_coords = [20.5937, 78.9629]
m = folium.Map(location=india_coords, zoom_start=5)


    # Create a heatmap layer using the list of tuples
# Fallback: if no coordinates computed, try using cached coordinates from previous run
if not city_coords_freq:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'previous_coords.pickle'), 'rb') as f:
            fallback = pickle.load(f)
            city_coords_freq = _normalize_points(fallback)
            if city_coords_freq:
                logging.info(f"Using fallback previous_coords.pickle with {len(city_coords_freq)} points")
            else:
                logging.warning("previous_coords.pickle normalization produced 0 points")
    except Exception:
        logging.info("No previous_coords.pickle available")

if city_coords_freq:
    try:
        HeatMap(city_coords_freq, radius=15, blur=10).add_to(m)
        logging.info(f"Heatmap layer added with {len(city_coords_freq)} points")
    except Exception:
        logging.exception("Failed to add HeatMap layer")
else:
    logging.warning("No coordinates available; saving base map only")

    # Display the map



base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
templates_path = os.path.join(project_dir, 'templates', 'final.html')
try:
    m.save(templates_path)
    logging.info(f"Map saved to {templates_path} with {len(city_coords_freq)} points")
    # Save coords for future fallback
    if city_coords_freq:
        try:
            with open(os.path.join(base_dir, 'previous_coords.pickle'), 'wb') as pf:
                pickle.dump(city_coords_freq, pf)
            logging.info(f"Saved {len(city_coords_freq)} points to previous_coords.pickle")
        except Exception:
            logging.exception("Failed to save previous_coords.pickle")
except Exception:
    logging.exception("Failed to save map HTML")
    #HeatMap(data).add_to(mapObj)




