# Bài 2 : Người dùng đang đứng tại khuôn viên Trường Đại học Mỏ - Địa chất (Tọa độ: 21.0722 Lat, 
# 105.7741 Long). Cần tính khoảng cách thực tế (theo đơn vị Mét) từ người dùng đến danh sách các trạm 
# xe buýt lân cận, xác định trạm gần nhất và vẽ đường nối trực quan. 

import geopandas as gpd 
from shapely.geometry import Point
import folium

center_humg = Point(105.7741 , 21.0722)
center_humg_phang = gpd.GeoSeries(center_humg , crs='EPSG:4326').to_crs('EPSG:32648').loc[0]

gdf_tram_se_bus = gpd.read_file('tram_se_bus.json')
gdf_tram_se_bus_phang = gdf_tram_se_bus.to_crs('EPSG:32648')

danh_sach_khoang_cach = gdf_tram_se_bus_phang.geometry.distance(center_humg_phang).round(2)

idx_gan_nhat = danh_sach_khoang_cach.idxmin()
diem_gan_nhat = gdf_tram_se_bus.loc[idx_gan_nhat , 'geometry']

m = folium.Map(location=[center_humg.y , center_humg.x] , zoom_start=13 , tiles='openStreetMap')

folium.Marker(
    location=[center_humg.y , center_humg.x],
    popup="Điểm chính",
    tooltip="Đại học Mỏ - Địa Chất",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

for idx , row in gdf_tram_se_bus.iterrows() : 
    lat = row.geometry.y
    lon = row.geometry.x

    folium.Marker(
        location=[lat , lon],
        popup="Điểm xe bus" ,
        tooltip=f"Điểm xe bus số {idx}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    if idx == idx_gan_nhat : 
        folium.PolyLine(
            locations=[[center_humg.y , center_humg.x] , [lat , lon]],
            color='green',
            weight=4,
            opacity=0.8,
            tooltip=f"Khoảng cách: {danh_sach_khoang_cach[idx]} m"
        ).add_to(m)

m.save('diem_se_bus_gan_nhat.html')