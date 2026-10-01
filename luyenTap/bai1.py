# Bài 1 : Giải mã file dữ liệu thô GPS theo chuẩn NMEA 0183 , trích xuất tọa độ chuyển đổi từ dạng DDMM.MMMM sang độ thập phân và đóng gói tệp GeoJSON , trực quan hóa
# lên bản đồ bẳng folium

# Chuỗi NMEA thô : $GPGGA,010000.00,2104.4155,N,10546.5793,E,1,09,1.2,15.0,M,,,,0000*0C
# -> Các thuộc tính được cách nhau bởi dấu phảy :
#  0 -> $GPGGA : mã câu lệnh 
#  1 -> 010000.00 : thời gian UTC 01h00p00s 
#  2,3 -> 2104.4155,N : vĩ độ (độ phút)
#  4,5 -> 10546.5793,E : kinh độ (độ phút)
#  6 -> 1 : trạng thái định vị (0 = chưa bắt đc , 1 = định vị GPS thường , 2 = DGPS/ RTK Float)
#  7 -> 09 : số lượng vệ tinh 
#  8 -> 1.2 : chỉ số HDOP : chỉ số đo độ lệch hình học mặt phẳng càng nhỏ càng chuẩn 
#  9,10 -> 15.0,M : độ cao 

import geopandas as gpd 
from shapely.geometry import Point
import folium 

# Hàm áp dụng công thức DD + (MM.MMMM / 60) -> giúp chuyển kinh độ / vĩ độ đang ở đơn vị độ phút sang độ thập phân
def chuyen_do_tp(val_raw) : 
    val = float(val_raw)

    degrees = int(val // 100)
    min = val % 100
    decimal = degrees + (min / 60)

    return decimal

diems = []

file_path = '12_nmea_100_points.txt'
# sử dụng hàm open() để đọc file .txt , từ khóa with đặt trước hàm open() giúp tạo khối code trong đó đọc file an toàn và thực thi code trong khối lệnh đó nếu gặp lỗi
# sẽ lập tức đóng file 
with open(file_path , "r" , encoding="utf-8") as file :   
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

# khởi tạo bản đồ folium 
ban_do = folium.Map(location=[gdf['latitude'].loc[0] ,gdf['longitude'].loc[0]] , zoom_start=18 , tiles='OpenStreetMap')

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