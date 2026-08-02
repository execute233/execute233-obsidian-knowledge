---
title: pandas
tags: [Python, pandas, DataFrame, 数据分析]
aliases: [Pandas]
---

# pandas

```python
import pandas as pd
```

## 数据结构和数据类型

DataFrame/Series 底层使用 [[numpy]] 数组。核心概念层级:

| 层级 | 类型 | 说明 |
| --- | --- | --- |
| DataFrame | | |
| | Series | |
| | 索引列 | 索引名,索引值;索引下标,行号 |
| | 数据列 | 列名;列值,具体数据 |

## Series 对象

类似于数组,由 index 和 value 两个数组组成。访问方式跟字典差不多。

### 创建 Series

```python
pd.Series()  # 一堆可选参数,一般第一个是数据
```

参数说明:

- `data` - 数据,可以是列表、数组、字典、标量值等
- `index` - 索引部分,用于对数据进行标记,默认是自增索引
- `dtype` - 数据类型
- `name` - Series 的名称,用于标识
- `copy` - 是否复制数据
- `fastpath` - 是否启用快速路径

### 常用方法

| 方法 | 作用 | 方法 | 作用 |
| --- | --- | --- | --- |
| `index` | 索引 | `values` | ndarray 数据 |
| `head(n)` | 前 n 行 | `tail(n)` | 后 n 行 |
| `dtype` | 数据类型 | `shape` | 形状(行数) |
| `describe()` | 统计描述 | `isnull()` | 元素是否全为 NaN |
| `notnull()` | 元素是否全为非 NaN | `unique()` | 去重 |
| `value_counts()` | 每个唯一值的出现次数 | `map(func)` | forEach |
| `apply(func)` | forEach | `astype(dtype)` | 转换为指定的类型 |
| `sort_values()` | 按值排序 | `sort_index()` | 索引进行排序 |
| `dropna()` | 删除缺失值(NaN) | `fillna(value)` | 填充缺失值 |
| `replace(to_replace, value)` | 替换指定的值 | `cumsum()` | 累计求和 |
| `cumprod()` | 累计乘积 | `shift(periods)` | 元素按指定的步数进行位移 |
| `rank()` | 排名 | `corr(other)` | 皮尔逊相关系数 |
| `cov(other)` | 协方差 | `to_list()` | 转 list |
| `to_frame()` | 转 DataFrame | `iloc[]` | 通过位置索引来选择数据 |
| `loc[]` | 通过标签索引来选择数据 | | |

## DataFrame 对象

![Exported image](_assets/pandas/pandas__11-51-45-0.png)

类似于二维数组或表格的对象,既有行索引,又有列索引。

- 行索引,表明不同行,横向索引,叫 index,0 轴,`axis=0`
- 列索引,表明不同列,纵向索引,叫 columns,1 轴,`axis=1`

### 创建 DataFrame

```python
pd.DataFrame()  # 创建对象,也一堆参数
```

参数说明:

- `data` - 数据
- `index` - 索引,就是下面第一列那个,一般自动生成
- `columns` - 字段名(列名)
- `dtype` - 数据类型
- `copy` - 是不是要复制原数据

创建对象的几个场景:

- 字典 + 列表实现

  |   | 语文 | 数学 | 英语 |
  | --- | --- | --- | --- |
  | 0 | 97 | 99 | 99 |
  | 1 | 95 | 92 | 95 |
  | 2 | 93 | 95 | 97 |

- 列表 + 元组实现
- 通过 numpy 实现

字典的 key 就是字段名,而其 value 是一列数据,比如 `data={"语文": [97, 95, 93], "数学": [99, 92, 95], "英语": [99, 95, 97]}`,其 DataFrame 就是上表。每个元组都是一行数据,字段名会自动生成,比如 `data = [(97, 99, 99), (95, 92, 95), (93, 95, 97)]` 等同于上表的数据。直接将 ndarray 作为 data 传入。

### 改名

```python
df.columns = 新的 columns
df.rename(index={指定索引: "指定值"}, inplace=True)  # 用于精准修改,inplace 确认是否要替换原来的
```

### 常用方法

