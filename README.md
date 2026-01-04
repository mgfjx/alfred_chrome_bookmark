# Alfred-Chrome浏览器书签检索

> 使用Alfred开发的一款快速检索查找书签的workflow.
主要原理: 读取当前用户Chrome书签文件(~/Library/Application Support/Google/Chrome/Default/Bookmarks)中的json数据，通过python写入到本地数据库中，再编写workflow，通过Alfred进行检索。

#### 用法

##### 1. 添加书签
呼出Alfred，输入`reload`即可添加书签为sqlite数据库，并会提示书签个数。每次在浏览器新收藏书签后，需要重新`reload`一次才能被检索到。
![alt text](descImages/desc1.png)
![alt text](descImages/desc2.png)

##### 2. 检索书签
按`cmd+shift+J`即可启动workflow，输入关键字即可进行检索。
###### 全局检索
直接输入关键字或拼音即可进行全局检索。支持同时检索两个关键字：只需要关键字用空格隔开即可。
![alt text](descImages/desc3.png)

###### 检索某文件夹下的书签
以`#`开头的关键字为文件夹名称，空格后为需要检索的书签关键字
![alt text](descImages/desc4.png)

###### 检索书签标题
以`@`开头，关键字空格隔开可同时检索两个关键字
![alt text](descImages/desc5.png)

###### 检索书签url
以`%`开头，关键字空格隔开可同时检索两个关键字
![alt text](descImages/desc6.png)
