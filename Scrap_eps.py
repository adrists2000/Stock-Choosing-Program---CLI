
import os
import json 
import Stock 


def Check_json_eps(input_no):
    
    option=1
    dict_no={}
    season=Stock.Decide_season()
    if season=="Q4":
        str_sea=str(Stock.Now()[0]-1)+season
    else:
        str_sea=str(Stock.Now()[0])+season    
    str_no=str(input_no)    
    str1=str(input_no)[0:2]+"xx"
    file_path="json/eps/"+ str1 + "_eps.json"        
    if os.path.exists(file_path):
        fp1 = open(file_path,'r') 
        dict_large=json.load(fp1)                
        if str_no in dict_large:
            if str_sea in dict_large[str_no]:   #設定最新一季!!  
                dict_no=dict_large[str_no]
                print("\n由原本JSON檔案讀取[" +str_no+ "]EPS資料成功(最新!)")
                option=0
            else: print("\n原本JSON檔案中[" +str_no+ "]的EPS資料不是最新")  #option=1 執行網路爬蟲
        else: print("\n"+str_no+"資料尚未在json檔案裡")              #option=1 執行網路爬蟲
    else: print("\n"+file_path+"檔案不存在")                        #option=1 執行網路爬蟲    
#    print(dict_no)
    return option,dict_no   
 
           
def Generate_URL_eps(input_no):
    url_0="https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={0}&YEAR_PERIOD=9999&RPT_CAT=M_QUAR" 
    url=url_0.format(str(input_no))
    print("由台灣股市資訊網擷取資料...")
    print("\n股票代號=",input_no)
    print("URL=",url)
    return url


def Delete_data_eps(no_list):
    for input_no in no_list:
        dict_large={}
        str1=str(input_no)[0:2]+"xx"
        str_no=str(input_no)
        file_path="json/eps/"+ str1 + "_eps.json"
        if os.path.exists(file_path):
            fp=open(file_path,'r') 
            dict_large=json.load(fp)
            fp.close()
            if str_no in dict_large:
                del dict_large[str_no]
                fp=open(file_path,'w')
                json.dump(dict_large,fp)
                fp.close()
                print("\n已刪除JSON檔案中"+str_no+"的EPS資料")
            else:
                print("\nJSON檔案中沒有"+str_no+"的EPS資料")

            
def Scrap_data_eps(input_no,soup):
    
    dict_large={}
    dict_small={}
    str1=str(input_no)[0:2]+"xx"
    str_no=str(input_no)
    file_path="json/eps/"+ str1 + "_eps.json"
    if os.path.exists(file_path):
        with open(file_path,'r') as fp1: 
            dict_large=json.load(fp1)
#    del dict_large[xxxx]                         # 此處可以刪除特定資料                       
    tag_test=soup.find(text="查無資料")          
    tag_div=soup.find(id="divFinDetail")
    if (tag_test != None) :
        print("台灣股市資訊網:查無此股票資料")        
    elif (tag_div != None):            
        print("\n--歷年每季獲利(EPS)--")
        for i in range(4*12):                     #設定抓取12年資料
            string="row"+str(i)
            tag_tr=tag_div.find(id=string)
            if (tag_tr != None):
                tag_nobr_list=tag_tr.select("td nobr")
                str1=tag_nobr_list[0].string
                tag3=tag_nobr_list[-3]
                tag_a=tag3.find("a")
                if (tag_a != None):
                    str2=tag_a.string
                    if ( str2 != (None and "-") ):
                        dict_small[str1]=str2
                        print(" ",str1,"    ",str2)
                    else:
                        print(" ",str1,"     (無EPS資料)")
                else:
                    print(" ",str1,"     (無EPS資料)")                                       
            else:
                print("超出歷史年份資料範圍!")
        dict_large[str_no]=dict_small 
        with open(file_path,'w') as fp1: 
            json.dump(dict_large,fp1)        
        print("--------------------")
        print("寫入JSON檔成功")
    else:
        print("台灣股市資訊網:目前連線錯誤") 
         
    return dict_small


