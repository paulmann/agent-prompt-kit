# agent-prompt-kit

[![许可证：MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![模块](https://img.shields.io/badge/modules-14-6f42c1)](PROMPT.md)
[![代码检查](https://img.shields.io/badge/lint-prompt__lint.py-informational)](tools/prompt_lint.py)
[![经验](https://img.shields.io/badge/experience-reuse-0f766e)](skills/experience-reuse/SKILL.md)
[![规则](https://img.shields.io/badge/lint%20rules-27-brightgreen)](tools/prompt_lint.py)
[![俄语版](https://img.shields.io/badge/lang-EN%20%2F%20RU-0ea5e9)](README.ru.md)

<!-- md-i18n:switcher -->
**其他语言：** [English](README.md) · [Deutsch](README.de.md) · 中文 · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Русский](README.ru.md)

<img src="https://github.com/paulmann/agent-prompt-kit/raw/main/assets/social-preview.png"
     alt="agent-prompt-kit —— 一套可移植的系统提示词，让智能体成为某个主题的专家"
     width="100%">

一个好的回答会随聊天一起消失。下一次遇到同一类工作时，新会话又从零开始：同样的摸索、同样的
死路、同样的问题。这套工具让这种重复变便宜——不是靠记得更牢，而是靠留下一个**已注册的工作
环境**。

一条命令，一个结果：一个目录——工作区，或一个已保存的智能体——里面已经备好该类工作的规则、
带可检验验收标准的领域卡、包含一个失败案例的可复用范例、既往工作库，以及给下一个窗口的
起始提示词。

| 命令做什么 | 为什么重要 |
|---|---|
| 读取当前会话**以及运行时的相关会话** | 素材是真实的工作，而不是对工作的描述 |
| 动手之前先写出任务卡（Task Card）与领域卡（Domain Card） | 主题是被声明的，不是被假设的 |
| 创建环境目录，每一部分都在位 | 下一轮从第十一步开始，而不是第一步 |
| 按运行时说明注册步骤 | HARNESS：一次点击；AutoClaw2：一次重新加载；假装不是这样，才是缺陷 |
| 交出一份起始提示词 | 没有交接的目录是博物馆，不是工作场所 |

本仓库中关于运行时的每一处说法，都标注为「此处实测」或「来自会话报告」——见
[`docs/INSTALL.md`](docs/INSTALL.md)。

> **状态。** 这里的每个数字都是 2026-10-24 针对 1.2.0 版用
> `python tools/prompt_lint.py` 实测得到的。较长的指南在 [`docs/`](docs/) 和
> [Wiki](https://github.com/paulmann/agent-prompt-kit/wiki) 中。

## 目录

- [这是什么](#这是什么)
- [数字一览](#数字一览)
- [安装](#安装)
- [运行时](#运行时)
- [使用方法](#使用方法)
- [十四个模块](#十四个模块)
- [经验复用](#经验复用)
- [质量闸门](#质量闸门)
- [可移植性](#可移植性)
- [文档](#文档)
- [语言](#语言)
- [开发](#开发)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

## 这是什么

一个文件 `PROMPT.md`，加上为了信任它、改造它所需的材料。

| 部件 | 它给你什么 |
|---|---|
| [`PROMPT.md`](PROMPT.md) | 系统提示词：14 个模块、14 项自检、10 条不变式 |
| [`AGENTS.md`](AGENTS.md) | 同一契约的机器可读形式，供读取仓库规则的编码智能体使用 |
| [`skills/experience-reuse/`](skills/experience-reuse/SKILL.md) | M13 技能：工作流程、适用性检查清单、四个记录模板、一份安全策略 |
| [`tools/experience.py`](tools/experience.py) | 经验库及其一条命令检索，含模式与密钥检查 |
| [`memory/`](memory/README.md) | 记录存放的位置；随套件附带三个已脱敏示例 |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | 校验模块完整性、翻译配对、占位符、链接、密钥、版本一致性、M13 与闸门宽度 |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | 三个领域，同一形态：常规案例、歧义案例、失败案例 |
| [`docs/`](docs/) | 设计理由、改造协议、QA 检查清单、对照目标的验证 |

这套提示词按下列顺序解决五个具体问题：

1. **主题漂移**——智能体去回答旁边那个更容易的问题。对策是任务卡（M1）与领域卡（M2）：
   它们必须在任何动作之前存在。
2. **编造的上下文**——对一条从未读过的消息线说「正如我们前面讨论过的」。对策是上下文台账
   （M3）与三种证据标签（M4）。
3. **无法核实的断言**——没有任何观察就声称「它能用」。对策是作业循环（M5）、能力表（M6）
   与闸门（M8）。
4. **重复劳动**——同一个任务被重新推导，因为没有任何东西把上一次的尝试呈现出来。对策是
   经验库及其适用性检查（M13）。
5. **复用成本**——换一个领域就得重写提示词。对策是专业化协议（M10）：一张卡、一个范例
   文件、一行验收标准。

## 数字一览

2026-10-24 在本仓库树中实测：

| 指标 | 数值 | 测量来源 |
|---|---:|---|
| 提示词中的模块 | 14 | `PROMPT.md`，标题 `M0`…`M13` |
| 自检行 | 14 | `grep -c '^\*\*Check:\*\*' PROMPT.md` |
| 不变式 | 10 | `PROMPT.md`，章节「Invariants」 |
| 质量闸门测试 | 12 | `PROMPT.md`，章节 M8 |
| 检查器中互不相同的规则标识 | 27 | `grep -o 'add("[a-z]*", "[a-z.-]*"' tools/prompt_lint.py \| sort -u` |
| 经验库自测 | 13 | `python tools/experience.py selftest` |
| 完整范例 | 3 + 3 条已脱敏记录 | `examples/`、`skills/experience-reuse/examples/` |
| 运行时依赖 | 0 | `tools/` 中的导入 |

## 安装

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit

python tools/prompt_lint.py            # exit 0 means the document is structurally complete
```

只需要 Python 3.11+。没有软件包，没有服务，没有账号。

## 运行时

同一套流程，三种不同的机制。模型能做什么、人必须做什么，每个运行时都不一样，这张表说清哪个
是哪个——或在本机实测，或标注为来自会话报告。

| 运行时 | 命令 | 模型做什么 | 人做什么 | 验证状态 |
|---|---|---|---|---|
| **AutoClaw2** | `/agent-prompt-kit`（也可用 `/skill:agent-prompt-kit`） | 把技能写入 `%USERPROFILE%\.pi\agent\skills\`，把命令写入 `...\prompts\` | 重新加载，让资源快照重建 | 在应用包内实测 |
| **HARNESS** | `/agent-prompt-kit` | 创建整个工作区目录及其全部文件 | 一次点击：把该目录添加为工作区 | 机制在此实测；点击来自报告 |
| **SagaAI** | — | 把 `PROMPT.md` 粘贴为作业契约 | 按运行时的要求操作 | **未验证**：安装器拒绝猜测 |

```bash
python tools/install.py --runtime autoclaw2 --check    # files plus registration state
python tools/install.py --runtime autoClaw2 --write    # install, backup anything it replaces
python tools/install.py --runtime harness  --write
```

安装器从不把需要人工的步骤报成已完成。在 HARNESS 中它打印那次点击；在 AutoClaw2 中它检查
资源清单，并在重新加载发生之前一直说 `NOT READY`。完整机制与陷阱表：
[`docs/INSTALL.md`](docs/INSTALL.md)。

## 使用方法

1. 打开 `PROMPT.md`。
2. 把 YAML 头部以下的所有内容粘贴到智能体的系统提示词字段。
3. 给智能体一个真实请求。它必须用任务卡、领域卡、交付物、证据标签和一行闸门结论来回答。

这套提示词刻意不绑定具体工具——见[可移植性](#可移植性)。三个互不相关领域的完整作答
示例在 [`examples/EXAMPLES.md`](examples/EXAMPLES.md)。

## 十四个模块

| 模块 | 它回答的问题 | 由什么验证 |
|---|---|---|
| M0 | 这是谁的声音，分哪两个阶段？ | 主体用一句话点名 |
| M1 | 实际被问的是什么？ | 任务卡，每个字段都填好或标为 `unknown` |
| M2 | 需要哪类专家，什么必须被验证？ | 领域卡，验收条件可检验 |
| M3 | 存在哪些上下文，它们有多好？ | 上下文台账，每条主张都有来源 |
| M4 | 我如何标注自己知道的东西？ | `[fact]` / `[inference]` / `[assumption]` |
| M5 | 如何在不破坏东西的前提下工作？ | 循环：界定 → 检索 → 计划 → 执行 → 验证 → 记录 |
| M6 | 我可以用什么，什么被禁止？ | 能力表、安全规则 |
| M7 | 回答是什么形状？ | 五个部分，外加可选的经验复用部分 |
| M8 | 我怎么知道它完成了？ | 十二项闸门，以一行汇报 |
| M9 | 这套提示词会怎么被击破？ | 十六种失效模式及其对策 |
| M10 | 如何把它指向一个新领域？ | 一张卡、一个范例文件、一行验收标准 |
| M11 | 好的回答长什么样？ | 三个完整范例 |
| M12 | 发送之前我检查什么？ | 五个问题，每个用一行回答 |
| M13 | 如何避免重做已经做过的工作？ | 计划前先检索、适用性判定、已脱敏的库 |

## 经验复用

M13 把「我们以前做过这个」从一句指望变成一次工具调用：

```bash
python tools/experience.py search "add nullable column to list endpoint" --limit 5
```

```text
query: add nullable column to list endpoint  ·  2 candidate(s)
  [ 25] recipe    add-nullable-column-to-list-endpoint validated overlap 5, validated, high confidence, verified 2d ago
  [ 11] failure   retry-migration-until-it-passes    validated overlap 1, validated, prior failure: read before acting
```

每一行都带着它排在这个位置的理由，因此智能体可以凭证据而不是凭感觉否掉一个候选。六个
问题决定是否复用——目标、环境、假设、验证覆盖、安全、时效——没有说明的改造算作盲抄。

它自己的测试实测出的拒绝项：含有形似密钥字面量的记录、缺少 `Rollback` 部分的配方、
没有 `last_verified_at` 却被标为 `validated` 的记录。它会警告的：超过 180 天的验证、
近乎重复的标题。它从不会做的：删除——记录以弃用方式处理，并指向替代它的那条。

## 质量闸门

智能体必须打印一行，例如 `gate 12/12` 或 `gate 10/12 — 6, 9 failed: <reason>`。这十二项
测试定义在 M8 中；实践中失败最频繁的两项是：

- **#4 证据覆盖**——一条从未进入上下文台账的事实性主张；
- **#6 验证**——没有任何命令或观察就声称「它能用」。

闸门行不是装饰：它让没看着智能体工作的那个人也能审计这份回答。`docs/QA.md` 把同样这
十二项测试变成一份人工评审检查清单。

## 可移植性

提示词里不出现任何工具名。能力按类别命名，并按运行时解析：

| 能力类别 | 映射示例 |
|---|---|
| `read-files` | 读取工具、shell `cat`、编辑器缓冲区 |
| `write-files` | 写入/补丁工具、heredoc、行内建议 |
| `run-commands` | shell、沙箱、CI 运行器 |
| `web-search` | 检索工具、浏览器、由用户提供的已抓取 URL |
| `publish` | git push、包仓库、wiki API |

如果某个运行时缺少某项能力，提示词会显式降级（M6）：它请求内容、把产物以文本形式给出，
或者点名缺失的能力。它从不假装。

已验证的导入目标：AutoClaw2、HARNESS、SagaAI，以及任何接受系统提示词的智能体。面向
机器的变体是 [`AGENTS.md`](AGENTS.md)。

## 文档

| 文档 | 内容 |
|---|---|
| [`docs/DESIGN.md`](docs/DESIGN.md) | 为什么用模块，哪些决策被否掉以及原因 |
| [`docs/ADAPTATION.md`](docs/ADAPTATION.md) | 十五分钟在新领域中完成专业化 |
| [`docs/QA.md`](docs/QA.md) | 由闸门导出的人工评审检查清单 |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | 最初的目标，逐条需求，附每条的检查方式 |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | 三个领域、三张卡、三行闸门结论 |

## 语言

英文文件是正本；俄语译本带 `.ru.md` 后缀——这是 GitHub 自己用的约定。两者由
`tools/prompt_lint.py` 保持同步：只要某个文档没有配对译本，它就让构建失败。

| 英语 | 俄语 |
|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) |
| [PROMPT.md](PROMPT.md) | [PROMPT.ru.md](PROMPT.ru.md) |
| [AGENTS.md](AGENTS.md) | [AGENTS.ru.md](AGENTS.ru.md) |
| [docs/VALIDATION.md](docs/VALIDATION.md) | [docs/VALIDATION.ru.md](docs/VALIDATION.ru.md) |

## 开发

```bash
python tools/prompt_lint.py            # structural contracts
python tools/prompt_lint.py --json     # machine-readable findings
```

修改提示词：

1. 编辑 `PROMPT.md`；保持模块标识稳定——工具和评审都会引用它们。
2. 在同一次提交中更新 `PROMPT.ru.md`。
3. 提升头部元数据里的 `version`，并在 `CHANGELOG.md` 中加一条；检查器会比较两者。
4. 反复运行检查，直到它返回 `0`。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。安全策略：[SECURITY.md](SECURITY.md)。

## 许可证

[MIT](LICENSE)。
