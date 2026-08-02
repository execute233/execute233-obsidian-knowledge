---
title: echo
tags: [liunx, Shell脚本]
aliases: [echo]
---

# echo

格式输出对比见 [[liunx/Shell脚本/printf]];输出到文件涉及 [[liunx/Shell脚本/输入-输出重定向]]。

## 常用选项

- `-n` 不换行输出，如 `echo -n "114514"`
- `-e` 启用转义字符解释

## 输出到文件

```bash
# 输出保存到文件
echo "normal log" > log.log
# 追加输出到文件
echo "normal log" >> log.log
```