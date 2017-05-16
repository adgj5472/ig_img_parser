import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
import os
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parser(username):
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe') # chrome瀏覽器
    #driver = webdriver.PhantomJS(executable_path='./phantomjs/bin/phantomjs.exe')  # PhantomJs
    url='https://www.instagram.com'
    driver.get(url+'/'+username)                #要爬的網址
    #-----------------------------------
    #創資料夾
    path=".//"+username
    if not os.path.isdir(path):
        os.mkdir(path)
    #-----------------------------------

    try:
        driver.find_element_by_link_text("載入更多內容").click() #按下"載入更多內容"
    except:
        print()

    while(True):
        old=driver.execute_script('return document.body.scrollHeight;')         #原本網頁頁面高度
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # 重複往下捲動
        time.sleep(0.5)
        new=driver.execute_script('return document.body.scrollHeight;')         #新的網頁頁面高度
        if(old==new):   	                                                    #判斷式成立為已到頁面底部
            break

    urllist=[]
    pageSource = driver.page_source  # 取得網頁原始碼
    soup=BeautifulSoup(pageSource,"html.parser")
    for a in soup.select('._8mlbc'):
        #print(a['href'])
        urllist.append(a['href'])
        driver.get(url+a['href'])
        imgsource=driver.page_source
        s=BeautifulSoup(imgsource,"html.parser")
        for img in s.select('._icyx7'):
            #print(img['src'])
            fname=img['src'].split('/')[-1] #檔名
            print(fname)  	    #檔名存入list
            res2=requests.get(img['src'],stream=True)
            f=open(path+"//"+fname,'wb')              #創建一個檔案 以binary寫入
            shutil.copyfileobj(res2.raw,f)  #檔案存檔
            f.close()                       
            del res2    	            #刪除暫存
    driver.close()  # 關閉瀏覽器
    driver.quit()   # 結束全部視窗

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def upload(dir_name,namelist): #上傳
    gauth = GoogleAuth()
    gauth.CommandLineAuth() #透過授權碼認證
    drive = GoogleDrive(gauth)
    for i in range(0,len(namelist)):
        try:
    #        file1 = drive.CreateFile({"title":namelist[i],"parents": [{"kind": "drive#fileLink", "id": "0Bzg_ffxdg0QHQ1J6aVZ5Z2pfUXM",'mimeType':'image/jpeg'}]}) #parents id 為雲端資料夾位置   
            #file1 = drive.CreateFile({"title":namelist[i],"parents": [{"kind": "drive#fileLink", "id": "0B14PTGPX5CPZblc1bURfVzI3VFE",'mimeType':'image/jpeg'}]}) #圖
            #file1 = drive.CreateFile({"title":namelist[i],"parents": [{"kind": "drive#fileLink", "id": "0B14PTGPX5CPZOXQ4R09WMldmb2M",'mimeType':'image/jpeg'}]})#陳語謙
            file1 = drive.CreateFile({"title":namelist[i],"parents": [{"kind": "drive#fileLink", "id": "0B14PTGPX5CPZQjRGbVF4bDFTbk0",'mimeType':'image/jpeg'}]})
            file1.SetContentFile('./'+dir_name+'/'+namelist[i])
            file1.Upload() #檔案上傳 
            print("Upload "+namelist[i]+" succeeded!")
        except:
            print("Uploading failed.")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filename(dir_name):# 資料夾下所有檔案
    filename_list=[]
    for root, dirs, files in os.walk(dir_name):
        #print(root)
        for f in files:
            filename_list.append(os.path.join(f))
    return filename_list
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#main
username_list=['cyc.85'] #要爬的帳號
for i in range(0,len(username_list)):
    #parser(username_list[i]) #開爬
    filename_list=filename(username_list[i]) #爬下來的檔案名稱
    #print(filename_list)
    upload(username_list[i],filename_list)  #上傳   dir_name,filename_list 
