**numpy****属性**  
NumPy的数组类被称作ndarray，有以下常用的属性：  
ndim - 维度  
shape - 形状，即几行几列  
size - 大小，数组元素  
dtype - 元素类型，datatype  
itemsize - 元素大小  
比如np.arrange(15),reshape(3, 5) 返回ndarray对象可以将[0, 1, …, 14]组合为3行5列矩阵  
我们也可以通过np.array()将py列表转为ndarray  
**ndarray****的创建**  
np.empty(shape, dtype=float, order='C')  
创建一个未初始化的指定大小的ndarray对象，  
order - 'C'或'F'，代表行或列优先  
np.zeros(shape, dtype=float, order='C')  
创建指定大小的ndarry对象，用0来填充  
np.ones(shape, dtype=float, order='C')  
同上，但是用1来填充  
np.zero_like(a, dtype=None, order='K', subok=True, shape=None)  
创建与给定ndarray形状相同的ndarray，但其中全部用0来填充  
np.ones_like()  
同上，但是用1来填充  
np.array(object, dtype=None, copy=True, order=None, subok=False, ndmin=0)  
把py列表转为ndarray,会复制数据，使用额外数据内存(仅源是ndarray时)  
object - 数组或嵌套的序列  
dtype - 元素的数据类型，对应np.数据类型  
copy - 对象是否需要复制  
order - 创建数组的样式，C为行方向，F为列方向，A为任意方向（默认）  
subok - 默认返回一个与基类型一致的数组  
ndim - 指定数组的最小维度  
np.asarray()  
用法同上，但是不会复制数据，使用原数据内存(仅源是ndarray时)  
np.arange(start, stop, step)  
类似于py的range()，可选参数同np.array()也有  
np.frombuffer(buffer, dtype=float, count=-1, offset=0)  
接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象  
np.fromiter(iterable, dtype, count=-1)  
从可迭代对象中建立 ndarray 对象，返回一维数组  
np.random 生成随机数  
.rand(3, 4) # 生成指定维度大小（3行4列）的随机多维浮点型数据〈二维），rand固定区间0.0～1.0  
.randint(-1, 5, size=(3, 4)) # 生成指定维度大小（3行4列）的随机多维整型数据（二维）,指定区间(-1, 5)  
.uniform(-1, 5, size=(3, 4)) # 生成指定维度大小的小数范围矩阵  
np.linspace(start, end, count, endpoint=True)  
生成等差数列，在[start, end]结束生成(包左包右)指定个数的元素  
endpoint - 是否包含结束值  
np.logspace(start, end, count, base=10)  
生成等比数列， 在[base^start,base^end]生成(包左包右)指定个数的元素  
可选参数同上  
**numpy****索引切片**  
切片操作  
类似于py中的列表，但是可以用,分隔维度，比如[0:2, 1:3]，提取二维下下标0, 1的数组，每个数组只保留下标1，2的元素  
我们也可以使用…来选择当前维度所有子维度，比如[…, 0]，提取所有二维下的数组，再提取其中索引为0的元素  
数组索引  
允许接收一个ndarray数组，ndarray中的数字都代表了该ndarray的下标，从中挑下来  
比如ndarr1=[[0, 1, 2], [3, 4, 5]; 则ndarr[ndarr2=[0, 5]]结果是[0, 5]  
花式索引  
也可以在[]里面使用，分隔使用多个ndarray挑指定元素出来  
比如ndarr[np.array(0, 1, 1), np.array(0, 0, 1)]结果是[0, 3, 4],当然，可以直接用1代表[1, 1, 1](整个维度)  
布尔索引  
直接在[]里面写条件判断，用法：  
x[~np.isnan(x)] # 筛出不是nan的元素  
x[x \< 20] += 20 # 把所有负数加20
 
**numpy****中的类型转换**  
使用ndarray对象中的astype()即可，里面传入np.数据类型或字符串，需要接收返回值  
**numpy****的内置函数**  
都是用于科学计算，传入num或者ndarray  
计算函数

|   |   |   |
|---|---|---|
|np.ceil() 向上取整|np.floor() 向下取整|np.rint() 四舍五入|
|np.abs() 绝对值|np.mnultiply() 乘法/矩阵乘法(行列一致)|np.divide() 除法/矩阵除法(行列一致)|
|np.where() 三元运算符|||

统计  
多维数组默认统计全部维度，可以指定axis参数，值为0按列统计，值为1按行统计

|   |   |   |
|---|---|---|
|np.mean() 平均值|np.sum() 和|np.max() 最大值|
|np.min() 最小值|np.std() 标准差|np.var() 方差|
|np.argmax() 最大值下标索引|np.argmin() 最小值下标索引|np.cumsum()/np.cumprod() 返回一维数组，每个元素是之前所有元素的累加和/累加积|

去重函数  
np.unique() 去重，返回新副本  
排序  
np.sort() 返回排序后的副本  
ndarray.sort() 对ndarray对象调用直接在原数据上修改  
迭代器  
np.nditer(arr, order='C') 返回迭代器，默认行序优先（F则为列），用于for in遍历  
使用ndarray.flat() 或 flatten() （返回拷贝，修改不会影响原数组）也可以获得迭代器  
其中order参数'C'(行)、'F'(列)、'X'(原顺序)、'K'(内存顺序)  
变形  
np.reshape()或ndarray.reshape()，指定转为几行几列，前者返回新数据后者不改变数据修改形状  
np.ravel() 一维化  
翻转  
.transpose() 或ndarry.T，对换数组的维度  
.rollaixs，向后滚动指定的轴  
.swapaxes，对换数组的两个轴  
**numpy****数学运算**  
矩阵乘法  
行列数一致的情况下使用 arr1 * arr2 或者 np.multiply(arr1, arr2)  
行列数不一致使用 .dot(arr1, arr2) 或者 @  
矩阵加减法  
直接使用数学运算符，行列相同的话就是每个元素对应相+-  
如果形状不同，就会触发广播机制，比如

![Exported image](_assets/numpy/numpy__11-51-38-0.png)