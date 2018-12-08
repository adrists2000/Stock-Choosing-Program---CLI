
import os
import csv  
import json
import Stock


def Decide_newest_day():
    yy=Stock.Now()[0]
    mm=Stock.Now()[1] 
#    print("用2412來查詢最近收盤日")
    url=Generate_URL_price(yy,mm,"2412")
    soup,option=Option1(Stock.Get_soup(url,310,0.1))    
    tag_tr_list=soup.select("tbody tr")
    if tag_tr_list != []:
        tr = tag_tr_list[-1]
        tag_td_list=tr.select("td")
        day=tag_td_list[0].string
    else:
        url=Generate_URL_price(yy,mm-1,"2412")
        soup,option=Option1(Stock.Get_soup(url,310,0.1))    
        tag_tr_list=soup.select("tbody tr")
        tr = tag_tr_list[-1]
        tag_td_list=tr.select("td")
        day=tag_td_list[0].string
        
    newest=day
    print("最近一日收盤日: ",newest)
    return newest


def Stockname():
    global Stock_name
    file_path0="json/other/stock_name.json"
    fp0= open(file_path0,'r')
    Stock_name=json.load(fp0)
    fp0.close()  


def Decide_date_price(input_no,newest):
    
    print("\n*********************************")   
    fp=open("Result.txt","a",encoding="utf8")
    
    str_no=str(input_no)
    if str_no in Stock_name:
        print("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]")   
        fp.write("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]\n")
    else:
        print("\n股票: ["+str_no+"]")   
        fp.write("\n股票: ["+str_no+"]\n")       
    fp.close()

    old_days=[]
    file_path="csv/"+ str_no + "_price.csv"
    if not os.path.exists(file_path):                # 輸入計算起始日期  視情況!!
        choice=0
        input_year=2013
        input_month=9
        end="102/09/00"
    else:
        fp = open(file_path,'r')
        reader=csv.reader(fp)        
        for row in reader:
            old_days.append(row)
        fp.close()

        if old_days==[]:
            choice=0
            input_year=2013
            input_month=9
            end="102/09/00"  
            print("原本CSV檔為空白檔案")
        else:
            end_all=old_days[-1]
#            print("原本CSV檔的最後一行:",end_all)
            if end_all==[] :
                choice=0
                input_year=2013
                input_month=9
                end="102/09/00"    
            else:
                end=end_all[0]
                if end != newest:                
                    choice=1
                    str_y=end[0:3]
                    str_m=end[4:6]
                    int_y=int(str_y)
                    int_m=int(str_m)
                    print("CSV檔需要再擷取資料更新")             
                    input_year=int_y+1911
                    input_month=int_m
                else:
                    choice=2
#                    print("CSV檔已為最新資料") 
                    input_year=2100           
                    input_month=12
                
#    print("CHOICE=",choice)
    return input_year,input_month,old_days,end,choice
            

def Decide_exist_price(input_no):
    decide_12={}
    str_no=str(input_no)
    file_path="json/other/decide_12.json"
    if os.path.exists(file_path):
        fp1 = open(file_path,'r') 
        decide_12=json.load(fp1)
        fp1.close()
        if str_no in decide_12:
            option=decide_12[str_no]
        else:
            yy=Stock.Now()[0]
            mm=Stock.Now()[1] 
            url=Generate_URL_price(yy,mm,input_no)
            soup,option=Option1(Stock.Get_soup(url,310,3.3))
            if option==2:
                url=Generate_URL_price2(yy,mm,input_no)
                soup,option=Option2(Stock.Get_soup(url,310,3.3))  
    else:
        yy=Stock.Now()[0]
        mm=Stock.Now()[1] 
        url=Generate_URL_price(yy,mm,input_no)
        soup,option=Option1(Stock.Get_soup(url,310,3.3))
        if option==2:
            url=Generate_URL_price2(yy,mm,input_no)
            soup,option=Option2(Stock.Get_soup(url,310,3.3))        
    
    decide_12[str_no]=option
#    print("OPTION=",option)
    fp1=open(file_path,'w')
    json.dump(decide_12,fp1)
    fp1.close()    
    return option
    
    
def Generate_URL_price(year,month,input_no):
    str_year=str(year)
    if month<10:
        str_month="0"+str(month)
    else:
        str_month=str(month)
    input_date=str_year+str_month+"01"  
    print("\n日期=",input_date)
    url_0="http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={0}&stockNo={1}"
    url=url_0.format(input_date,str(input_no))
#    print("URL=",url)
    return url
            

def Generate_URL_price2(year,month,input_no):
    str_year=str(year-1911)
    if month<10:
        str_month="0"+str(month)
    else:
        str_month=str(month)
    input_date=str_year+"/"+str_month  
    print("\n日期=",input_date)
    url_0="http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_print.php?l=zh-tw&d={0}&stkno={1}&s=0,asc,0"
    url=url_0.format(input_date,str(input_no))
