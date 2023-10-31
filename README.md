# map_IP_range

### 專案目的
工作地點中各單位的 IP 位址範圍每年可能會變動，因此需要將前一年份的 IP 與當年度的 IP 比對，以匹配每個 IP 變動前所屬單位

### 專案流程
1. 資料前處理: 將 IP 位址進行資料前處理  
   ![image](https://github.com/Clairechn/map_IP_range/assets/43264051/77007c00-fa80-46c8-b84a-e7ba788ca909)  
   將 IP 位址範圍的格式統一為 'IP 起始位址' 及 'IP 結束位址'  
   ![image](https://github.com/Clairechn/map_IP_range/assets/43264051/f22f176a-33e4-4dfc-bec1-2cae35adf046)  
2. 資料比對: 將前年的所有 IP 存為 nested dictionary 後比對
   (1) Nested dictionary 結構
       以上圖 IP 位址為例，nested dict = {'120.114.240':{'2':2}, '120.114.241':{'255':3}, '140.116.167':{'0':4, '15':5}}  
       - key: IP 位址的前 24 個位元  
       - value(sub-dict): sub-key 為 IP 起始位址的後 8 個位元，sub-value 為前年檔案的 row index  
   (2) 排序 Nested dictionary: 將各 sub-dict 以 sub-key 值由小到大排序  
   (3) 比對 IP  
       以當年 IP 位址的前 24 個位元比對 nested dict 的 key，若匹配則再用 IP 起始位址的後 8 個位元比對 value 的 sub-dict  
       找到比 IP 起始位址小的 IP 中，最大的那一筆 IP，並取它的 row index 以找到該筆資料  
