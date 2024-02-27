import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo biến driver ở mức global
driver = None

@pytest.fixture(scope="module")
def setup_teardown():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield
    driver.quit()

def test_add_laptop_to_cart(setup_teardown):
    """
    Kiểm tra quá trình thêm laptop vào giỏ hàng trên trang web Amazon.
    """
    # Mở trang web
    driver.get("https://www.amazon.in/")

    # Tìm thanh tìm kiếm và nhập "laptop"
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_bar.clear()
    search_bar.send_keys("laptop")
    search_bar.submit()

    # Chờ cho kết quả tìm kiếm xuất hiện và chọn mục đầu tiên
    first_search_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item"))
    )
    first_search_result.click()

    # Chờ cho trang chi tiết sản phẩm được tải hoàn chỉnh và tìm nút "Thêm vào giỏ hàng"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
    )

    # Lưu lại tiêu đề sản phẩm để kiểm tra sau này
    product_title = driver.find_element(By.ID, "productTitle").text

    # Nhấp vào nút "Thêm vào giỏ hàng"
    add_to_cart_button.click()

    # Chờ cho thông báo "Đã thêm vào giỏ hàng" xuất hiện
    added_to_cart_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='huc-v2-order-row-confirm-text']"))
    )

    # Kiểm tra xem thông báo đã hiển thị đúng cho việc thêm vào giỏ hàng chưa
    assert "Đã thêm vào giỏ hàng" in added_to_cart_message.text

    # Kiểm tra tiêu đề sản phẩm đã được thêm vào giỏ hàng có đúng không
    assert product_title in driver.page_source

    # Đợi 3 giây để cho thông báo biến mất
    time.sleep(3)

# Chạy test
if __name__ == "__main__":
    pytest.main()


