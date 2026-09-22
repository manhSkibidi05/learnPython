# Review day 2 : 

# Bài 6 : Viết hàm trong_ha_noi(lat, lon) trả về True nếu điểm nằm trong Hà Nội (lat 20.9–21.2, lon 105.7–106.0).

def trong_ha_noi(lat , lon) : 
    if(lat > 20.9 and lat < 21.2 and lon > 105.7 and lon < 106.0) :
        return True
    return False

print(trong_ha_noi(21 , 105.8))

# -> sử dụng hàm giúp tái sử  dụng lại code với các giá trị khác nhau 

# - module : Bản chất là 1 file python (.py) có thể chứa các hàm , class , biến -> khi muốn sử dụng các chức năng của module đó trong file khác cần import nó
# -> Các nhóm module : 
# + Standard library (thư viện chuẩn python): các module do chính python tạo ra  -> vd : math
# + Third-Party Libraries (thư viện do bên thứ 3) : các module do bên thứ ba tạo , có thể tải về thông qua pip  -> vd : geopandas , folium ...
# + Local modules : các module do chính người dùng tạo -> vd : file.py do người dùng tạo

# - package (gói) : Là một thư mục chứa nhiều module 

# - import : Là câu lệnh có thể giúp thêm 1 module/package vào file mới để có thể tái sử dụng 
# -> Các cách import module : 
#import math 
# -> import + tên module dùng chính tên module truy cập vào các thuộc tính và phương thức 

#import geopandas as gpd
# -> import + tên module + as + alias (tên viết tắt được quy định của module đó)

#from shapely.geometry import Point 
# -> from + tên module + import + tên class/hàm -> chỉ import 1 class/hàm từ module đó 

# Phần 8 : Lập trình hướng đối tượng (OOP- object oriented programming)

# -> OOP : Là phương pháp tư duy mô phỏng các đối tượng ngoài đời thực vào trong mã nguồn . Đối với backend GIS , OOP cực kỳ quan trọng vì bản thân các thư viện như
# Shapely hay Geopandas đều coi mỗi đối tượng địa lý (Point , Polygon , Layer) là 1 object 

# 8.1. Bốn khái niệm cốt lõi trong OOP 
# - Class (lớp) : Bản thiết kế hoặc khuân mẫu , nó định nghĩa các đặc tính và hành vi chung mà mọi đối tượng tạo ra từ nó sẽ có 
# - Object (đối tượng) : Một thể hiện cụ tể được tạo ra từ class 
# - Attributes (thuộc tính) : Các biến khởi tạo bên trong class giúp lưu trữ thông tin , đặc điểm về đối tượng 
# - Methods (phương thức) : Các hàm được định nghĩa bên trong class giúp mô tả hành vi mà đối tượng có thể thực hiện 

# 8.2. Ví dụ thực tế : Định nghĩa class biểu diễn điểm dịch vụ (spatial point) trong python backend 

import math 

