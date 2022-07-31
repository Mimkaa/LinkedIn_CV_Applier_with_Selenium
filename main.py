from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
PATH = "D:\python_projects\selenium\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
#
# driver.get("https://www.google.com/")
# title = driver.title
# assert "Google" in driver.title
#
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
class CV_Applier:
    def __init__(self, driver_path, data):

        self.driver = webdriver.Chrome(driver_path)
        self.my_info = data
        self.current_page = 1

    def login_in_linckedin(self):
        self.driver.get("https://www.linkedin.com/")
        assert "LinkedIn" in self.driver.title

        login_email = self.driver.find_element(By.NAME,'session_key')
        login_email.clear()
        login_email.send_keys(self.my_info['email'])
        password = self.driver.find_element(By.NAME,'session_password')
        password.clear()
        password.send_keys(self.my_info['password'])
        password.send_keys(Keys.RETURN)



    def search_job(self):
        # go to Jobs
        jobs_link = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        jobs_link.click()

        # click on the search bar
        search_bar_job = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id*='jobs-search-box-keyword-id-ember']")))
        search_bar_job.clear()
        search_bar_job.send_keys(self.my_info['job'])

        search_bar_location = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id*='jobs-search-box-location-id-ember']")))
        search_bar_location.click()
        search_bar_location.clear()
        search_bar_location.send_keys(self.my_info['location'])
        search_bar_job.send_keys(Keys.RETURN)


    def filter(self):
        # filter by easy apply
        filter_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="All filters"]')))
        filter_button.click()
        time.sleep(1)
        toggle = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/ul/li[7]/fieldset/div")
        toggle.click()
        time.sleep(1)
        apply_button = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Show")]')))
        apply_button.click()



    def get_offers(self):
        all_vacancies = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results-list__text")
        dumped_string = ''
        for el in all_vacancies:
            dumped_string += el.text + " "
        # 24 (starting from 0) max number of offers on one page
        all_result_num = [int(s) for s in dumped_string.split(' ') if s.isnumeric()][0]




        for p in range(all_result_num//25):
            next_page = self.driver.find_element(By.CSS_SELECTOR, f"[aria-label='Page {self.current_page}']")
            next_page.click()
            time.sleep(3)
            for i in range(25):

                time.sleep(1)
                all_results = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item.occludable-update")
                hover = ActionChains(self.driver).move_to_element(all_results[i])
                hover.perform()
                titles = all_results[i].find_elements(By.CSS_SELECTOR,'.ember-view.job-card-container__link.job-card-list__title')
                all_titles_num = len(titles)
                for j in range(all_titles_num):
                    self.submit_application(titles[j])
                    titles = self.driver.find_elements(By.CSS_SELECTOR,'.ember-view.job-card-container__link.job-card-list__title')

            self.current_page +=1
            if p == all_result_num//35 - 1:
                self.close_session()




        # next page



    def submit_application(self, title):
        # follow the job`s link
        try:
            job_link = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, title.text)))
            job_link.click()
            # let it load
            time.sleep(1)

            # click easy apply
            try :

                easy_apply_button = WebDriverWait(self.driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Easy")]')))
                easy_apply_button.click()

                # try applying
                time.sleep(1)

                # input phone number
                try:
                    input_phone = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/form/div/div[1]/div[3]/div[2]/div/div/input")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(input_phone)
                    actions.click()
                    actions.perform()
                    input_phone.clear()
                    input_phone.send_keys(self.my_info["phone"])

                    next_button = WebDriverWait(self.driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Next")]')))
                    actions = ActionChains(self.driver)
                    actions.move_to_element(next_button)
                    actions.click()
                    actions.perform()

                except NoSuchElementException:
                    pass

                for i in range(1):
                    try:
                        next_button = WebDriverWait(self.driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Next")]')))
                        actions = ActionChains(self.driver)
                        actions.move_to_element(next_button)
                        actions.click()
                        actions.perform()
                    except TimeoutException:
                        pass

                # dealing with inputs
                try :
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, ".ember-text-field.ember-view.fb-single-line-text__input")
                    for inp in inputs:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(inp)
                        actions.click()
                        actions.perform()
                        inp.clear()
                        inp.send_keys('2')
                except:
                    pass

                # find and deal with radiobuttons
                try:
                    div_with_radiobuttons = self.driver.find_elements(By.CSS_SELECTOR, ".fb-radio-buttons")

                    for div in div_with_radiobuttons:
                        radiobuttons = div.find_elements(By.XPATH, "//*[@type='radio']")
                        for r in radiobuttons:
                            if r.get_attribute("value") == "Yes":
                                actions = ActionChains(self.driver)
                                actions.move_to_element(r)
                                actions.click()
                                actions.perform()

                except NoSuchElementException:
                    pass

                # click review Button
                try:
                    review_button = self.driver.find_element(By.XPATH, '//button[contains(., "Review")]')
                    actions = ActionChains(self.driver)
                    actions.move_to_element(review_button)
                    actions.click()
                    actions.perform()

                except NoSuchElementException:
                    pass

                # submit
                try:
                    submit_button = self.driver.find_element(By.XPATH, '//button[contains(., "Submit")]')
                    actions = ActionChains(self.driver)
                    actions.move_to_element(submit_button)
                    actions.click()
                    actions.perform()
                except NoSuchElementException:
                    pass


            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                pass




            # return back
            current_page = self.driver.current_url
            while True:
                current_page1 = self.driver.current_url
                if current_page1[:31] == current_page[:31]:
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(1)
                else:
                    break
            time.sleep(1)
        except ElementClickInterceptedException:
            pass






    def close_session(self):
        self.driver.close()

data = {
        }
cv_applier = CV_Applier(PATH, data)
cv_applier.login_in_linckedin()
try:
    cv_applier.search_job()
except:
    time.sleep(10)
    cv_applier.search_job()
cv_applier.filter()
time.sleep(3)
cv_applier.get_offers()

#cv_applier.close_session()