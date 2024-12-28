


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Locators import TestLocators
from Data import WebData
from excel_functions import Excel_Functions


excel_file = WebData().EXCEL_FILE


sheet_number = WebData().SHEET_NUMBER


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)



driver.maximize_window()


driver.get(WebData().URL)


rows = Excel_Functions(excel_file, sheet_number).row_count()


for row in range(2, rows+1):
    try:
        username = Excel_Functions(excel_file, sheet_number).read_data(row, 7)
        password = Excel_Functions(excel_file, sheet_number).read_data(row, 8)

        # Wait for username field and enter data
        wait.until(EC.presence_of_element_located((By.NAME, TestLocators().usernameLocator))).send_keys(username)

        # Wait for password field and enter data
        wait.until(EC.presence_of_element_located((By.NAME, TestLocators().passwordLocator))).send_keys(password)

        # Wait for the submit button and click it
        wait.until(EC.element_to_be_clickable((By.XPATH, TestLocators().submitButton))).click()

        # validation code for test-cases

        try:
            wait.until(EC.url_contains(WebData().DASHBOARD_URL))
            print(f"SUCCESS : Login success with USERNAME = {username} and PASSWORD = {password}")
            Excel_Functions(excel_file, sheet_number).write_data(row, 9, "TEST PASS")

            # Wait for logout button and perform logout
            logout_button = wait.until(EC.presence_of_element_located((By.XPATH, TestLocators().logoutButton)))
            ActionChains(driver).click(logout_button).perform()
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout"))).click()
        except TimeoutException:
            print(f"FAIL : Login failed with USERNAME = {username} and PASSWORD = {password}")
            Excel_Functions(excel_file, sheet_number).write_data(row, 9, "TEST FAIL")
    except Exception as e:
        print(f"Error processing row {row}: {e}")

   # Quit the driver
driver.quit()


