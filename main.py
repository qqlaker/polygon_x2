import datetime
import time
import requests
from steamauth import steamauth
from webcreate import Webcreate
import selenium


class Polygon(object):

    def __init__(self, url):
        self.url = url
        self.driver = Webcreate()._driverinit()
        self.driver.get(self.url)
        Polygon.main(self)

    def main(self):
        if type(self.url) != str:
            return TypeError
        with open("configs/accs.txt", "r") as f:
            self.__login, self.__password = f.readline().strip().split(' ')
        steamauth(self.driver, self.__login, self.__password)
        self.amount_input = self.driver.find_element_by_id("roulette_amount")
        self.clear_button = self.driver.find_element_by_class_name("clear.button_amount_r")
        self.gray_buttons = self.driver.find_elements_by_class_name("gray_inline.button_amount_r")
        self.add10_button = self.gray_buttons[0]
        self.x2_button = self.gray_buttons[-1]
        self.bid_button = self.driver.find_element_by_class_name("red_button.betButton")
        self.balance = self.get_current_balance()
        if self.check_spin():
            self.clear_button.click()
            self.add10_button.click()
            self.bid_button.click()
            last_bid = 10
            time.sleep(20)
        minus_count = 0
        while True:
            self.balance = self.get_current_balance()
            t = "0"
            while t == "0":
                t = self.driver.find_element_by_id("red_bets_my").find_element_by_tag_name("span").text
            if minus_count > 7:
                time.sleep(600)
                minus_count = 0
            if "-" in t:
                minus_count += 1
                self.x2_button.click()
                last_bid *= 2
            elif "+" in t:
                self.clear_button.click() # TODO: Ставит только по 10
                self.add10_button.click()
                last_bid = 10
            if self.check_spin():
                self.bid_button.click()

    def get_current_balance(self):
        __balance = self.driver.find_element_by_id("balance_r").text
        if int(__balance) < 80:
            print("Balance lower than 80")
            raise Exception
        return int(__balance)

    def save_last_number(self, number):
        with open("configs/memory.txt", "a") as f:
            f.write(str(number))

    def check_spin(self):
        self.spin_text = "text"
        while self.spin_text != "":
            self.spin_text = self.driver.find_element_by_class_name("progress_timer").text
            print(self.spin_text)
            time.sleep(2)
        time.sleep(15)
        return True


if __name__ == '__main__':
    ur = "https://plg.bet/ru?login"
    polygon = Polygon(ur)