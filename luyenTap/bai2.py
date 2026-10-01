# Bài 2 : Tính toán dữ liệu accuracy và loại bỏ các điểm nhiễu , sau đó nối tất cả các điểm hợp thành dạng đường , chuyển đổi hệ tọa độ và tính toán khoảng cách 
# và vận tốc trung bình , triển khai thuật toán phát hiện điểm dừng nghỉ và trực quan hóa bản đồ bằng folium

import geopandas as gpd
from shapely.geometry import Point , LineString
import folium 
from datetime import datetime , timedelta

# Hàm chuyển kinh độ / vĩ độ về đơn vị độ thập phân
def chuyen_do_tp(val_raw) : 
    val = float(val_raw)

    degrees = int(val // 100)
    min = val % 100 
    decimal = degrees + (min / 60)

    return decimal

# Hàm chuyển chuỗi thời gian về dạng datetime
def chuyen_thoi_gian(time_raw) : 
    time_raw = f"{time_raw[:2]}:{time_raw[2:4]}:{time_raw[4:6]}" 

    hom_nay = datetime.today().date()
    date_time_str = str(hom_nay) + ' ' + time_raw  
    
    date_time_utc = datetime.strptime(date_time_str , "%Y-%m-%d %H:%M:%S")
    return date_time_utc

diems = []

# Đọc file và thêm vào mảng các dict chứa thông tin 1 điểm gồm tọa độ , thời gian , độ sai số 
with open('12_nmea_100_points.txt' , 'r' , encoding='utf-8') as file : 
    for line in file : 
        line = line.strip()
        if(line.startswith('$GPGGA')) : 
            parts = line.split(',')

            lat = chuyen_do_tp(parts[2])
            lon = chuyen_do_tp(parts[4])

            date_time = chuyen_thoi_gian(parts[1])

            hdop = float(parts[8])
            accuracy = round(hdop * 3.0, 1) # tính accuracy (độ sai số về mặt vị trí ) = HDOP * UERE với UERE mặc định ≈ 3.0m

            diems.append({
                "time" : date_time,
                "latitude" : lat,
                "longitude" : lon,
                "accuracy" : accuracy,
                "geometry" : Point(lon , lat)
            })

# Chuyển dữ liệu từ danh sách sang gdf giúp quản lý và phân tích dữ liệu
gdf = gpd.GeoDataFrame(diems , crs='EPSG:4326')
gdf_accuracy = gdf.loc[gdf['accuracy'] < 20]  # lọc dựa trên độ sai số về mặt vị trí , lấy những điểm sai số < 20m

# Nối toàn bộ điểm thành 1 đường 
duong = LineString(zip(gdf_accuracy['longitude'] , gdf_accuracy['latitude']))  
gs_duong = gpd.GeoSeries(duong , crs='EPSG:4326')
gs_duong_met = gs_duong.to_crs('EPSG:32648')

# Tính tổng quãng đường 
total_distance_m = gs_duong_met.length.loc[0]
total_distance_km = total_distance_m / 1000

# Tính tổng thời gian
gdf_accuracy['time'] = gpd.pd.to_datetime(gdf_accuracy['time']) # ép tất cả giá trị cột time kiểu là string sang kiểu datetime 
time_start = gdf_accuracy['time'].min()
time_end = gdf_accuracy['time'].max()
total_time_seconds = (time_end - time_start).total_seconds()
total_time_hours = total_time_seconds / 3600

# Tính vận tốc trung bình 
avg_speed = total_distance_km / total_time_hours

print("\n=== BÁO CÁO PHÂN TÍCH QUỸ ĐẠO ===")
print(f"- Tổng quãng đường thực tế: {total_distance_km:.3f} KM ({total_distance_m:.1f} m)")
print(f"- Thời gian di chuyển: {total_time_hours:.1f} giờ")
print(f"- Vận tốc trung bình: {avg_speed:.2f} km/h")

# Thuật toán phát hiện điểm dừng nghỉ 
# -> Nếu 1 điểm là điểm dừng nghỉ thì thỏa mãn đồng thời các điều kiện sau : 
# + Khoảng cách 2 điểm < 100 m
# + Thời gian di chuyển 2 điểm > 15 phút
# + Vận tốc khi di chuyển < 1 km/h
# -> Khi khoảng cách 2 điểm ngắn nhưng thời gian di chuyển thực tế lại mất nhiều hơn thời gian dự kiến ban đầu khi duy trì vận tốc trung bình 

# 1. Đổi hệ tọa độ sang EPSG:32648 để tính khoảng cách chính xác theo Mét
gdf_meters = gdf_accuracy.to_crs("EPSG:32648").copy()

# 2. Tính Khoảng cách (mét) giữa điểm hiện tại và điểm ngay trước đó
gdf_meters['dist_m'] = gdf_meters.geometry.distance(gdf_meters.geometry.shift())

# 3. Tính Thời gian di chuyển (phút) giữa 2 điểm kề nhau
gdf_meters['time_diff_min'] = gdf_meters['time'].diff().dt.total_seconds() / 60.0

# 4. Tính Vận tốc di chuyển (km/h) giữa 2 điểm
# (dist_m / 1000) / (time_diff_min / 60) -> đơn vị km/h
gdf_meters['speed_kmh'] = (gdf_meters['dist_m'] / 1000.0) / (gdf_meters['time_diff_min'] / 60.0)

# ---------------------------------------------------------
# THỰC THI ĐIỀU KIỆN ĐIỂM DỪNG NGHỈ
# ---------------------------------------------------------
cond_distance = gdf_meters['dist_m'] < 100.0         # Khoảng cách < 100m
cond_time     = gdf_meters['time_diff_min'] > 15.0   # Thời gian > 15 phút
cond_speed    = gdf_meters['speed_kmh'] < 1.0        # Vận tốc < 1 km/h

# Lọc các điểm thỏa mãn ĐỒNG THỜI 3 điều kiện trên
stop_points = gdf_meters[cond_distance & cond_time & cond_speed].copy()

print(f"\n Tìm thấy {len(stop_points)} điểm dừng nghỉ thỏa mãn điều kiện")

# ---------------------------------------------------------
# TRỰC QUAN HÓA BẢN ĐỒ BẰNG FOLIUM
# ---------------------------------------------------------

# 1. Xác định vị trí trung tâm bản đồ (Lấy trung bình cộng tọa độ các điểm hợp lệ)
center_lat = gdf_accuracy['latitude'].mean()
center_lon = gdf_accuracy['longitude'].mean()

# Khởi tạo bản đồ Folium với góc nhìn trung tâm
m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="OpenStreetMap")