| 方法 | 作用 | 方法 | 作用 |
| --- | --- | --- | --- |
| `head(n=5)` | 前 n 行数据 | `tail(n=5)` | 后 n 行数据 |
| `info()` | 简要信息 | `describe()` | 统计信息 |
| `shape` | 行列数 | `columns` | 所有列名 |
| `index` | 所有索引 | `dtypes` | 每列的数据类型 |
| `sort_values(by)` | 按指定列排序 | `sort_index()` | 按索引排序 |
| `dropna()` | 删除含 NaN 的行或列 | `fillna(value)` | 用指定值填充缺失值 |
| `isnull()` | 判断缺失值,返回 Bool 类型的 DataFrame | `notnull()` | 与左边相反 |
| `loc[]` | 按标签索引选择数据 | `iloc[]` | 按位置索引选择数据 |
| `at[]` | 访问单个元素 | `iat[]` | 访问单个元素 |
| `apply(func)` | 对每个元素应用一个函数 | `applymap(func)` | 同 apply |
| `groupby(by)` | 分组操作 | `pivot_table()` | 创建透视表 |
| `merge()` | 合并多个 DataFrame,类似 SQL 的 JOIN | `concat()` | 按行或列连接多个 DataFrame |
| `to_csv(), to_excel(), to_json()` | 导出 | `query()` | 用 SQL 风格查询 |
| `duplicated()` | 返回 Bool 的 DataFrame,指示每行是否重复 | `drop_duplicates()` | 删除重复的行 |
| `set_index()` | 设置指定的列为索引 | `reset_index()` | 重置索引 |
| `transpose()` | 转置(行列交换) | `drop()` | 删行 0 或列 1,用 axis 指定 |

## 数据类型

DataFrame 或 Series 中的类型有很多,包括:

- `object` - 字符串
- `int`, `float`, `bool`, `nan`
- `datetime` - 日期时间
- `timedelta` - 时间差
- `category` - 分类

## 基本数据操作

### 索引操作

先列后行(先写是哪个列,再是哪个行),如:

```python
df["time"]  # 获得名称为 time 的 Series 对象
df["time"]["count"]  # 先拿到名称为 time 的 Series 对象,然后砸到名为 count 的列,获取单元格内容
```

结合 loc 与 iloc:

```python
df.loc[行索引, 列名]
df.iloc[行号, 列索引]
```

也可以使用切部分数据操作:

```python
df.loc[行索引开始: 行索引结束, [指定的那些列名]]  # 用来挖出 DataFrame 的一小块区域,行两边都包
# 同样的,iloc 也可以这样做 [start: end, start: end],一样行两边都包,但都包左不包右
```

### 赋值操作

简单,直接 `=` 就行:

```python
df[列名] = xxx  # 直接对指定列所有数据赋同一个值
df[列名][行名] = xxx  # 指定的单元格赋值
```

### 排序操作

按索引排序 `df.sort_index`。基于一个值排序:

```python
df.sort_values(by=指定的列名, ascending=True)  # 按指定的列名升序排序
df.sort_values(by=[…], ascending=[…])  # 指定多个排序,遇到相同的交给后面继续排序
```

Series 排序:Series 也可以 `.sort_index` 或者 `.sort_values` 来排序。

## DataFrame 运算

### Series 对象

- `add()` 对该 Series 对象所有数据相加操作,等同于 `series + x`,需要用变量接收数据
- `sub()` 减法,乘除略
- `series 逻辑运算符 指定值` 返回一个新的 Series 对象,里面存储 bool 指示是否满足条件,塞 DF 里
- `isin([…])` 是否在某个值,相当于 `series == 值1 | series == 值2 | …`

### DataFrame 对象

```python
df[df[指定列名] 逻辑运算符 值]  # 筛选 DF 里面指定列中满足指定条件的所有行组成新的 DF
```

复杂多个条件逻辑判断需要 `()` 指定优先级。同样,可以用 query 函数写,如 `.query("列名 > xx & 列名 < xx")`, `query("列名 in [xxx]")`。

### 统计运算

```python
df.describe()  # 获得很多统计结果,count, mean, std, min, max 等
df.sum()  # 针对于每列求和,对 Series 引用就是对其里面的数据求和,下面几个函数一样
mean()  # 平均值
median()  # 中位数
cumsum()  # 逐个累计求和,返回 Series 或 DataFrame
```

### apply 自定义运算

```python
apply(func, axis=0)  # 默认 0 是列,1 是行
```

## 文件读取与存储

### CSV

```python
pd.read_csv()  # 从 CSV 文件读取数据并加载为 DataFrame
```

参数说明:

