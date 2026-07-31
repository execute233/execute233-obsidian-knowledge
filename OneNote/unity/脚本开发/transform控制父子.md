---
title: transform控制父子
tags: [unity, 脚本开发]
aliases: [transform控制父子]
---

# transform控制父子

```cs

void Start()
{
// 当前物体绝对/相对位置,绝对/相对旋转,缩放
Debug._Log_(transform.position);
Debug._Log_(transform.localPosition);
Debug._Log_(transform.rotation); // 四元数
Debug._Log_(transform.localRotation);
Debug._Log_(transform.eulerAngles); // 欧拉角
Debug._Log_(transform.localEulerAngles);
Debug._Log_(transform.localScale);
// 当前物体的前方等等
Debug._Log_(transform.forward);
// 父子关系
// 获取父物体
GameObject parentGameObject = transform.parent.gameObject;
// 获取子物体个数
Debug._Log_(transform.childCount);
// 获取子物体
Transform find = transform.Find("name");
Transform child = transform.GetChild(0);
// 解除所有子物体关系
transform.DetachChildren();
// 判断一个物体是否是另一个物体的子物体
bool result = child.IsChildOf(transform); // true
// 设置父物体
child.SetParent(transform);
}
void Update()
{
// 时刻看向某个点
transform.LookAt(Vector3.zero);
// 旋转方法
transform.Rotate(Vector3.up, 1); // 朝up方向顺时针旋转1度
// 绕某个给提旋转(类似于公转),这里绕原点up轴旋转10度
transform.RotateAround(Vector3.zero, Vector3.up, 10);
// 移动,每帧向指定向量移动距离
transform.Translate(Vector3.forward * 0.1f);
}
```