
import os
import requests
import time
import csv
import json
from bs4 import BeautifulSoup


def List_all():

    List_NO=[]
    List_0=[1216,1232,1513,1521,1730,1773,1788,2330,2373,2385,2412,2414,2480,2823,2891,2892,3010,3042,3045,3501,4205,4527,4535,4904,5880,6023,6224,6508,6803,8341,8422,8435,8926,9908,9911,9942] # 4103, 6024,8341
    List_1=[1215,1229,1264,1307,1712,2420,2450,2451,2459,2493,2616,2729,2820,2908,3130,3702,4104,4974,5871,6112,6189,6201,6216,6263,6277,6281,6285,8923,8931,9917,9925,9941,9943]    
    List_2=[1231,1451,1558,1726,2105,2114,2355,2433,2608,2903,4506,4532,4706,5706,6128,6192,6206,6214,9930,9933]
    List_3=[1233,1507,1604,2382,2834,2880,2881,2882,2884,2885,2886,2890,2891,2892,2912,5312,5434,5880,6136,6184,6202,8083,8406,9924]
    List_NO.extend(List_0)
    List_NO.extend(List_1)
    List_NO.extend(List_2)
    List_NO.extend(List_3)    
    List_4=[1580,1593,2376,2455,2889,3563,4305,4736,5007,5487,5706,6146,8210,8446,9905,9937]    #待確認穩定型
    List_5=[2104,2476,3088,3213,3416,3479,3705,5493,6154,6290,6464,8042,8255,8916]    #待確認選股區
    List_6=[1234,1702,2377,2383,2397,2441,2727,3299,3617,3665,5287,5388,8016,8050]              #待確認成長型
    List_7=[1535,1537,1560,1707,1723,2015,2104,2114,2347,3022,3023,3388,4104,4175,4722,6184,8109,8114,9904,9910,9951]  #雜誌 #8359    
    List_NO.extend(List_4)
    List_NO.extend(List_5)
    List_NO.extend(List_6)
    List_NO.extend(List_7)      
    print("\n作者自選定存股清單:")
#    print(List_NO)
            
    return List_NO


def Now():
    sec0=time.time()
    tlocal=time.localtime(sec0)
    # tlocal[0],tlocal[1],tlocal[2],tlocal[3],tlocal[4],tlocal[5] 代表 年 月 日 時 分 秒 
    return tlocal
    

def Decide_season():
    month=Now()[1]
    day=Now()[2]
    days=(month-1)*30+day
    if days>315: season="Q3"
    elif days>225 and days<=315: season="Q2"
    elif days>105 and days<=225: season="Q1"
    else: season="Q4"    
    return season


def Make_dir(string):
    if not os.path.exists(string+"/"):
        os.mkdir(string)
        print(string+"資料夾已建立")
    else:
        print(string+"資料夾已存在")
 

def Get_list_300(number):
    print("\n取得市值排名前"+number+"之股票清單中...")
    List_num=[]
    url="https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%85%AC%E5%8F%B8%E7%B8%BD%E5%B8%82%E5%80%BC%E6%9C%80%E9%AB%98%40%40%E5%85%AC%E5%8F%B8%E7%B8%BD%E5%B8%82%E5%80%BC%40%40%E5%85%AC%E5%8F%B8%E7%B8%BD%E5%B8%82%E5%80%BC%E6%9C%80%E9%AB%98&SHEET=%E5%85%AC%E5%8F%B8%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99&RPT_TIME=&SHEET2=%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B"
    soup=Get_soup(url,310,0.3)                
    tag_tr=soup.find(id="hrow0") 
    tag_list=[tag_tr]
    tag_list0=tag_tr.find_next_siblings()
    tag_list.extend(tag_list0)    
    print("市值排名   股票號碼")    
    for tag in tag_list:
        td_list=tag.find_all("td")
        s1=td_list[0].string
        s2=td_list[1].nobr.a.string
        print(s1,"       ",s2)
        List_num.append([s1,s2])
        if s1==number:
            break        
    file_path="csv/stock300.csv"
    fp = open(file_path,'w',newline='')
    writer=csv.writer(fp)
    for small_list in List_num:
        writer.writerow(small_list)
    fp.close()    


