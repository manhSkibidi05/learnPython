# DAY 1 : THƯ VIỆN PANDAS

import pandas as pd 
import numpy as np 

# ĐỊNH NGHĨA : 
# - Pandas là  thư viện mã nguồn mở hàng đầu của Python được thiết kế chuyên biệt cho việc thao tác , xử lý và phân tích dữ liệu 
# - Thư viện này cung cấp các cấu trúc dữ liệu hiệu năng cao , linh hoạt và dễ sử dụng , giúp biến  các tập dữ liệu thô , phức tạp thành dạng các bảng có cấu trúc
# tương tự như sheet Microsoft hay Excel , các bảng trong cơ sở dữ liệu 

# -> 2 cấu trúc dữ liệu cốt lõi trong pandas : 
# - Series : Mảng một chiều chứa dữ liệu cùng kiểu (tương ứng 1 cột dữ liệu trong bảng)
# - DataFrame : Bảng dữ liệu hai chiều chứa nhiều cột dữ liệu và hàng -> 1 hàng tương ứng 1 bản ghi dữ liệu của 1 đối tượng 

# CÔNG DỤNG : 
# - Pandas được xem là 'xương sống' trong các quy trình làm việc với dữ liệu (Data science , machine learning , analytics , GIS) nhờ các công dụng chíng sau : 

# A. Đọc và ghi dữ liệu đa dạng 
# - Hỗ trợ đọc / ghi dữ liệu từ nhiều định dạng file khác nhau một cách nhanh chóng : CSV , Excel , JSON , HTML...

# B. Làm sạch và Tiền xử lý dữ liệu 
# - Xử lý dữ liệu khuyết : Phát hiện , loại bỏ hoặc điền giá trị thay thế cho các ô dữ liệu 
# - Xử lý dữ liệu trùng lặp : Tìm và xóa các dòng dữ liệu bị lặp lại 
# - Chuẩn hóa kiểu dữ liệu : Chuyển đổi linh hoạt giữa các kiểu dữ liệu -> có thể chuyển chuỗi sang số , ép kiểu ngày tháng

# C. Thao tác và biến đổi dữ liệu 
# - Lọc và truy vấn : Trích xuất các dòng / cột dữ liệu thỏa mãn điều kiện cụ thể 
# - Tạo cột mới : Tự động hóa việc tính toán và thêm cột dựa trên cột sẵn có 
# - Sắp xếp : Sắp xếp dữ liệu theo thứ tự tăng / giảm của một hay nhiều cột 

# D. Tổng hợp và thống kê dữ liệu 
# - Nhóm dữ liệu : Nhóm các tập dữ liệu theo tiêu chí và tính toán các chỉ số thống kê (tổng , trung bình...)
# - Hợp nhất : Kết nối nhiều bảng dữ liệu dựa trên cột chung -> giống JOIN trong SQL

# E. Tiên đề cho phân tích không gian 
# - Trong lĩnh vực GIS , pandas nền tảng trực tiếp tạo nên geoPandas . Mọi thao tác xử lý bảng thuộc tính của dữ liệu địa lý như tên , địa chỉ ... đều dựa trên chính
# xác câu lệnh của pandas

# -> pandas bản chất là thư viện của python giúp lưu trữ tạm thời dữ liệu tương tự cách lưu trữ dữ liệu dạng bảng sql , nhờ vậy có thể dễ dàng lọc , truy xuất , thông 
# kê dữ liệu một cách nhanh chóng . 
# -> Khác với database nơi lưu trữ dữ liệu lâu dài thì pandas chỉ lấy 1 phần dữ liệu từ database để xử lý dữ liệu đó bằng python sau đó trả kết quả cho API hoặc ghi lại vào database


# 1 . Đọc / ghi dữ liệu 
# 1.1. Đọc file dữ liệu 

# - Đọc file dữ liệu sử dụng phương thức : read_csv("tên_file") -> sử dụng đọc file .csv 
# -> Khi đọc file dữ liệu trả về dữ liệu kiểu DataFrame là dữ liệu dạng bảng chứa các hàng và cột 

