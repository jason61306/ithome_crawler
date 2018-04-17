# Scrapy for Ithome
攀附Ithome的Scrapy爬蟲。

## 環境
使用環境為python 2.7+

## 建置開發環境
### Python 環境
安裝Python套件
```python
    pip install -r requirements.txt
```

### SQL 環境
到sql_schema目錄，使用init.sql初始化SQL。
```bash
    $ mysql -u root -p crawler < init.sql
```

假如這個過程中有發生錯誤，請先進入SQL中並輸入指令：
```sql
    $ FLUSH PRIVILEGES;
```
然後再重新執行一次。

若要重設SQL，到sql_schema目錄，使用reset.sql刪除SQL。
```bash
    $ mysql -u root -p crawler < reset.sql
```


### ES 環境
到es_schema目錄，使用 init.py建置開發環境的elasticsearch。
```bash
    $ python init.py -d
```

若要重設es，到es_schema目錄，使用reset.py刪除建立的elasticsearch。
```bash
    $ python reset.py -d
```
## 執行
進入根目錄,執行下列命令啟動scrapy
```bash
    $ scrapy crawl ithome -a start=1 -a end=5 -a env=development
```

start,end為爬取頁數(例如範例為爬1-5頁)，
env為執行環境選擇(包含：development)，
此外start,end, env可不輸入，如下所示，如此所有頁面皆會爬取，並選擇執行環境為development。
```bash
    $ scrapy crawl ithome
```

### 相關套件
scrapy
elasticsearch
mysql-connector-python

## 說明文件
[Scrapy](https://scrapy.org/)

## 執行結果
![image](https://github.com/jason61306/ithome_crawler/blob/master/pic/ES.png)
![image](https://github.com/jason61306/ithome_crawler/blob/master/pic/SQL.png)
