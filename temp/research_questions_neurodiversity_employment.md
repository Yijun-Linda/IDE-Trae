# 心智障碍青年就业支持研究核心问题

项目：TRAE SOLO 挑战赛「Hello AI 科技致善」公益赛道
命题：心智障碍群体就业支持
研究场景：上海塘桥街道"塘·空间"（梦工坊咖啡馆）
日期：2026-04-16

---

## 核心待验证假设

心智障碍青年在就业场景中最大的卡点到底是什么？

### 假设一：视觉提示的形式适配性

**假设陈述**：心智障碍青年在理解复杂工作流程时高度依赖视觉支持，但视觉提示的有效性取决于其具体形式（文字、静态图片、动态视频）与任务复杂度、个体认知能力的匹配程度。

**待验证子问题**：
1. 在梦工坊咖啡馆的具体工作场景中，哪些任务步骤需要视觉提示支持？
2. 当前使用的视觉提示是什么形式？（纸质清单、图片卡片、视频演示、口头指令等）
3. 不同形式视觉提示的使用效果如何？（青年能否独立完成任务、需要多少次提示、完成时间等）
4. 是否存在"提示过度"或"提示不足"的情况？（认知负荷是否合适）
5. 个体差异如何影响视觉提示形式的选择？（读写能力、认知水平、感官偏好等）

**文献依据**：
- 视频示范（Video Modeling）对自闭症青少年和成人的工作技能训练有显著效果（Meta分析，PMC8992915）
- 辅助技术效果量：PND 91%，SMD 2.84（Morash-Macneil 2018）
- 提示系统研究：最少到最多提示（Least-to-Most Prompting）和最多到最少提示（Most-to-Most Prompting）都有效，但适用场景不同
- 现有商业应用（Task Analysis Lite, Work Autonomy, MeMINDER）主要聚焦于任务提示和视觉支持

**假设推导：你的说法中包含的子假设**

当你问"心智障碍青年是否高度依赖视觉"时，实际上隐含了以下未经检验的假设：

| 层级 | 隐含假设 | 潜在问题 |
|------|---------|---------|
| **形式假设** | 视觉提示优于其他感官通道（听觉、触觉） | 文献显示多感官整合往往比单一视觉更有效 |
| **普适假设** | 所有心智障碍青年都适用视觉提示 | 个体差异极大，自闭症与智力障碍的感官偏好可能不同 |
| **线性假设** | 视频 > 图片 > 文字（效果排序） | 实际上取决于任务类型：简单任务图片足够，复杂任务才需要视频 |
| **静态假设** | 视觉形式一旦确定就固定使用 | 文献支持"渐进式淡出"（prompt fading），提示应随能力提升而减少 |
| **技术假设** | 数字化视觉提示优于纸质提示 | 未考虑技术接受度、设备可用性、辅导员配置能力等现实约束 |
| **因果假设** | 视觉提示不足是导致任务失败的主因 | 可能忽略了动机、情绪、环境干扰等其他因素 |

**关键洞察**：

你的问题本身揭示了一个更根本的研究方向——不是"哪种视觉形式最好"，而是：

1. **匹配问题**：如何为特定个体、特定任务、特定场景匹配最合适的提示形式？
2. **层级问题**：如何设计从最多支持到最少支持的渐进式提示系统？
3. **反馈问题**：如何根据青年的实时表现动态调整提示策略？

这正是 AI 可以发挥作用的地方：不是替代现有的视觉提示，而是让提示系统变得**自适应**——根据任务复杂度、个体能力、实时表现，智能选择最合适的提示形式和内容。

---

### 假设一修正：从"视觉形式选择"到"异质性适配"

**核心认知跃迁**：心智障碍青年是一个极具异质性的群体，设计一套通用的视觉形式不可行。

**亚群体差异分析**：