#    print("URL=",url)
    return url


def Option_fixed(soup):
    tag_tr_list=soup.select("tbody tr")
    if tag_tr_list==[]: 
        print("此日期尚無資料")
        skip=1
    else: skip=0
    return soup,skip

    
def Option1(soup):  
    tag_tr_list=soup.select("tbody tr")
    option=1
    if tag_tr_list==[]: 
        print("改查詢上櫃公司")
        option=2
    else: print("此股票屬於上市公司") 
    return soup,option


def Option2(soup):
    tag_tr_list=soup.select("tbody tr")
    option=2
    if tag_tr_list==[]: 
        print("上市上櫃公司皆查無資料")
        option=3
    else: print("此股票屬於上櫃公司")
    return soup,option

    
def Scrap_data_price(input_year,input_month,end,choice,soup):
    
    int_y=int(end[0:3])
    int_m=int(end[4:6]) 
    int_d=int(end[7:9])
    new_data=[]
    tag_tr_list=soup.select("tbody tr")
    if choice==1 and ( (input_year-1911)==int_y and input_month==int_m ):
        for tr in tag_tr_list:
            tag_td_list=tr.select("td")
            small_list=[]
            date=tag_td_list[0].string
            price=tag_td_list[6].string
            day=date[7:9]
            if int(day)>int_d:
                small_list.append(date)
                small_list.append(price)
                new_data.append(small_list)
    else :                                                
        for tr in tag_tr_list:
            tag_td_list=tr.select("td")
            small_list=[]
            small_list.append(tag_td_list[0].string)
            small_list.append(tag_td_list[6].string)
            new_data.append(small_list)
    print("  日期         收盤價")
    for list in new_data:
        print(list)
    return new_data


def Save_new_days(input_no,new_days):
    file_path="csv/"+str(input_no) + "_price.csv"     
    fp = open(file_path,'a',newline='')
    writer=csv.writer(fp)
    for small_list in new_days:
        writer.writerow(small_list)
    fp.close()        


def Compare_MA_price(input_no,old_days,new_days,cond3):

    large_list=[]
    large_list.extend(old_days)
    large_list.extend(new_days)
#    print("\n所有日期之收盤價")
#    print(large_list)  
#    print("\n資料總天數=",len(large_list))
    
    cond3.sort()
    day_list,count_list,sum_list=[],[],[]
    aa=1
    for yy in cond3:
        count=0 
        sum_a=0
        bb=240*yy+1
        if (yy*240) > len(large_list):
            bb=len(large_list)+1
        for i in range(aa,bb):
            str0=large_list[-i][1]
            if (str0 == "--"):
                count+=1
            elif not str0.isdigit():
                list0=str0.split(",")
                str1="".join(list0)
                sum_a=sum_a+float(str1)
            else:
                sum_a=sum_a+float(str0)
        day_list.append((bb-1))
        count_list.append(count)
        sum_list.append(sum_a)
        aa=bb
    
    for i in range(1,240):
        str0=large_list[-i][1]
        if str0 != "--":
            if str0.isdigit():                
                newest=float(str0)
            else:
                list0=str0.split(",")
                str1="".join(list0)
                newest=float(str1)
            break
             
    fp=open("Result.txt","a",encoding="utf8")
    summation=0
    miss=0 
    match=0
    for i in range(len(cond3)):
        summation += sum_list[i]
        miss += count_list[i]        
        ma=summation/float(day_list[i]-miss)      
        print("\n"+str(cond3[i])+"年均線計算:")
        print("無資料天數=",miss,", 實際計算天數=",(day_list[i]-miss) )#,"總和=",summation)
        print("移動平均線=",ma)
    
        fp.write(str(cond3[i])+"年移動平均線= "+str(ma)+"\n")
        if newest < ma:
            print("最新收盤價= "+str(newest)+" < "+str(cond3[i])+"年均線")
            fp.write("最新收盤價 ="+str(newest)+" < "+str(cond3[i])+"年均線\n")
            match+=1
        else:
            print("最新收盤價= "+str(newest)+" >= "+str(cond3[i])+"年均線")
            fp.write("最新收盤價= "+str(newest)+" >= "+str(cond3[i])+"年均線\n")

    fp.write("\n*************************************\n")
    fp.close()    
    select=0
    if match==len(cond3): select=1      
    return select


def Calculate_price(input_no,old_days,new_days,cond4):
    
    large_list=[]
    large_list.extend(old_days)
    large_list.extend(new_days) 
