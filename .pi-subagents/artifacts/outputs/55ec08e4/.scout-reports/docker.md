# docker 目录 markdown 格式审计

## 概况
- 文件总数: 7
- 影响笔记数: 7 (全部)
- 子目录: `docker/` (6 文件) / `docker-compose/` (1 文件)
- 文件清单:
  - `E:/个人知识/OneNote/docker/docker/单机容器编排.md` (264 B)
  - `E:/个人知识/OneNote/docker/docker/存储管理.md` (2 118 B)
  - `E:/个人知识/OneNote/docker/docker/容器与镜像.md` (6 623 B)
  - `E:/个人知识/OneNote/docker/docker/网络管理.md` (1 431 B)
  - `E:/个人知识/OneNote/docker/docker/资源管理.md` (1 539 B)
  - `E:/个人知识/OneNote/docker/docker/配置与运行.md` (657 B)
  - `E:/个人知识/OneNote/docker/docker-compose/安装与配置.md` (547 B)

## 偏离清单

### 高优

**H1. 全部标题用粗体伪标题,无真实 `#` 层级(标题层级)**
- 涉及全部 6 个 docker 子文件,共 16 处 `**xxx**` 充当章节标题
- 位置:
  - 单机容器编排.md:1 `**快速开始**`
  - 存储管理.md:1,15 `**容器持久化存储**` / `**容器数据共享**`
  - 容器与镜像.md:1,22,55,78,91 `**初识容器与镜像**` / `**镜像结构介绍**` / `**构建镜像**` / `**发布到远程仓库**` / `**案例:使用****IDEA****打包****SpringBoot****镜像**`
  - 网络管理.md:1,14,20,25 `**容器网络类型**` / `**自定义网络**` / `**容器间网络**` / `**容器与外部网络**`
  - 资源管理.md:1,12,24 `**容器控制操作**` / `**物理资源管理**` / `**容器监控**`
  - 配置与运行.md:1 `**配置与运行**`
- 影响:Obsidian 大纲/导航/搜索层级失效;无 TOC 锚点;无法用 `#`/ `##` 划分层级

**H2. 全部 7 个文件零代码块(结构异常 - 代码块缺失)**
- `grep -F '\`'` 在所有 7 个文件上均返回 0 命中,即不存在任何 ``` ``` ``` 围栏,也没有反引号行内代码
- 影响:大量 shell 命令、JSON 配置、systemd unit、Dockerfile、docker compose 命令被当作普通段落渲染
- 高频证据:
  - 配置与运行.md:整段 `daemon.json` JSON(行 7-12)、`[Service]` 块(行 19-22)、所有 `sudo systemctl ...` 命令都是纯文本
  - 容器与镜像.md:全部 `docker pull / run / images / exec / build / commit / export / save / search / login / push / tag / volume / network ...` 命令、`FROM ubuntu` / `RUN apt update && ...` / `COPY target/app.jar app.jar` / `CMD java -jar app.jar` / `EXPOSE 8080` Dockerfile 段
  - 资源管理.md:行 3-11、14-19、26-30 全部命令裸奔,包含长达 130+ 字符的 `docker run -d -p 9000:9000 --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data 6053537/portainer-ce`
  - 存储管理.md:`ADD ...` / `VOLUME ...` Dockerfile 指令(行 26-27)也是纯文本
  - 单机容器编排.md:`apt install docker-compose-plugin` 与 `version: "3.9" # docker对应的版本号` 都没有围栏
  - 安装与配置.md:全部 `docker compose up -d` / `docker-compose start/stop/restart` / `docker compose down` / `docker compose build` 等命令裸文本

**H3. 连续加粗合并问题 `**案例:使用****IDEA****打包****SpringBoot****镜像**`(强调风格 / 特殊残留)**
- 容器与镜像.md:91,本意应为 `**案例:使用 IDEA 打包 SpringBoot 镜像**` 或 `## 案例:使用 IDEA 打包 SpringBoot 镜像`
- 问题:5 对 `**` 紧邻,渲染后 IDEA/SpringBoot 与前后文本粘连;也加重了 H1 伪标题问题

**H4. 段落完全无空行分隔(结构异常 - 段落挤压)**
- 资源管理.md:1539 B 文件内 0 行空行,3 个章节 + 命令全部粘在同一段
- 网络管理.md:1431 B 文件内只有 1 行空行,4 个章节几乎全部粘连
- 存储管理.md:2118 B 文件内只有 3 行空行,大量命令后立刻接下一行说明
- 容器与镜像.md:也有段落挤压(如 4-21 行命令连排)
- 影响:渲染时变成连续段落,句中命令与说明视觉上混淆

**H5. 安装与配置.md 完全没有章节标记(标题层级 / 结构异常)**
- `docker-compose/安装与配置.md`:全文无 `#` 也无 `**xx**`,章节依靠裸文本 `安装` / `配置` / `运行` / `启动、停止、重启` / `查看compose状态` / `停止并删除容器` / `重新构建镜像` 分段,严重扁平

### 中优

**M1. 链接文本与 URL 完全相同(链接冗余)**
- 容器与镜像.md:79 `[https://hub.docker.com/repositories](https://hub.docker.com/repositories)` 显示文本=URL,应改为描述性文本如 `[Docker Hub Repositories](https://hub.docker.com/repositories)`
- 配置与运行.md:10 `"http-proxy": "[http://127.0.0.1:7890](http://127.0.0.1:7890)"` 出现在 JSON 内,本应是 JSON 字符串 `"http://127.0.0.1:7890"` 但被当成链接渲染(同时叠加 H2 代码块缺失问题)
- 配置与运行.md:11 `"https-proxy": "[http://127.0.0.1:7890](http://127.0.0.1:7890)"` 同上