- `filepath_or_buffer` - 路径或文件对象
- `sep` - 分隔符
- `header` - 行标题
- `names` - 自定义列名
- `usecols` - 读取指定的列,可以是列名或列索引
- `dtype` - 数据类型
- `skiprows` - 跳过文件开头指定的行数,或传入行号列表
- `nrows` - 读取前 N 行
- `na_values` - 指定那些值应该视为缺失值
- `skipfooter` - 跳过文件结尾指定行数
- `encoding` - 文件编码格式

```python
DataFrame.to_csv()  # 将 DataFrame 写入到 CSV 文件
```

参数说明:

- `path_or_buffer` - 目标路径或文件对象
- `sep` - 分隔符
- `index` - 是否写入行索引
- `columns` - 指定列
- `header` - 是否写入列名
- `mode` - 写入模式,w 写 a 追加
- `encoding` - 编码
- `line_terminator` - 自定义行结束符
- `quotechar` - 用于引用的字符,默认为 `"`
- `date_format` - 自定义日期格式
- `doublequote` - 是否把包含引号的文本用双引号括起来

我们可以使用 drop 删除指定的行 0 或列 1,用 axis 指定,也可以用 columns 或 index 指定。

### Excel

```python
pd.read_excel(io)  # 读取 excel 文件,返回 DataFrame
```

参数说明:

- `sheet_name=0` - 指定要读取的工作表名称或索引。默认为 0,即第一个工作表。
- `header=0` - 指定用作列名的行。默认为 0,即第一行。
- `names=None` - 用于指定列名的列表。如果提供,将覆盖文件中的列名。
- `index_col=None` - 指定用作行索引的列。可以是列的名称或数字。
- `usecols=None` - 指定要读取的列。可以是列名的列表或列索引的列表。
- `dtype=None` - 指定列的数据类型。可以是字典格式,键为列名,值为数据类型。
- `engine=None` - 指定解析引擎。默认为 None,pandas 会自动选择。
- `converters=None` - 用于转换数据的函数字典。
- `true_values=None` - 指定应该被视为布尔值 True 的值。
- `false_values=None` - 指定应该被视为布尔值 False 的值。
- `skiprows=None` - 指定要跳过的行数或要跳过的行的列表
- `nrows=None` - 指定要读取的行数。
- `na_values=None` - 指定应该被视为缺失值的值。
- `keep_default_na=True` - 指定是否要将默认的缺失值(例如 NaN)解析为 NA。
- `na_filter=True` - 指定是否要将数据转换为 NA。
- `verbose=False` - 指定是否要输出详细的进度信息。
- `parse_dates=False` - 指定是否要解析日期。
- `date_parser=<no_default>` - 用于解析日期的函数。
- `date_format=None` - 指定日期的格式。
- `thousands=None` - 指定千位分隔符。
- `decimal='.'` - 指定小数点字符。
- `comment=None` - 指定注释字符。
- `skipfooter=0` - 指定要跳过的文件末尾的行数。
- `storage_options=None` - 用于云存储的参数字典。
- `dtype_backend=<no_default>` - 指定数据类型后端。
- `engine_kwargs=None` - 传递给引擎的额外参数字典。

```python
DataFrame.to_excel(io)  # 将 DataFrame 写入 Excel 文件
```

参数说明:

- `sheet_name='Sheet1'` - 指定写入的工作表名称,默认为 `'Sheet1'`。
- `na_rep=''` - 指定在 Excel 文件中表示缺失值(NaN)的字符串,默认为空字符串。
- `float_format=None` - 指定浮点数的格式。如果为 None,则使用 Excel 的默认格式。
- `columns=None` - 指定要写入的列。如果为 None,则写入所有列。
- `header=True` - 指定是否写入列名作为第一行。如果为 False,则不写入列名。
- `index=True` - 指定是否写入索引作为第一列。如果为 False,则不写入索引。
- `index_label=None` - 指定索引列的标签。如果为 None,则不写入索引标签。
- `startrow=0` - 指定开始写入的行号,默认从第 0 行开始。
- `startcol=0` - 指定开始写入的列号,默认从第 0 列开始。
- `engine=None` - 指定写入 Excel 文件时使用的引擎,默认为 None,pandas 会自动选择。
- `merge_cells=True` - 指定是否合并单元格。如果为 True,则合并具有相同值的单元格。
- `inf_rep='inf'` - 指定在 Excel 文件中表示无穷大值的字符串,默认为 `'inf'`。
- `freeze_panes=None` - 指定冻结窗格的位置。如果为 None,则不冻结窗格。
- `storage_options=None` - 用于云存储的参数字典。
- `engine_kwargs=None` - 传递给引擎的额外参数字典。

