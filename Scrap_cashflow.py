
import os
import json 
import Stock 

def Check_json_cashflow(input_no):
    
    if Stock.Now()[1] >= 5:
        end_y=Stock.Now()[0]-1                       #視情況 此處設定每年5月作切換
    else: 
        end_y=Stock.Now()[0]-2                         #end_y=所需資料的最新一年
    season=Stock.Decide_season()
    if season=="Q4":
        str_sea=str(Stock.Now()[0]-1)[2:4]+season
    else:
        str_sea=str(Stock.Now()[0])[2:4]+season        #str_sea=所需資料的最新一季
        
    option=1
    dict_no={} 
    str_no=str(input_no)
    str1=str_no[0]+"xxx"      
    file_path="json/cashflow/"+ str1 + "_cashflow.json"    #      
    if os.path.exists(file_path):
        fp1 = open(file_path,'r') 
        dict_large=json.load(fp1)                
        if str_no in dict_large:
            if str(end_y) in dict_large[str_no]:   #設定最新一年!! 須確定  
                dict_no=dict_large[str_no]
                print("\n由原本JSON檔案讀取[" +str_no+ "]Cashflow資料成功(最新!)")
                option=0
            elif str_sea in dict_large[str_no]:
                print("\n["+str_no+"]的Cashflow資料可能尚未滿一年!")
                option=0
            else: print("\n原本JSON檔案中[" +str_no+ "]的Cashflow資料不是最新的")  #option=1 執行網路爬蟲
        else: print("\n"+str_no+"的Cashflow資料尚未在json檔案裡")              #option=1 執行網路爬蟲
    else: print("\n"+file_path+"檔案不存在")                        #option=1 執行網路爬蟲    
    print(dict_no)
    return option,dict_no,end_y 


def Generate_URL_cashflow(input_no):
    url_0="https://goodinfo.tw/StockInfo/StockCashFlow.asp?STOCK_ID={0}&RPT_CAT=M_YEAR" 
    url=url_0.format(str(input_no))
    print("由台灣股市資訊網擷取資料...")
    print("\n股票代號=",input_no)
    print("URL=",url)
    return url


def Delete_data_cashflow(no_list):
    for input_no in no_list:
        dict_large={}
        str1=str(input_no)[0]+"xxx"
        str_no=str(input_no)
        file_path="json/cashflow/"+ str1 +"_cashflow.json" 
        if os.path.exists(file_path):
            fp=open(file_path,'r') 
            dict_large=json.load(fp)
            fp.close()
            if str_no in dict_large:
                del dict_large[str_no]
                fp=open(file_path,'w')
                json.dump(dict_large,fp)
                fp.close()
                print("\n已刪除JSON檔案中"+str_no+"的自由現金流量資料")
            else:
                print("\nJSON檔案中沒有"+str_no+"的自由現金流量資料")
                
                
def Scrap_data_cashflow(input_no,soup,cond6):
    
    dict_large={}
    dict_small={}
    str1=str(input_no)[0]+"xxx"
    str_no=str(input_no)
    file_path="json/cashflow/"+ str1 + "_cashflow.json"
    if os.path.exists(file_path):
        with open(file_path,'r') as fp1: 
            dict_large=json.load(fp1)                           
    tag_test=soup.find(text="查無資料")          
    tag_div=soup.find(id="divDetail")
    if (tag_test != None) :
        print("台灣股市資訊網:查無此股票資料")        
    elif (tag_div != None):            
        print("\n--歷年每年自由現金流量(億)--")
        for i in range(12):                     #設定抓取12年資料 視情況!!
            string="row"+str(i)
            tag_tr=tag_div.find(id=string)
            if (tag_tr != None):
                tag_nobr_list=tag_tr.select("td nobr")
                str1=tag_nobr_list[0].string
                tag5=tag_nobr_list[-5]
                tag_a=tag5.find("a")
                if (tag_a != None):
                    str2=tag_a.string
                    if ( str2 != (None and "-") ):
                        dict_small[str1]=str2
                        print(" ",str1,"    ",str2)
                    else:
                        print(" ",str1,"     (無自由現金流量資料)")                      
                else:
                    print(" ",str1,"     (無自由現金流量資料)")        
            else:
                print("超出歷史年份資料範圍!")
        dict_large[str_no]=dict_small                 # 由於前面option=1,而option=0的情況已跳過
        with open(file_path,'w') as fp1: 
            json.dump(dict_large,fp1)        
        print("--------------------")
        print("寫入JSON檔成功")
    else:
        print("台灣股市資訊網:目前連線錯誤") 
         
    return dict_small    
   
    