class SpatialPoint : 
    # Hàm khởi tạo -> được tự động gọi khi tạo 1 object
    def __init__(self , name : str , lat : float , lon : float , category : str):
        # khởi tạo thuộc tính của class : 
        self.name = name
        self.lat = lat
        self.lon = lon
        self.category = category

    # khởi tạo phương thức : trả về định dạng geojson 
    def to_geojson(self) -> dict : 
        return {
            "type" : "Feature",
            "geometry" : {
                "type" : "Point",
                "coordinates" : [self.lon , self.lat]
            },
            "properties" : {
                "name" : self.name,
                "category" : self.category
            }
        }

    # Method (Phương thức 2): Tính khoảng cách xấp xỉ theo đường chim bay đến điểm khác (km)
    def distance_to(self, other_point: 'SpatialPoint') -> float:
        # Công thức đơn giản hóa khoảng cách giữa 2 tọa độ
        lat_diff = math.radians(other_point.lat - self.lat)
        lng_diff = math.radians(other_point.lon - self.lon)
        
        a = math.sin(lat_diff / 2)**2 + math.cos(math.radians(self.lat)) * math.cos(math.radians(other_point.lat)) * math.sin(lng_diff / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        radius_earth_km = 6371.0
        return round(radius_earth_km * c, 2)

# Khởi tạo object từ class SpatialPoint trên 
store_a = SpatialPoint(name='Cửa hàng bia' , lat=10.7769 , lon=106.7009 , category='store')
store_b = SpatialPoint(name="Cửa hàng Thủ Đức", lat=10.8505, lon=106.7719, category="Retail")

# Truy cập Thuộc tính (Attributes)
print(f"Tên địa điểm: {store_a.name}")
print(f"Tọa độ: [{store_a.lat}, {store_a.lon}]")

# Gọi Phương thức (Methods)
# Xuất dữ liệu ra chuẩn GeoJSON để trả về cho API
geojson_data = store_a.to_geojson()
print("GeoJSON Output:", geojson_data)

# Tính khoảng cách giữa Cửa hàng A và Cửa hàng B
dist = store_a.distance_to(store_b)
print(f"Khoảng cách giữa 2 cửa hàng: {dist} km")

# -> Từ khóa self : Đại diện cho đối tượng đang thực thi phương thức 

# 8.3. Bài tập thực hành 

class GeofencePolygon : 
    def __init__(self , name : str , center_lat : float , center_lon : float , radius_km : float):
        self.name = name
        self.lat = center_lat
        self.lon = center_lon
        self.radius = radius_km

    def contains_point(self , point : 'SpatialPoint') -> bool : 
        # Sử dụng công thức haversine tính khoảng cách giữa 2 điểm trên bản dồ : điểm 1 (x , y) , điểm 2 (x , y) , bán kính trung bình trái đất R = 6371 km

        # Bước 1 : tính độ lệch góc (đổi sang radian)
        lat_diff = math.radians(point.lat - self.lat)
        lon_diff = math.radians(point.lon - self.lon)

        # Bước 2 : tính biến trung gian a 
        a = (math.sin(lat_diff / 2)**2 + math.cos(math.radians(self.lat)) * math.cos(math.radians(point.lat)) * math.sin(lon_diff / 2)**2)

        # Bước 3 : tính góc trung tâm c 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Bước 4 : tính khoảng cách thực tế d = R x c với R là bán kính trung bình của trái đất 
        radius_earth_km = 6371
        d = round(radius_earth_km * c , 2)

        # -> theo yêu cầu bài toán kiểm tra xem điểm trên bản đồ có nằm trong khu vực giao hàng điểm trung tâm hay không 
        if self.radius >= d :
            return True
        else :
            return False

shoppe_polygon = GeofencePolygon(name = 'shoppe food' , center_lat=10.8505 , center_lon=106.7719 , radius_km= 10)
check = shoppe_polygon.contains_point(store_a)
print(f'{store_a.name} có nằm trong vùng ship của {shoppe_polygon.name} không : {check}')

# Phần 9 : Xử lý lỗi (try / except)

# - Định nghĩa : sử dụng cấu trúc try except với các đoạn code có thể gặp lỗi và xử lí khi lỗi xảy ra không làm crash ứng dụng 

# - Cú pháp : 
try : 
    # code có thể lỗi 
    so = int('adus')
except ValueError : # lỗi được quy định bởi python 
    # xử lý khi gặp lỗi 
    print('Không chuyển được thành số')

# - Các trường hợp lỗi thường gặp : 
# -> FileNotFoundError : File không tồn tại 
# -> KeyError : Truy cập key không tồn tại trong dict
# -> IndexError : Truy cập list ngoài phạm vi
# -> ValueError : Chuyển đổi kiểu thất bại 
# -> AttributeError : Gọi method không tồn tại 
# -> IndentationError : Thụt lề sai 
# -> NameError : Dùng biến chưa khai báo 

# Review : 
# Bài tập tạo class điểm với thuộc tính kinh độ , vĩ độ , name , category và có phương thức sử dụng để tính toán ra khoảng cách địa lý (khoảng cách đường chim bay) 
# giữa 2 tọa độ

class diem_dia_ly : 
    def __init__(self , lat : float , lon : float , name : str , category : str ):
        self.lat = lat 
        self.lon = lon
        self.name = name
        self.category = category

    def khoang_cach_dia_ly(self , lat : float , lon : float) -> float :
        # Công thức đơn giản hóa khoảng cách giữa 2 tọa độ
        lat_diff = math.radians(lat - self.lat)
        lng_diff = math.radians(lon - self.lon)
        
        a = math.sin(lat_diff / 2)**2 + math.cos(math.radians(self.lat)) * math.cos(math.radians(lat)) * math.sin(lng_diff / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        radius_earth_km = 6371.0
        return round(radius_earth_km * c, 2)


diem_p = diem_dia_ly(21.0323 , 105.1122 , 'nhà của toi' , 'home')
diem_k = diem_dia_ly(21.8382 , 105.9212 , 'nhà của bạn' , 'home')

khoang_cach_mot = diem_p.khoang_cach_dia_ly(diem_k.lat , diem_k.lon)
print(f"Khoảng cách giữa điểm {diem_p.name} và điểm {diem_k.name} là : {khoang_cach_mot} km")