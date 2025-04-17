from typing import List, Tuple
import requests
import pandas as pd

# OneMap API Configuration
EMAIL = "dillonchong01@gmail.com"
PASSWORD = "T0126546BClash"
TOKEN_URL = "https://www.onemap.gov.sg/api/auth/post/getToken"
SEARCH_URL = "https://www.onemap.gov.sg/api/common/elastic/search"

# Authenticate OneMap API
def authenticate() -> str:
    """
    Authenticate with OneMap API and returns access token
    """
    payload = {"email": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(TOKEN_URL, json=payload)
        response.raise_for_status()
        return response.json().get("access_token", None)
    except requests.RequestException as e:
        print(f"Authentication failed: {e}")
        return None
    
# Obtain Latitude and Longitude from OneMaps
def get_lat_long(locations: List[str], api_token: str) -> pd.DataFrame:
    """
    Given a list of location names, retrieve latitude and longitude from OneMap.

    Args:
        locations: List of string addresses to geocode.
        api_token: Auth token for OneMap API.

    Returns:
        DataFrame with columns ['Address', 'Lat', 'Long'].
    """
    lat_long_data: List[Tuple[str, float, float]] = []

    # Get Lat - Long for each Unique Address
    for address in locations:
        try:
            response = requests.get(
                SEARCH_URL,
                params={"searchVal": address, "returnGeom": "Y", "getAddrDetails": "N"},
                headers={"Authorization": f"{api_token}"}
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            if results:
                latitude = float(results[0]["LATITUDE"])
                longitude = float(results[0]["LONGITUDE"])
            else:
                latitude, longitude = 0.0, 0.0

        except Exception as e:
            print(f"Request failed for '{address}': {e}")
            latitude, longitude = 0.0, 0.0
            
        lat_long_data.append((address, latitude, longitude))

    return pd.DataFrame(lat_long_data, columns=["Address", "Lat", "Long"])


STATIONS = [
    "Jurong East MRT", "Bukit Batok MRT", "Bukit Gombak MRT", "Choa Chu Kang MRT", "Yew Tee MRT",
    "Kranji MRT", "Marsiling MRT", "Woodlands MRT", "Admiralty MRT", "Sembawang MRT",
    "Canberra MRT", "Yishun MRT", "Khatib MRT", "Yio Chu Kang MRT", "Ang Mo Kio MRT",
    "Bishan MRT", "Braddell MRT", "Toa Payoh MRT", "Novena MRT", "Newton MRT",
    "Orchard MRT", "Somerset MRT", "Dhoby Ghaut MRT", "City Hall MRT", "Raffles Place MRT",
    "Marina Bay MRT", "Marina South Pier MRT", "Expo MRT", "Pasir Ris MRT",
    "Tampines MRT", "Simei MRT", "Tanah Merah MRT", "Bedok MRT", "Kembangan MRT",
    "Eunos MRT", "Paya Lebar MRT", "Aljunied MRT", "Kallang MRT", "Lavender MRT",
    "Bugis MRT", "Tanjong Pagar MRT", "Outram Park MRT", "Tiong Bahru MRT", "Redhill MRT",
    "Queenstown MRT", "Commonwealth MRT", "Buona Vista MRT", "Dover MRT", "Clementi MRT",
    "Chinese Garden MRT", "Lakeside MRT", "Boon Lay MRT", "Pioneer MRT", "Joo Koon MRT",
    "Gul Circle MRT", "Tuas Crescent MRT", "Tuas West Road MRT", "Tuas Link MRT", "HarbourFront MRT",
    "Chinatown MRT", "Clarke Quay MRT", "Little India MRT", "Farrer Park MRT", "Boon Keng MRT",
    "Potong Pasir MRT", "Woodleigh MRT", "Serangoon MRT", "Kovan MRT", "Hougang MRT",
    "Buangkok MRT", "Sengkang MRT", "Punggol MRT", "Punggol Coast MRT", "Bras Basah MRT",
    "Esplanade MRT", "Promenade MRT", "Nicoll Highway MRT", "Stadium MRT", "Mountbatten MRT",
    "Dakota MRT", "MacPherson MRT", "Tai Seng MRT", "Bartley MRT", "Lorong Chuan MRT",
    "Marymount MRT", "Caldecott MRT", "Botanic Gardens MRT", "Farrer Road MRT", "Holland Village MRT",
    "one-north MRT", "Kent Ridge MRT", "Haw Par Villa MRT", "Pasir Panjang MRT", "Labrador Park MRT",
    "Telok Blangah MRT", "Bukit Panjang MRT", "Cashew MRT", "Hillview MRT", "Hume MRT",
    "Beauty World MRT", "King Albert Park MRT", "Sixth Avenue MRT", "Tan Kah Kee MRT", "Stevens MRT",
    "Rochor MRT", "Bayfront MRT", "Downtown MRT", "Telok Ayer MRT", "Fort Canning MRT",
    "Bencoolen MRT", "Jalan Besar MRT", "Bendemeer MRT", "Geylang Bahru MRT", "Mattar MRT",
    "Ubi MRT", "Kaki Bukit MRT", "Bedok North MRT", "Bedok Reservoir MRT", "Tampines West MRT",
    "Tampines East MRT", "Upper Changi MRT", "Woodlands North MRT", "Woodlands South MRT", "Springleaf MRT",
    "Lentor MRT", "Mayflower MRT", "Bright Hill MRT", "Upper Thomson MRT", "Napier MRT",
    "Orchard Boulevard MRT", "Great World MRT", "Havelock MRT", "Maxwell MRT", "Shenton Way MRT",
    "Gardens by the Bay MRT", "Tanjong Rhu MRT", "Katong Park MRT", "Tanjong Katong MRT", "Marine Parade MRT",
    "Marine Terrace MRT", "Siglap MRT", "Bayshore MRT"
    ]

MALLS = [
    "100 AM", "111 Somerset", "313@Somerset", "AMK Hub", "Anchorpoint",
    "Aperia Mall", "Bedok Mall", "Bugis Junction", "Bugis+", "Bukit Panjang Plaza",
    "Capitol Singapore", "Causeway Point", "Century Square", "Changi City Point", "Chijmes",
    "Chinatown Point", "Cineleisure Orchard", "City Square Mall", "Clarke Quay", "Clarke Quay Central",
    "Compass One", "Cross Street Exchange", "Downtown East", "East Village", "Eastpoint Mall",
    "Far East Plaza", "Forum The Shopping Mall", "Funan Mall", "Great World", "Greenwich V",
    "HarbourFront Centre", "Heartland Mall Kovan", "Hillion Mall", "HillV2", "Hougang 1",
    "Hougang Mall", "i12 Katong", "Icon Village", "IMM", "ION Orchard",
    "JCube", "Jem", "Jubilee Square", "Junction 10",
    "Junction 8", "Junction 9", "Jurong Point", "Kallang Wave Mall", "Kap Mall",
    "Katong V", "Kinex", "Lot One", "Mandarin Gallery", "Marina Square",
    "Millenia Walk", "NEX", "Ngee Ann City", "Northpoint City", "One Raffles Place",
    "Orchard Central", "Orchard Gateway", "Pacific Plaza", "Palais Renaissance", "Paragon",
    "Parkway Parade", "Paya Lebar Quarter", "Paya Lebar Square", "Plaza Singapura", "Raffles City",
    "Republic Plaza", "Rivervale Mall", "Robertson Walk", "Scotts Square", "Shaw Centre",
    "Shoppes at Marina Bay Sands", "Singpost Centre", "Square 2", "Sun Plaza", "Suntec City",
    "Tampines 1", "Tampines Mall", "Tanglin Mall", "Tanglin Place", "The Cathay",
    "The Centrepoint", "The Clementi Mall", "The Poiz Centre", "The Seletar Mall", "The Star Vista",
    "The Woodleigh Mall", "Thomson Plaza", "Tiong Bahru Plaza", "UE Square", "United Square",
    "Valley Point", "Velocity @ Novena Square", "VivoCity", "Waterway Point", "West Coast Plaza",
    "West Mall", "Westgate", "Wheelock Place", "White Sands", "Wisma Atria",
    "YewTee Point"
    ]

SCHOOLS = [
    "Admiralty Primary School", "Ai Tong School", "Alexandra Primary School", "Anderson Primary School", "Anglo-Chinese School (Junior)",
    "Anglo-Chinese School (Primary)", "Angsana Primary School", "Bukit Panjang Primary School", "Bukit View Primary School", "Canberra Primary School",
    "Catholic High School", "CHIJ Our Lady of the Nativity", "CHIJ Primary (Toa Payoh)", "CHIJ St. Nicholas Girls' School", "Chongfu School",
    "Chongzheng Primary School", "Chua Chu Kang Primary School", "Compassvale Primary School", "Concord Primary School", "Dazhong Primary School",
    "De La Salle School", "Elias Park Primary School", "Eunos Primary School", "Evergreen Primary School", "Fairfield Methodist School (Primary)",
    "Fengshan Primary School", "Fern Green Primary School", "Fernvale Primary School", "Frontier Primary School", "Geylang Methodist School (Primary)",
    "Gongshang Primary School", "Greenwood Primary School", "Henry Park Primary School", "Holy Innocents' Primary School", "Hong Wen School",
    "Horizon Primary School", "Hougang Primary School", "Huamin Primary School", "Jing Shan Primary School", "Junyuan Primary School",
    "Jurong West Primary School", "Juying Primary School", "Keming Primary School", "Kheng Cheng School", "Kong Hwa School",
    "Kranji Primary School", "Kuo Chuan Presbyterian Primary School", "Lakeside Primary School", "Maha Bodhi School", "Maris Stella High School",
    "Marsiling Primary School", "Mee Toh School", "Methodist Girls' School (Primary)", "Nan Chiau Primary School", "Nan Hua Primary School",
    "Nanyang Primary School", "Naval Base Primary School", "Ngee Ann Primary School", "North View Primary School", "Northland Primary School",
    "Oasis Primary School", "Pasir Ris Primary School", "Paya Lebar Methodist Girls' School (Primary)", "Pei Chun Public School", "Pei Hwa Presbyterian Primary School",
    "Poi Ching School", "Princess Elizabeth Primary School", "Punggol Green Primary School", "Punggol Primary School", "Qifa Primary School",
    "Radin Mas Primary School", "Raffles Girls' Primary School", "Red Swastika School", "River Valley Primary School", "Riverside Primary School",
    "Rivervale Primary School", "Rosyth School", "Rulang Primary School", "Sembawang Primary School", "Sengkang Green Primary School",
    "Shuqun Primary School", "Singapore Chinese Girls' Primary School", "South View Primary School", "Springdale Primary School", "St. Andrew's Junior School",
    "St. Anthony's Primary School", "St. Hilda's Primary School", "St. Joseph's Institution Junior", "St. Margaret's School (Primary)", "Tampines North Primary School",
    "Tampines Primary School", "Tanjong Katong Primary School", "Tao Nan School", "Teck Ghee Primary School", "Temasek Primary School",
    "Waterway Primary School", "Wellington Primary School", "West Spring Primary School", "Westwood Primary School", "White Sands Primary School",
    "Xinmin Primary School", "Yangzheng Primary School", "Yu Neng Primary School", "Zhangde Primary School", "Zhenghua Primary School",
    "Valour Primary School", "Northshore Primary School"
]



if __name__ == "__main__":
    # Authenticate and get API Token
    api_token = authenticate()
    if api_token is None:
        print("Authentication failed. Exiting...")
        exit(1)

    df = pd.read_csv("datasets/Cleaned_Resale_Data.csv")

    # Get Lat/Long of Resale HDB
    hdb_locations = df["Address"].unique()
    hdb_lat_long_df = get_lat_long(hdb_locations, api_token)
    hdb_lat_long_df.to_csv("datasets/coordinates/HDB_LatLong.csv", index=False)

    # Get Lat/Long of MRTs
    mrt_lat_long_df = get_lat_long(STATIONS, api_token)
    mrt_lat_long_df.to_csv("datasets/coordinates/MRT_LatLong.csv", index=False)

    # Get Lat/Long of Malls
    mall_lat_long_df = get_lat_long(MALLS, api_token)
    mall_lat_long_df.to_csv("datasets/coordinates/Mall_LatLong.csv", index=False)

    # Get Lat/Long of Primary Schools (that are oversubscribed)
    school_lat_long_df = get_lat_long(SCHOOLS, api_token)
    school_lat_long_df.to_csv("datasets/coordinates/School_LatLong.csv", index=False)