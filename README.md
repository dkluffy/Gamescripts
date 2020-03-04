# Gamescripts

扩展方便的并发按键机器人

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


在devicebind.py/下添加相关映射，可用支持更多动作
devicebind.py/PC_bind = {
    "mouse":{"move":pag.moveTo,"click":pag.click},
    "keyboard":{}
}

#可以支持android模拟器/物理机(需要连接ADB)，需要额外两个实现 ADB抓图和发送命令，暂时未添加，以后会加入
devicebind.py/Andriod_bind = {}

```

## 开发备忘

- 目标：并发、分布式、扩展规则
- 目前实现了大部分功能
- 版本说明:
  * 当前:v0.1a
  * 版本格式 [大版本：0~inf].[新增功能/bug修复:0~99][ab：a - 初版非稳定；b - 稳定]
  
 - 并发支持：
  * 目前支持多线程、协程、多线程程运行模式
  * 但是只有多线程、协程支持机器人统一管理；多进程由于通信比较复杂，统一管理还在开发中
  * 使用示例在`main.py` 和 `mian_ceshi.py`中
 
 - 程序逻辑：
 sensor(抓图，并转换成命令
  
  ## 版本计划
  
  计划在下一个版本中加入：
  - SIFT算子： 增强应用环境（需配合ML中的聚类算法)
  - 分离多线程和多进程入口，添加完整使用方法
