import json
import os

class ProxyManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self._load_proxies()

    def _load_proxies(self):
        """Tải danh sách proxy từ file JSON."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # Đảm bảo dữ liệu là một list và chuyển đổi thành set để dễ quản lý duy nhất
                    self.proxies = set(data) if isinstance(data, list) else set()
                except json.JSONDecodeError:
                    self.proxies = set() # Nếu file bị lỗi, khởi tạo rỗng
        else:
            self.proxies = set() # Nếu file chưa tồn tại, khởi tạo rỗng
        self._save_proxies() # Đảm bảo file được tạo nếu chưa có

    def _save_proxies(self):
        """Lưu danh sách proxy hiện tại vào file JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.proxies), f, indent=2)

    def _validate_proxy_format(self, proxy):
        """Kiểm tra định dạng cơ bản của proxy (ip:port)."""
        return isinstance(proxy, str) and ':' in proxy

    def get_all_proxies(self):
        """Trả về toàn bộ danh sách proxy hiện có."""
        return list(self.proxies)

    def add_proxies(self, new_proxies):
        """Thêm một hoặc nhiều proxy mới vào danh sách.
        Trả về số lượng proxy đã được thêm.
        """
        added_count = 0
        for proxy in new_proxies:
            if self._validate_proxy_format(proxy) and proxy not in self.proxies:
                self.proxies.add(proxy)
                added_count += 1
            else:
                print(f"Skipping invalid or duplicate proxy: {proxy}")
        if added_count > 0:
            self._save_proxies()
        return added_count

    def remove_proxies(self, proxies_to_remove):
        """Xóa một hoặc nhiều proxy khỏi danh sách.
        Trả về số lượng proxy đã được xóa.
        """
        removed_count = 0
        for proxy in proxies_to_remove:
            if self._validate_proxy_format(proxy) and proxy in self.proxies:
                self.proxies.remove(proxy)
                removed_count += 1
            else:
                print(f"Skipping proxy not found or invalid: {proxy}")
        if removed_count > 0:
            self._save_proxies()
        return removed_count

    def set_all_proxies(self, new_list_proxies):
        """Đặt lại toàn bộ danh sách proxy bằng danh sách mới.
        Trả về số lượng proxy đã được cập nhật.
        """
        new_set = set()
        for proxy in new_list_proxies:
            if self._validate_proxy_format(proxy):
                new_set.add(proxy)
            else:
                print(f"Skipping invalid proxy format for set: {proxy}")
        
        self.proxies = new_set
        self._save_proxies()
        return len(new_set)

