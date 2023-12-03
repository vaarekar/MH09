import cv2
import pytesseract
import time
import urllib.request
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from selenium.webdriver.common.by import By
import pandas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

# OldVersion
DismisPopup = '//*[@id="bs_alert"]/div/div/div[2]/button'
captchatampering = '//*[@id="caseHistoryDiv"]'
invalidcaptchascreen = '//*[@id="caseHistoryDiv"]/p'
InvalidCaptchaErrorXpath = '//*[@id="bs_alert"]/div/div/div[1]'
invalidcnrxpath = '//*[@id="bs_alert"]/div/div/div[1]'
# backbtnxpath='//*[@id="bckbtn"]'
# casetypexpath='//*[@id="shareSelect"]/table[1]/tbody/tr[1]/td[2]'
# FilingNumberxpath  ='//*[@id="shareSelect"]/table[1]/tbody/tr[2]/td[2]'
# FillingDatexpath ='//*[@id="shareSelect"]/table[1]/tbody/tr[2]/td[4]'
# RegistrationNumberxpath ='//*[@id="shareSelect"]/table[1]/tbody/tr[3]/td[2]/label'
# RegistrationDatexpath= '//*[@id="shareSelect"]/table[1]/tbody/tr[3]/td[4]/label'
# FirstHearingDatexpath ='//*[@id="shareSelect"]/table[2]/tbody/tr[1]/td[2]/strong'
# NextHearingDatexpath ='//*[@id="shareSelect"]/table[2]/tbody/tr[2]/td[2]/strong'
# CaseStagexpath ='//*[@id="shareSelect"]/table[2]/tbody/tr[3]/td[2]/label/strong'
# CaseDisposedxPath='//*[@id="shareSelect"]/table[2]/tbody/tr[3]/td[2]/strong'
# CourtNumberxpath ='//*[@id="shareSelect"]/table[2]/tbody/tr[4]/td[2]/label/strong'
# petitionerxpath ='//*[@id="caseHistoryDiv"]/form/div/table[1]/tbody/tr/td'
# DecisionDatexpath='//*[@id="shareSelect"]/table[2]/tbody/tr[2]/td[2]/strong'
# NatureOfDisposalxpath ='//*[@id="shareSelect"]/table[2]/tbody/tr[4]/td[2]/label/strong'
# CourtNumberForDisposedCasexpath='//*[@id="shareSelect"]/table[2]/tbody/tr[5]/td[2]/label/strong'


# NewVersion
IsSomethingWrong='//*[@id="validateError"]/div/div/div[2]/div/div[1]'

DismisPopup = '//*[@id="validateError"]/div/div/div[1]/button'

InvalidCaptchaErrorXpath = '//*[@id="validateError"]/div/div/div[2]/div/div[1]'
invalidcnrxpath = '//*[@id="bs_alert"]/div/div/div[1]'
backbtnxpath = '//*[@id="main_back_cnr"]'
casetypexpath = '//*[@id="history_cnr"]/table[1]/tbody/tr[1]/td[2]'
FilingNumberxpath = '//*[@id="history_cnr"]/table[1]/tbody/tr[2]/td[2]'
FillingDatexpath = '//*[@id="history_cnr"]/table[1]/tbody/tr[2]/td[4]'
RegistrationNumberxpath = '//*[@id="history_cnr"]/table[1]/tbody/tr[3]/td[2]/label'
RegistrationDatexpath = '//*[@id="history_cnr"]/table[1]/tbody/tr[3]/td[4]/label'
FirstHearingDatexpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[1]/td[2]/strong'
NextHearingDatexpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[2]/td[2]/strong'
CaseStagexpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[3]/td[2]/label/strong'
CaseDisposedxPath = '//*[@id="history_cnr"]/table[2]/tbody/tr[3]/td[2]/strong'
CourtNumberxpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[4]/td[2]/label/strong'
# petitionerxpath ='//*[@id="caseHistoryDiv"]/form/div/table[1]/tbody/tr/td'
petitionerxpath = '//*[@id="history_cnr"]/table[3]/tbody/tr/td'
DecisionDatexpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[2]/td[2]/strong'
NatureOfDisposalxpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[4]/td[2]/label/strong'
CourtNumberForDisposedCasexpath = '//*[@id="history_cnr"]/table[2]/tbody/tr[5]/td[2]/label/strong'


def get_captcha(driver, element):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    # logandshow(location)
    size = element.size
    # logandshow(size)
    # saves screenshot of entire page
    driver.save_screenshot("tmpimg1.png")

    # uses PIL library to open image in memory
    image = Image.open("tmpimg1.png")

    left = location['x'] + 5
    top = location['y'] + 5
    right = location['x'] + size['width'] - 5
    bottom = location['y'] + size['height'] - 5

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save('img1.png')  # saves new cropped image