#df = pd.read_csv('fake_data.csv')

# - Có thể đọc file dữ liệu từ đường dẫn 
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
#df = pd.read_csv(url)

# 1.2. Các tham số quan trọng của phương thức : read_csv()
df = pd.read_csv(
    "dia_diem.csv", # tên file
    sep=',',    # dấu phân cách (mặc định dấu , )
    encoding='utf-8' ,   # encoding (VN hay gặp utf-8-sig)
    header=0 , # dòng nào là header (0 = dòng đầu)
    # tự đặt tên cho cột nếu file không có header 
    usecols=['name' , 'lat' , 'lon'], # chỉ đọc vài cột
    nrows=1000 # chỉ đọc 1000 dòng đầu
)

# vd : 
dia_diem = pd.read_csv('dia_diem.csv')
print(dia_diem)

# -> Lưu ý khi đọc dữ liệu : 
# - Với dòng đầu tiên của file dữ liệu DataFrame nhận định nó là dòng chứa header (tên cột)
# - Các dòng tiếp theo bản ghi của 1 đối tượng được sẵp xếp bắt đầu từ 0 
# - Mỗi ô dữ liệu được ngăn cách mặc định dấu phảy 

# 1.3. Ghi file csv 
# - Khi dữ liệu đang ở dạng DataFrame có thể tạo thành file .csv mới sau khi mà dữ liệu đã được xử lý / thống kê xong 
dia_diem.to_csv("output.csv" , index=False , encoding='utf-8-sig') # thuộc tính đầu là tên file tạo ra , thuộc tính index sẽ loại bỏ cột index đếm số dữ liệu (0,1,2...)


# 2. Xem dữ liệu - head , info , describe , shape 
# -> Khi nhận file lạ luôn chạy 5 lệnh này đầu tiên 

# 2.1. shape 
# - Là thuộc tính của dữ liệu kiểu DataFrame giúp trả về kích thước của bảng gồm (a , b ) -> a là bản ghi (hàng) , b là cột 
print(dia_diem.shape)

# 2.2. head() / tail() / sample()
# - Các hàm này giúp trả về số bản ghi dữ liệu nhất định có thể từ đầu file / cuối file / ngẫu nhiên giữa các file 

print(dia_diem.head(6)) # head() : trả về số bản ghi đầu file có thể truyền số cụ thể nếu không mặc định là 5 bản ghi đầu 

print(dia_diem.tail(2)) # tail() : giống với head() nhưng trả về số bản ghi từ cuối lên 

print(dia_diem.sample(3)) # sample() : giống với head() nhưng trả về số bản ghi ngẫu nhiên 

# 2.3. infor()
# - Hàm này trả về thông tin tổng quan của file csv khi lưu vào DataFrame 
print(dia_diem.info())

# 2.4. describe() 
# - Hàm này tạo ra bảng thống kê dữ liệu về tất cả các cột dữ liệu dạng số , các thông tin gồm số lượng , min , max , trung bình...
print(dia_diem.describe())

# 3. Chọn cột / hàng
# - lấy ra số lượng cột hay loại cột dựa trên tên mà do yêu cầu đề bài đề cập đến  

# 3.1. Chọn 1 cột 

name = dia_diem['name'] # sử dụng tên DataFrame['tên_cột'] 1 dấu ngoặc vuông -> lấy tất cả dữ liệu của cột này 
print(name)
print(name.iloc[2]) # sử dụng icloc để truy cập vào giá trị của cột dựa vào chỉ số index của cột đó 

# 3.2. Chọn nhiều cột 

core_info = dia_diem[['name' , 'lat' , 'lon']] # sử dụng tên DataFrame[['tên_cột1' , 'tên_cột2']] 2 dấu ngoặc vuông -> lấy tất cả dữ liệu của các cột đã chọn 
print(core_info)

