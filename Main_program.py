
import Stock
import Scrap_eps
import Scrap_eps2
import Scrap_price
import Scrap_roe
import Scrap_cashflow

EXE=1
while EXE==1:
    LIST_INPUT,COND,PRIORITY,Q = Stock.Main_stock()
    #LIST_INPUT=[1580,1593,2376,2455,2889,3563,4305,4736,5007,5487,5706,6146,8210,8446,9905,9937]   
    #COND=[True,5,[5,0.9],[1,5],[4,0.8],[6,4],6]
    #PRIORITY=["a","b","c","d","e","f"]   
    for I in PRIORITY:
        if   I==("a"):
            LIST_OUTPUT=Scrap_eps.Main_eps(LIST_INPUT,COND[1])
        elif I==("b"):
            LIST_OUTPUT=Scrap_eps2.Main_eps2(LIST_INPUT,COND[2]) 
        elif I=="c" or I=="d":
            LIST_OUTPUT=Scrap_price.Main_price(LIST_INPUT,COND[3],COND[4],I) 
        elif I=="e":        
            LIST_OUTPUT=Scrap_roe.Main_roe(LIST_INPUT,COND[5])
        elif I=="f":
            LIST_OUTPUT=Scrap_cashflow.Main_cashflow(LIST_INPUT,COND[6])
        if COND[0]:    
            LIST_INPUT=LIST_OUTPUT
    
    if Q: EXE=0
    else: EXE=Stock.End_stock(COND[0],LIST_OUTPUT)
        








