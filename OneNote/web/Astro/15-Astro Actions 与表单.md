---
title: 第 15 课：Astro Actions 与表单
tags: ["Astro", "frontend", "课程", "课程-15"]
aliases: ["第 15 课", "Astro Actions 与表单", "第 15 课：Astro Actions 与表单"]
---
# 第十五课：Astro Actions 与表单

### 15.1 第一个 Action

> [!important] 运行前提
> Action 是服务器函数。生产部署必须有能够处理按需请求的 Adapter；纯静态文件主机无法执行 Action handler。

~~~ts
// src/actions/index.ts
import { ActionError, defineAction } from 'astro:actions';
import { z } from 'astro/zod';

export const server = {
  subscribe: defineAction({
    input: z.object({
      email: z.string().email(),
    }),
    handler: async ({ email }) => {
      const exists = await hasSubscriber(email);

      if (exists) {
        throw new ActionError({
          code: 'CONFLICT',
          message: '该邮箱已经订阅',
        });
      }

      await createSubscriber(email);
      return { ok: true };
    },
  }),
};
~~~

客户端调用：

~~~astro
<form id="subscribe-form">
  <label>
    邮箱
    <input name="email" type="email" required />
  </label>
  <button>订阅</button>
  <p id="feedback" aria-live="polite"></p>
</form>

<script>
  import { actions } from 'astro:actions';

  const form = document.querySelector<HTMLFormElement>('#subscribe-form');
  const feedback = document.querySelector<HTMLParagraphElement>('#feedback');

  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const email = String(formData.get('email') ?? '');

    const { data, error } = await actions.subscribe({ email });

    if (feedback) {
      feedback.textContent = error ? error.message : '订阅成功';
    }

    if (data) form.reset();
  });
</script>
~~~

### 15.2 直接接收 FormData

~~~ts
export const server = {
  createComment: defineAction({
    accept: 'form',
    input: z.object({
      postId: z.string().min(1),
      content: z.string().min(2).max(1000),
    }),
    handler: async (input, context) => {
      const user = context.locals.user;

      if (!user) {
        throw new ActionError({
          code: 'UNAUTHORIZED',
          message: '请先登录',
        });
      }

      return createComment({
        userId: user.id,
        postId: input.postId,
        content: input.content,
      });
    },
  }),
};
~~~

### 15.3 结果模型

~~~ts
const { data, error } = await actions.subscribe({ email });

if (error) {
  console.error(error.code, error.message);
  return;
}

console.log(data);
~~~

原型阶段也可：

~~~ts
const data = await actions.subscribe.orThrow({ email });
~~~

正式 UI 通常显式处理 error 更合适。

官方依据：[Actions](https://docs.astro.build/en/guides/actions/)

### 15.4 Action 不是授权边界的替代品

Zod 只验证数据形状。Action handler 内仍要验证：

- 用户是否登录；
- 是否有权修改目标资源；
- 资源是否存在；
- 是否触发业务限制；
- 是否需要防滥用。

不要相信客户端传来的 <code>userId</code>，应从可信 session / locals 获取。
