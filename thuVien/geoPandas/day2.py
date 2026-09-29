# Review day1 : 

# - Tạo bảng geoDataFrame với cột geometry dạng điểm : 
# -> Sử dụng hàm : gpd.points_from_xy() khởi tạo cột với các đối tượng điểm nhanh chóng từ dữ liệu có sẵn
# -> gpd.points_from_xy() nhận vào tham số có thể là mảng/cột dữ liệu kinh độ và vĩ độ từ đó tạo ra cột dữ liệu dạng Point(x , y) một cách nhanh chóng , ngoài ra có 
# tham số z cho tọa độ 3D và tham số crs nhận vào hệ tọa độ của bảng dữ liệu này 

# - Tạo bảng geoDataFrame với cột geometry dạng đường và vùng : 

# + Dữ liệu dạng đường : Một linestring cần một danh sách chuỗi các điểm liên tiếp
# + Dữ liệu dạng vùng : Một polygon cần một danh sách điểm khép kín 
# -> Vì cấu trúc dữ liệu thô đường và vùng rất biến ảo nên geoPandas không có hàm ngắn gọn giống điểm points_from_xy() , vậy khi phát triển phần mềm GIS người ta xử
# lí dữ liệu đường và vùng bằng 3 cách chuẩn sau : 

# - Cách 1 : Đọc từ định dạng chuẩn (GeoJSON , Shapefile , WKT , WKB) -> phổ biến 90% sử dụng cách này trong thực tế 
# -> Trong dự án thực tế dữ liệu dạng đường và vùng hiếm được lưu thành các cột X , Y rời rạc chúng sẽ được đóng gói sẵn dưới dạng GeoJSON , shapefile hoặc chuỗi WKT
# -> Các dữ liệu dạng đường và vùng được lưu trữ sẵn trong file và chúng ta sử dụng hàm đọc file để lưu trữ các giá trị đó vào bảng gdf

    # + Đọc trực tiếp từ file GeoJSON / shapefile : 
    # -> Sử dụng hàm gpd.read_file() : geoPandas tự động phân tích và tạo cột geometry cho cả LineString và Polygon mà không cần dựng hình thủ công 

    # + Đọc từ chuỗi WKT (khi lưu trong database hoặc csv) : 
    # -> Chuỗi WKT là chuẩn định dạng văn bản để mô tả hình học . vd : 'LINESTRING(106.2 10.6 , 123.2 13.2)' . Và gpd hỗ trợ chuyển đổi nhanh bằng hàm gpd.GeoSeries.from_wkt()

import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point

# Dữ liệu từ CSV và chứa cột dữ liệu là chuỗi định  dạng WKT 
df_csv = pd.DataFrame({
    'name': ['Tuyến đường A', 'Khu vực B'],
    'wkt_geom': [
        'LINESTRING (106.69 10.77, 106.70 10.78, 106.71 10.79)',
        'POLYGON ((106.69 10.77, 106.70 10.77, 106.70 10.78, 106.69 10.77))'
    ]
})

# Chuyển đổi từ WKT sang cột geometry trong gdf 
gdf_csv = gpd.GeoDataFrame(
    df_csv ,
    geometry=gpd.GeoSeries.from_wkt(df_csv['wkt_geom']),
    crs='EPSG:4326'
)
print(gdf_csv)
# - Cách 2 : Gom các điểm (x , y) thành đường / vùng 
# - Cách 3 : Dựng đường / vùng từ các phép biến đổi không gian 

# _____________________________________DAY2______________________________________

# 4.Chuyển hệ tọa độ 
# - Sử dụng hàm : to_crs('hệ_tọa_độ') -> Sử dụng để chuyển đổi qua lại giữa hệ tọa độ địa lý và hệ tọa độ phẳng 

# - vd : Tính khoảng cách 2 tọa độ cho trước , 2 điểm cách nhau ~85 mét

p1 = Point(105.8430, 21.0050)   # ĐH Mỏ
p2 = Point(105.8435, 21.0056)   # Bách Khoa

array_points = gpd.points_from_xy([p1.x , p2.x] , [p1.y , p2.y] , crs='EPSG:4326')

array_points = array_points.to_crs('EPSG:32648')
print(array_points)

khoang_cach = array_points[0].distance(array_points[1])
print(khoang_cach)

# -> Sử dụng hệ tọa độ nào ? khi nào ? 
# - Với hệ tọa độ địa lý (EPSG:4326) : Sử dụng khi đọc file / ghi file và chia sẻ dữ liệu 
# - Với hệ tọa độ phẳng (EPSG:32648) : Sử dụng khi tính khoảng cách , diện tích , khoảng đệm buffer ... các phép tính toán hình học 2D
# - Với hệ tọa độ phẳng dành riêng cho web (EPSG:3857) : Sử dụng hiện thị web với thư viện Folium tự chuyển sang hệ tọa độ này khi render

# 5. Lọc dữ liệu thuộc tính + không gian
# 5.1. Lọc dựa trên cột dữ liệu thuộc tính 
# -> Giống với cách lọc của pandas , có thể sử dụng thuộc tính định vị loc hoặc iloc để lọc dữ liệu

df = pd.read_csv('vi_tri.csv')
df_filter = df.loc[: , ['name' , 'type' , 'address' , 'year']]
gdf = gpd.GeoDataFrame(
    df_filter,
    geometry=gpd.points_from_xy(x=df['lon'] , y=df['lat']),
    crs='EPSG:4326'
)
# Thuộc tính định vị gpd.loc : 
# + giá trị đầu là số hàng muốn lấy dựa vào tên hàng hoặc số index hàng -> index1 : index2 nếu để rỗng : thì lấy toàn bộ hàng
# + giá trị 2 là số cột muốn lấy dựa vào tên cột -> 'cột1' hoặc có thể nhận danh sách cột ['cột1' , 'cột2']

# - Lấy dữ liệu 1 cột 
gdf_name = gdf.loc[ : , 'name']
print(gdf_name)

# - Cắt dữ liệu với cả hàng và cột 
gdf_cut = gdf.loc[1 : 2 , ['name' , 'type']]
print(gdf_cut)

# - Lọc dữ liệu với điều kiện của cột thuộc tính trong bảng gdf : giá trị đầu của thuộc tính loc là điều kiện của 1 cột dữ liệu , giá trị 2 là các cột muốn lấy 
gdf_DH = gdf.loc[gdf['type'] == 'ĐH' , ['name' , 'type' , 'geometry']]
print(gdf_DH)

# - Lọc với nhiều điều kiện 
gdf_DH_2000 = gdf.loc[(gdf['type'] == 'ĐH') & (gdf['year'] > 2000) , ['name' , 'type' , 'geometry']]
print(gdf_DH_2000)

# 5.2. Lọc dữ liệu không gian với  bảng gdf
# - Dữ liệu không gian (spatial data) Là : Bất kỳ dữ liệu nào mô tả vị trí , hình dáng và ranh giới của các đối tượng trên bề mặt trái đất . Nó bao gồm 3 dạng hình
# học cơ bản và các biến thể nâng cao 
    # 1. Point (điểm) cặp tọa độ (x , y)
    # 2. LineString (đường) chuỗi liên tiếp của nhiều điểm (x1 , y1) , (x2 , y2)... có thứ tự
    # 3. Polygon (vùng) tập hợp các điểm nối lại thành một đường khép kín , bao bọc một khoảng diện tích 
    # 4. Multi-geometries & GeometryCollection : Tập hợp nhiều điểm / đường / vùng gom thành 1 đối tượng 



