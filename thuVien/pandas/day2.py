# Review day1 : 

# Pandas là : Là thư viện cung cấp kiểu dữ liệu dạng bảng 2 chiều và dạng mảng 1 chiều phù hợp cho các thao tác , xử lý và phân tích dữ liệu 
    # + DataFrame (bảng 2 chiều) : Gồm các dữ liệu chia thành các hàng và cột với cấu trúc giống với cơ sở dữ liệu sql 
    # + Series (mảng 1 chiều) : Là danh sách dữ liệu có cùng kiểu -> 1 cột dữ liệu trong bẳng 

# Với cấu trúc dạng bảng có thể sử dụng nhiều thuộc tính và phương thức có sẵn để có thể thực hiện các thao tác : Ghi dữ liệu từ file , chuyển từ Df xuất thành file ,
# xem kích thước và thông tin bảng dữ liệu , lấy dữ liệu từ 1 hay nhiều cột , lọc dữ liệu dựa trên điều kiện ...

# Câu hỏi : 

# 1. Đọc dữ liệu , in shape + info + describe 

import pandas as pd 

dia_danh_df = pd.read_csv("dia_diem.csv")

print(dia_danh_df.shape) # thuộc tính shape : trả về thông tin chứa kích thước của bảng gồm số lượng hàng , số lượng cột
print(dia_danh_df.info()) # hàm info() : trả về thông tin tổng quan về bảng dữ liệu gồm số lượng bảng , số lượng cột , kiểu dữ liệu của từng cột ...
print(dia_danh_df.describe()) # hàm describe() : trả về thông tin các cột dạng số và tính toán các biểu thức từng cột : số lượng , min , max , trung bình...

# 2. Đọc dữ liệu chỉ lấy các cột name , lat , lon , type 

# -> Bảng df sử dụng dấu ngoặc vuông để truy cập vào bảng dữ liệu , từ đó dựa vào biểu thức để lọc ra dữ liệu cần thiết -> có thể cột dữ liệu , hàng với các cột chỉ định , 
# hàng với điều kiện cột ...

cot_name = dia_danh_df['name']      # truyền vào 1 chuỗi -> trả về danh sách mảng 1 chiều (series) có tên cột tương ứng với chuỗi đó
dia_danh_toa_do_df = dia_danh_df[['name' , 'lat' , 'lon' , 'type']]     # truyền vào danh sách chuỗi -> trả về bảng nhưng với các cột tương ứng với danh sách chuỗi
print(cot_name)
print(dia_danh_toa_do_df)

# 3. Lọc các địa điểm ở quận Đống Đa và là trường đại học 

# -> Truyền biểu thức điều kiện vào dấu ngoặc vuông : các biểu thức điều kiện bọc dấu ngoặc tròn thì có thể kết hợp nhiều điều kiện khác bằng các ký tự : ~ (not) , & (and) , | (or)
# -> Các biểu thức điều kiện thường là điều kiện 1 cột các cột lọc dữ liệu dựa trên điều kiện đó trả về các hàng true/false và lấy các hàng mang giá trị true 
trg_dh_dong_da_df = dia_danh_df[(dia_danh_df['type'] == 'ĐH') & (dia_danh_df['address'].str.contains('Đống Đa'))]
print(trg_dh_dong_da_df)

# 4. Lọc các địa điểm có loại là bệnh viện và THPT trong cột type 

# -> Để lấy các lựa chọn cụ thể trong cùng 1 cột thì sử dụng hàm isin() cần truyền vào danh sách chứa các lựa chọn cần lọc đó 
bv_thpt_df = dia_danh_df[dia_danh_df['type'].isin(['THPT' , 'Bệnh viện'])]
print(bv_thpt_df)

# -> Để lọc bảng dựa trên điều kiện của cột thì cần truy cập vào bảng với cú pháp df[] , sau đó cần truyền vào dấu [] các biểu thức điều kiện của cột có thể là :
# + lọc điều kiện đơn giản 1 cột
# + lọc với kết hợp điều kiện của các cột ~ , & , | 
# + lọc danh sách thỏa mãn điều kiện của 1 cột -> hàm isin
# + lọc từ khóa trong chuỗi -> sử dụng thuộc tính str để dùng các hàm của chuỗi


# Học tiếp pandas ngày 2 : 

# 5. Sắp xếp 
# -> sử dụng hàm sort_values() để sắp xếp bảng theo 1 cột nhất định 
# -> sort_values() gồm 2 tham số quan trọng cần truyền  : cột -> có thể tên cột hoặc danh sách cột , ascending -> giá trị true/false có thể danh sách true/false , với
# ascending= true tăng dần và false giảm dần 

# -> sắp xếp dựa 1 cột
df_year_sorted =  dia_danh_df.sort_values('year' , ascending=True)
print(df_year_sorted)

# -> sắp xếp dựa nhiều cột 
df_name_year_sorted = dia_danh_df.sort_values(['name' , 'year'] , ascending=[True , False])
print(df_name_year_sorted)

# 6. Nhóm -> Cực kỳ quan trọng 

# - Cú pháp :  
test = dia_danh_df.groupby('type').agg({
    'name' : 'count',
    'year' : 'sum'
})
print(test)

# -> Hàm groupby() : sử dụng để nhóm các nhóm có chung giá trị trong cùng 1 cột và cột đó dựa trên tham số truyền vào -> nhóm có chung giá trị là 1 nhóm 
# -> Hàm agg() có thể truyền vào func , dict , ... nhưng hầu hết sử dụng dict : với các thuộc tính truyền vào sẽ dựa vào đó để tính toán dựa trên các nhóm ,
    # thuộc tính gồm key : tên cột và value : hàm aggregate thực thi trên cột đó 