#    print("\n資料總天數=",len(large_list))
    
    yy=cond4[0]
    miss=0 
    sum_all=0 
    sum2_all=0
    if (yy*240) < len(large_list): 
        dd=240*yy+1           
    else: 
        dd=len(large_list)+1
        
    for i in range(1,dd):
        str0=large_list[-i][1]
        if (str0 == "--"):
            miss+=1
        elif not str0.isdigit():
            list0=str0.split(",")
            str1="".join(list0)
            sum_all += float(str1)
            sum2_all += pow(float(str1),2)
        else:
            sum_all += float(str0)
            sum2_all += pow(float(str0),2)
    
    select=0
    fp = open("Result.txt","a",encoding="utf8")
    if (dd-1-miss)==0:
        print("無法計算過去幾年股價的變異係數")
        fp.write("\n無法計算過去幾年股價的變異係數\n")
    else:
        avg = sum_all/float(dd-1-miss)
        var = ( sum2_all/float(dd-1-miss) ) - (avg*avg)
        dev = pow(var,0.5)
        coef = dev/avg
        print("計算總天數=",str(dd-1-miss))        
        fp.write("計算總天數= "+str(dd-1-miss))
        print("過去"+str(yy)+"年平均股價="+str(avg) )
        fp.write("\n過去"+str(yy)+"年平均股價="+str(avg))
#        print("sum2_all=",sum2_all)
#        print("sum2_all/float(dd-1-miss)=",sum2_all/float(dd-1-miss) )
#        print("變異數=",var)
        print("標準差=",dev)
        print("變異係數=",coef)
        fp.write("\n標準差="+str(dev)+"    變異係數= "+str(coef))        
        if coef < cond4[1]:
            print("變異係數小於"+str(cond4[1]) )
            fp.write("\n變異係數小於"+str(cond4[1])+"\n")
            select=1            
        else:
            print("變異係數大於"+str(cond4[1]) )
            fp.write("\n變異係數大於"+str(cond4[1])+"\n")  

    fp.write("\n*************************************\n")
    fp.close()        
    return select
     
#------------------------------------------------------------------------------    
       
def Main_price(LIST_NO,COND3,COND4,I):
    
    print("\n\n*******************[Main_price Program]*******************\n")
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n\n*******************[Main_price Program]*******************\n\n")

    NEWEST=Decide_newest_day() 
    Stockname()
    LIST_SELECT=[]    
    for INPUT_NO in LIST_NO:
        OPTION=168
        OLD_DAYS,NEW_DAYS=[],[]
        INPUT_YEAR,INPUT_MONTH,OLD_DAYS,END,CHOICE = Decide_date_price(INPUT_NO,NEWEST)
        if CHOICE!=2:                                     # 檔案尚未存在(CHOICE)=0, 檔案存在但非最新=1 ,最新=2
            OPTION=Decide_exist_price(INPUT_NO)    
            if OPTION!=3:                                 # 上市(OPTION)=1,上櫃=2, 皆無資料=3
                while( INPUT_YEAR <= Stock.Now()[0] ):
                    while(INPUT_MONTH<=12):
                        if( (INPUT_YEAR==Stock.Now()[0]) and (INPUT_MONTH==Stock.Now()[1]+1) ):    # 最新截止日期
                            break
                        if OPTION==1 :                                 
                            URL=Generate_URL_price(INPUT_YEAR,INPUT_MONTH,INPUT_NO)
                            SOUP,SKIP=Option_fixed(Stock.Get_soup(URL,310,3.3))
                        if OPTION==2 :                                   
                            URL=Generate_URL_price2(INPUT_YEAR,INPUT_MONTH,INPUT_NO)
                            SOUP,SKIP=Option_fixed(Stock.Get_soup(URL,310,3.3))    
                        #Soup_to_note(INPUT_NO,INPUT_DATE,SOUP)
                        if SKIP==0:
                            NEW_DATA=Scrap_data_price(INPUT_YEAR,INPUT_MONTH,END,CHOICE,SOUP)
                            NEW_DAYS.extend(NEW_DATA)

                        INPUT_MONTH+=1                
                    INPUT_YEAR+=1
                    INPUT_MONTH=1                    
                Save_new_days(INPUT_NO,NEW_DAYS) 

        if OPTION!=3:
                
            if I=="c":                             
                SELECT=Compare_MA_price(INPUT_NO,OLD_DAYS,NEW_DAYS,COND3)
                if (SELECT==1): LIST_SELECT.append(INPUT_NO)
            if I=="d":
                SELECT=Calculate_price(INPUT_NO,OLD_DAYS,NEW_DAYS,COND4)
                if (SELECT==1): LIST_SELECT.append(INPUT_NO)
                
    print("\n階段選股清單:")
    print(LIST_SELECT)
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n階段選股清單:\n"+str(LIST_SELECT)+"\n")
    
    return LIST_SELECT
   
#------------------------------------------------------------------------------

if __name__=="__main__":
    
    COND3=[5,3]
    COND4=[5,0.3]
    I="d"

#    LIST_NO=Stock.List_all()
    LIST_NO=Stock.Read_list_300("300") 
#    LIST_NO=[6677,1101,1102,1104]
    LIST_SELECT=Main_price(LIST_NO,COND3,COND4,I)



    


