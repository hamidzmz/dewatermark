from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import os
import keyboard

folder_path = r"M:\Webcrawler\dsProject\Getting_Pictures\pictures-skytech"
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

source_directory = r"C:\Users\Hamidreza\Downloads"
destination_directory = r"Z:\Skytech_Pictures_withoutwatermark"

timeout = 50

# Initialize Chrome WebDriver outside the loop
driver = webdriver.Chrome(executable_path="C:\Program Files\chromedriver-win32\chromedriver.exe")
driver.get("https://dewatermark.ai/")

for image_file in image_files:
    print(image_file)
    input_path = os.path.join(folder_path, image_file)

    

    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/button'))
        )
        element.click()
        time.sleep(3)
        keyboard.write(input_path)
        keyboard.press_and_release('enter')

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]'))
        )

        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]').click()

        WebDriverWait(driver, 50).until(
            EC.staleness_of(driver.find_element(By.XPATH, ' //*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[1]/div/div/div'))
        )

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Download")]'))
        )
        driver.execute_script("arguments[0].click();", button)

        start_time = time.time()
        file_moved = False
        while time.time() - start_time <= timeout:
            files = os.listdir(source_directory)
            for file in files:
                source_path = os.path.join(source_directory, file)
                if os.path.isfile(source_path) and file.lower().endswith('.jpeg'):
                    new_filename = image_file
                    destination_path = os.path.join(destination_directory, new_filename)
                    shutil.move(source_path, destination_path)
                    print(f"File {file} moved successfully to {new_filename}.")
                    file_moved = True
                    break
            if file_moved:
                break
            time.sleep(1)

        if not file_moved:
            print("Timeout reached. No new jpg file created.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.refresh()  # Refresh the page for the next iteration

# Close the WebDriver after processing all image files
driver.quit()
