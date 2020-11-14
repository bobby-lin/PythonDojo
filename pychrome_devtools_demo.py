import PyChromeDevTools
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()

chrome.Page.navigate(url="http://www.nytimes.com/")
chrome.wait_event("Page.frameStoppedLoading", timeout=60)

#Wait last objects to load
time.sleep(5)

cookies=chrome.Network.getCookies()
for cookie in cookies["result"]["cookies"]:
    print ("Cookie:")
    print ("\tDomain:", cookie["domain"])
    print ("\tKey:", cookie["name"])
    print ("\tValue:", cookie["value"])
    print ("\n")