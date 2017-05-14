okcoin_app 文档说明及问题

运行环境：python3.6
额外库：PyQt5 (pyqt5.6 anaconda自带)   websocket (https://github.com/websocket-client/websocket-client)

程序文件夹名：okcoin_app
1. 启动程序：main.py
2. REST：okcoin_rest.py (rest封装的调用接口) okcoin_rest_API.py (rest底层发送指令) http_MD5_util.py (http发送格式)
3. WEBSOCKET: okcoin_websocket.py (websocket封装的调用接口)
4. 数据处理： data_filter.py
5. UI：UI_ALL.ui (Qt Designer生成的UI界面布局）ui_app.py (由UI_ALL.ui生成的py文件） ui_methed.py (ui逻辑功能）

运行方法： python3 main.py

软件说明：
采集信息：
1. btc_cny (国内比特币) 最新行情
2. btc_cny 市场深度 深度为 0.01 显示最新40条信息
3. btc_cny 交易记录 显示最新40条信息
4. btc_cny K线数据 时间间隔 1分钟 显示最新40条K线数据

简要软件运行方式：
1. 启动软件
2. 点击“连接”按钮，建立websocket长连接，并发送4个采集数据的指令和接收数据
3. 将收到的数据使用 DataFilter类处理并存入采集队列。
4. UI界面有4个定时器，定时检查采集队列并提取需要显示的数据，更新界面。
5. 若定时器检查队列时发现数据间隔1秒以上未更新，则使用rest方式主动采集对应数据，并将数据处理加入采集队列。
6. 关闭UI窗口，断开 websocket 连接 ，停止定时器，退出程序。

遇到过的问题及解决：
1. 问题：websocket连接中的 ticker，depth数据只在数据变化时候发送，所以会出现较长时间（多秒）未发送数据，而导致需要频繁发送rest。
	解决：限制rest发送次数，减少无用rest发送。
2. 问题：由于websocket和rest发送是多线程。在ticker数据接收中，有时候rest的数据比websocket数据还要新，导致web的数据丢弃，而web的数据间隔超过1秒就要再发rest，导致一直发送rest数据。
	解决：修改检查rest发送的条件，改web数据超过1秒间隔，为显示更新数据的1秒间隔。
3. 问题：rest和websocket的数据格式大不相同。
	解决：编写 DataFilter类专门处理格式并统一格式。

程序不足：
1. 程序结构问题，一开始我对采集数据任务不明确，程序结构不好，不够通用，现在采集比特币的4种数据，没有做成通用结构，要再采集莱特币的话就需要改很多细节，而代码可重用的少。
2. 只做了数据采集及显示，没有做数据保存的内容。

应改善：
1. 要保存数据，应该再思考哪些数据需要保存，及保存数据的存储格式等内容。