def Determine_cashflow(input_no,dict_no,end_y,cond6):        
    
    select=0
    if dict_no!={}:
        fp = open("Result.txt","a",encoding="utf8")
        file_path0="json/other/stock_name.json"
        fp0= open(file_path0,'r')
        Stock_name=json.load(fp0)
        fp0.close()
        str_no=str(input_no)        
        if str_no in Stock_name:
            print("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]")
            fp.write("\n股票: ["+str_no+"] ["+Stock_name[str_no]+"]\n")
        else:
            print("\n股票號碼= "+str_no)
            fp.write("\n股票號碼= "+str_no)
        print("\n年份     自由現金流量")
        fp.write("\n年份     自由現金流量")
        miss=0
        sum_all=0
        for i in range(cond6):
            str1=str(end_y-i)
            if str1 in dict_no:
                str2=dict_no[str1]
                print(str1,"    ",str2)
                fp.write("\n"+str1+"     "+str2)
                if str2 != ("-" and "--") :
                    if not str2.isdigit():
                        list0=str2.split(",")
                        str22="".join(list0)
                        sum_all += float(str22)
                    else:
                        sum_all += float(str2)
                else: miss+=1
            else: miss+=1
        
        count=cond6-miss
        if count==0:
            print("\n無法計算過去幾年的自由現金流量")
            fp.write("\n無法計算過去幾年的自由現金流量")
        else:
            avg=sum_all/float(count)
            if avg > float(0):
                print("\n過去"+str(count)+"年的自由現金流量平均大於0 (無資料年數為"+str(miss)+"年)")
                fp.write("\n過去"+str(count)+"年的自由現金流量平均大於0 (無資料年數為"+str(miss)+"年)\n")
                select=1
            else:
                print("\n過去"+str(count)+"年的自由現金流量平均小於0 (無資料年數為"+str(miss)+"年)")
                fp.write("\n過去"+str(count)+"年的自由現金流量平均小於0 (無資料年數為"+str(miss)+"年)\n")

        print("\n---------------------------------------------")
        fp.write("\n---------------------------------------------\n")
        fp.close()        
    return select
        
#--------------------------------------------------------------------------------

def Main_cashflow(LIST_NO,COND6):
    
    print("\n\n***************[Main_Cashflow Program]***************\n")
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n\n***************[Main_Cashflow Program]***************\n\n") 
        
    LIST_SELECT=[]        
    for INPUT_NO in LIST_NO:
        OPTION,DICT_NO,END_Y=Check_json_cashflow(INPUT_NO)
        if OPTION==1:
            URL=Generate_URL_cashflow(INPUT_NO)
            SOUP=Stock.Get_soup(URL,310,3.5)
            DICT_NO=Scrap_data_cashflow(INPUT_NO,SOUP,COND6) 
        SELECT=Determine_cashflow(INPUT_NO,DICT_NO,END_Y,COND6)                   
        if (SELECT==1): LIST_SELECT.append(INPUT_NO)
        
    print("\n階段選股清單:")
    print(LIST_SELECT)
    with open("Result.txt","a",encoding="utf8") as fp:
        fp.write("\n階段選股清單:\n"+str(LIST_SELECT)+"\n")
        
    return LIST_SELECT

#------------------------------------------------------------------------

if __name__=="__main__":

    no_list=[1563,8341,6024]
#    Delete_data_cashflow(no_list)
    
#    LIST_NO=Stock.List_all()    
    LIST_NO=[1563,8341,6024,3711] 
    COND6=9
    LIST_SELECT=Main_cashflow(LIST_NO,COND6)









