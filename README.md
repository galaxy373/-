## ***一、介绍***

***\*工具\****：python+selenium自动化

***\*目的\****：爬取***\*安居客\****网站上天津20个区的所有小区相关数据

***\*网站链接\****：https://tianjin.anjuke.com/community/

***\*学习（selenium）\****：[原理与安装 - 白月黑羽 (byhy.net)](https://www.byhy.net/auto/selenium/01/)

***\*参考网站\****：[selenium爬取安居客北京租房_selenium 中国网络经纪人-CSDN博客](https://blog.csdn.net/qq_68809241/article/details/143452395?ops_request_misc=&request_id=&biz_id=102&utm_term=利用selenium爬取安居客&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-143452395.142^v101^control&spm=1018.2226.3001.4187)

***\*数据\****：共计9303条（约）小区的相关数据，包括小区的地区、名字、每平方米价格、特征、详细地址、总户数、竣工时间、所属商圈、停车位、物业费、停车费

 

## ***二、方式***

#### ***\*1.直接爬取\****

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps1.jpg) 

网页显示一共有20473个小区，但是每页有25个小区的信息，可以显示的信息一共只有50页，如图：

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps2.jpg) 

按照这种方式一共只能爬取1250个小区的相关数据，所以采取其他方式。

 

#### ***\*2.分区同时爬取\****

参考main.py文件。

可以分不同区进行爬取，因为每个区的数据在150-700不等，平均在500左右，也就是25页左右，这样就不会超过50页，于是就可以循环页数爬取所有数据。

对下面除了天津周边的20个区以此循环，然后在每个区进行页面循环，再对该页面的每个小区进行循环的数据提取。

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps3.jpg) 

问题——由于程序的不稳定性，所以可能出现在爬了一段时间之后程序被打断，然后需要重新等待资源的爬取，中断的调试不方便。

 

#### ***\*3.分区分别爬取\****

对这20个区的界面进行爬取。

 

## ***三、实现过程***（展示部分代码）

#### ***\*1.通用\****

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps4.jpg) 

初始化浏览器驱动器并打开网页。

 

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps5.jpg) 

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps6.jpg) 

信息的存储。

 

#### ***\*2.主界面信息\****

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps7.jpg) 

（主界面图）

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps8.jpg) 

通过元素的CSS定位元素。先将该界面的所有小区信息存到一个list中，然后进行遍历，依次提取小区的名字、价格、标签（特点）。

 

#### ***\*3.详细页面信息\****

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps9.jpg) 

（详细页面）

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps10.jpg) 

通过找到主界面的每一个小区链接按钮，点击之后进入小区的详细界面。然后对地点、竣工时间、总户数、停车位、物业费、停车费等信息进行定位并爬取。在储存到相应对象之后再返回主界面继续执行程序。

注意，这里似乎不需要 driver.switch_to.window()函数切换handle，因为没有打开新的窗口，只是主界面转为详情页面，所以driver还是操纵本窗口。但是遇到那种点击详情界面之后出现新界面的（例如CSDN），这种时候需要操控新界面的元素则需要用driver.switch_to.window()函数切换新界面的handle。

 

 

## ***四、存留的问题***

#### ***\*1.无头模式与登录\****

在selenium自动化中有一种无头浏览器模式，在此模式下不会弹出可见的窗口，可以节省系统资源，也不用等待网页渲染，可以大大节省时间。

![img](file:///C:\Users\Thinkpad\AppData\Local\Temp\ksohtml19776\wps11.jpg) 

但是问题在于这个安居客网站在每次用webdriver打开网页的时候都要求登录，可以扫码或者账号密码登录。如果利用无头模式，一直加载不出来，可能是因为卡在登录这个环节了，尝试了以下两种方式都不成功：

方法1——用无头模式，同时用selenium自带的截图函数，想将登录界面截图，同时sleep（20）秒，在此期间用手机扫码截屏的二维码。但是这种方式最后失败了，因为根本不会渲染网页，所以也不会出现二维码，所以就没有截图。

方法2——尝试用cookie跳过二维码和验证码的登录，但是最后不知道为啥运行不成功（可能后续还要学一下cookie的原理和用法）

方法3——先创建一个driver1对象，用于打开网页，driver1的设定中没有headless 参数，所以就没有隐藏网页。在执行完登录的代码之后，新创建了一个driver2对象，这个对象有headless参数，打算让driver2接替driver1的控制作用，继续执行对网页界面的操控。但是不知道为什么，也不能执行。

 

#### ***\*2.网络问题\****

需要找一个网络环境好的地方运行，因为要是网络不好，网页加载时间过长就容易中断程序的执行，需要重新执行代码。这反应出程序不够稳定，可以思考如何通过修改代码增加程序的稳定性。

 

#### ***\*3.网站有自带的反爬机制\****

在执行过程中，有时候会遇到人机验证，需要点击按钮；同时有时候会判定在爬虫，从而强制性禁止浏览网页。

对于第一种情况暂时的解决方式也是自己主动点击，然后重新启动程序，因为人机验证之后一段时间内不会出现人机验证；对于第二种情况，可以登录vpn切换IP地址之后（我用的是学校的VPN），再重新运行程序。

 
