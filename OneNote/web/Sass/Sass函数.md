---
title: Sass 函数
tags: [sass, 函数]
aliases: []
---

# Sass 函数

## 字符串函数

| 函数 | 说明 |
| --- | --- |
| `quote(string)` | 给字符串添加引号 |
| `str-index(string, substring)` | 返回 `substring` 在 `string` 中第一次出现的位置；未匹配返回 `null` |
| `str-insert(string, insert, index)` | 在 `string` 的 `index` 位置插入 `insert` |
| `str-length(string)` | 返回字符串的长度 |
| `str-slice(string, start, end)` | 截取子串，`start` / `end` 设置起止位置 |
| `to-lower-case(string)` | 转小写 |
| `to-upper-case(string)` | 转大写 |
| `unique-id()` | 返回无引号的随机字符串（仅保证单次 Sass 编译中唯一） |
| `unquote(string)` | 移除字符串的引号 |

## 数字函数

| 函数 | 说明 |
| --- | --- |
| `abs(number)` | 绝对值 |
| `ceil(number)` | 向上取整 |
| `comparable(num1, num2)` | 判断两个数是否可以比较 |
| `floor(number)` | 向下取整 |
| `max(number...)` | 最大值 |
| `min(number...)` | 最小值 |
| `percentage(number)` | 数字转百分比 |
| `random()` | 返回 0–1 之间的随机小数 |
| `random(number)` | 返回 1 到 `number` 之间的整数（含两端） |
| `round(number)` | 四舍五入取整 |

## 列表函数

Sass 列表是不可变的，每次操作返回新列表。**列表的起始索引为 1**，不是 0。

| 函数 | 说明 |
| --- | --- |
| `append(list, value, [separator])` | 向列表尾部追加元素，`separator` 可指定逗号或空格 |
| `index(list, value)` | 返回元素 `value` 的索引位置 |
| `is-bracketed(list)` | 判断列表是否使用中括号 |
| `join(list1, list2, [separator, bracketed])` | 合并两个列表 |
| `length(list)` | 列表长度 |
| `list-separator(list)` | 列表分隔符（空格或逗号） |
| `nth(list, n)` | 取第 `n` 项 |
| `set-nth(list, n, value)` | 设置第 `n` 项的值 |
| `zip(lists)` | 把多个列表按相同索引重组为多维列表 |

## 映射函数

Sass Map 同样不可变，每次操作返回新 Map。

| 函数 | 说明 |
| --- | --- |
| `map-get(map, key)` | 取 key 对应的 value（无则返回 `null`） |
| `map-has-key(map, key)` | 判断是否存在 key |
| `map-keys(map)` | 返回所有 key 组成的列表 |
| `map-merge(map1, map2)` | 合并两个 map |
| `map-remove(map, keys...)` | 移除指定 key |
| `map-values(map)` | 返回所有 value 组成的列表 |