```python
pd.ExcelFile(path)  # 可以处理多个表单,并在不重新打开文件的情况下访问其中的数据
```

- `.sheet_name` - 返回文件中所有表单的名称列表
- `.parse(sheet_name)` - 解析指定表单并返回 DataFrame
- `.close()`

```python
pd.ExcelWriter(path)  # 可在一个 Excel 文件中写入多个工作表,并且可以更灵活地控制写入过程
```

参数说明:

- `engine` - 用于指定写入 Excel 文件的引擎。如果为 None,则 pandas 会自动选择一个可用的引擎(默认优先选择 openpyxl,如果不可用则选择其他可用引擎)。常见的引擎包括 `'openpyxl'`(用于 .xlsx 文件)、`'xlsxwriter'`(提供高级格式化和图表功能)、`'odf'`(用于 OpenDocument 格式如 .ods)等。
- `date_format` - 指定写入 Excel 文件中日期的格式字符串,例如 `"YYYY-MM-DD"`。
- `datetime_format` - 指定写入 Excel 文件中日期时间对象的格式字符串,例如 `"YYYY-MM-DD HH:MM:SS"`。
- `mode` - 默认为 `'w'`,表示写入模式。如果设置为 `'a'`,则表示追加模式,向现有文件中添加工作表(仅支持部分引擎,如 openpyxl)。
- `storage_options` - 这是一个可选参数,用于指定与存储后端连接的额外选项,例如认证信息、访问权限等,适用于写入远程存储(如 S3、GCS)。
- `if_sheet_exists` - 默认为 `'error'`,指定如果工作表已经存在时的行为。选项包括 `'error'`(抛出错误)、`'new'`(创建一个新工作表)、`'replace'`(替换现有工作表的内容)、`'overlay'`(在现有工作表上覆盖写入)。
- `engine_kwargs` - 用于传递给引擎的其他关键字参数。这些参数会传递给相应引擎的函数,例如 `xlsxwriter.Workbook(file, **engine_kwargs)` 或 `openpyxl.Workbook(**engine_kwargs)` 等。

### MySQL

需要 `sqlalchemy` 与 `pymysql`:

```python
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://username:password@hostname:port/data")
df.to_sql("数据表名称", engine, index=是否添加自增主键, if_exists='append')
```

### JSON

```python
pd.read_json()
```

参数说明:

- `orient=None` - JSON 数据的结构方式,默认是 `'columns'`
- `dtype=None` - 强制指定列的数据类型
- `convert_axes=True` - 是否转换行列索引
- `convert_dates=True` - 是否将日期解析为日期类型
- `keep_default_na=True` - 是否保留默认的缺失值标记,如 NaN
- `line=False` - 是否逐行读取 json 对象,即每行都是独立的 json,把 `[]` 用行分割了

常见的 `orient` 参数选项:

- `split` - `{"index":["a","b"],"columns":["A","B"],"data":[[1,2],[3,4]]}`,使用键 index、columns 和 data 结构
- `records` - `[{"A":1,"B":2},{"A":3,"B":4}]`,每个记录是一个字典,表示一行数据
- `index` - `{"a":{"A":1,"B":2},"b":{"A":3,"B":4}}`,使用索引为键,值为字典的方式
- `columns` - `{"A":{"a":1,"b":3},"B":{"a":2,"b":4}}`,使用列名为键,值为字典的方式
- `values` - `[[1,2],[3,4]]`,只返回数据,不包括索引和列名

```python
df.to_json()  # 跟上面差不多
```

## DataFrame 数据的 CURD

### 增加列

```python
df["列名"] = 值  # 直接新建新列,这行下来的都是同一个数据
df["列名"] = []  # 直接给列表赋值
df["列名"] = df["列名"] 运算 值  # 也可通过获得的其他 Series 进行计算赋值
df.assign(c1=…, [c2=…, c3=…])  # 直接添加一个或 n 个列
df["列名"] = np.where(series == ?, true_result, false_result)  # 根据某列的值判断增加新的列
```

### 删除列

```python
df.drop(axis="columns" 或 "index")  # 除非指定 inplace,不会修改原数据
del df["列名"]  # 删除列,会修改原数据,要删多个里面再套个列表
```

### 去重

```python
df.drop_duplicates()  # DataFrame 去重,就是行去重,删去重复的行,可以 inplace
series.drop_duplicates()
```