# - Hàm aggregate phổ biến : 
    # + count : đếm số dòng không tính NaN 
    # + size : đếm số dòng tính NaN
    # + sum : tổng
    # + mean : trung bình

thong_ke = dia_danh_df.groupby("type").agg(
    so_luong=("name", "count"),
    lat_tb=("lat", "mean"),
    lon_tb=("lon", "mean")
).round(4)

print(thong_ke)

# 7. Nối bảng 
# - Sử dụng hàm merge để gộp 2 bảng DataFrame có chung 1 cột dữ liệu lại với nhau thành 1 bảng DataFrame 
# -> Điều kiện cột dữ liệu chung thường là cột id có thể 2 bảng DataFrame chung cột id nhưng có thể không chung giá trị 

df_food_1 = pd.DataFrame({
    'food_id' : [1 , 2 , 3 ,5],
    'food_name' : ['Bún bò huế ' , 'Bánh canh' , 'Trà đá' , 'Phở']
}) # -> Có thể khởi tạo DataFrame bằng gọi object DataFrame và truyền vào các cột = key và hàng = value 

df_food_2 = pd.DataFrame({
    'food_id' : [1 , 2 , 4 , 6],
    'food_position' : ['Hà Nội' , 'Hải Phòng' , 'Thanh Hóa' , 'Nam Định']
})

df_food_all = pd.merge(df_food_1 , df_food_2 , how='outer' , on='food_id') 
print(df_food_all)

# - Các tham số cần thiết truyền vào hàm merge : 
    # + 2 tham số bảng DataFrame để merge với nhau 
    # + Tham số on='tên_cột_chung' Dựa vào cột dữ liệu chung để gộp 2 bảng với nhau 
    # + Tham số how='cách_gộp': Dựa vào cách gộp này mà tạo ra bảng dữ liệu hoàn toàn khác nhau 
        # -> inner : Chỉ lấy giá trị mà 2 bảng đều có ở cột chung 
        # -> left : Giữ nguyên giá trị cột chung bảng trái còn bảng phải chỉ lấy giá trị chung -> áp dụng khi bảng trái bảng chính chỉ gộp thêm dữ liệu từ bảng phải 
        # -> right : Giữ nguyên giá trị cột chung bảng phải còn bảng trả chỉ lấy giá trị chung -> áp dụng khi bảng phải bảng chíng chỉ gộp thêm dữ liệu từ bảng trái
        # -> outer : Giữ tất cả giá trị cột chung của cả 2 bảng -> tạo ra các giá trị NaN do thiếu dữ liệu 

# 8.Xử lý NaN 

# 8.1. Phát hiện NaN : Sử dụng hàm isna() kiểm tra giá trị NaN

df_food_all.isna().sum() # -> sử dụng hàm sum đếm NaN từng cột
df_food_all.isna().sum().sum() # -> tổng NaN 
df_food_all.any() # -> cột nào có NaN 

# 8.2. Xóa dòng/cột có NaN : Sử dụng hàm dropna() -> Dựa vào tham số truyền vào mà cách sử lý NaN khác nhau 
df_food_all.dropna() # -> không truyền vào gì xóa dòng nếu tồn tại NaN trong dòng
dia_danh_df.dropna(subset=['lat' , 'lon']) # -> chỉ xóa dòng nếu lat hoặc lon = NaN 
df_food_all.dropna(how='all') # -> chỉ xóa dòng nếu tất cả giá trị = NaN 
df_food_all.dropna(axis=1) # -> xóa cột nếu có NaN
df_food_all.dropna(thresh=3) # -> xóa dòng nếu có >= 3 giá trị không NaN 

# 8.3. Điền giá trị thay thế NaN : Sử dụng hàm fillna() -> Dựa vào tham số truyền vào để cách điền thay giá trị NaN 

df_food_all['food_name'] = df_food_all['food_name'].fillna('Không tồn tại') # -> truy cập cột food_name với các giá trị NaN thay bằng không tồn tại 
print(df_food_all)

# 8.4. Thay thế giá trị cụ thể : Sử dụng hàm replace() 

df_food_all['food_position'] = df_food_all['food_position'].replace(['Hà Nội' , 'Hải Phòng' , 'Thanh Hóa'] , ['HN' , 'HP' , '36'])
print(df_food_all)

# -------------------->  loc và iloc : Bản chất là 2 thuộc tính định vị nên cần truyền vào dữ liệu định vị trong dấu []

# 1. loc : Định vị dựa trên nhãn của dòng hoặc cột -> tên dòng / cột

# 1.1. Lấy dữ liệu cụ thể từ 1 hàng 1 cột 
food1 = df_food_all.loc[1 , 'food_name'] # -> nếu dòng không có tên nhãn dùng giá trị index 
print(food1)

# 1.2. Cắt lát dữ liệu : Quy tắc cắt lát [start : stop] -> hàm loc() bao gồm lấy cả điểm stop 
food2 = df_food_all.loc[1:2 , 'food_id' : 'food_name']
print(food2)

#1.3. Lọc dựa trên điều kiện boolean : truyền vào mảng chứa các dữ liệu true/false -> Chiếu lên bảng df mảng true/false 
# -> lấy hàng mang dữ liệu true với cột tương ứng được chọn 
food3 = df_food_all.loc[df_food_all['food_name'].str.contains('h') , 'food_position']
print(food3)

# -> Sử dụng hàm loc() để loc dữ liệu này có thể chỉ  định những cột muốn lấy dữ liệu dựa trên điều kiện 