# - Lưu ý : 
    # + df['name'] : trả về 1 cột dữ liệu mang kiểu là entries nên có thể sử dụng các thuộc tính và phương thức của entries
    # + df[['name']] : trả về 1 cột dữ liệu nhưng là lấy của DataFrame và không mang kiểu entries nên không sử dụng các thuộc tính / phương thức của nó 
    # + df['name' , 'lat'] : Khi lấy nhiều cột sử dụng cách này sẽ gây lỗi do entries chỉ là dữ liệu 1 cột duy nhất 

# 3.3. Chọn hàng theo index 
# - Sử dụng iloc để lấy 1 dữ liệu cụ thể dựa trên chỉ số index để lấy dữ liệu như 1 hàng / 1 ô dữ liệu 

print(dia_diem.iloc[0]) # lấy tất cả dữ liệu hàng 0
print(dia_diem.iloc[0 , 1]) # lấy dữ liệu của hàng 0 cột 1 

# 4. Lọc hàng - Kỹ năng quan trọng nhất 
# -> Đây là phần bạn dùng nhiều nhất trong pandas và geoPandas 

# 4.1. Lọc hàng một điều kiện đơn giản 
# - Cú pháp : tên_dataFrame[điều kiện của 1 cột (entries)] -> điều kiện cột trả về true / false nêu true giữ lại các bản ghi đó 

dia_diem_dh = dia_diem[dia_diem['type'] == 'ĐH']
dia_diem_lat = dia_diem[dia_diem['lat'] >= 21]
print(dia_diem_dh)

# -> Sử dụng với trường hợp các dữ liệu cần lấy dựa trên điều kiện của 1 thuộc tính nào đó 

# 4.2. Lọc hàng với nhiều điều kiện 
# - Cú pháp : tên_dataFrame[(điều kiện cột 1) & (điều kiện cột 2)]

dia_diem_dhLat = dia_diem[(dia_diem['lat'] >= 21.0058) & (dia_diem['type'] == 'ĐH')]
print(dia_diem_dhLat)

# - Lưu ý : 
    # + Dùng các ký tự : & , | , ~  . Thay cho các toán tử so sánh : and , or , not 
    # + Bọc các cụm điều kiện của 1 cột trong khối ngoặc đơn () 

# -> Sử dụng đối với trường hợp các dữ liệu cần lấy cần kết hợp nhiều điều kiện của các thuộc tính khác nhau 

# 4.3. Lọc hàng với danh sách thuộc tính thỏa mãn trong cùng 1 cột 
# - Cú pháp : tên_dataFrame[tên_cột.isin([TH1 , TH2...])]

dia_diem_truong = dia_diem[dia_diem['type'].isin(['ĐH', 'THPT'])]
print(dia_diem_truong)

# -> lấy 1 cột dữ liệu gọi hàm isin() : Hàm này cần truyền vào danh sách các dữ liệu thỏa mãn . Các bản ghi có thuộc tính nằm trong cột có sở hữu 1 trong danh sách dữ liệu này 
# thì được giữ lại bản ghi 

# -> Sử dụng đối với trường hợp trong 1 cột dữ liệu có nhiều hơn 1 thuộc tính cần lấy 

# 4.5. Lọc theo chuỗi con 

dia_diem_bv = dia_diem[dia_diem['name'].str.contains('Bệnh viện' , case=False , na=False)] 

# -> Sử dụng hàm contrains() của thuộc tính str , hàm contrains() trả về true/false bằng cách so sánh chuỗi con có tồn tại bên trong chuỗi thuộc tính 
# -> thuộc tính case=False : không phân biệt hoa thường , na=False : bỏ qua NaN 

# 4.6. Các hàm sử dụng để lọc khác : between , isna , notna 

# Trong khoảng
df_vn = dia_diem[dia_diem["lat"].between(8.0, 23.5)]   # vĩ độ VN

# Loại NaN / giữ NaN
df_clean = dia_diem[dia_diem["address"].notna()]
df_null = dia_diem[dia_diem["address"].isna()]

# 4.7. Query - Cách viết gọn 

# Thay vì:
df_x = dia_diem[(dia_diem["lat"] > 21.0) & (dia_diem["type"] == "ĐH")]

# Viết gọn hơn:
df_x = dia_diem.query("lat > 21.0 and type == 'ĐH'") 