**M2. 中英标点混用(中文/英文标点)**
- 配置与运行.md:6 `方式一:` 使用全角冒号 `:` (U+FF1A)
- 配置与运行.md:16 `方式二:` 使用半角冒号 `:` — 同文件同列表项风格不一致
- 其余中文正文与标点整体使用全角,无明显混用

**M3. 隐含列表未标记为列表(列表风格 / 结构异常)**
- 单机容器编排.md:`安装插件` / `IDEA配置` 是并列条目但用纯段落
- 存储管理.md / 资源管理.md / 网络管理.md 中大量 `步骤1 → 命令 → 步骤2` 的并列内容也未使用 `-` 或 `1.` 列表
- 容器与镜像.md:行 27-28、51-53、76 已使用 `-` 无序列表,可见作者有能力写列表;问题仅在剩余并列段落未统一

### 低优

**L1. 行内 `<…>` 角括号残留(HTML 残留)**
- 容器与镜像.md:21 `docker rmi <reposity_name>` 行内出现裸角括号,在 CommonMark 下可能被当作 raw HTML 处理
- 另有 `docker rm <容器名称/容器ID>`、`docker network connect <网络名称> <容器名/容器ID>`、`docker start -i <容器ID>` 等,本应进入代码块(与 H2 同源)
- 影响低:因未闭合 HTML 标签,大多数渲染器会保留文本;但在某些解析器下会触发歧义

**L2. 容器与镜像.md 容器与镜像.md 第 76 行 `- 镜像名:latest` 列表项下不缩进(列表风格一致性)**
- 行 51-53 三条 `- 文件读取/创建和修改/删除文件` 是说明性条目;行 76 单独 `- 镜像名:latest` 与上下文(shell 命令链 cat | docker import)混排,视觉错位

### 已确认无问题

- **Frontmatter**:所有文件均无 YAML frontmatter;若 Obsidian 全库规则允许空 frontmatter 则合规,否则为待办(本次按"未发现残留 frontmatter"归类为 PASS)
- **表格**:无任何表格残留(`grep '^|'` 全部 0)
- **图片引用**:5 处 `![[_assets/...png]]` Obsidian wikilink 风格一致,符合"图片 wikilink 化"已完成的预期
- **行尾空格 / 反斜杠转义 / 空 Untitled**:本次扫描未发现 `\\` 转义残留或 `Untitled` 空标题

## 自动修复可行性

### 完全可自动 (机械正则可解)
- **H1 标题提升** — 把每行 `^\*\*([^*]+)\*\*$` 替换为对应层级 `## 标题` 或 `### 标题`,层级需要约定(可启发式按出现顺序赋 `##`/`###`),7 文件共 16 处
- **H3 合并连续 `**` 标记** — `s/\*\*\*\*+/ /g` 即可将 `使用****IDEA****打包` 修成 `使用 IDEA 打包`,1 处
- **H5 安装与配置.md 加标题** — 给裸文本 `安装`/`配置`/`运行`/...加 `##` 前缀,7 处
- **M1 链接文本简化** — 把显示文本与 URL 完全相同的 markdown 链接改为裸 URL,3 处(其中 2 处在 JSON 内,需先剥离代码块上下文)
- **M2 标点归一** — 全角/半角冒号统一(选定全角 `:` 与中文一致),2 处
- **L1 行内角括号处理** — 把含 `<…>` 的命令整行包入行内代码或代码块;作为 H2 修复的一部分一并处理

### 需人工判断
- **H2 代码块重建** — 需要判断每段裸命令/配置属于哪种语言(bash / json / dockerfile / systemd / yaml),并选择合适的围栏起始;尤其配置与运行.md 同时含 JSON 和 systemd unit,需要拆段;容器与镜像.md 内嵌的 `cat … | docker import -c 'CMD …' -c 'ENV …' -m … - 镜像名:latest` 跨行 shell 是否合并为一段也需判断
- **H4 段落空行补齐** — 哪些位置是"段落→段落"还是"说明→命令"的边界需要逐处确认;资源管理.md/网络管理.md/存储管理.md 全文都需要梳理
- **M3 隐含列表** — 单机容器编排.md 的 `安装插件` / `IDEA配置` 等条目是否升级为列表需要作者确认

### 不可自动
- **Frontmatter 是否统一加 tags/aliases** — 涉及笔记元数据策略,只能由人决定

## 推荐处理顺序

1. **H2 代码块重建**(影响最大:全部 7 文件,决定后续命令/链接处理边界)
   - 先处理 配置与运行.md(语法最明确:JSON + systemd unit)
   - 再处理 容器与镜像.md(命令+多语言混合)
   - 最后处理 资源管理.md / 网络管理.md / 存储管理.md / 单机容器编排.md / 安装与配置.md
2. **H3 合并连续加粗**(1 处,顺手修)
3. **H1 标题层级重写 + H5 补标题**(7 文件 16+7 处,需约定层级映射)
4. **M2 标点归一**(配置与运行.md 2 处)
5. **M1 链接简化**(3 处;其中 2 处会被 H2 自动带入代码块而消解,仅 1 处真正残留)
6. **H4 段落空行补齐**(3 个挤压文件,人工判断为主)
7. **M3 / L2 隐含列表与列表风格**(依赖作者意图,最后处理)