def readimage():
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    img = cv2.imread("img1.png")
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w * 2, h * 2))
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    captchatext = pytesseract.image_to_string(thr)
    captchatext = ''.join(ch for ch in captchatext if ch.isalnum())
    captchatext = captchatext.strip()
    return captchatext


def isinvalidcnrpopup(driver):
    try:
        logandshow("Checking for invalid CNR Popup ")
        invcnr = driver.find_element(By.XPATH, InvalidCNRxpath)
        logandshow("Text Found :"+invcnr.text)
        if 'CNR' in invcnr.text:
            # logandshow("Invalid CNR Screen found , dismissing it ")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="bs_alert"]/div/div/div[2]/button'))).click()
            return "INVALIDCNR"
    except:
        return "CHECKNEXT"

    return "CHECKNEXT"

def issomethingwrng(driver):
    try:
        logandshow("Checking for oops something wrong  ")
        somethingwrong = driver.find_element(By.XPATH,IsSomethingWrong)
        logandshow("Text Found :"+invcnr.text)
        if 'wrong' in str.lower(somethingwrong.text):
            # logandshow("Invalid CNR Screen found , dismissing it ")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, DismisPopup))).click()
            return "SOMETHINGWRONG"
    except:
        return "CHECKNEXT"

    return "CHECKNEXT"

def isinvalidcaptchascreen(driver):
    try:
        logandshow("Checking if Invalid captha screen is there ")
        invalidcaptcha = driver.find_element(By.XPATH, invalidcaptchascreen)
        logandshow("Text Found :"+invalidcaptcha.text)
        bckbtn = driver.find_element(By.XPATH, backbtnxpath)
        bckbtn.click()
        return "INVALIDCAPTCHA"
    except:
        return "CHECKNEXT"


def iscaptchatempering(driver):
    try:
        logandshow("Checking if captcha temparing screen is there ")
        temparingcaptcha = driver.find_element(By.XPATH, captchatampering)
        logandshow("Text Found:"+temparingcaptcha.text)
        if "tampering" in temparingcaptcha.text:
            bckbtn = driver.find_element(By.XPATH, backbtnxpath)
            bckbtn.click()
            return "TEMPARINGCAPTCHA"
    except:
        return "CHECKNEXT"

    return "CHECKNEXT"


def isentervalidcaptchapopup(driver):
    try:
        logandshow("Checking for enter valid captha popup ")
        entervcaptcha = driver.find_element(By.XPATH, InvalidCaptchaErrorXpath)
        logandshow("Text Found:"+entervcaptcha.text)
        if "Enter valid" in entervcaptcha.text:
            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            return "ENTERVALIDCAPTCHA"
        if "THERE IS AN ERROR" in entervcaptcha.text:
            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            bckbtn = driver.find_element(By.XPATH, backbtnxpath)
            bckbtn.click()
            return "INVALIDCNR"

    except:
        return "CHECKNEXT"

    return "CHECKNEXT"

def isentervalidCNRpopup(driver):
    try:
        logandshow("Checking for enter valid CNR popup ")
        entervcaptcha = driver.find_element(By.XPATH, InvalidCaptchaErrorXpath)
        logandshow("Text Found:"+entervcaptcha.text)
        if "16" in entervcaptcha.text:
            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            return "INVALIDCNR"
        if "Invalid Captcha" in entervcaptcha.text:
            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            btn = driver.find_element(By.XPATH, backbtnxpath)
            btn.click()
            return "INVALIDCAPTCHA"

    except:
        return "CHECKNEXT"

    return "CHECKNEXT"

def isinvalidcaptchapopup(driver):
    try:
        logandshow("Checking  if Invalid Captcha Popup is there")
        invc = driver.find_element(By.XPATH, InvalidCaptchaErrorXpath)
        logandshow("Text Found:"+invc.text)
        if "Invalid" in invc.text:
            logandshow("Attempting Dismiss popup ")

            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            btn=driver.find.element(By.XPATH,backbtnxpath)  # This is required only for new version
            btn.click() # This is required only for new version
            return "INVALIDCAPTCHAPOPUP"
        if "Only alphabets and numbers" in invc.text:
            logandshow("Invalid alphabets popup found Attempting Dismiss popup ")
            btn = driver.find_element(By.XPATH, DismisPopup)
            btn.click()
            logandshow("Invalid alphabets popup found so returning INVALIDCNR to skip this ")
            return "INVALIDCNR"



    except:
        return "CHECKNEXT"


    return "CHECKNEXT"


