import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.fixture(scope="module")
def setup_teardown():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield
    driver.quit()

def test_multilanguage_functionality(setup_teardown):
    """
    kiểm tra chức năng đa ngôn ngữ trên trang web Amazon.

    Các bước:
        1. Mở trang web.
        2. Thay đổi ngôn ngữ sang tiếng Anh.
        3. Xác minh rằng nội dung trang web được dịch chính xác sang tiếng Anh.
        4. Thay đổi ngôn ngữ sang tiếng Hàn.
        5. Xác minh rằng nội dung trang web được dịch chính xác sang tiếng Hàn.
    """

    driver.get("https://www.amazon.in/")

    # Lấy element ngôn ngữ
    language_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "icp-nav-flyout"))
    )

    # Nhấp vào menu dropdown để chọn ngôn ngữ
    language_element.click()

    # Chọn tiếng Anh
    language_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchLanguage"))
    ))
    language_select.select_by_value("en_IN")

    # Xác minh nội dung tiếng Anh
    assert "Hello, Sign in" in driver.page_source
    assert "Customer Service" in driver.page_source

    # Chọn tiếng Hàn
    language_select.select_by_value("ko_IN")

    # Xác minh nội dung tiếng Hàn
    assert "안녕하세요, 로그인" in driver.page_source
    assert "고객 센터" in driver.page_source

# Chạy test
if __name__ == "__main__":
    pytest.main([__file__, "-s"])


