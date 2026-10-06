[English](README.md) · [한국어](README.ko.md) · **简体中文**

# SoWhat Decks：用 Claude Code 生成结论先行的 PPT 汇报

让编码智能体（coding agent）做出结论先行、可直接编辑的 PowerPoint（.pptx）汇报 PPT。

把笔记和数据交给智能体。它先规划故事线，再在你自己的模板上生成带原生图表的 .pptx，并在别人看到之前先审阅一遍。它面向董事会汇报、投资人更新、战略建议这类按咨询报告写法制作的 PPT。每页的标题是一句完整的结论，下面放支撑它的证据。

免费开源（MIT）。[Pro](#pro) 增加高级图表和演示文稿方案（deck recipes）。

![示例演示文稿中的六页幻灯片：执行摘要、斜率图、堆积柱状图、折线图和决策页，每页标题都是一句完整的话](docs/img/hero.png)

## 只看标题

同一份第三季度董事会汇报的两个版本，用同一组样例数据制作。左边的草稿每页用主题词作标题；右边是用 SoWhat Decks 重做的版本。两者都在 [`examples/03-review-before-after`](examples/03-review-before-after/) 中。演示文稿是英文的，下表标题为中文译文。

| 草稿 | 用 SoWhat Decks 重做 |
|---|---|
| 执行摘要 | 第三季度超出计划，但 SMB 流失使年末 ARR 少 $230k；我们建议把两个招聘名额调到客户上线（onboarding） |
| 第三季度 ARR 桥图 | 期末 ARR 为 $11.05M，超出计划 1.4%；由于流失上升，超出幅度小于新增 ARR |
| 分客户群流失 | SMB 流失的 ARR 自第一季度以来翻了一倍多，现在抵消了三分之一的新签约 |
| 上线产能 | 每位专员负责的新客户增加 41%，配置完成率从 68% 降到 55% |
| 下一步 | 请董事会批准人员调整，以及修订后的年末预测 $11.85M |

只扫一遍右栏，就能知道发生了什么、为什么，以及董事会需要决定什么。`deck-storyline` 的标题检查把草稿 14 个标题中的 8 个标为错误，另有 3 个标为警告（[输出](examples/storyline-tests/control-topic-titles/title-lint.txt)）。

![从故事线到审阅完成的演示文稿：deck-review 框出草稿的问题，deck-storyline 重写标题，deck-build 重做幻灯片，最终审阅为 0 个 high、0 个 medium 问题](docs/img/demo.gif)

## 试一试

安装后（见下文），把下面任意一条粘贴给你的智能体：

> 用 deck-review 检查 ./my-deck.pptx，告诉我最重要的五处修改。

> 用 deck-storyline 根据 ./notes.md 和 ./metrics.csv 规划一份 10 页的董事会汇报。需要的决定是：批准第四季度招聘计划。然后用 deck-build 做出来。

幻灯片内容目前支持英语、韩语和日语，中文幻灯片还没有测试过（见[限制](#限制)）。

## 安装

**Claude Code 插件**

    /plugin marketplace add WQGGSEY/sowhat-decks
    /plugin install sowhat-decks@sowhat-decks

**skills CLI**

    npx skills add WQGGSEY/sowhat-decks

**Claude 应用（claude.ai）：** 从[最新版本](https://github.com/WQGGSEY/sowhat-decks/releases/latest)下载技能 ZIP。每个版本都有每个技能各一个 ZIP，以及包含全部四个技能的 ZIP。在 Claude 中打开 Customize > Skills，点击 +，依次选择 Create skill、Upload a skill，每次上传一个技能 ZIP（菜单名称以英文界面为准）。需要开启代码执行（Code execution）。这种方式我们还没有测试过。

**手动安装：** 把 `skills/` 里的文件夹复制到 `~/.claude/skills/`。

需要 Python 3.9 或更高版本和 python-pptx。LibreOffice 和 pypdfium2 是可选的。装了它们，deck-build 会导出 PDF 和 PNG 预览，deck-review 也会检查渲染后的幻灯片；deck-review 的标注图片还需要 Pillow。脚本不会安装任何东西。

已在 macOS 上的 Claude Code 中测试。其他智能体和 Claude 应用尚未测试（见[限制](#限制)）。

## 工作原理

| 技能 | 作用 | 产出 |
|---|---|---|
| `deck-storyline` | 把你的目的、受众、需要的决定和材料整理成一个核心信息（governing message）和 SCQA，并为每页写出一句完整的标题和所需的证据。缺口标记为 `[DATA NEEDED]`，并做只读标题测试。 | `storyline.md`，只有标题的幽灵演示文稿（ghost deck） |
| `deck-build` | 在你的 .pptx 或 .potx 模板上生成演示文稿：12 种版式、来源行、页码、演讲者备注，以及英语、韩语和日语字体。 | `deck.pptx`、`deck.pdf`、幻灯片 PNG |
| `deck-exhibits` | 根据要表达的信息选择图表，并用原生图表或形状绘制：条形图、折线图、堆积柱状图、高亮表格、2×2 矩阵、流程箭头图。 | 数据保存在文件里的图表 |
| `deck-review` | 渲染任何工具做出的 .pptx，检查标题、字号、文字溢出、超出页面的形状、以图片粘贴的图表和缺失的来源，再按评分标准给每页打分。自动修复从不改动文字和数字。 | `review.md`、标注后的 PNG、`deck.fixed.pptx` |

这些技能要求智能体只使用你的材料或注明来源的数字。材料不足以支撑某个结论时，幻灯片上会写 `[DATA NEEDED]`，审阅也会标出来；[`examples/storyline-tests`](examples/storyline-tests/) 中的幽灵演示文稿展示了这两步。发送前请核对数字。

## 示例

每个文件夹都有任务说明、输入材料、故事线、演示文稿规格、演示文稿（.pptx 和 PDF）、幻灯片 PNG、审阅结果和来源，还有一份写明重建所用提示词和命令的 README。最终版本没有 deck-review 自动检查的 high 或 medium 问题；`tests/test_examples.py` 在每次改动时都会检查。示例演示文稿是英文的。

| | 示例 | 依据 | 打开 |
|---|---|---|---|
| <img src="examples/01-investor-update/preview/slide-05.png" width="280" alt="幻灯片：2025 年净利润的大部分来自一次性税收收益"> | **投资人更新**，13 页 | 一家上市公司的 FY2025 10-K 和两封股东信，每个数字都注明来源 | [PDF](examples/01-investor-update/deck.pdf) · [PPTX](examples/01-investor-update/deck.pptx) · [故事线](examples/01-investor-update/storyline.md) · [审阅](examples/01-investor-update/review.md) |
| <img src="examples/02-market-entry/preview/slide-06.png" width="280" alt="幻灯片：按收入调整后，印度尼西亚的在线市场至少是其他候选市场的两倍"> | **先进入哪个东南亚市场？** 13 页 | 世界银行指标，注明来源。公司是虚构的 | [PDF](examples/02-market-entry/deck.pdf) · [PPTX](examples/02-market-entry/deck.pptx) · [故事线](examples/02-market-entry/storyline.md) · [审阅](examples/02-market-entry/review.md) |
| <img src="examples/03-review-before-after/preview/slide-02.png" width="280" alt="幻灯片：以请求结尾的董事会汇报摘要"> | **董事会汇报，审阅后重做**，14 页 | 样例数据，每页都有标注。包含一份故意埋了问题的草稿及其审阅 | [草稿审阅](examples/03-review-before-after/review.md) · [草稿 PDF](examples/03-review-before-after/before-review/render/before.pdf) · [重做后 PDF](examples/03-review-before-after/deck.pdf) · [提示词](examples/03-review-before-after/README.md#prompts-and-commands) |

## 审阅任何 PPT

`deck-review` 适用于任何工具或任何人做的 .pptx。它会渲染幻灯片，列出细心的审阅者会发现的问题，并把薄弱的标题改写成结论。在示例 03 的董事会汇报草稿中，它发现了 1 个 high、18 个 medium 和 11 个 low 问题：主题词标题、三张以图片粘贴的图表、小于 12 pt 的文字、没有来源的图表，以及写成“TBD”的预测。

![左：草稿幻灯片，deck-review 框出了主题词标题和以图片粘贴的图表。右：重做后的幻灯片，有完整句子的标题、原生堆积柱状图和来源行](docs/img/review-before-after.png)

## 免费版与 Pro 对比

| | 免费版（MIT） | Pro（$29 一次性付款） |
|---|---|---|
| 技能 | deck-storyline、deck-build、deck-exhibits、deck-review | 全部四个，另加 exhibits-pro、deck-recipes、brand-fit |
| 故事线（核心信息、SCQA、行动标题、只读标题测试） | ✓ | ✓ |
| 版式 | 12 种核心版式 | 12 种核心版式，另加 10 类演示文稿的页面规划 |
| 你的模板 | 使用模板自带的版式和占位符 | 另加复杂模板的品牌映射，并能把旧演示文稿迁移到新模板 |
| 图表 | 6 种：条形图、折线图、堆积柱状图、高亮表格、2×2 矩阵、流程箭头图 | 21 种：上述 6 种，另加瀑布图、Mekko 图、甘特路线图、哈维球表、价值驱动树、议题树、龙卷风图、漏斗图、变化箭头柱状图、四象限散点图、热力图表格、RAG 记分卡、组织架构图、RACI、基准点图 |
| 审阅任何 .pptx | ✓ | ✓，另加品牌检查 |
| 示例 | 3 份演示文稿，其中一份有审阅前后对比 | 另加 10 份，每个方案一份 |
| 故事线工作表（PDF） | | ✓ |
| 更新 | 本仓库 | 12 个月内的所有 v1.x 版本 |
| 许可 | MIT | 限一人使用，演示文稿数量不限 |

## Pro

免费版已能做出完整的演示文稿。Pro 用于更难的场景。

- **另加 15 种图表**，全部原生、可编辑：瀑布图、Mekko 图、甘特路线图、哈维球表、价值驱动树、议题树、龙卷风图、漏斗图、变化箭头柱状图、四象限散点图、热力图表格、RAG 记分卡、组织架构图、RACI、基准点图
- **10 个演示文稿方案**，每个都附完整示例（.pptx 和 PDF）：战略建议、市场进入、董事会审议、融资、指导委员会、商业论证、尽职调查、产品路线图、复盘、客户提案
- **brand-fit**：映射复杂的公司模板，并把旧演示文稿迁移过去
- 一页故事线工作表，以及 12 个月内的所有 v1.x 更新

$29 一次性付款 · 14 天退款 · 限一人使用，演示文稿数量不限

**[查看 SoWhat Decks Pro 的内容](https://sowhatlabs.gumroad.com/l/sowhat-decks-pro)**

## 限制

- 渲染使用 LibreOffice。没有它时，deck-review 只做结构检查，跳过视觉检查。
- PowerPoint 的换行可能和 LibreOffice 或 Keynote 略有不同。发送前请在 PowerPoint 中打开最终版本检查。
- 免费版绘制 6 种图表。瀑布图、Mekko 图、树状图和路线图在 Pro 中。
- 母版很多或占位符不常见的模板，在免费版中可能需要手动映射版式。
- deck-review 只读取 .pptx。它打不开 .ppt、.key 或有密码保护的文件，也不检查 SmartArt 和嵌入对象的内部。
- deck-review 的自动检查会有遗漏。它判断“以图片粘贴的图表”靠的是寻找深色坐标轴线；在示例 03 的 12 个主题词标题中，标题检查漏掉了一个，后来在评分标准的只读标题环节发现。
- Google 幻灯片：导入 .pptx 即可。这些技能不调用 Google Slides API。
- 已在 macOS 上的 Claude Code 中用英文和韩文演示文稿测试。日文只做过冒烟测试。其他智能体尚未测试。
- 幻灯片语言设置（deck-build 的 `meta.language`）只有 `en`、`ko`、`ja` 三种，其中 `ko` 和 `ja` 会设置对应的东亚字体。中文没有对应设置，中文幻灯片还没有测试过。
- Claude 应用和 Claude for PowerPoint：每个 SKILL.md 都有为聊天和 Claude for PowerPoint 设计的无代码模式，但还没有在那里测试过。

## 隐私

脚本在你的电脑上运行，不发起任何网络请求。智能体能看到你给它的文件。LibreOffice 渲染时可能会访问演示文稿中嵌入的链接，所以对陌生人发来的文件，请用 `--no-render` 运行 deck-review。

## 开发

    python3 -m pip install python-pptx pypdfium2 pytest
    python3 -m pytest -q

渲染测试只在安装了 LibreOffice 时运行。修改仓库的规则见 `AGENTS.md`。`tools/build_skill_zips.py` 生成发布用的 ZIP（发布工作流在每个 `v*` 标签上运行它），`tools/make_readme_images.py` 用示例幻灯片重新生成 `docs/img/` 中的图片。

## 许可证

MIT。示例演示文稿使用注明来源的公开数据，或标注为样例数据的数据。投资人更新示例是用公开文件制作的示意，与其描述的公司无关联。示例是开发期间由 Claude Code 智能体按照这些技能制作的，每个示例的 README 都重述了提示词并列出命令。

SoWhat Decks 是独立项目，与 Anthropic 和 Microsoft 无关联。

本文是[英文 README](README.md) 的译文。如有出入，以英文版为准。
