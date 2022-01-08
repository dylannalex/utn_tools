from utn_tools import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from abc import ABC
from time import sleep


class UtnBot:
    LOGIN_WEBSITES = ("autogestion", "email")

    def __init__(self, username, password, legajo) -> None:
        self.username = username
        self.password = password
        self.legajo = legajo
        self.sleep_time = settings.SLEEP_SECONDS
        options = Options()
        options.add_argument("log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path=settings.CHROMEDRIVER_PATH, options=options
        )

    def login(self, website: str) -> None:
        """
        website(str):   "autogestion" or "email"
        """
        if website not in UtnBot.LOGIN_WEBSITES:
            raise ValueError(f"Invalid website: {website}")

        sleep(self.sleep_time)
        self.driver.get("https://sysacad.frm.utn.edu.ar/login.php")
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(
            self.password, Keys.RETURN
        )

        sleep(self.sleep_time)
        if website == "autogestion":
            self._click_autogestion()

        if website == "email":
            self._click_email()

    def _click_autogestion(self):
        self.driver.find_element(By.CLASS_NAME, "habilitado").click()

    def _click_email(self):
        self.driver.find_element(By.TAG_NAME, "a").click()
        sleep(self.sleep_time)
        self.driver.find_element(By.NAME, "_pass").send_keys(self.password, Keys.RETURN)


class RollBot(UtnBot):
    ROLES = ("pa", "j2", "a1", "pt")
    DO_NOT_ANSWER_VALUE = "-1"
    STUDENT_QUESTIONS_ELEMENT = "p"
    STUDENT_QUESTIONS = 7
    TEACHER_QUESTIONS = 19

    def complete_rolls(self):
        self.login("autogestion")
        self.driver.get(
            f"http://encuesta.frm.utn.edu.ar/encuesta_materia/encuestamat.php?legajo={self.legajo}"
        )
        sleep(self.sleep_time)
        while True:
            polls = self.driver.find_elements(By.NAME, "completar")
            if not polls:
                return
            poll = polls[0]
            poll.click()
            sleep(self.sleep_time)
            self._complete_student_roll()
            self._complete_teacher_roll()
            self._send_roll()
            sleep(self.sleep_time)

    def _complete_student_roll(self):
        for i in range(1, RollBot.STUDENT_QUESTIONS + 1):
            self.driver.find_element(
                By.NAME, f"{RollBot.STUDENT_QUESTIONS_ELEMENT}{i}"
            ).click()

    def _complete_teacher_roll(self):
        availables_roles = [
            role for role in RollBot.ROLES if self._does_role_exist(role)
        ]
        for role in availables_roles:
            for i in range(1, RollBot.TEACHER_QUESTIONS + 1):
                try:
                    select = Select(self.driver.find_element(By.NAME, f"{role}{i}"))
                    select.select_by_value(RollBot.DO_NOT_ANSWER_VALUE)
                except Exception:
                    print(f"[ERROR] role {role}{i} does not exist")

    def _does_role_exist(self, role):
        try:
            self.driver.find_element(By.NAME, f"{role}1")
            return True
        except Exception:
            return False

    def _send_roll(self):
        self.driver.find_element(By.NAME, "button2").click()