def checkerrors(driver):
    result = issomethingwrng(driver)
    if result != "CHECKNEXT":
        # refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
        # refreshcaptcha.click()
        return result

    result = isentervalidCNRpopup(driver)
    if result != "CHECKNEXT":
        # refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
        # refreshcaptcha.click()
        return result

    result = isinvalidcnrpopup(driver)
    if result != "CHECKNEXT":
        # refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
        # refreshcaptcha.click()
        return result
    result = isinvalidcaptchascreen(driver)
    if result != "CHECKNEXT":
        return result
    result = isinvalidcaptchapopup(driver)
    if result != "CHECKNEXT":
        #refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
        #refreshcaptcha.click()
        return result
    result = isentervalidcaptchapopup(driver)
    if result != "CHECKNEXT":
        refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
        refreshcaptcha.click()
        return result
    result = iscaptchatempering(driver)
    if result != "CHECKNEXT":
        return result

    return "OK"


def attemptcnr(cnrnumber, driver):
    try:
        placecnrhere = driver.find_element("name", "cino")
        placecnrhere.clear()
        placecnrhere.send_keys(cnrnumber)
        placecnrhere.send_keys(Keys.TAB)

        # time.sleep(2)
        capmaxrefresh = 5
        captchatext = ''
        captchahere = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div/form/div/input")
        while captchatext.strip() == '':
            capimage = driver.find_element(By.ID, "captcha_image")
            get_captcha(driver, capimage)
            captchatext = readimage()
            if captchatext.strip() == '':
                capmaxrefresh = capmaxrefresh - 1
                refreshcaptcha = driver.find_element(By.CLASS_NAME, "refresh-btn")
                refreshcaptcha.click()
                if capmaxrefresh < 0:
                    break
        if captchatext.strip() == '':
            return "Blank Captcha"

        captchahere.clear()
        # time.sleep(2)
        logandshow(captchatext)
        captchahere.send_keys(captchatext)
        hitsearch = driver.find_element("id", "searchbtn")
        # time.sleep(1)
    except  Exception as e:
        print(str(e))
        #a=input("Returning NOT OK , Hit Entere Key")
        issomethingwrng(driver)
        return "NOTOK"

    try:
        hitsearch.click()
    except:
        logandshow("Wait and see what happens")
    time.sleep(1)
    result = checkerrors(driver)
    if result != "OK" and result != "INVALIDCNR":
        return result
    if result == "INVALIDCNR":
        return "OK"  # Return OK so that it starts processing next CNR
    # to identify the table rows
    # logandshow("************ALL VALIDATIONS PASSED*************")
    time.sleep(2)
    CaseType = ''
    FilingNumner = ''
    FillingDate = ''
    RegistrationNumber = ''
    RegistrationDate = ''
    FirstHearingDate = ''
    NextHearingDate = ''
    CaseStage = ''
    CourtNumberIfCaseNotDisposed = ''
    Pettioner = ''
    DecisionDate = ''
    NatureofDisposal = ''
    CourtNumberForDisposedCase = ''
    CaseDisposed = ''

    # WebDriverWait(driver, 200).until(EC.visibility_of(driver.find_element(By.ID, 'bckbtn')))
    cnrdata = []
    cnrdata.append(cnrnumber)
    maxtries = 5
    while maxtries > 0:
        try:
            CaseType = driver.find_element(By.XPATH, casetypexpath).text
            break
        except  Exception as e:
            logandshow("Page Not loaded yet ")
            maxtries = maxtries - 1
            time.sleep(2)

    if maxtries <= 0:
        backbtn = driver.find_element(By.XPATH, backbtnxpath)
        backbtn.click()
        return "NOT OK"

    try:
        CaseType = driver.find_element(By.XPATH, casetypexpath).text
    except  Exception as e:
        CaseType = 'NOTFOUND'

    try:
        FilingNumner = driver.find_element(By.XPATH, FilingNumberxpath).text
    except  Exception as e:
        FilingNumner = 'NOTFOUND'

    try:
        FillingDate = driver.find_element(By.XPATH, FillingDatexpath).text
    except  Exception as e:
        FillingDate = 'NOTFOUND'

    try:
        RegistrationNumber = driver.find_element(By.XPATH, RegistrationNumberxpath).text
    except  Exception as e:
        RegistrationNumber = 'NOTFOUND'

    try:
        RegistrationDate = driver.find_element(By.XPATH, RegistrationDatexpath).text
    except  Exception as e:
        RegistrationDate = 'NOTFOUND'

    try:
        FirstHearingDate = driver.find_element(By.XPATH, FirstHearingDatexpath).text
    except  Exception as e:
        FirstHearingDate = 'NOTFOUND'

    try:
        NextHearingDate = driver.find_element(By.XPATH, NextHearingDatexpath).text
    except  Exception as e:
        NextHearingDate = 'NOTFOUND'

    try:
        CaseStage = driver.find_element(By.XPATH, CaseStagexpath).text
    except  Exception as e:
        CaseStage = 'NOTFOUND'

    try:
        CaseDisposed = driver.find_element(By.XPATH, CaseDisposedxPath).text
        logandshow("CASE DISPOSED FOUND IS : " + CaseDisposed)
    except  Exception as e:
        CaseDisposed = 'NOTFOUND'

    try:
        CourtNumberIfCaseNotDisposed = driver.find_element(By.XPATH, CourtNumberxpath).text
    except  Exception as e:
        CourtNumberIfCaseNotDisposed = 'NOTFOUND'

    try:
        Pettioner = driver.find_element(By.XPATH, petitionerxpath).text
    except  Exception as e:
        Pettioner = 'NOTFOUND'

    try:
        DecisionDate = driver.find_element(By.XPATH, DecisionDatexpath).text
    except  Exception as e:
        DecisionDate = 'NOTFOUND'

    try:
        NatureofDisposal = driver.find_element(By.XPATH, NatureOfDisposalxpath).text
    except  Exception as e:
        NatureofDisposal = 'NOTFOUND'

    try:
        CourtNumberForDisposedCase = driver.find_element(By.XPATH, CourtNumberForDisposedCasexpath).text
    except  Exception as e:
        CourtNumberForDisposedCase = 'NOTFOUND'

    cnrdata.clear()
    cnrdata.append(cnrnumber)
    cnrdata.append(CaseType)
    cnrdata.append(FilingNumner)
    cnrdata.append(FillingDate)
    cnrdata.append(RegistrationNumber)
    cnrdata.append(RegistrationDate)
    cnrdata.append(FirstHearingDate)

    if 'Case disposed' in CaseDisposed:
        cnrdata.append(DecisionDate)
        cnrdata.append(CaseDisposed)
    else:
        cnrdata.append(NextHearingDate)
        cnrdata.append(CaseStage)

    if 'Case disposed' in CaseDisposed:
        cnrdata.append(CourtNumberForDisposedCase)
    else:
        cnrdata.append(CourtNumberIfCaseNotDisposed)

    cnrdata.append(Pettioner)

    if 'Case disposed' in CaseDisposed:
        cnrdata.append(NatureofDisposal)
    else:
        cnrdata.append('NOT DISPOSED')

    # logandshow("Data rtrival done going back ... ")
    backbtn = driver.find_element(By.XPATH, backbtnxpath)
    backbtn.click()
    # logandshow("Screen Found for ",cnrnumber)
    return cnrdata


