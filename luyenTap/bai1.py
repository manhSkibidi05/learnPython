# Bài 1 : Giải mã file dữ liệu GPS theo chuẩn NMEA 0183 , trích xuất tọa độ chuyển đổi từ dạng DDMM.MMMM sang độ thập phân và đóng gói tệp GeoJSON 

# Chuỗi NMEA thô : $GPGGA,010000.00,2104.4155,N,10546.5793,E,1,09,1.2,15.0,M,,,,0000*0C
# -> Các thuộc tính được cách nhau bởi dấu phảy :
#  0 -> $GPGGA : mã câu lệnh 
#  1 -> 010000.00 : thời gian UTC 01h00p00s ; 
#  2,3 -> 2104.4155,N : vĩ độ (độ phút)
#  4,5 -> 10546.5793,E : kinh độ (độ phút)

import geopandas as gpd 
from shapely.geometry import Point
import folium 

def chuyen_do_tp(val_raw) : 
    val = float(val_raw)

    degrees = int(val // 100)
    min = val % 100
    decimal = degrees + (min / 60)

    return decimal

diems = []

file_path = '12_nmea_100_points.txt'
with open(file_path , "r" , encoding="utf-8") as file : # sử dụng hàm open() mở file , từ khóa with đứng trước hàm open() thực thi code trong khối with khi gặp lỗi sẽ đóng file  
    for line in file : 
        line = line.strip()
        if(line.startswith('$GPGGA')) : 
            parts = line.split(',')
            lat_raw = parts[2]
            lon_raw = parts[4]

            lat = chuyen_do_tp(lat_raw)
            lon = chuyen_do_tp(lon_raw)

            diems.append({
                "latitude" : lat,
                "longitude" : lon,
                "geometry" : Point(lon , lat)
            })

gdf = gpd.GeoDataFrame(diems , crs='EPSG:4326')
gdf.to_file('results.json' , driver='GeoJSON') # xuất ra file GeoJSON

center_hanoi = Point(105.81746473658592 , 21.025818006907244)
ban_do = folium.Map(location=[center_hanoi.y , center_hanoi.x] , zoom_start=13 , tiles='OpenStreetMap')

for idx , row in gdf.iterrows() : 
    lat = row.geometry.y
    lon = row.geometry.x

    folium.Marker(
        location=[lat , lon],
        popup="Điểm" ,
        tooltip=f"Điểm số {idx}",
        icon=folium.Icon(color="pink", icon="info-sign")
    ).add_to(ban_do)

ban_do.save('diem_dinh_vi.html') # xuất ra file html 