| 亚群体 | 认知特点 | 视觉偏好 | 潜在陷阱 |
|--------|---------|---------|---------|
| **自闭症谱系** | 极佳的视觉学习者，但存在感官敏感性 | 有人对文字规律极度敏感，有人完全依赖图形；可能对动态信息过载 | 统一使用视频可能适得其反 |
| **唐氏综合征** | 听觉短期记忆短板，社交动机强 | 需要长时间留存的视觉提示，偏好社交互动式学习 | 纯静态图片可能缺乏互动性 |
| **智力障碍（非特指）** | 抽象思维受限，具体化学习为主 | 高度依赖图形化、步骤化提示 | 文字提示几乎无效 |

**认知负荷视角的重新审视**：

- **文字**：需要抽象解码，对许多心智障碍者门槛过高，在特殊教育语境下通常不被视作直接的视觉支持
- **图片**：直观但缺乏动态过程，对于需要连贯动作的任务可能不够明确
- **视频**：展现全过程但包含大量转瞬即逝的冗余信息，会极大挑战工作记忆，导致"看了后半段忘了前半段"

**对调研方法的影响**：

1. **样本分层**：观察时需记录每位青年的具体诊断类型（自闭症/唐氏/智力障碍等），而非混为一谈
2. **任务分解粒度**：需要识别哪些任务是"步骤型"（适合图片序列）vs "流程型"（适合视频或动态演示）
3. **记忆辅助设计**：视频需要配合"暂停-回顾"机制，或分解为短视频片段，避免工作记忆超载
4. **辅导员策略差异**：观察辅导员是否针对不同青年使用不同的提示策略，以及他们如何判断"这个青年适合哪种形式"

**对产品设计的启示**：

这一认知跃迁意味着产品不能是"一套视觉方案适配所有人"，而需要具备以下特征：

1. **个性化配置**：允许辅导员为每个青年配置最适合的提示形式组合
2. **渐进式调整**：随着能力提升，能够从视频→图片→文字逐步淡出
3. **任务类型感知**：自动识别任务属性，推荐最合适的提示形式
4. **记忆辅助机制**：视频必须支持分段播放、重复观看、关键帧标记

**核心待验证假设的演进**：

从"哪种视觉形式最有效"演进为"如何为特定亚群体、特定任务、特定能力水平匹配最优的提示策略组合"。

---

## 现场观察重点

### 问题一：求助环节识别
心智障碍青年们在哪些环节需要反复求助？

### 问题二：督导干预模式
督导/辅导员反复提醒的事项是什么？

---

## 研究方法论

采用轻量级现场观察优先于完整文献综述。通过快速摸底梦工坊咖啡馆的真实工作场景，识别 friction points，再决定后续设计方向。

---

## 下一步行动

1. 联系"塘·空间"安排现场观察
2. 记录青年与督导的互动模式
3. 识别高频求助场景和重复提醒内容
4. 基于观察结果确定产品核心功能

---

## 文献检索关键词

### 中文关键词

宏观层面：心智障碍、智力障碍、就业支持、职业康复、支持性就业、庇护性就业、职业转衔

微观层面：工作流程、任务分解、视觉提示、社交沟通、职场适应、辅导员、就业辅导员、督导支持

### 英文关键词

宏观层面：intellectual disability、developmental disability、autism spectrum disorder、competitive integrated employment、supported employment、job coaching、workplace accommodation

微观层面：task analysis、visual supports、social skills training、job carving、natural supports、workplace buddy、systematic instruction

### 布尔逻辑检索式（推荐优先使用）

**检索式一：参与式方法在残障就业中的应用**

(intellectual disability OR developmental disability OR autism OR "intellectual developmental disorder") AND (employment OR workplace OR job) AND ("participatory design" OR "co-design" OR "co-creation" OR "user-centered" OR "person-centered")

**检索式二：工作场景中的任务支持策略**

