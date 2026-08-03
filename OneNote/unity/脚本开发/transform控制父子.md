---
title: transform控制父子
tags: [unity, 脚本开发]
aliases: [transform控制父子]
---

# transform控制父子

`transform` 是 Unity 中操作物体位置/旋转/缩放的核心组件,生命周期方法(`Update`/`Start`)见 [[unity/脚本开发/初步认识|初步认识]];获取物体的方式见 [[unity/脚本开发/游戏物体的获取|游戏物体的获取]]。

```cs
void Start()
{
    // 当前物体的绝对/相对位置
    Debug.Log(transform.position);
    Debug.Log(transform.localPosition);
    // 当前物体的绝对/相对旋转(四元数)
    Debug.Log(transform.rotation);
    Debug.Log(transform.localRotation);
    // 当前物体的欧拉角
    Debug.Log(transform.eulerAngles);
    Debug.Log(transform.localEulerAngles);
    // 当前物体的缩放
    Debug.Log(transform.localScale);
    // 当前物体的前向向量
    Debug.Log(transform.forward);

    // 父子关系
    // 获取父物体
    GameObject parentGameObject = transform.parent.gameObject;
    // 获取子物体个数
    Debug.Log(transform.childCount);
    // 按名字获取子物体
    Transform find = transform.Find("name");
    // 按索引获取子物体
    Transform child = transform.GetChild(0);
    // 解除所有子物体的父子关系
    transform.DetachChildren();
    // 判断一个物体是否是另一个物体的子物体
    bool result = child.IsChildOf(transform); // true
    // 设置父物体
    child.SetParent(transform);
}

void Update()
{
    // 时刻注视某个点
    transform.LookAt(Vector3.zero);
    // 旋转方法:绕自身 up 轴顺时针旋转 1 度
    transform.Rotate(Vector3.up, 1);
    // 绕某个点旋转(类似于公转),这里绕原点 up 轴旋转 10 度
    transform.RotateAround(Vector3.zero, Vector3.up, 10);
    // 移动,每帧向指定向量移动距离
    transform.Translate(Vector3.forward * 0.1f);
}
```
