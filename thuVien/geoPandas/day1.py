# - GeoPandas là gì ? 
# -> GeoPandas là thư viện mã nguồn mở hàng đầu trong python giúp làm việc với dữ liệu địa không gian (spatial data) một cách đơn giản và hiệu quả 
# -> Về bản chất GeoPandas mở rộng cấu trúc bảng từ DataFrame sang GeoDataFrame với 1 cột dữ liệu cố định tên là geometry để lưu trữ các đối tượng hình học (Point , LineString , Polygon)

# - GeoPandas là sự kết hợp của Pandas , Shapely , PyPROJ ? 
# -> Nếu dùng các thư viện riêng lẻ quy trình làm việc rất cồng kềnh : 
    # + Pandas để lưu trữ , lọc dữ liệu 
    # + Shaply dựng hình bản đồ 
    # + Tự gọi PyPROJ để đổi hệ tọa độ
# -> GeoPandas ra đời giúp đóng gói toàn bộ quy trình trên và phân chia nhiệm vụ cho 3 thư viện cốt lõi trên : Pandas -> quản lý bảng thuộc tính , shapely tính toán 
# hình học 2D , PyPROJ chuyển đổi hệ tọa độ 

# - Nếu GeoPandas đã tích hợp 3 thư viện trên có cần phải import các thư viện đó nữa không ? 
# -> Không bắt buộc phải import các thư viện đó trừ khi cần sử dụng các hàm hoặc đối tượng riêng lẻ của các thư viện đó 
# -> Không cần import các thư viện ngoài trên khi chỉ thao tác dữ liệu trên bảng GeoDataframe sẵn có hoặc cột GeoSeries
# -> Cần import các thư viện ngoài khi :  
    # + Cần import Pandas : Sử dụng các phương thức cấp cao của Pandas như khởi tạo dữ liệu thô từ dictionary , đọc file csv , nối nhiều bảng
    # + Cần import Shapely : Tự tạo 1 đối tượng hình học đơn lẻ để so sánh hoặc truy vấn với GeoDataFrame
    # + Cần import ProPROJ : Thực hiện thao tác biến đổi tọa độ phức tạp cho các điểm dữ liệu đơn lẻ mà không muốn đưa vào 1 GeoDataFrame

# GeoPandas là gì : Thư viện python mã nguồn mở được sử dụng để quản lý và phân tích dữ liệu không gian dưới dạng bảng gdf 
# GeoPandas là sự kết hợp của các thư viện : pandas , ProJ , shapely 
    # + pandas : Quản lý các dữ liệu dưới dạng bảng giống df nhưng có thêm cột geometry là một cột đặc biệt chứa dữ liệu các hình học không gian nên gọi là bảng gdf (geoDataFrame)
    # + pyPROJ : Quản lý hệ tọa độ hiện tại của các đối tượng địa lý , đảm nhận thuộc tính crs và có thể chuyển qua lại giữa các hệ tọa độ bằng phương thức to_crs()
    # + shapely : Sử dụng định nghĩa đối tượng địa lý dưới dạng hình học 2D và cung cấp các công thức toán học để tính toán khoảng cách , diện tích ...

# ________________________________________DAY 1 ______________________________________________

# 1. GeoDataFrame và DataFrame 

import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point

df = pd.DataFrame({
    "name" : ['Hà Nội' , 'Hải Phòng' , 'Thanh Hóa'],
    "lat" : [21.22 , 21.55 , 21.33],
    "lon" : [105.67 , 105.21 , 105.99]
})
print(df)

gdf = gpd.GeoDataFrame(
    df , 
    geometry=gpd.points_from_xy(df['lon'] , df['lat']) ,
    crs='EPSG:4326'
)
print(gdf)

# - Các thuộc tính và phương thức kiểm tra bảng gdf (geoDataFrame)
print(type(gdf))
print(gdf.crs)
print(gdf.geometry.name)

# - 2 thuộc tính cốt lõi của bảng gdf (geoDataFrame) : 

# + Thuộc tính gdf.crs : 
    # - Lúc này bạn đang truy cập vào thuộc tính quản lý hệ tọa độ của toàn bộ bảng gdf
    # - Bên dưới hệ thống thuộc tính này do thư viện pyPROJ quản lí
    # - Mục đích sử dụng : 
        # 1. Khai báo xem dữ liệu đang dùng hệ tọa độ nào giúp bạn biết đang ở hệ tọa độ địa lý hay hệ tọa độ phẳng
        # 2. Tiền đề sử dụng hàm to_crs() , cần biết mình đang ở hệ tọa độ nào trước khi chuyển sang hệ tọa độ khác

# + Thuộc tính gdf.geometry : 
    # - Lúc này bạn đang truy cập vào cột geometry chứa dữ liệu hình học không gian 
    # - Cột này trả về một đối tượng kiểu GeoSeries , mỗi ô chứa một đối tượng hình học không gian của shapely (Point , LineString , Polygon)
    # - Mục đích sử dụng : 
        # 1. Thực hiện các phép tính toán không gian hàng loạt : Gọi hàm tính toán của shapely lên toàn bộ hàng của cột (diện tích , chiều dài...)
        # 2. Trích xuất thuộc tính hình học : Lấy ra các đặc tính hình học như tọa độ tâm , ranh giới ngoài hay kiểm tra hình học có hợp lệ không 
        # 3. Thao tác vẽ / hiện thị bản đồ : Khi bạn gọi gdf.plot() , GeoPandas tự động lấy dữ liệu từ gdf.geometry để render hình ảnh ra màn hình 

