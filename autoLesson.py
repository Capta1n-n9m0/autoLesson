from pathlib import Path
from selenium import webdriver
from time import sleep
from platform import system
from webdriver_manager.chrome import ChromeDriverManager

# Enter you moodle login and password
# USERNAME = ""
# PASSWORD = ""

class Browser:
    def __init__(self, url):
        print("Setting up browser")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.get(url)
        self.active_tab = self.browser.current_window_handle
        self.tabs = self.browser.window_handles
        print("Browser is ready to rock")

class LessonLoginner(Browser):
    def __init__(self, login: str, password: str):
        print("Logining to moodle unistra")
        super().__init__("https://cas.unistra.fr/cas/login")
        self.browser.find_element_by_id("username").send_keys(login)
        self.browser.find_element_by_id("password").send_keys(password)
        self.browser.find_element_by_id("login-btn").click()
        print("Login successful")

    def lesson(self, lesson_link):
        print("Starting entering lesson")
        self.browser.get(lesson_link)
        supposed_title = "BigBlueButton - " + self.browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/section/div/div/div[1]/h3").text
        print(f"Supposed title is: {supposed_title}")
        self.browser.find_element_by_id("join_button_input").click()
        print("Waing for BBB session to load")
        sleep(20)
        print("Joined BBB session")
        self.tabs = self.browser.window_handles
        for tab in self.tabs:
            if tab != self.active_tab:
                self.browser.switch_to.window(tab)
                if self.browser.title == supposed_title:
                    print("Title is fine, the window is right.")
                    self.browser.find_element_by_class_name("icon-bbb-listen").click()
                    print("Audio is connected. We have connected successfully.")
                    break
                else:
                    print(f"Wrong tab! Actual title({self.browser.title}) is not equal to supposed title({supposed_title})!")
        print("End of method")

def main():
    try:
        import creds
    except ImportError:
        print("""
        You should create creds.py, where you would store password from moodle platform.
        write username as user var
        write password as passwd var
        Example:
        user = "abbas-aliyev"
        passwd = "qwerty123"
        """)
        exit(1)
    USERNAME = creds.user
    PASSWORD = creds.passwd
    if USERNAME == "" and PASSWORD == "":
        print("You didn't enter you login and/or password.")
        print("Please edit autoLesson.py file.")
        input("Press enter to exit")
        exit(1)
    session = LessonLoginner(USERNAME, PASSWORD)
    print("For testing i am using math session")
    session.lesson("https://moodle3.unistra.fr/mod/bigbluebuttonbn/view.php?id=573257")


if __name__ == '__main__':
    ...