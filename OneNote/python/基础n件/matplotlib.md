import matplotlib.pyplot as plt  
**图像绘制流程**  
创建画布 plt.figure() # 返回fig对象，其实可以不用接收  
figsize - 指定图的长宽  
dpi - 图像的清晰度  
绘制图像  
plt.plot(x, y) # x轴，y轴的数据  
显示图像  
plt.show()

![Anatomy of a figure](_assets/matplotlib/matplotlib__11-51-53-0.png)

基础绘图功能(注意要在plot以后设置)  
plt.plot()可以用字符串传入第三个参数  
颜色字符：'b' 蓝色，'m' 洋红色，'g' 绿色，'y' 黄色，'r' 红色，'k' 黑色，'w' 白色，'c' 青绿色，'#008000' RGB 颜色符串。多条曲线不指定颜色时，会自动选择不同颜色。  
线型参数：'‐' 实线，'‐‐' 破折线，'‐.' 点划线，':' 虚线。  
标记字符：'.' 点标记，',' 像素标记(极小点)，'o' 实心圈标记，'v' 倒三角标记，'^' 上三角标记，'\>' 右三角标记，'\<' 左三角标记...等等  
显示刻度  
plt.xticks(x, **kwargs)  
plt.yticks(y, **kwargs)  
这个要求一一对应  
比如绘制1950年到2000年数据每五年打标签，那么values就是[1950, 1955, 1960…], 而y_label就是[1950年, 1955年, 1960年…]  
添加网格  
plt.grid(linestyle='-', alpha=1)  
可以指定网格样式：  
- 实线  
-- 虚线  
-. 地图中边界线的样式  
: 全是点的线  
添加标题  
plt.title(title, fontsize=12)  
添加xy轴标签  
plt.xlable(lable, fontsize=12)  
plt.ylable(lable, fontsize=12)  
保存图片  
pklt.savefig(io)  
一个画布里绘制多个  
只要多次调用plt.plot即可，可使用color=''等指定线的颜色  
添加图例：  
plt.legend(loc="best") # 指定的选项很多  
多个坐标系显示 - 面相对象的设置方法  
在一切操作之前要创建画布，若nrows=1,ncols=2,画布是两个相同x但不同y的图  
plt.subplots(nrows=, ncols=, figsize=, dpi=) # 返回元组，fig画布对象，axes坐标轴对象  
nrow相当于多少个横的x，ncols相当于多少个竖下来的y  
axes就是个列表了，使用axes指定在哪个图上操作，像上面plt那样操作但要加set_，比如  
axes[0].set_title(), axes[0].set_xlabel()  
其它常见图形:仅展示一部分  
精华就是ctrl+c和ctrl+v  
[https://matplotlib.org/stable/gallery/index.html](https://matplotlib.org/stable/gallery/index.html)  
柱状图  
plt.bar(x, width, align='center', **kwargs)  
x - 传递的数据  
width - 柱状图宽度  
align - 对齐方式  
直方图  
plt.hist(x, bin=None)  
bin - 组距  
饼图  
plt.pie(x, labels=, autopct=, colors)  
x - 数量，自动算百分比  
labels - 每部分名称  
autopct - 占比显示指定%1.2f%%  
colors - 每部分颜色  
散点图  
plt.scatter(x, y)