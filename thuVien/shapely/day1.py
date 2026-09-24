from shapely.geometry import Point , LineString , Polygon 

# 1. Khái niệm 
    # - Shapely là thư viện Python mã nguồn mở dùng để tạo , thao tác , và phân tích các đối tượng hình học phẳng 
    # -> Shapely chỉ quan tâm đến hình học thuần thúy (tọa độ , hình dáng) . Nó không quản lý các dữ liệu thuộc tính (tên , địa điểm...) và không quản lý hệ tọa độ 
    # (CRS) do vậy khi tính toán đơn vị sẽ hoàn toàn phụ thuộc và hệ tọa độ 

# 2. Các đối tượng hình học cơ bản 

# 2.1. Point 
# - Point là điểm gồm 2 giá trị (x , y) -> với dữ liệu địa lý (lon , lat)

p = Point(105.3333,21.2112) # -> Sử dụng object Point cung cấp giá trị cho 2 tham số tương ứng (x , y)
print(p)

# - Cạm bẫy lớn nhất cần lưu ý : (x , y) = (lon , lat) 
    # + Trong toán học mặt phẳng trục x (nằm ngang ) và trục y (nằm dọc)
    # + Trong địa lý kinh độ lon (chạy ngang) và vĩ độ lat (chạy dọc)
    # -> Mà shapely theo toán học (x , y) nên khi biểu diễn tọa độ địa lý (lon , lat)

# - Một số thuộc tính của object Point 
print(p.x) # kinh độ trục ngang 
print(p.y) # vĩ độ trục dọc
print(p.wkt) # well-known text : định dạng chuỗi chuẩn để trao đổi hình học 
print(p.geom_type) # Loại hình 

# - Cách tạo danh sách Point với danh sách dữ liệu ban đầu 
coords = [
    (105.8430, 21.0050),   # ĐH Mỏ
    (105.8435, 21.0056),   # ĐH Bách Khoa
    (105.8350, 21.0085),   # THPT Kim Liên
]
points = [Point(lon , lat) for lon , lat in coords]

# 2.2. LineString 
# - LineString là đường gồm danh sách các điểm nối với nhau nhưng điểm đầu không trùng với điểm cuối 

duong = LineString([
    (105.66 , 21.33),
    (105.16 , 21.43),
    (105.46 , 21.63),
]) # -> Sử dụng object LineString truyền vào tham số là danh sách các tuple mỗi tuple chứa dữ liệu (x , y)
print(duong)

# - Một số thuộc tính của object LineString 
print(duong.length) # độ dài -> đơn vị theo tọa độ
print(duong.bounds) 
print(duong.geom_type) # dạng hình học 

# 2.3. Polygon 
# - Polygon là đa giác gồm danh sách các điểm nối với nhau và điểm đầu luôn trùng với điểm cuối
# -> Với shapely luôn tự động khép kín lại đa giác = cách tự động khai báo điểm cuối trùng với điềm đầu

da_giac = Polygon([
    (105.840, 21.000),   
    (105.850, 21.000),   
    (105.850, 21.010),   
    (105.840, 21.010) 
]) # -> Sử dụng object Polygon truyền tham số là danh sách tuple mỗi tuple chứa dữ liệu gồm (x , y)

print(da_giac) # -> khi không khai báo điểm cuối shapely tự động khai báo nó trùng với điểm đầu 

# - Các thuộc tính của object Polygon 
print(da_giac.area) # diện tích đa giác -> đơn vị dựa vào hệ tọa độ
print(da_giac.length) # chu vi đa giác
print(da_giac.centroid) # tâm đa giác
print(da_giac.exterior) # viền ngoài đa giác
print(da_giac.geom_type) # dạng hình học 

# -> Shapely là thư viện giúp cung cấp các đối tượng hình học được biểu diễn dưới dạng mặt phẳng 2D từ đó có thể dễ dàng tính toán khoảng cách , chu vi , diện tích...
# - Point : Đối tượng dạng điểm dữ liệu cần truyền vào là tuple gồm (x , y) 
# - LineString : Đối tượng dạng đường dữ liệu cần truyền vào là danh sách tuple cần ít nhất 2 điểm  
# - Polygon : Đối tượng dạng vùng dữ liệu cần truyền vào là danh sách tuple cần ít nhất 3 điểm với điều đầu luôn trùng điểm cuối

# 3. Phương thức tứ đại -> 4 phương thức dùng thường xuyên

# 3.1. distance() -> tính khoảng cách 
# - Hàm này được gọi bởi 1 đối tượng hình học và cần truyền vào 1 đối tượng hình học từ đó áp dụng công thức tính pi-ta-go tính khoảng cách

