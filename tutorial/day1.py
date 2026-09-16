# Phần 1 - Biến và kiểu dữ liệu 

# 1.1. Biến là gì 

ten_nha = 'nha tao'
vi_do = 102.32
kinh_do = 205.33
da_tot_nghiep = False

# -> Biến là hộp có nhãn chứa dữ liệu có thể truy cập dữ liệu đã khởi tạo bằng tên 

# 1.2. Các kiểu dữ liệu
# list  vd:  [1,2,3] -> dùng để lưu danh sách điểm , tọa độ 
# dict  vd: {'name' : 'a'} -> dùng để lưu thuộc tính của 1 địa điểm 
# tuple vd: (21,105) -> dùng để lưu cặp tọa độ (lat , lon)

# 1.3. Cách in dữ liệu ra màn hình 

ten = 'phan manh'
lat , lon = 21.0303 , 105.2222

print(f"Tao tên là {ten} <>")
print(f"Tọa độ tao là : vĩ độ {lat} , kinh độ {lon}")

# -> cách in dữ liệu của biến đặt vào chung chuỗi dùng cú pháp sau : print(f'{ten_bien}...')

# Phần 2 - Toán tử 

# 2.1. Toán tử toán học 

a,b = 40 , 20 
print(a // b) # chia lấy phần nguyên
print(a % b) # chia lấy phần dư

# -> sử dụng để tính toán toán học

# 2.2. Toán từ so sánh 

print( 5 == 5) # true
print (5 != 5) # false

# -> sử dụng để so sánh giá trị hoặc biểu thức 

# 2.3. Toán tử logic 

bieu_thuc_1 = (21 > 5) and (21 > 22) # and : trả về true nếu cả 2 biểu thức true 
bieu_thuc_2 = False or (5 < 2) # or : trả về true nếu 1 biểu thức trả về true 
bieu_thuc_3 = not bieu_thuc_1 # not : trả về giá trị ngược lại true -> false

# Phần 3 : Cấu trúc dữ liệu (QUAN TRỌNG NHẤT)

# 3.1. List (Danh sách) 
# Danh sách : Là danh sách các dữ liệu có cùng kiểu dữ liệu lưu trữ liên tục với nhau trong dấu []
# -> sử dụng để lưu trữ dữ liệu có cùng kiểu dữ liệu có thể dễ dàng truy cập thông qua chỉ số index 

list_food = ['bún bò huế' , 'bánh mì' , 'bún real']
list_number = [2,3,4,4,5,6,7,4]

print(list_food[0])
print(list_number[1])

# - Các phương thức cung cấp sẵn của list 
list_food.append('phở cuốn')
list_food.remove('bánh mì')
list_food.insert( 1 ,'phở' )
print(len(list_food)) # kích thước của list 

# - List lồng nhau 
diem = [
    [21.111 , 105.333],
    [21.112 , 105.343],
    [21.141 , 105.133],
]
# -> sử dụng list lồng nhau khi 1 phần tử cần lưu là nhiều list có cùng cấu trúc 

# 3.2. Dictionary (từ điển) 
# Từ điển : Bao gồm nhiều cặp khóa key-value mang thông tin về chung 1 đối tượng được lưu trữ với nhau bằng dấu {}
# -> sử dụng để lưu trữ 1 đối tượng bao gồm nhiều dữ liệu khác nhau không cùng kiểu và có thể truy cập dữ liệu đó thông qua key

truong_mo_dia_chat = {
    "name" : "ĐH mỏ địa chất",
    "lat" : 21.004,
    "lon" : 105.828,
    "address" : "3 phố viên"
}
print(f' Tên trường : {truong_mo_dia_chat["address"]}')
print(f' Địa chỉ : {truong_mo_dia_chat["name"]}')

# - Thêm / sửa dữ liệu thông qua key 
truong_mo_dia_chat['address'] = 'Số 3 Phố Viên'
truong_mo_dia_chat['phone'] = 12345789

# - Kiểm tra 1 thuộc tính có tồn tại hay không thông qua key 
if "phone" in truong_mo_dia_chat :
    print('Có điện thoại mò')

# - Lấy giá trị một cách an toàn bằng phương thức get
print(truong_mo_dia_chat.get('email','Chưa có email'))

# - Danh sách list chứa nhiều dict 
truong_list = [
    {"name": "ĐH Mỏ", "lat": 21.005, "lon": 105.843, "type": "ĐH"},
    {"name": "ĐH Bách Khoa", "lat": 21.0056, "lon": 105.8435, "type": "ĐH"},
    {"name": "THPT Kim Liên", "lat": 21.0085, "lon": 105.835, "type": "THPT"},
]
# -> Sử dụng khi cần lưu trữ nhiều đối tượng có cùng cấu trúc vào danh sách 

for t in truong_list : 
    print(f"tên trường : {t['name']}")

# 3.3. Tuple 
# Tuple : Giống với list nhưng không thể thay đổi cấu trúc ban đầu lúc khai báo , các dữ liệu lưu trữ trong dấu ()
# -> Sử dụng các trường hợp dữ liệu cố định không thay đổi 

toa_do_mo = (21.005 , 105.333)
print(toa_do_mo[0])

# 3.4. Set 
# Set : Tập hợp các dữ liệu không trùng lặp , các dữ liệu được lưu trữ trong dấu {}
# -> Sử dụng với tập hợp dữ liệu không trùng lặp 

loai_truong = {"ĐH" , "THPT" , "THCS" , "THCS"} 
print(loai_truong) # Khi in ra tự loại bỏ các dữ liệu lặp

# Phần 4 : Câu lệnh điều kiện (if / elif / else)

# 4.1. Cú pháp cơ bản 
# - Quy tắc : Python dùng thụt lề để tạo ra khối code riêng phục vụ cho câu lệnh trước đó -> thay cho dấu {} 

troi_mua = True
if troi_mua == True :
    print('Trời đang mưa')
else :
    print('Trời đang tạnh')

# -> Sử dụng if nếu cấu trúc điều kiện phức tạp và lồng nhau 

# 4.2. Toán tử 3 ngôi 

tuoi = 21 
trang_thai = "Người lớn" if tuoi > 18 else "Trẻ em"
print(trang_thai)

# -> Sử dụng toán tử 3 ngôi với các cấu trúc điều kiện đơn giản dùng trên 1 dòng duy nhất

# Phần 5 : Vòng lặp 

# 5.1. For - Duyệt qua list và dict

# - Duyệt tất cả các phần tử có trong 1 list
for num in list_number :
    print(f"{num}")

# - Duyệt tất cả các key trong 1 dict 
for key in truong_mo_dia_chat : 
    print(key)

# - Duyệt cả key và value trong 1 dict 
for key , value in truong_mo_dia_chat.items() : 
    print(f'{key} = {value}')

# 5.2. White - Vòng lặp chạy khi điều kiện vẫn đúng 
dem = 0 
while dem == 4 :
    print(dem)
    dem = dem + 1

# 5.3. Break / continue - Kết thúc vòng lặp / bỏ qua lần lặp hiện tại 

for i in range(10) : 
    if i == 5 :
        break
    print(i)

for i in range(10) : 
    if i % 2 != 0 :
        continue
    print(i)
