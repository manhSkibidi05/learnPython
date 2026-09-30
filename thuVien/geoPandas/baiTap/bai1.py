# Bài 1 : Hệ thống nhận một tập dữ liệu các địa điểm tham quan (Points of Interest - POI) tại Hà Nội dưới 
# dạng GeoJSON. Cần lọc ra các địa điểm thuộc loại "Museum" (Bảo tàng) và có rating >= 4.6, trực quan hóa lên bản đồ 
# Web và xuất ra tệp GeoJSON mới. 

import geopandas as gpd
from shapely.geometry import Point
import folium 

gdf = gpd.read_file('du_lieu.json')     # -> Đọc file json định dạng geoJSON tạo ra bảng geoDataFrame

gdf_filter = gdf.loc[(gdf['category'] == 'Museum') & (gdf['rating'] >= 4.6)]  # -> Lọc bảng gdf dựa vào dữ liệu thuộc tính 

if isinstance(gdf_filter , gpd.GeoDataFrame) :  # -> hàm isinstance(biến , đối tượng) : giúp kiểm tra 1 biến có phải thể hiện của 1 đối tượng cụ thể không 
    gdf_filter.to_file('bao_tang.json') # -> nếu có giúp ép kiểu biến đó và sử dụng các phương thức của đối tượng đó : hàm to_file() giúp xuất file cụ thể 

# Hiện thị các điểm bảo tảng lên bản đồ 
center_hanoi = Point(105.81746473658592 , 21.025818006907244) # -> Tạo điểm trung tâm của bản đồ

m = folium.Map(location=[center_hanoi.y , center_hanoi.x] , zoom_start=13 , tiles='OpenStreetMap') # -> khởi tạo bản đồ folium 


if isinstance(gdf_filter , gpd.GeoDataFrame) : 
    for i , row in gdf_filter.iterrows() :      # thêm các điểm thỏa mãn điểm kiện hiện thị lên bản đồ folium bằng các marker 
        lon = row.geometry.x
        lat = row.geometry.y

        popup_content = f"""
        <div style='width: 200px;'>
            <h4><b>{row.get('name', 'Bảo tàng')}</b></h4>
            <p><b>Địa chỉ:</b> {row.get('address', 'Đang cập nhật')}</p>
            <p><b>Đánh giá:</b> ⭐ {row.get('rating', 'N/A')}</p>
        </div>
        """

        # Cắm Marker lên bản đồ
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=row.get('name', 'Xem chi tiết'),
            icon=folium.Icon(color='red', icon='university', prefix='fa') # Dùng biểu tượng bảo tàng
        ).add_to(m)

m.save('ban_do_bao_tang.html') # -> Xuất ra file bản đồ vừa định nghĩa