def logandshow(*args):
    for arg in args:
        print(str(arg))
        logging.info(str(arg))


# Main Program Starts Here
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='MH09.log')
logging.info("Starting Script ... ")
chrome_options = webdriver.ChromeOptions()
# Chrome v75 and lower:
#chrome_options.add_argument("--headless")
# Chrome v 76 and above (v76 released July 30th 2019):
#chrome_options.headless = False
chrome_options.binary_location=r'.\chromedriver\chrome\chrome.exe'
#chrome_options.add_argument("webdriver.chrome.driver",r".\chromedriver\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(executable_path=r".\chromedriver\chromedriver\chromedriver.exe",options=chrome_options)
# driver = webdriver.Chrome('./chromedriver')
# driver.set_window_position(-10000, 0)
cnrlink = 'https://services.ecourts.gov.in/ecourtindia_v6/'
driver.get(cnrlink)

excel_data_df = pandas.read_excel('PendingCases.xlsx', sheet_name='Pending')
# logandshow(excel_data_df)

cnrlist = excel_data_df['CNR'].tolist()

AllData = []

donecount = 1
cnrcount = len(cnrlist)

for cnr in cnrlist:

    retval = "NOTOK"
    logandshow("       ")
    logandshow("       ")
    logandshow(
        str(donecount) + " of " + str(cnrcount) + "  CNR = " + cnr + "   ############################################")
    logandshow("       ")
    # driver.get(cnrlink)
    time.sleep(1)
    while retval != "OK":
        retval = attemptcnr(cnr, driver)
        if type(retval) == str:
            if retval == "OK":
                logandshow("****************************CNR Does not exists " + cnr)
                donecount = donecount + 1
            logandshow(cnr, retval)
        else:
            logandshow(retval)
            AllData.append(retval)
            donecount = donecount + 1
            retval = "OK"

df = pandas.DataFrame(AllData, columns=['CNR', 'CASE TYPE', 'FILING NUMBER', 'FILING DATE', 'REG NUMBER', 'REG DATE',
                                        'FIRST HEARING', 'NEXT HEARING/DECISIONDATE', 'STAGE', 'COURT', 'PETIONER',
                                        'NATUREOFDISPOSAL'])
df.to_excel('output.xlsx')

driver.close()
sys.exit()

