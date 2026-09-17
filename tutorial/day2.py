# review day 1: 

# Bài tập : 
# Bài 1 : Tạo 3 biến: ten_truong, vi_do, kinh_do. In ra câu: "Trường X ở tọa độ (lat, lon)".

ten_truong = 'ĐH Mỏ'
vi_do = 21.0201
kinh_do = 105.3101
print(f"Trường {ten_truong} ở tọa độ ({vi_do} , {kinh_do})")

# -> biến (variable) : lưu trữ dữ liệu vào 1 ô nhớ , có thể truy cập dữ liệu thông qua tên biến 
# -> Quy ước đặt tên biến , hàm 
ten_bien = 'value' # snake_case cho biến / hàm
PI = 3.14 # UPPER_CASE cho hằng số
class DiaDiem : # PascalCase cho class
    pass

# Bài 2 : Tạo list 5 thành phố Việt Nam. In phần tử đầu, cuối, và độ dài.
cities = ['Hà Nội' , 'Đà Nẵng' , 'Huế' , 'Cần thơ' , 'Sài Gòn']
print(f"Phần tử đầu : {cities[0]} , Phần tử cuối : {cities[len(cities) - 1]} , Độ dài : {len(cities)}")

# -> list (danh sách) : cơ sở dữ liệu lưu trữ danh sách dữ liệu được lưu trữ liên tục và giống nhau về kiểu dữ liệu , có thể truy cập dữ liệu thông qua chỉ số index 

# Bài 3 : Tạo dict mô tả 1 địa điểm có name, lat, lon, type. In tên địa điểm.
my_flat = {
    "name" : "406/47 xuân phương",
    "lat" : 21.3212,
    "lon" : 105.3211,
    "type" : "Flat"
}
print(f"Tên trọ : {my_flat.get('name')}")

# -> dict (từ điển) : cơ sở dữ liệu lưu trữ đối tượng mang nhiều thuộc tính khác nhau , thuộc tính bao gồm key kiểu string và value có thể mang bất cứ kiểu gì 
# có thể truy cập dữ liệu thuộc tính của 1 đối tượng thông qua phương thức get(key)

# Bài 4 : Cho nhiet_do, in ra "Nóng" nếu > 30, "Mát" nếu 20–30, "Lạnh" nếu < 20.
nhiet_do = 24
if nhiet_do > 30 :
    print('Nóng')
elif nhiet_do <= 30 and nhiet_do >= 20 : 
    print('Mát')
else :
    print('Lạnh')

# Bài 5 : Cho list 5 tọa độ [lat, lon]. Duyệt và in từng cặp.
coordinates = [
    [21 , 105],
    [22 , 106],
    [23 , 107],
    [24 , 108],
    [25 , 109],
]
for toa_do in coordinates :
    print(toa_do)

# Phần 6 : Hàm (function)

# 6.1. Cú pháp 

# Hàm không có giá trị trả về
def ten_ham(tham_so) :
    # thân hàm : xử lý tác vụ có thể tái sử dụng
    cak = tham_so + 'adu'
    print(cak)
ten_ham('anh tao')
ten_ham('em tao')

# Hàm có giá trị trả về 
def nhan_muoi(tham_so = 10) : 
    return tham_so * 10
print(nhan_muoi())
print(nhan_muoi(20))

# Bài tập : Lọc danh sách địa điểm theo loại. 
# -> Hàm nhận đầu vào là 1 danh sách các trường , loại trường muốn lọc và đầu ra là 1 danh sách mới đã lọc dựa trên loại trường
truong_list = [
    {"name": "ĐH Mỏ", "type": "ĐH"},
    {"name": "THPT Kim Liên", "type": "THPT"},
    {"name": "ĐH Bách Khoa", "type": "ĐH"},
    {"name": "ĐH Mỏ", "type": "ĐH"},
    {"name": "THPT Phạm con bò", "type": "THPT"},
]

def filter_type(list , type) : 
    result = []
    for school in list : 
        if school.get("type") == type :
            result.append(school)
    return result

print(filter_type(truong_list , 'ĐH'))

# Phần 7 : Import và Module 

# 7.1. Module 
# - Bản chất : Một module đơn giản là 1 file python chứa mã nguồn , bao gồm các hàm , lớp hoặc biến đã được định nghĩa 
# - Mục đích : Chia nhỏ chương trình lớn thành nhiều file độc lập , giúp dễ quản lý , bảo trì và tái sử dụng 
# - Package (gói) : Là một thư mục chứa nhiều file module , thường đi kèm một file  đặc biệt __init__.py để báo cho python biết đây là một gói dữ liệu 

# 7.2. Import
# - Bản chất : Import là câu lệnh dùng để nạp 1 module hoặc package (từ thư viện chuẩn của python , thư viện cài qua pip , hoặc file .py do bạn tự định nghĩa) vào file
# hiện tại để sử dụng 

# - Cú pháp import phổ biến : 

#   import <tên_module> : Nạp toàn bộ module vào file hiện tại 
import math
print(math.sqrt(8)) # gọi bằng tên module đó

#   import <tên_module> as <alias> : Nạp toàn bộ module vào nhưng đổi tên viết tắt cho gọn gàng và dễ gọi 
import geopandas as gpd 

#   from <tên_module> import <tên_object> : Chỉ nạp một thành phần cụ thể từ 1 module có thể là biến , hàm , lớp
from shapely.geometry import Point
p = Point(105.77 , 21.07) 

# 7.3. Các quy ước chuẩn (PEP 8) khi dùng import 
# - Vị trí đặt import bắt buộc ở đầu file 
# - Các nhóm module : standard library (thư viện chuẩn python) : os , math , json... , Third-Party Libraries (thư viện cài qua bên thứ 3 qua pip) : geopandas , folium..
# local modules (module tự viết trong dự án) : các file .py mà bạn tạo trong thư mục dự án

