# 手机system apk的提取代码

思路极其简单：

1. 罗列出所有system apk

>  adb shell pm list packages -f -s

2. 拉取apk

> adb pull {apk_path} \"{dest_path}\""