p1 = Point(105.22 , 21.21)
p2 = Point(105.34 , 21.42)
khoang_cach = p1.distance(p2) # -> tính khoảng cách giữa 2 điểm 

line1 = LineString([(102.22 , 12.33) , (112.22 , 33.12)])
khoan_cach2 = p1.distance(line1) # -> tính khoảng cách giữa 1 điểm và 1 đường 

# Point → Polygon (điểm ở ngoài, khoảng cách = cạnh gần nhất)
poly = Polygon([(0,0), (2,0), (2,2), (0,2)])
p_out = Point(3, 1)
print(p_out.distance(poly))   # 1.0

# Point → Polygon (điểm ở TRONG, khoảng cách = 0)
p_in = Point(1, 1)
print(p_in.distance(poly))    # 0.0

# 3.2. buffer() -> vùng đệm 
# - Hàm này được gọi bởi 1 đối tượng hình học và truyền tham số là 1 số -> tạo ra một polygon mới đại diện cho vùng không gian bao quanh đối tượng ban đầu trong bán 
# kính bằng với giá trị truyền vào 

vung_dem = p.buffer(1) 
# -> Tạo ra đối tượng vùng với bán kính 1 tính từ điểm ra

# 3.3. within() / contains() -> quan hệ chứa 

hanoi = Polygon([
    (105.70, 20.90), (106.00, 20.90),
    (106.00, 21.20), (105.70, 21.20)
])
diem_dh_mo = Point(105.8430, 21.0050)

# - hàm within() : Trả về true/false giúp kiểm tra 1 đối tượng có nằm bên trong 1 đối tượng hay không 
print(diem_dh_mo.within(hanoi))

# - hàm contains() : Trả về true/false giúp kiểm tra 1 đối tượng có chứa 1 đối tượng con nằm trong hay không 
print(hanoi.contains(diem_dh_mo))

# 3.4. intersects() -> giao nhau 

poly1 = Polygon([(0,0), (3,0), (3,3), (0,3)])
poly2 = Polygon([(2,2), (5,2), (5,5), (2,5)])

print(poly1.intersects(poly2))   # True — có chồng lấn
print(poly1.intersection(poly2)) # POLYGON ((2 2, 2 3, 3 3, 3 2, 2 2))

# - Hàm intersects() : Trả về true/false với đối tượng hình học gọi hàm này và cần truyền vào 1 đối tượng hình học khác và trả về true nếu tập hợp giao điểm của 2 đối
# tượng có ít nhất 1 điểm chung 

# - Các trường hợp thực tế trả về true : 
    # + Polygon - Point : Điểm nằm bên trong hoặc nằm trên ranh giới vùng
    # + Polygon - Linestring : Đường nằm xuyên qua hoặc bên trong vùng 
    # + Polygon - Polygon : 2 vùng lấn diện tích lên nhau hoặc nằm trong nhau 
    # + LineString - LineString : 2 đường cắt nhau
# -> Trả về false chỉ khi 2 hình rời rạc không liên quan đến nhau 

# 4. Hệ tọa độ 
# - Có 2 hệ tọa độ chính : Hệ tọa độ địa lý và hệ tọa độ phẳng
# 4.1. Hệ tọa độ địa lý 
    # + Bản chất : Mô phỏng trái đất dưới dạng hình cầu 3D
    # + Đơn vị đo : Độ thập phân 
    # + Dùng trong trường hợp lưu trữ dữ liệu toàn cầu về các đối tượng địa lý , dùng với hệ thống GPS khi thu thập dữ liệu thô và truyền / nhận dữ liệu qua API

# 4.2. Hệ tọa độ phẳng  
    # + Bản chất : Trải phẳng bề mặt cong trái đất lên mặt phẳng 2D 
    # + Đơn vị đo : Mét
    # + Dùng khi tính toán khoảng cách, diện tích chính xác trên ứng dụng bản đồ phẳng 

# 4.3. Ảnh hưởng trực tiếp tới tính toán trong shapely 
# - Bản chất shapely là bộ máy tính toán hình học mặt phảng 2D , nó thực hiện các phép toán x, y trên mặt phẳng mà không biết hoặc tự động chuyển hệ tọa độ
# -> Khi bạn truyền tọa độ vào shapely nó chỉ coi đó là các con số giá trị trên trục 2D xy đơn thuần 
# -> Thư viện shapely chỉ hoạt động giữa trên toán học thuần thúy trên mặt phẳng mà không quan tâm đến : đơn vị đo , hệ tọa độ , bề mặt trái đất