(intellectual disability OR autism OR "down syndrome") AND (employment OR "supported employment") AND ("task analysis" OR "visual supports" OR "systematic instruction" OR "job coaching" OR "workplace accommodation")

**检索式三：就业辅导员角色与支持模式**

("job coach" OR "employment specialist" OR "support worker") AND (intellectual disability OR developmental disability) AND ("natural supports" OR "workplace buddy" OR mentoring OR scaffolding)

**检索式四：社交沟通障碍与职场适应**

(autism OR "autism spectrum disorder" OR ASD) AND employment AND ("social skills" OR communication OR "workplace social" OR "pragmatic language" OR "social navigation")

**检索式五：辅助技术在工作场所的应用**

(intellectual disability OR cognitive disability) AND employment AND ("assistive technology" OR "mobile app" OR "digital tool" OR "AI support" OR "just-in-time" OR prompting)

**检索式六：系统性综述与元分析（优先筛选）**

(intellectual disability OR developmental disability) AND employment AND (review OR "systematic review" OR meta-analysis OR "evidence-based" OR "best practice")

---

## 问题演变记录

**初始问题**：从文献综述找到 gap，再到社区做共创研究，产出源于真实需求的解决方案。

**深层意图反思**：现场观察虽然重要，但在去"塘·空间"之前，需要背景知识来指导观察。想知道该看什么、问什么，而不是盲目记录。文献综述的价值不是替代现场，而是建立初步观察框架，让现场观察更高效。

**策略调整**：先用"task analysis + intellectual disability + employment"和"视觉提示 + 心智障碍 + 就业"各搜3-5篇近五年综述，快速了解学术界认为最有效的支持策略及落地障碍，带着背景去现场观察。

---

## 关于 AI 在检索式中的定位

**提问**：为什么关键词里没有 AI？比赛是用选手的 AI 和 AI agent 工具能力设计作品，而不是让心智障碍者使用 AI 和 AI agent 工具帮助他们的工作？

**深层意图**：意识到比赛规则和产品设计之间可能存在张力。想确认是应该做一个"用 AI 工具开发的传统辅助产品"，还是做一个"让心智障碍者直接使用 AI"的前沿产品。这个问题的答案会影响技术选型和文献检索方向。

**回答**：TRAE 是 AI IDE 工具，比赛评审维度是"切题、实战、过程、社会价值"，重点在于开发者如何使用 AI 工具高效构建解决方案，而不是作品必须让心智障碍者直接使用 AI。但 AI 当然可以成为解决方案的一部分。检索式五已包含"AI support"和"assistive technology"。学术界关于"AI 直接辅助心智障碍者就业"的研究还很少，大多数文献集中在传统的视觉提示、任务分解、人工督导等成熟方法上。

**结论**：先理解基础支持策略，再判断哪些环节可以被 AI 增强。文献检索的首要目标是了解心智障碍者就业支持的基础原理和有效策略，而不是先入为主地假设 AI 是解决方案。

---

## 优先检索计划

**第一轮：基础理论与最佳实践**
- 检索式六：(intellectual disability OR developmental disability) AND employment AND (review OR "systematic review" OR meta-analysis OR "evidence-based" OR "best practice")
- 目标：了解领域内公认有效的干预方法

**第二轮：具体支持策略**
- 检索式二：(intellectual disability OR autism OR "down syndrome") AND (employment OR "supported employment") AND ("task analysis" OR "visual supports" OR "systematic instruction" OR "job coaching" OR "workplace accommodation")
- 目标：了解任务分解、视觉提示等具体策略的实施方式

**第三轮：辅助技术与 AI 应用**
- 检索式五：(intellectual disability OR cognitive disability) AND employment AND ("assistive technology" OR "mobile app" OR "digital tool" OR "AI support" OR "just-in-time" OR prompting)
- 目标：了解技术辅助工具在就业场景中的应用现状与可能性

---

*记录来源：与 AI 协作对话，确定从文献驱动转向现场验证的研究策略*
