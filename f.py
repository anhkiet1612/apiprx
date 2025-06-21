import os

def classify_and_update_proxies(input_file_path, unique_output_file_path, duplicate_output_file_path):
    """
    Đọc proxy từ file đầu vào, so sánh với các proxy đã có trong file duy nhất,
    sau đó cập nhật file duy nhất và file trùng lặp.

    Args:
        input_file_path (str): Đường dẫn đến file .txt chứa proxy mới cần xử lý.
        unique_output_file_path (str): Đường dẫn đến file .txt để lưu/cập nhật các proxy duy nhất.
        duplicate_output_file_path (str): Đường dẫn đến file .txt để lưu các proxy trùng lặp.
    """
    
    # ---- THAY ĐỔI QUAN TRỌNG ----
    # Bước 1: Đọc tất cả các proxy ĐÃ CÓ trong file unique để biết cái nào đã tồn tại.
    # Sử dụng set để kiểm tra sự tồn tại cực kỳ nhanh.
    seen_proxies = set()
    if os.path.exists(unique_output_file_path):
        print(f"Đang đọc dữ liệu cũ từ file: {unique_output_file_path}")
        with open(unique_output_file_path, 'r', encoding='utf-8') as f_unique_read:
            for line in f_unique_read:
                seen_proxies.add(line.strip())
        print(f"Đã đọc xong. Hiện có {len(seen_proxies)} proxy duy nhất.")
    # -----------------------------

    # Các danh sách để lưu kết quả từ lần chạy này
    new_unique_proxies_to_add = []
    duplicates_to_write = []
    
    # Bước 2: Đọc và xử lý file đầu vào MỚI
    if not os.path.exists(input_file_path):
        print(f"Lỗi: File đầu vào '{input_file_path}' không tồn tại.")
        return

    print(f"\nBắt đầu xử lý file đầu vào mới: {input_file_path}")
    initial_count = 0
    skipped_invalid_count = 0
    processed_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            initial_count += 1
            proxy = line.strip()

            if not proxy or ':' not in proxy:
                skipped_invalid_count += 1
                continue
            
            processed_count += 1
            # Kiểm tra xem proxy đã từng xuất hiện trong file unique cũ hoặc trong lần quét này chưa
            if proxy not in seen_proxies:
                # Nếu chưa từng thấy, đây là một proxy mới và duy nhất
                new_unique_proxies_to_add.append(proxy)
                seen_proxies.add(proxy) # Cập nhật ngay vào set để xử lý các proxy trùng lặp trong chính file input
            else:
                # Nếu đã thấy rồi, nó là proxy trùng lặp
                duplicates_to_write.append(proxy)
    
    # Bước 3: Thống kê và ghi file
    print("\n--- Thống kê lần chạy này ---")
    print(f"Tổng số dòng đọc từ file '{input_file_path}': {initial_count}")
    print(f"Số dòng không hợp lệ/trống bị bỏ qua: {skipped_invalid_count}")
    print(f"Số proxy hợp lệ được xử lý: {processed_count}")
    print(f"Số proxy DUY NHẤT MỚI được tìm thấy: {len(new_unique_proxies_to_add)}")
    print(f"Số proxy TRÙNG LẶP được tìm thấy: {len(duplicates_to_write)}")

    # Ghi các proxy duy nhất MỚI vào file (chế độ 'a' - append)
    # Thao tác này sẽ thêm vào cuối file mà không xóa dữ liệu cũ
    if new_unique_proxies_to_add:
        print(f"\nĐang ghi {len(new_unique_proxies_to_add)} proxy duy nhất MỚI vào file: {unique_output_file_path}")
        with open(unique_output_file_path, 'a', encoding='utf-8') as f_unique_append:
            for proxy in sorted(new_unique_proxies_to_add):
                f_unique_append.write(proxy + '\n')
    else:
        print(f"\nKhông có proxy duy nhất nào mới để thêm vào {unique_output_file_path}.")

    # Ghi file proxy trùng lặp (có thể ghi đè hoặc ghi tiếp tùy bạn, ở đây dùng ghi tiếp 'a')
    if duplicates_to_write:
        print(f"Đang ghi {len(duplicates_to_write)} proxy trùng lặp vào file: {duplicate_output_file_path}")
        with open(duplicate_output_file_path, 'a', encoding='utf-8') as f_duplicate:
            for proxy in sorted(duplicates_to_write):
                f_duplicate.write(proxy + '\n')
    else:
        print(f"Không tìm thấy proxy trùng lặp nào trong lần chạy này.")

    print("\nHoàn thành!")


# --- Phần thực thi chính ---
if __name__ == "__main__":
    # Đặt tên file cho các proxy DUY NHẤT (File này sẽ được cập nhật liên tục)
    output_unique_file = 'duynhat.txt'
    
    # Đặt tên file cho các proxy TRÙNG LẶP
    output_duplicate_file = 'trung.txt'

    # Yêu cầu người dùng nhập tên file proxy gốc
    input_proxy_file = input("Nhập tên file proxy cần xử lý (ví dụ: data.txt): ")

    classify_and_update_proxies(input_proxy_file, output_unique_file, output_duplicate_file)

    # Sau khi chạy script này:
    # 1. duynhat.txt: Sẽ chứa các proxy duy nhất từ tất cả các lần chạy trước cộng với các proxy duy nhất mới từ lần chạy này.
    # 2. trung.txt: Sẽ chứa các proxy bị trùng lặp.