### 修改

```python
df["已有列名"] = xxx  # 修改已有列的数据
df["列名"].replace(old, new)  # 修改指定单元格的数据,注意 replace
```

### 查询

```python
df.sort_values([…])  # 指定一行或多行里的数据进行排序
df[["列名1", …]]  # 获取单个或多个行,返回 DataFrame
df.query()  # 一样的
```

### 排序

```python
df.rank()  # 针对每列都会排名
```

可指定 `method`:

- `average` - 默认,排名评分不连续,数值相同的评分一致,都为平均值
- `min` - 不连续,数值相同评分一致,都为最小值
- `max` - 不连续,数值相同评分一致,都为最大值
- `dense` - 连续,数值相同评分一致

为解决上面问题,我们可以对单独的 `series.rank(method)`。

## 高级处理 - 缺失值处理

### 判断缺失值

```python
pd.isnull()  # 判断是否有缺失值,传入 DataFrame 或 Series,返回 bool 版本的 DataFrame 或 Series
```

### 删除缺失值

```python
df.dropna()  # 删除缺失值,默认行,注意 inplace
np.all(pd.notnull(…))  # 判断某列是否是包含缺失值的列,阵列都是 True 才是 True
```

### 填充缺失值

```python
df.fillna()  # 将缺失值全部替换为指定值
df["列名"].fillna(df["列名"].mean())  # 替换指定列的 NaN 为平均值,注意 inplace
```

也可以使用 `for series in df.columns` 循环获取列名来填充每个列的 NaN 为平均值。`np.all(pd.notnull(df/series))` 只有全部为 True 才为 True。

### 非 NaN 的转化

比如有 `?` 这样的值,需要替换它:

```python
replace('?', np.nan)  # 全部替换为 nan 再进行操作
```

## 高级处理 - 数据合并

```python
pd.concat([data1, data2], axis=)  # 按行或列进行合并,默认 outer,不能 right 或 left
pd.merge(left, right, how='inner', on=None)  # on 为关联哪些字段
```

## 高级处理 - 数据分组

```python
df.groupby("列名")  # 指定按列或多列进行分组,返回 DataFrameGroupBy 对象
```

### 分组聚合

```python
DataFrameGroupBy()  # 获取指定的分组,有多个行进行分组就用多个
DataFrameGroupBy.agg({'列名1': '聚合函数名', '列名2': '聚合函数名'})  # 聚合函数
DataFrameGroupBy["列名"].聚合函数()  # 同上,返回 Series,[[]] 可以返回 DataFrame
```

### 分组过滤

```python
DataFrameGroupBy.filter(lambda x: x["指定列"].针对列的计算方法 条件表达式)
# 等价于 DataFrameGroupBy["列名"].filter(lambda x: x.针对列的计算方法 条件表达式)
# 等价于 df.query()
```

x 是除了分组列的 DataFrame 对象,这里是筛选出符合条件的行。

## 高级处理 - 交叉表与透视表

```python
data = {
    "性别": ["男", "女", "男", "女", "男", "女"],
    "购买": ["是", "否", "是", "是", "否", "否"],
}
df = pd.DataFrame(data)
```

交叉表:计篡一列数据对于另外一列数据的分组个数:

```python
pd.crosstab(df["性别"], df["购买"])  # 创建交叉表
# 结果如下:
# 购买  否  是
# 性别
# 女   2  2
# 男   2  2
```

透视表:指定某一列对于另外一列的关系,也可以实现:

```python
df.pivot_table(index="性别", columns="购买", values="购买", aggfunc="count")
```

`aggfunc` 可以替换为其他的,mean、min 都行。

## 绘图

```python
DataFrame.plot()  # 绘制折线图,第一列作为 x 轴,第二列作为 y 轴
DataFrame.plot.bar(color=[])  # 柱状图
```

对于相同的参数,可以定义 map 存储,传参只要 `**` 解开就行,如:

```python
args = {'figsize': (10, 5), 'color': ['r', 'g', 'b']}
DataFrame.plot(**args)
```

## 实战

### 找到指定列中最小或最大的行

```python
df[指定行].max()  # 获取值
df[df[xxx] == df[xxx].max]  # 筛选,获取行
df.sort_values(xxx)  # 排序
df.nlargest(n, xxx)  # 找到列中最大的几个行
```

### 找到最新的数据

参照上面,对时间进行比较即可,建议使用 `sort_values`。