# 2. Vẽ đường quỹ đạo di chuyển (PolyLine) nối tất cả các điểm đã lọc
coords = list(zip(gdf_accuracy['latitude'], gdf_accuracy['longitude']))
folium.PolyLine(
    locations=coords,
    color="red",
    weight=4,
    opacity=0.7,
    tooltip="Quỹ đạo di chuyển"
).add_to(m)

# 3. Cắm mốc Điểm Bắt Đầu (Start Point) và Điểm Kết Thúc (End Point)
start_row = gdf_accuracy.iloc[0]
end_row = gdf_accuracy.iloc[-1]

folium.Marker(
    location=[start_row['latitude'], start_row['longitude']],
    popup=f"<b>BẮT ĐẦU</b><br>Thời gian: {start_row['time'].strftime('%H:%M:%S')}",
    tooltip="Điểm bắt đầu",
    icon=folium.Icon(color="green", icon="play", prefix="fa")
).add_to(m)

folium.Marker(
    location=[end_row['latitude'], end_row['longitude']],
    popup=f"<b>KẾT THÚC</b><br>Thời gian: {end_row['time'].strftime('%H:%M:%S')}",
    tooltip="Điểm kết thúc",
    icon=folium.Icon(color="darkred", icon="flag", prefix="fa")
).add_to(m)

# 4. Vẽ tất cả các điểm GPS thông thường dạng CircleMarker nhỏ
for idx, row in gdf_accuracy.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color="dodgerblue",
        fill=True,
        fill_color="dodgerblue",
        fill_opacity=0.8,
        popup=f"Thới gian: {row['time'].strftime('%H:%M:%S')}<br>Accuracy: {row['accuracy']}m"
    ).add_to(m)

# 5. Đánh dấu ĐIỂM DỪNG NGHỈ (Nếu tìm thấy điểm thỏa mãn 3 điều kiện)
if not stop_points.empty:
    for idx, row in stop_points.iterrows():
        # Cắm Marker màu đỏ kèm biểu tượng tạm dừng
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=(
                f"<b> ĐIỂM DỪNG NGHỈ</b><br>"
                f"Thời điểm: {row['time'].strftime('%H:%M:%S')}<br>"
                f"Thời gian dừng: {row['time_diff_min']:.1f} phút<br>"
                f"Khoảng cách dịch chuyển: {row['dist_m']:.1f} m<br>"
                f"Vận tốc: {row['speed_kmh']:.2f} km/h"
            ),
            tooltip=f"Điểm dừng nghỉ ({row['time_diff_min']:.1f} phút)",
            icon=folium.Icon(color="red", icon="pause", prefix="fa")
        ).add_to(m)
        
        # Vẽ vòng tròn bán kính thể hiện vùng dừng nghỉ
        folium.Circle(
            location=[row['latitude'], row['longitude']],
            radius=100,  # Vùng 100m theo điều kiện
            color="red",
            weight=1,
            fill=True,
            fill_color="red",
            fill_opacity=0.2
        ).add_to(m)

# 6. Lưu bản đồ ra file HTML
m.save("quydao_gps_ban_do.html")