def Compare_eps(input_no,dict_no,cond1):        
    
    select=0
    if dict_no!={}:
        dic=dict_no 
        yy=Stock.Now()[0]
        mm=Stock.Now()[1]
        if mm>=5:  use_y=str(yy)       # 以5月作為分界 視情況!!
        else: use_y=str(yy-1)        
        on_off=[]
        for i in range(0,cond1+1):
            yy=int(use_y)-i
            strQ1=str(yy)+"Q1"
            strQ2=str(yy)+"Q2"
            strQ3=str(yy)+"Q3"
            strQ4=str(yy)+"Q4"
            on_of=[yy,0,0,0,0]
            if strQ1 in dic: 
                on_of[1]=1
                if strQ2 in dic: 
                    on_of[2]=1
                    if strQ3 in dic: 
                        on_of[3]=1
                        if strQ4 in dic:
                            on_of[4]=1
#            print(on_of)                    
            on_off.append(on_of)            
        num_q=on_off[0].index(0) -1
                   
        file_path0="json/other/stock_name.json"
        fp0= open(file_path0,'r')
        Stock_name=json.load(fp0)
        fp0.close()
        
        fp = open("Result.txt","a",encoding="utf8") 
        str_no=str(input_no)        
        if str_no in Stock_name:
            print("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]")
            fp.write("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]\n")
        else:
            print("\n股票號碼= "+str_no)
            fp.write("\n股票號碼= "+str_no)                
       
        sum_list=[]
        sum2=0
        for i in range(0,cond1+1):
            yy=int(use_y)-i
            sum1=0
            if on_off[i][num_q]==1:
                for j in range(1,num_q+1):
                    str0=str(yy)+"Q"+str(j) 
                    if dic[str0] != ("-" and "--") :
                        sum0=float(dic[str0])
                        sum1+=sum0
                print(str(yy)+"年前"+str(num_q)+"季累計EPS=",sum1)
                fp.write(str(yy)+"年前"+str(num_q)+"季累計EPS="+str(sum1)+"\n")

            sum_list.append(sum1)            
            sum2+=sum1            
        
        miss=sum_list.count(0)
        count=cond1-miss
        if count==0:
            avg=0
            print("無法計算過去同期累計的EPS")
            fp.write("無法計算過去同期累計的EPS\n")
        else:
            avg=(sum2-sum_list[0]) / float(count)
            print("miss=",miss,"count=",count)       
            print("過去"+str(count)+"年平均同期累計的EPS=",avg)
            fp.write("過去"+str(count)+"年平均同期累計的EPS= "+str(avg)+"\n")
            if sum_list[0]>=avg :
                print("今年目前累計的EPS >= 過去"+str(count)+"年平均同期累計的EPS")
                fp.write("今年目前累計的EPS >= 過去"+str(count)+"年平均同期累計的EPS\n")
                select=1
            else:
                print("今年目前累計的EPS < 過去"+str(count)+"年平均同期累計的EPS")
                fp.write("今年目前累計的EPS < 過去"+str(count)+"年平均同期累計的EPS\n")            

        fp.write("\n******************************************\n")   
        fp.close()
    print("\n**********************************************") 
    return select
    
#-------------------------------------------------------

def Main_eps(LIST_NO,COND1):
    
    print("\n\n***************[Main_EPS Program]***************\n")
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n\n***************[Main_EPS Program]***************\n\n")   
    
    LIST_SELECT=[]        
    for INPUT_NO in LIST_NO:
        OPTION,DICT_NO=Check_json_eps(INPUT_NO)
        if OPTION==1:
            URL=Generate_URL_eps(INPUT_NO)
            SOUP=Stock.Get_soup(URL,310,3.5)
            DICT_NO=Scrap_data_eps(INPUT_NO,SOUP) 
        SELECT=Compare_eps(INPUT_NO,DICT_NO,COND1)                   
        if (SELECT==1): LIST_SELECT.append(INPUT_NO)
        
    print("\n階段選股清單:")
    print(LIST_SELECT)
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n階段選股清單:\n"+str(LIST_SELECT)+"\n")
        
    return LIST_SELECT
        
#----------------------------------------------------------

if __name__=="__main__":

#    no_list=[8359]
#    Delete_data_eps(no_list)
    
    LIST_NO=Stock.List_all() 
#    LIST_NO=Stock.Read_list_300("300") 
    LIST_NO=[8359] 
    COND1=10
    LIST_SELECT=Main_eps(LIST_NO,COND1)

   


    
    
    
    
    
    


