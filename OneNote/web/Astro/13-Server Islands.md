---
title: 第 13 课：Server Islands
tags: ["Astro", "frontend", "课程", "课程-13"]
aliases: ["第 13 课", "Server Islands", "第 13 课：Server Islands"]
---
# 第十三课：Server Islands

### 13.1 使用场景

静态文章页中只有用户菜单需要按请求读取 cookie：

~~~astro
<!-- src/components/UserMenu.astro -->
---
const sessionId = Astro.cookies.get('session')?.value;
const user = sessionId ? await findUser(sessionId) : null;
---

{
  user
    ? <a href="/account">你好，{user.name}</a>
    : <a href="/login">登录</a>
}
~~~

页面：

~~~astro
---
import UserMenu from '../components/UserMenu.astro';
---

<header>
  <a href="/">Astro Notes</a>

  <UserMenu server:defer>
    <span slot="fallback" aria-busy="true">加载账户…</span>
  </UserMenu>
</header>
~~~

需要 Adapter 来执行延迟服务器渲染。

### 13.2 与 Client Island 对比

| 维度 | Client Island | Server Island |
|---|---|---|
| 指令 | <code>client:*</code> | <code>server:defer</code> |
| 主要运行处 | 浏览器 | 服务器 |
| 典型任务 | 状态、点击、输入 | cookie、个性化、慢服务器数据 |
| 是否发送框架 JS | 会 | 组件本身不会 |
| 页面是否等待它 | 初始 HTML 视实现而定 | 不阻塞主体，独立请求 |
| fallback | 框架自有 loading 或 HTML | <code>slot="fallback"</code> |

### 13.3 工作方式

Astro 构建时会：

1. 将 <code>server:defer</code> 组件拆成特殊路由；
2. 主页面先输出不包含最终岛内容的 HTML；
3. 输出 fallback 和一个小脚本；
4. 浏览器独立请求服务器岛；
5. 完成后替换 fallback。

官方依据：[Server islands](https://docs.astro.build/en/guides/server-islands/)

### 13.4 设计注意

- fallback 尺寸接近真实内容，减少 CLS；
- 不要把页面主要内容都拆成 Server Island；
- 个性化区域不要进入公共缓存；
- 服务器岛的 Props 会编码进生成的 URL，因此不要把秘密当 Props 传入；
- 敏感信息应在岛内部通过 cookie / session 查询。