# 2. Tạo geoDataFrame từ tọa độ có sẵn 
# - Sử dụng hàm : gpd.points_from_xy() -> trong geoPandas là 1 hàm tiện ích dùng để biến đổi nhanh 2 cột tọa độ riêng biệt x , y thành 1 cột dữ liệu gồm các đối tượng
# điểm Point của shapely 
# -> Hàm này thường được sử dụng để đọc dữ liệu từ các file bảng thuần thúy như CSV , excel , bảng cơ sở dữ liệu sql nới mà tọa độ kinh độ và vĩ độ ở 2 cột riêng biệt
# chứ chưa có hình học không gian  

# - Cú pháp : gpd.points_from_xy(x , y , z=none , crs=none)
    # + x : cột / mảng dữ liệu tọa độ trục x (kinh độ)
    # + y : cột / mảng dữ liệu tọa độ trục y (vĩ độ)
    # + z : Có thể có hoặc không chứa độ cao z nếu có dữ liệu 3D
    # + crs : Có thể có hoặc không hệ tọa độ gán cho chuỗi điểm vừa tạo 

# -> Tại sao dùng hàm này thay vì dùng vòng lặp để khởi tạo cột geometry :
    # - Cách cũ : Sử dụng hàm apply hoặc vòng lặp để khởi tạo điểm -> chạy chậm vì phải chạy từng dòng 1 bằng python thuần
    # - Cách mới : Sử dụng hàm points_from_xy được tối ưu hóa bằng thuật toán vectorized -> xử lý song song trên C/C++ cho tốc độ khởi tạo nhanh gấp hàng trăm lần trên
    # các tập dữ liệu lớn 

# -> Cơ chế vectorized - Xử lý vector hóa của hàm points_from_xy() :
    # - Bạn truyền nguyên cột df.lon (mảng x) và df.lat (mảng y) vào hàm  , geoPandas đẩy 2 mảng xuống mã máy C/C++ bên dưới xử lý 
    # - Tốc độ cực kỳ nhanh bộ máy C ghép cặp tọa độ x , y của hàng triệu dòng cùng 1 lúc trên RAM trước khi trả về kết quả cho python 

# - Bài tập : Chuyển file csv thành dữ liệu bảng gdf 
dia_diem_df = pd.read_csv('vi_tri.csv')

array_points = gpd.points_from_xy(dia_diem_df['lon'] , dia_diem_df['lat'] , crs='EPSG:4326')

dia_diem_filter_df = dia_diem_df.loc[: , ['name' , 'type' , 'address' , 'year']]

dia_diem_gdf = gpd.GeoDataFrame(dia_diem_filter_df , geometry=array_points)
print(dia_diem_gdf)
print(dia_diem_gdf.crs)

# - Tạo geoDataFrame bằng danh sách có sẵn : 
coords = [
    (105.8430, 21.0050, "ĐH Mỏ"),
    (105.8435, 21.0056, "Bách Khoa"),
    (105.8350, 21.0085, "Kim Liên"),
]

gdf = gpd.GeoDataFrame(
    [{'name' : n , 'geometry' : Point(lon , lat)} for lon , lat , n in coords],
    crs='EPSG:4326'
)

# - Tạo geoDataFrame từ shapely Point

gdf = gpd.GeoDataFrame({
    'name' : ['A' , 'B'],
    'year' : [2002 , 2001],
    'geometry' : [Point(103.22 , 21.22) , Point(103.22 , 21.33)]
} , crs='EPSG:4326')
# -> tham số đầu tiên (data) của class GeoDataFrame có thể là 1 dataFrame , 1 dict chứa các thộc tính key là tên cột và value các giá trị cột đó , 1 danh sách dict 

# 3. Đọc / ghi dữ liệu 
# 3.1. Đọc dữ liệu 

# - Sử dụng hàm : gpd.read_file('tên_file')
# Đọc từ file local
# gdf = gpd.read_file("data.geojson") -> file geoJSON
# gdf = gpd.read_file("shapefile.shp") -> file shp
# gdf = gpd.read_file("data.gpkg")                     # GeoPackage
# gdf = gpd.read_file("data.gpkg", layer="roads")      # chọn layer
# gdf = gpd.read_file("data.geojson.zip")              # file nén

# Đọc từ URL (rất hay dùng cho dữ liệu mở)
# url = "https://raw.githubusercontent.com/.../data.geojson"
# gdf = gpd.read_file(url) -> Đọc file từ đường linhk thường là dữ liệu mở 

# -> Đối với file csv cần đọc bằng thư viện pandas tạo ra bảng dataFrame sau đó khởi tạo bảng GeoDataFrame từ bảng dataFrame đó 

# 3.2. Ghi dữ liệu 

# gdf.to_file("out.geojson", driver="GeoJSON")
# gdf.to_file("out.gpkg", driver="GPKG")
# gdf.to_file("out.shp")    # shapefile — không cần driver

# -> Sử dụng hàm : to_file('tên_file_xuất' , driver='định dạng file') chuyển bảng geoDataFrame thành các file cụ thể với định dạng tùy chọn 

# 3.3. Bảng chọn định dạng 
# - Định dạng GeoJSON : Ưu điểm web-friendly , đọc bằng mắt -> dùng khi chia sẻ file , web , các dạng file nhỏ
# - GeoPackage : Ưu điểm nhanh , nhiều layer , khuyến nghị dùng định dạng này -> dùng khi lưu trữ , các dạng file lớn 
# - Shapefile : Ưu điểm tương thích rộng -> dùng khi nhận yêu cầu 
# - Parquet : Ưu điểm nhanh nhất -> dùng với dữ liệu lớn 
