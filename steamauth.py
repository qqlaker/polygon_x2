from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time, urllib, os, json
from PIL import Image
from steampy.guard import generate_one_time_code

def steamauth(driver_steam, login, password):

    def getcode(share):
        shared_secret = share
        one_time_authentication_code = generate_one_time_code(shared_secret)
        return one_time_authentication_code

    def is_element_present(driver_steam, id_type, id_locator):
        element_found = True
        driver_steam.implicitly_wait(1)
        try:
            element = WebDriverWait(driver_steam, 5).until(
                EC.presence_of_element_located((id_type, id_locator))
            )
        except:
            element_found = False
        driver_steam.implicitly_wait(10)
        return element_found

    def check_twofactorauth_message():
        while True:
            def presense_of_element():
                element_found = True
                try:
                    WebDriverWait(driver_steam, 0).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'twofactorauth_message'))
                    )
                except:
                    element_found = False
                return element_found

            while presense_of_element():

                try:
                    if any(message.is_displayed() for message in driver_steam.find_elements_by_class_name('twofactorauth_message')):
                        return False
                except StaleElementReferenceException:
                    if any(message.is_displayed() for message in driver_steam.find_elements_by_class_name('twofactorauth_message')):
                        return False

                if 'steamcommunity.com/openid' not in driver_steam.current_url:
                    return True

    while True:
        if is_element_present(driver_steam, By.ID, 'steamAccountName'):
            driver_steam.find_element_by_id('steamAccountName').send_keys(login)
            driver_steam.find_element_by_id('steamPassword').send_keys(password)
            driver_steam.find_element_by_class_name('btn_green_white_innerfade').click()
            break
        else:
            if is_element_present(driver_steam, By.CLASS_NAME, 'OpenID_loggedInAccount'):
                driver_steam.find_element_by_class_name('btn_green_white_innerfade').click()
                break

        driver_steam.implicitly_wait(2)

        if is_element_present(driver_steam, By.ID, 'error_display'):
            if driver_steam.find_element_by_id('error_display').is_displayed():
                print('Неверный логин или пароль')
                return False
            else:
                break

    while 'steamcommunity.com/openid' in driver_steam.current_url:
        if driver_steam.find_element_by_id('login_twofactorauth_message_entercode').is_displayed():
            if is_element_present(driver_steam, By.ID, 'twofactorcode_entry'):
                print('Введите Steam Guard код для {}'.format(login))
                try:
                    a = False
                    mafiles = os.listdir('configs/mafiles')
                    for mafile in mafiles:
                        with open(f'configs/mafiles/{mafile}', 'r') as f:
                            json_mafile = json.load(f)
                            cur_login = json_mafile['account_name']
                            if login == cur_login:
                                a = True
                                shared = json_mafile['shared_secret']
                                tfc = getcode(shared)
                                print('>', tfc)
                    if a != True:
                        tfc = input('> ')
                except:
                    tfc = input('> ')
                inp = driver_steam.find_element_by_id('twofactorcode_entry')
                btn = driver_steam.find_element_by_id('login_twofactorauth_buttonset_entercode')
                btn = btn.find_element_by_class_name('auth_button.leftbtn')
                inp.send_keys(tfc)
                btn.click()
                driver_steam.implicitly_wait(2)
                if check_twofactorauth_message():
                    break

        elif driver_steam.find_element_by_id('login_twofactorauth_message_incorrectcode').is_displayed():
            time.sleep(3)
            print('Вы ввели неправильный код, попробуйте ещё раз')
            print('Введите Steam Guard код для {}'.format(login))
            try:
                mafiles = os.listdir('configs/mafiles')
                for mafile in mafiles:
                    with open(f'configs/mafiles/{mafile}', 'r') as f:
                        json_mafile = json.load(f)
                        cur_login = json_mafile['account_name']
                        if login == cur_login:
                            shared = json_mafile['shared_secret']
                            tfc = getcode(shared)
                            print('>', tfc)
            except:
                tfc = input('> ')
            if is_element_present(driver_steam, By.ID, 'login_twofactorauth_buttonset_incorrectcode'):
                btn = driver_steam.find_element_by_id('login_twofactorauth_buttonset_incorrectcode')
                btn = btn.find_element_by_class_name('auth_button.leftbtn')
                inp.send_keys(tfc)
                btn.click()
                driver_steam.implicitly_wait(2)
                if check_twofactorauth_message():
                    break

        elif driver_steam.find_element_by_id('captcha_entry').is_displayed() and driver_steam.find_element_by_id('error_display').is_displayed():
            if is_element_present(driver_steam, By.ID, 'captchaImg'):
                imgurl = driver_steam.find_element_by_id('captchaImg').get_attribute('src')
                urllib.request.urlretrieve(imgurl, "captcha.png")
                time.sleep(2)
                img = Image.open("captcha.png")  # Открытие избражения желательно проводить в интерфейсе
                print('Введите текст с изображения')
                img.show()
                captcha = input('> ')
                try:
                    os.remove("captcha.png")
                except:
                    pass
                driver_steam.find_element_by_id('input_captcha').send_keys(captcha)
                driver_steam.find_element_by_class_name('btn_green_white_innerfade').click()
                driver_steam.implicitly_wait(2)
                if check_twofactorauth_message():
                    break

        elif driver_steam.find_element_by_id('error_display').is_displayed():
            print('За последнее время в вашей сети произошло слишком много безуспешных попыток входа.\n Пожалуйста, подождите и повторите попытку позже. (Перезагрузи wifi)')
            exit()  # Сделать перезапуск или режим ожидания
    return True