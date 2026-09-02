---
title: 第 08 课：客户端脚本与 Web Components
tags: ["Astro", "frontend", "课程", "课程-8"]
aliases: ["第 08 课", "客户端脚本与 Web Components", "第 08 课：客户端脚本与 Web Components"]
---
# 第八课：客户端脚本与 Web Components

### 8.1 什么时候不需要 Vue

以下功能通常一个浏览器脚本就够：

- 复制按钮；
- 展开 / 收起；
- 主题切换；
- 对话框；
- 给 Web Component 绑定事件；
- 页面加载后增强已有 HTML。

~~~astro
<button id="copy-button" data-text="Astro">复制</button>

<script>
  const button = document.querySelector<HTMLButtonElement>('#copy-button');

  button?.addEventListener('click', async () => {
    const text = button.dataset.text ?? '';
    await navigator.clipboard.writeText(text);
    button.textContent = '已复制';
  });
</script>
~~~

普通无属性的 <code>&lt;script&gt;</code>：

- 默认支持 TypeScript；
- 会被 Vite 打包；
- 自动成为 module；
- 同一组件在一页出现多次时，脚本会去重；
- 足够小的脚本可能自动内联。

官方依据：[Scripts and event handling](https://docs.astro.build/en/guides/client-side-scripts/)

### 8.2 is:inline

~~~astro
<script is:inline>
  // 原样输出；不处理 TS，不解析 import，不去重。
</script>
~~~

使用场景：

- 必须在页面极早执行的主题初始化；
- public 目录脚本；
- 外部 CDN 脚本；
- 必须原样输出的片段。

> [!warning]
> script 只要带了除 <code>src</code> 以外的属性，就不会进入普通处理流程。不要随手加属性后又期待 TypeScript、打包与去重继续生效。

### 8.3 从服务器传数据到脚本

用 <code>data-*</code>：

~~~astro
---
interface Props {
  message: string;
}

const { message } = Astro.props;
---

<astro-greeting data-message={message}>
  <button>打招呼</button>
</astro-greeting>

<script>
  class AstroGreeting extends HTMLElement {
    connectedCallback() {
      const button = this.querySelector('button');
      const message = this.dataset.message ?? 'Hello';
      button?.addEventListener('click', () => alert(message));
    }
  }

  customElements.define('astro-greeting', AstroGreeting);
</script>
~~~

Web Component 很适合：

- 同一组件可能出现多次；
- 需要把 DOM 查询限制在当前实例；
- 希望自包含生命周期；
- 不值得引入 Vue runtime。

### 8.4 浏览器 API 不在 frontmatter

错误：

~~~astro
---
const theme = localStorage.getItem('theme');
---
~~~

原因：构建时和服务器没有浏览器 <code>window</code>、<code>document</code>、<code>localStorage</code>。

正确：放进 <code>&lt;script&gt;</code> 或 Vue Island。