def Read_list_300(number):
    print("\n取得市值排名前"+number+"之股票清單中...")
    file_path="csv/stock300.csv"
    if os.path.exists(file_path):
        fp = open(file_path,'r')
        reader=csv.reader(fp)        
        List_NO=[]
        num=0
        for row in reader:
            List_NO.append(row[1])
            num+=1
            if num==int(number):
                break
        fp.close()
    print(List_NO)    
    return List_NO    


def Get_stock_name():
    print("取得上市上櫃股票號碼跟名稱")
    list1=[i for i in range(11,38)] 
    list2=[i for i in range(41,69)]
    list2.remove(63)
    list3=["00","01",74,75,80,81,82,83,84,89,91,98,99]
    total=[]
    total.extend(list1)
    total.extend(list2)
    total.extend(list3)
    Stock_name={}
    Stock_number={}
    for no in total:
        url_0="https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E5%85%A8%E9%83%A8&STOCK_CODE={0}&SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&SHEET2=%E6%97%A5&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99"
        url=url_0.format(str(no))
        soup=Get_soup(url,180,3)
        tag_test=soup.find(text="查無資料!!") 
        if tag_test==None:
            tag_tr_0=soup.find(id="row0")
            if tag_tr_0!=None:
                tag_tr_123=tag_tr_0.find_next_siblings()
                tag_tr_list=[]
                tag_tr_list.append(tag_tr_0)
                tag_tr_list.extend(tag_tr_123)
                for tr in tag_tr_list: 
                    td_list=tr.find_all("td")
                    str0=td_list[0].nobr.a.string
                    str1=td_list[1].nobr.a.string
                    print(str0,str1)
                    Stock_name[str0]=str1
                    Stock_number[str1]=str0
            else: print("id=row0搜尋不到")
        else: print("此號碼開頭查無資料!")
    file_path1="json/other/stock_name.json"
    file_path2="json/other/stock_number.json"
    fp1= open(file_path1,'w')  
    json.dump(Stock_name,fp1) 
    fp1.close()
    fp2= open(file_path2,'w')  
    json.dump(Stock_number,fp2) 
    fp2.close()    
    
    fp1= open(file_path1,'r')
    Stock_name0=json.load(fp1)
    print(Stock_name0)
    fp2= open(file_path2,'r')
    Stock_number0=json.load(fp2)
    print(Stock_number0)


    
