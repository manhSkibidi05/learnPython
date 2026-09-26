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

# ________________________________________DAY 1 ______________________________________________

# 1. GeoDataFrame và DataFrame 


import geopandas as gpd 
import pandas as pd 

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