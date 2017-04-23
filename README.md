# 作業二-21點連線版
##實作功能
* 可五位玩家連線
* 莊家發牌
* 玩家選擇是否加牌
* 分數結算

##程式說明與截圖
首先是一位玩家及一個莊家的模擬狀況(1 server-1 client)
client端需輸入兩個參數 -- host,port
![](https://github.com/miyuiki/PythonHW02-BlackJack/blob/master/screenshot/%E6%93%B7%E5%8F%96%E9%81%B8%E5%8F%96%E5%8D%80%E5%9F%9F_001.jpg?raw=true)

以下模擬莊家與玩家間的輸贏狀況

![](https://github.com/miyuiki/PythonHW02-BlackJack/blob/master/screenshot/%E6%93%B7%E5%8F%96%E9%81%B8%E5%8F%96%E5%8D%80%E5%9F%9F_002.jpg?raw=true)

![](https://raw.githubusercontent.com/miyuiki/PythonHW02-BlackJack/master/screenshot/%E6%93%B7%E5%8F%96%E9%81%B8%E5%8F%96%E5%8D%80%E5%9F%9F_003.jpg)

![](https://raw.githubusercontent.com/miyuiki/PythonHW02-BlackJack/master/screenshot/%E6%93%B7%E5%8F%96%E9%81%B8%E5%8F%96%E5%8D%80%E5%9F%9F_004.jpg)

![](https://raw.githubusercontent.com/miyuiki/PythonHW02-BlackJack/master/screenshot/%E6%93%B7%E5%8F%96%E9%81%B8%E5%8F%96%E5%8D%80%E5%9F%9F_005.jpg)

以下是多個玩家連入server的狀況
第一個玩家決定不補牌後，會等待其他玩家決定
當所有玩家都決定不補牌後(或有人爆掉)，再輪到莊家補牌

![](https://raw.githubusercontent.com/miyuiki/PythonHW02-BlackJack/master/screenshot/%E5%B7%A5%E4%BD%9C%E5%8D%80%201_006.jpg)

另外根據21點規則，可當1點或是10點
當爆掉後則當成1點
再算點數部分由一個while迴圈來實現
```
point = point - 3 * kc - 2 * qc - jc + 9 * ac
    if ac > 0 and point > 21:
        cnt = ac
        while point > 21 and cnt != 0:
            point = point - 9
            cnt = cnt - 1

    return point


```


![](https://raw.githubusercontent.com/miyuiki/PythonHW02-BlackJack/master/screenshot/%E5%B7%A5%E4%BD%9C%E5%8D%80%201_007.jpg)```

