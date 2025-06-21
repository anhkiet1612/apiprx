from flask import Flask, Response
import os

app = Flask(__name__)

# Thay đổi đường dẫn đến file chứa proxy thành .txt
PROXY_FILE = 'duynhat.txt'

def load_proxies():
    """
    Tải danh sách proxy từ file văn bản (.txt), mỗi proxy một dòng.
    Nếu file không tồn tại hoặc lỗi, trả về danh sách rỗng.
    KHÔNG loại bỏ các proxy trùng lặp từ file.
    """
    proxies = [] # Khởi tạo là một danh sách để giữ tất cả các dòng, bao gồm cả trùng lặp
    raw_line_count = 0
    valid_line_count = 0

    print(f"DEBUG: Attempting to load proxies from {PROXY_FILE}")

    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                raw_line_count += 1
                stripped_line = line.strip()
                
                if stripped_line and ':' in stripped_line:
                    proxies.append(stripped_line) # Thêm vào danh sách
                    valid_line_count += 1
                else:
                    print(f"DEBUG: Skipping invalid or empty line: '{line.strip()}' (raw: {repr(line)})")
    else:
        print(f"ERROR: {PROXY_FILE} not found. Returning empty list.")
    
    print(f"DEBUG: Total raw lines read from file: {raw_line_count}")
    print(f"DEBUG: Lines passed basic validation (stripped_line and ':' in it): {valid_line_count}")
    print(f"DEBUG: Number of proxies loaded (including duplicates): {len(proxies)}") # Cập nhật thông báo cho chính xác

    # Quan trọng: Cần trả về danh sách 'proxies'
    return proxies 

# Định nghĩa đường dẫn API chính của bạn
# Khi truy cập http://127.0.0.1:3434/prokie/oam/nona/api/proxy,
# hàm này sẽ được gọi và trả về danh sách proxy.
@app.route('/prokie/oam/nona/api/proxy')
def get_custom_proxies_endpoint():
    """
    Endpoint trả về danh sách proxy từ file proxies.txt
    dưới dạng văn bản (mỗi proxy một dòng), bao gồm cả trùng lặp.
    """
    proxies = load_proxies()
    proxy_string = "\n".join(proxies)
    
    # Trả về Response với mimetype là text/plain, giống như hình ảnh bạn gửi
    return Response(proxy_string, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=3434) # Vẫn dùng cổng 3434