def Get_soup(url,time1,time2):
    headers={"user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    aa=1
    while(aa==1):
        try:
            html=requests.get(url,headers=headers)
            aa=0
        except requests.exceptions.ConnectionError as ex3:
            print("網路連線錯誤: " + str(ex3) )
            print("等待"+str(time1)+"秒再次嘗試連線")
            time.sleep(time1)
        
    if html.status_code==requests.codes.ok:        
        html.encoding="utf8"
        print("HTML取得成功")
        soup=BeautifulSoup(html.text, "lxml")
        print("SOUP取得成功")  
    else:
        print("HTML取得失敗")
        print("SOUP取得失敗") 
        soup=[]
    time.sleep(time2)
    return soup


def Stock_input():

    file_path="json/other/stock_number.json"
    with open(file_path,'r') as fp2:
        Stock_number=json.load(fp2) 
    List_NO=[]
    typing="1"  
    times=0    
    while(typing=="1"):
        if times==0:                
            str0=input("\n請輸入股票代號或股票名稱: ")
            if str0 in Stock_number:
                str1=Stock_number[str0]
                List_NO.append(str1)
                print("已列入股票清單")                        
            elif str0 :
                List_NO.append(str0)
                print("已列入股票清單")
        else:
            str0=input("\n請輸入股票代號或股票名稱, (或者輸入[0]結束): ")
            if str0=="0": 
                typing="0"
            else:
                if str0 in Stock_number:
                    str1=Stock_number[str0]
                    List_NO.append(str1)
                    print("已列入股票清單")                        
                else:
                    List_NO.append(str0)
                    print("已列入股票清單")
                       
        print("(若輸入股票名稱 系統未自動轉換成股票號碼" )
        print(" 代表此一輸入為無效 需自行查詢股票號碼)")
        print("\n目前的股票清單:")        
        print(List_NO)
        times+=1    
    return List_NO


def Choice4():

    List_NO=[]
    file_path="csv/User_lists.csv"
    bb=1
    while (bb==1):
        print("[1] 新增股票清單")
        print("[2] 刪除股票清單")
        print("[3] 使用儲存的股票清單作篩選")
        print("[4] 直接輸入股票清單作篩選")
        print("[5] 返回主目錄")
        
        s0=input("請輸入[1~4]: ")
        if s0 =="1":
            List0=Stock_input()
            fp1=open(file_path,'a',newline='')
            writer=csv.writer(fp1)
            writer.writerow(List0)
            print("已儲存股票清單")
            fp1.close()
        elif s0 =="2":
            cc=1
            while (cc==1):
                Saving=[]
                fp1 = open(file_path,'r')
                reader=csv.reader(fp1)        
                for row in reader:
                    Saving.append(row)
                fp1.close()
                for i in range(len(Saving)):
                    print("股票清單"+str(i+1)+":")
                    print(Saving[i])          
                dd=1
                while (dd==1):
                    s3=input("請輸入要刪除的股票清單號碼 (或輸入[0]結束刪除): ")
                    if s3 in [str(i) for i in range(1,len(Saving)+1)]:
                        ii=int(s3)-1
                        del Saving[ii]
                        fp2=open(file_path,'w',newline='')
                        writer=csv.writer(fp2)
                        for row in Saving:
                            writer.writerow(row)
                        fp2.close()
                        dd=0
                    elif s3=="0":
                        dd=0
                        cc=0
                    else: print("輸入號碼錯誤")
        elif s0 =="3":
            Saving=[]
            List_NO=[]
            fp1 = open(file_path,'r')
            reader=csv.reader(fp1)        
            for row in reader:
                Saving.append(row)
            fp1.close()
            for i in range(len(Saving)):
                print("股票清單"+str(i+1)+":")
                print(Saving[i])
            times=0
            cc=1
            while (cc==1):
                if times==0:
                    s3=input("請輸入要加入的股票清單號碼: ")
                    if s3 in [str(i) for i in range(1,len(Saving)+1)]:
                        ii=int(s3)-1
                        List_NO.extend(Saving[ii])
                        print("目前加入的股票清單:")
                        print(List_NO)
                        times=1
                    else: print("輸入號碼錯誤")
                else:
                    s3=input("請輸入要加入的股票清單號碼 (或輸入[0]開始篩選): ")
                    if s3 in [str(i) for i in range(1,len(Saving)+1)]:
                        ii=int(s3)-1
                        List_NO.extend(Saving[ii])
                        print("目前加入的股票清單:")
                        print(List_NO)
                        times+=1
                    elif s3=="0":
                        cc=0
                    else: print("輸入號碼錯誤")                    
            bb=0
            aa=0
        elif s0 =="4": 
            List_NO=Stock_input()
            bb=0
            aa=0
        elif s0 =="5":
            bb=0
            aa=1
        else:
            print("輸入失敗")
        
    return aa,List_NO
   

def Soup_to_note(string1,string2,soup):
    filename="{0}_{1}.txt".format(string1,string2)
    prettysoup=soup.prettify()
    fp=open(filename,"w",encoding="utf8")
    fp.write(prettysoup)
    print("將SOUP寫入檔案",filename)
    fp.close()

#----------------------------------------------------------------------

def Main_stock():
    
    print("\n\n******************[選股程式]*****************")
    print("*********************************************")
    
    aa=1
    while(aa==1):       
        print("\n請選擇股票清單: ")
        print("[1] 作者自選定存股清單")
        print("[2] 市值排名前150之股票清單")
        print("[3] 市值排名前300之股票清單")
        print("[4] 自訂股票清單")
        print("(或輸入[5]更新所有內建資料庫數據)")
        print("(或輸入[q]結束程式)")
        bb=1
        while(bb==1):        
            choice=input("請輸入[1~5]或[q]: ")
            if choice=="1":
                List_NO=List_all()
                bb=0
                aa=0
            elif choice=="2": 
                List_NO=["市值排名前150之股票"] 
                bb=0
                aa=0
            elif choice=="3":
                List_NO=["市值排名前300之股票清單"]
                bb=0
                aa=0
            elif choice=="4":
                bb=0
                aa,List_NO=Choice4()
            elif choice=="5":    
                yes=input("此更新可能會耗上幾個小時，若確定請輸入[y]，或輸入[任意鍵]重新選擇: ")
                if yes=="y": 
                    bb=0
                    aa=0
                else: bb=0
            elif choice=="q":
                bb=0
                aa=0
            else: 
                print("輸入錯誤")
                bb=0


    
    if choice in ["1","2","3","4"]:
        
        print("\n最初股票清單:",List_NO)
        print("\n*****************************************************")
        print("\n篩選條件(a):")
        print("今年目前累計的EPS 大於等於 過去(_)年平均同期累計的EPS")
        print("\n篩選條件(b):")
        print("近(_)年EPS的變異係數小於(_)")
        print("\n篩選條件(c):")   
        print("最新收盤價 小於 (_)年均線")
        print("\n篩選條件(d):")
        print("近(_)年股價的變異係數小於(_)")
        print("\n篩選條件(e):")
        print("過去(_)年ROE 平均大於(_)% ")
        print("\n篩選條件(f):")
        print("過去(_)年自由現金流 平均大於0 ") 
        print("\n*****************************************************")       
        print("請選擇所要的篩選條件,並且排序")
        print("(提示:順序只影響篩選股票之過程，不影響最終篩選結果)")
    
        eng=["a","b","c","d","e","f"]
        cond1,cond6=0,0
        cond2,cond3,cond4,cond5=[],[],[],[]
        priority=[]
        Q=False
        for i in range(1,7):
            print("\n請選擇第"+str(i)+"順位篩選條件:")
            if i==1:
                while True:
                    s0=input("請輸入[a~f]: ")
                    if s0 in eng :
                        print("第"+str(i)+"順位篩選條件:",s0)
                        priority.append(s0)
                        eng.remove(s0)
                        break
                    else: print("輸入失敗")
            else:
                while True:
                    s0=input("請輸入[a~f], 或輸入[0]不再選擇篩選條件: ")
                    if s0 in eng :
                        print("第"+str(i)+"順位篩選條件:",s0)
                        priority.append(s0)
                        eng.remove(s0)
                        break
                    elif s0=="0": break
                    else: print("輸入失敗")        
            if s0=="0": break  
        
        print("\n*******************************")   
        for I in priority:
        
            if I=="a" :
                bb=1
                while(bb==1):
                    print("\n選股條件(a):")
                    print("今年目前累計的EPS 大於等於 過去(_)年平均同期累計的EPS")
                    s1=input("請輸入[1~10]: ")
                    if s1 in [str(i) for i in range(1,11)]:
                        print("\n選股條件(a):")
                        print("今年目前累計的EPS 大於等於 過去"+s1+"年平均同期累計的EPS")
                        cond1=int(s1)
                        bb=2
                    else:
                        print("輸入失敗")

            if I=="b" :
                bb=1
                while(bb==1):
                    print("\n篩選條件(b):")
                    print("近(_)年EPS的變異係數小於(_)")
                    print("(提示:)") 
                    print("(篩選穩定獲利的公司，可先嘗試設定近[5]年 變異係數小於[0.16])")
                    print("(但仍需視實際情況再調整變異係數)")
                    print("(變異係數較大者，可能屬於成長型或者獲利較不穩定的公司)")
                    s21=input("請輸入[1~10]年: ")
                    if s21 in [str(i) for i in range(1,11)]:
                        while True:
                            print("\n篩選條件(b):")
                            print("近"+s21+"年EPS的變異係數小於(_)")
                            s22=input("請輸入[0~3]: ")
                            try:
                                aa=float(s22)
                                print(aa)
                                if aa>0 and aa<=3:
                                    break
                                else:
                                    print("數值超過範圍")
                            except ValueError:
                                print("輸入失敗")
                                       
                        print("\n選股條件(b):")
                        print("近"+s21+"年EPS的變異係數小於"+s22)
                        cond2=[int(s21),float(s22)]
                        bb=2 
                    else: print("輸入失敗")
                            
            if I=="c" :            
                bb=1
                times=0
                while (bb==1):        
                    print("\n選股條件(c):")   
                    print("最新收盤價 小於 (_)年均線")
                    if times==0:
                        s3=input("請輸入[1~5]: ")
                        if s3 in [str(i) for i in range(1,6)]:
                            cond3.append(int(s3))
                            times=1
                        else:
                            print("輸入失敗")           
                    else:
                        s3=input("請輸入[1~5], 或者輸入[0]結束: ")
                        if s3 in [str(i) for i in range(1,6)]:
                            if int(s3) in cond3:
                                print("輸入條件重複")
                            else:
                                cond3.append(int(s3))
                                times+=1
                        elif s3 =="0":
                            bb=2
                        else:
                            print("輸入失敗")               
                    print("\n選股條件(c):")
                    for yr in cond3: 
                        print("最新收盤價 小於 "+str(yr)+"年均線")

            if I=="d" :
                bb=1
                while(bb==1):
                    print("\n篩選條件(d):")
                    print("近(_)年股價的變異係數小於(_)")
                    print("(提示:)") 
                    print("(篩選股價穩定的公司，可先嘗試設定近[5]年 變異係數小於[0.15])")
                    print("(但仍需視實際情況再調整變異係數)")
                    print("(變異係數較大者，可能屬於成長型或者股價起伏較大的公司)")
                    s41=input("請輸入[1~5]年: ")
                    if s41 in [str(i) for i in range(1,6)]:
                        while True:
                            print("\n篩選條件(d):")
                            print("近"+s41+"年股價的變異係數小於(_)")
                            s42=input("請輸入[0~3]: ")
                            try:
                                aa=float(s42)
                                print(aa)
                                if aa>0 and aa<=3:
                                    break
                                else:
                                    print("數值超過範圍")
                            except ValueError:
                                print("輸入失敗")

                        print("\n選股條件(d):")
                        print("近"+s41+"年E股價的變異係數小於"+s42)
                        cond4=[int(s41),float(s42)]
                        bb=2                       
                    else: print("輸入失敗")
                    
            if I=="e" :
                bb=1
                while(bb==1):
                    print("\n選股條件(e):")
                    print("過去(_)年ROE 平均大於(_)% ")
                    print("(提示:)")
                    print("(均標可設定 [5]年[10]%) ")
                    print("(高標可設定 [5]年[15]%) ")
                    s51=input("請輸入[1~10]年: ")
                    if s51 in [str(i) for i in range(1,11)]:
                        print("過去"+s51+"年ROE 平均大於()%")
                        s52=input("請輸入[0~50]% :")
                        if s52 in [str(i) for i in range(1,51)]:
                            print("\n選股條件(e):")
                            print("過去"+s51+"年ROE 平均大於"+s52+"%")
                            cond5=[int(s51),int(s52)]
                            bb=2
                        else:
                            print("輸入失敗")
                    else:
                        print("輸入失敗")   

            if I=="f" :               
                bb=1
                while(bb==1):
                    print("\n選股條件(f):")
                    print("過去(_)年自由現金流 平均大於0 ")
                    s6=input("請輸入[1~10]: ")
                    if s6 in [str(i) for i in range(1,11)]:
                        print("\n選股條件(f):")
                        print("過去"+s6+"年自由現金流 平均大於0 ")
                        cond6=int(s6)
                        bb=2
                    else:
                        print("輸入失敗")    
        
        Condition=[True,cond1,cond2,cond3,cond4,cond5,cond6]
#        print("Condition",Condition)         
        print("\n*****************************************************") 
                
        print("\n最初股票清單:",List_NO)
        fp = open("Result.txt","w",encoding="utf8")
        fp.write("******************選股程式******************\n")
        fp.write("\n最初選股清單:\n")    
        fp.write(str(List_NO))

        times=1
        for I in priority:       
            if I=="a" :
                print("\n選股條件順位"+str(times)+" : ")
                print("今年目前累計的EPS 大於等於 過去"+str(cond1)+"年平均同期累計的EPS")
                fp.write("\n選股條件順位"+str(times)+" : ")
                fp.write("今年目前累計的EPS 大於等於 過去"+str(cond1)+"年平均同期累計的EPS")
            elif I=="b" :
                print("\n選股條件順位"+str(times)+" : ")
                print("近"+s21+"年EPS的變異係數小於"+s22)
                fp.write("\n選股條件順位"+str(times)+" : ")
                fp.write("近"+s21+"年EPS的變異係數小於"+s22)
            elif I=="c" :
                print("\n選股條件順位"+str(times)+" : ")
                for yr in cond3: 
                    print("最新收盤價小於"+str(yr)+"年均線")
                fp.write("\n選股條件順位"+str(times)+" : ")
                for yr in cond3: 
                    fp.write("最新收盤價小於"+str(yr)+"年均線  ")
            elif I=="d" :
                print("\n選股條件順位"+str(times)+" : ")
                print("近"+s41+"年股價的變異係數小於"+s42)
                fp.write("\n選股條件順位"+str(times)+" : ")
                fp.write("近"+s41+"年股價的變異係數小於"+s42)
            elif I=="e" :
                print("\n選股條件順位"+str(times)+" : ")
                print("過去"+s51+"年ROE 平均大於"+s52+"%")
                fp.write("\n選股條件順位"+str(times)+" : ")
                fp.write("過去"+s51+"年ROE 平均大於"+s52+"%")
            elif I=="f" :
                print("\n選股條件順位"+str(times)+" : ")
                print("過去"+s6+"年自由現金流 平均大於0 ")
                fp.write("\n選股條件順位"+str(times)+" : ")
                fp.write("過去"+s6+"年自由現金流 平均大於0 ")
            times+=1

        fp.close()        
        print("\n*****************************************************")    
    
        start=input("\n請按任意鍵開始: ")  

        if choice=="2":       
            List_NO=Read_list_300("150")            
        elif choice=="3":
            List_NO=Read_list_300("300") 
        
    elif choice=="5":    
        List_NO=List_all()
        Get_list_300("300")
        List_300=Read_list_300("300")
        List_NO.extend(List_300)
        #Get_stock_name()
        Condition=[False,5,[2,0.3],[1],[2,0.3],[5,15],5]
        priority=["a","b","c","e","f"]
        Q=False

    elif choice=="q":    
        List_NO=[]
        Condition=[False,5,[2,0.3],[1],[2,0.3],[5,15],5]
        priority=[]
        Q=True
        
    return List_NO,Condition,priority,Q

#------------------------------------------------------------

def End_stock(cond0,list_output):
    
    if cond0:        
        print("\n最終符合條件的股票清單:")
        fp=open("Result.txt","a",encoding="utf8")
        fp.write("\n\n最終符合條件的股票清單:\n\n")
        file_path="json/other/stock_name.json"
        if os.path.exists(file_path):
            with open(file_path,'r') as fp1:
                Stock_name=json.load(fp1)
            
            length=len(list_output)
            for i in [j for j in range(length-3) if j%3==0] :
                s0=str(list_output[i])
                s1=str(list_output[i+1])
                s2=str(list_output[i+2])
                if (s0 in Stock_name) and (s1 in Stock_name) and (s2 in Stock_name): 
                    print("%6s%6s" %( "("+s0+")",Stock_name[s0] ) ,end="        " )
                    print("%6s%6s" %( "("+s1+")",Stock_name[s1] ) ,end="        " )
                    print("%6s%6s" %( "("+s2+")",Stock_name[s2] ) )
                    fp.write("("+s0+") "+Stock_name[s0]+"\n")
                    fp.write("("+s1+") "+Stock_name[s1]+"\n")
                    fp.write("("+s2+") "+Stock_name[s2]+"\n")
                else:
                    for ss in [s0,s1,s2]:
                        if ss in Stock_name:
                            print("%6s%6s" %( "("+ss+")",Stock_name[ss] ) )
                            fp.write("("+ss+") "+Stock_name[ss]+"\n")
                        else:
                            print("%6s" %ss)
                            fp.write("("+ss+")\n")

            if length%3==0:                       #剩下的最後幾個股票
                if length==0: length0=0
                else        : length0=3
            else:
                length0=length%3
            for i in range(1,length0+1):
                ss=str(list_output[-i])
                if ss in Stock_name:
                    print("%6s%6s" %( "("+ss+")",Stock_name[ss] ) ,end="        " )
                    fp.write("("+ss+") "+Stock_name[ss]+"\n")                
                else:
                    print("%6s" %ss)
                    fp.write("("+ss+")\n")

        else:
            print(list_output)
            with open("Result.txt","a",encoding="utf8") as fp:
                fp.write("\n"+str(list_output)+"\n")
        fp.close()

    else: print("\n已更新所有內建資料庫數據") 

    choice=input("\n\n請按任意鍵回到開始目錄，或者輸入[q]結束程式: ") 
    if choice=="q":exe=0
    else: exe=1
    
    return exe
    
#-----------------------------------------------------------

if __name__=="__main__":

#    List_NO=Read_list_300("300")
    List_NO,Condition,priority,Q = Main_stock()
#    Get_stock_name()
#    cond0=True
#    list_output=[2412,3501,4305,4736,5007,5487,5706,6146,8210]
#    exe=End_stock(cond0,list_output)

        
        
        
        
        

