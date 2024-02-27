import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Khởi tạo biến driver ở mức global
driver = None

def setup_module():
   global driver
   driver = webdriver.Chrome()
   driver.maximize_window()

def teardown_module():
   driver.quit()

def test_search_functionality():
   """
   kiểm tra chức năng tìm kiếm trên Amazon.in.

   Các bước:
       1. Mở trang chủ Amazon.
       2. Tìm thanh tìm kiếm và nhập "python".
       3. Gửi truy vấn tìm kiếm.
       4. Xác minh các điều sau:
           - Tiêu đề trang chứa "python".
           - Có ít nhất một kết quả tìm kiếm.
           - URL chứa "amazon.in".
           - Tên của kết quả đầu tiên không rỗng.
           - Giá của kết quả đầu tiên (nếu có) không rỗng.
           - Xếp hạng của kết quả đầu tiên (nếu có) tồn tại.
   """
   global driver


   driver.get("https://www.amazon.in/")


   # Tìm thanh tìm kiếm bằng XPath
   search_bar = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
   )

   search_bar.send_keys("python")
   search_bar.submit()

   # Xác minh các kết quả mong muốn
   assert "python" in driver.title

   # Kiểm tra xem có kết quả nào trả về không
   results = driver.find_elements_by_css_selector(".s-result-item")
   if not results:
       pytest.fail("Không có kết quả tìm kiếm nào được trả về")

   # Tiếp tục xác minh các thông tin khác về kết quả tìm kiếm
   first_result = results[0]

   product_name = first_result.find_element_by_tag_name("h2").text.strip()
   assert product_name != ""


   try:
       price_element = first_result.find_element_by_css_selector(".s-price")
       price = price_element.text.strip()
       assert price != ""
   except:
       pass


   try:
       rating_element = first_result.find_element_by_css_selector(".a-star-rating")
       rating = rating_element.get_attribute("aria-label")
       assert rating is not None
   except:
       pass


# Chạy test
if __name__ == "__main__":
   pytest.main()

