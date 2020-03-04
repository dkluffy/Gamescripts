# Gamescripts

- 扩展方便的并发按键机器人；
- 个人练手项目，不是很规范；
- 这是我刷YYS的小脚本发展而来的[python2老版](https://github.com/dkluffy/Gamescripts/tree/old-python2)
- 这本质上只是一个模拟按键的东西，算不上外挂；
- 使用别过度；虽然用了很久没被封号(没有东西可以检测，难道对方要封锁PYTHON进程？)
- **如果是做端游的脚本，一定要用管理员运行，否则，不能发送点击指令给游戏窗口**

## 使用说明

`python main.py  --targets "bc_win2 bc_win1  bc_tz"`

使用快捷键 F12 ，可用停止脚本；

```python
--targets #目标，就是需要匹配的目标按钮等，图片名称，支持这些后缀vision.py/Validate_IMG_EXT = ["png","jpeg","jpg"] 
   目标名称的前两个字符用于关联相关动作
     devicebind.py/sda_map = {"bc":["mouse","click"],
               "kd":["keyboard","keyDown"],
                "None":["mouse","move"]}
--max_step=100 #count_point 的最大匹配次数
--count_point="bc_tz" #匹配到这个目标max_step+1
--imgsdir="yys1080p" #目标存放目录
(用GOOGLE  的python-fire实现的命令行，命令行参数可以任意变)


在devicebind.py/下添加相关映射，可用支持更多动作
devicebind.py/PC_bind = {
    "mouse":{"move":pag.moveTo,"click":pag.click},
    "keyboard":{}
}

#可以支持android模拟器/物理机(需要连接ADB)，需要额外两个实现 ADB抓图和发送命令，暂时未添加，以后会加入
devicebind.py/Andriod_bind = {}

```

## 开发备忘

- 目标：并发、分布式、扩展规则(计划支持YAML格式)
- 版本号说明:
  * 当前:v0.1a
  * 版本格式 [新增功能：0 - inf].[bug修复:0 - 99].[ab：a - 初版非稳定；b - 稳定]
  
### 并发支持

  * 目前支持多线程、协程、多线程程运行模式
  * 但是只有多线程、协程支持机器人统一管理；多进程由于通信比较复杂，统一管理还在开发中
  * 使用示例在`main.py` 和 `mian_ceshi.py`中
 
### 程序逻辑

   * `sensor --> robot -->executor(callbacks)`
   * `sensor`: 包装了抓图和匹配目标两个功能，用于获得目标坐标/当前状态
   * `executor`: 执行`robot`发来的命令；通过调用`ExecutorCallBack`实例实现统计、日志、通信等各种功能
   * 命令格式 `CMD = namedtuple("CMD",["device","action","code","status"],defaults=[None])`
   * `robot`: 负责执行`sensor`获得目标坐标/当前状态；通过`bind_status` 生成相应命令`CMD`，然调用`executor`执行`CMD`
   * 之所以把原来几行解决的问题搞OO这么繁琐，是为了支持分布式和可扩展
  
  ## 版本计划
  
  计划在下一个版本中加入：
  - SIFT算子： 增强应用环境（需配合ML中的聚类算法)
  - 分离多线程和多进程入口，添加完整使用方法
  - 有时间把YAML格式支持也做了
