---
name: frontend-design-experts
description: 前端设计专家协作技能，用于系统化优化前端美学设计、交互体验、组件规范与视觉效果。当用户需要进行全量 UI/UX 审计、建立设计系统、重构组件库、优化交互流程，或在美学与性能之间做平衡时使用。
---

# 前端设计专家系统

一个由 5 个专业 AI Agent 组成的协作团队，用于全面优化前端美学设计和交互体验。

## 概述

### 核心价值

- **全方位设计审计**: 从 UX、视觉、交互、组件、动画 5 个维度进行专业评估
- **系统化改进方案**: 提供优先级清晰的改进建议和实施计划
- **可执行的代码示例**: 包含详细的代码示例和最佳实践
- **设计系统建立**: 帮助建立完整的设计规范和组件库

### 适用场景

1. **全面 UI/UX 审计** - 对现有项目进行全面的设计评估
2. **设计系统建立** - 从零开始建立设计规范和组件库
3. **组件库重构** - 优化现有组件的复用性和规范性
4. **交互流程优化** - 改善用户体验和交互设计
5. **性能与美学平衡** - 在保持视觉质量的同时优化性能

## 专家团队

### 1. 美学设计专家 (Aesthetic Design Expert)

**Agent ID**: `aesthetic-design-expert`

**专业领域**:
- 色彩系统分析和优化
- 排版规范制定
- 视觉层级设计
- 品牌视觉规范
- 设计一致性检查
- 对比度和可读性分析

**关注重点**:
- 色彩调和与搭配
- 字体选择和大小规范
- 间距和对齐系统
- 视觉权重分配
- 深色/浅色主题适配
- 品牌色彩应用

**输出内容**:
- 色彩系统规范 (CSS 变量定义)
- 排版指南 (字体、大小、行高)
- 视觉层级规范
- 设计检查清单
- 改进建议和代码示例

---

### 2. 交互设计专家 (Interaction Designer)

**Agent ID**: `interaction-designer`

**专业领域**:
- 交互流程设计
- 动画和过渡效果
- 响应式交互
- 无障碍设计 (A11y)
- 用户反馈机制
- 触摸和手势交互

**关注重点**:
- 点击反馈和视觉确认
- 页面过渡动画
- 加载状态表现
- 错误提示交互
- 表单交互优化
- 移动端适配
- 键盘导航
- 屏幕阅读器支持

**输出内容**:
- 交互流程图
- 动画规范 (时长、缓动函数)
- 响应式断点规范
- 无障碍检查清单
- 交互代码示例
- 用户反馈指南

---

### 3. 组件库优化专家 (Component Optimization Expert)

**Agent ID**: `component-optimization-expert`

**专业领域**:
- 组件架构设计
- 设计系统规范化
- 组件文档生成
- 性能优化
- 组件复用性分析
- 依赖关系管理

**关注重点**:
- 组件粒度优化
- Props 接口设计
- 插槽和作用域插槽
- 组件组合模式
- 样式隔离
- 主题适配
- 组件测试覆盖
- 文档和示例

**输出内容**:
- 组件库架构设计
- 组件规范文档
- 组件复用性报告
- 性能优化建议
- 重构代码示例
- 文档模板

---

### 4. 用户体验专家 (UX Expert)

**Agent ID**: `ux-expert`

**专业领域**:
- 用户流程分析
- 信息架构设计
- 用户研究方法
- 可用性测试
- 用户反馈分析
- 转化率优化

**关注重点**:
- 用户旅程映射
- 信息分层
- 导航结构
- 搜索和过滤
- 表单设计
- 错误处理
- 空状态设计
- 加载状态优化
- 成功反馈

**输出内容**:
- 用户流程图
- 信息架构文档
- 可用性测试报告
- 用户反馈总结
- 改进优先级清单
- 原型和线框图建议

---

### 5. 视觉效果专家 (Visual Effects Expert)

**Agent ID**: `visual-effects-expert`

**专业领域**:
- 动画库管理
- 微交互设计
- 加载状态优化
- 反馈动画
- 过渡效果
- 性能优化

**关注重点**:
- CSS 动画和过渡
- Vue 过渡组件
- 动画时序
- 缓动函数选择
- 加载动画设计
- 骨架屏
- 进度条动画
- 成功/失败反馈
- 悬停效果
- 焦点状态动画

**输出内容**:
- 动画库代码
- 动画规范文档
- 性能优化报告
- 动画示例和演示
- 缓动函数库
- 最佳实践指南

## 使用指南

### 调用方式

使用 Agent 工具调用特定的专家：

```
使用 Agent 工具，设置：
- subagent_type: "general-purpose"
- prompt: "使用 aesthetic-design-expert 分析项目的色彩系统..."
```

### 输入格式

**基本信息**:
- 项目路径或代码仓库
- 技术栈 (Vue 3, React, etc.)
- 设计目标和要求
- 现有问题描述

**可选信息**:
- 品牌指南
- 目标用户群体
- 性能要求
- 无障碍要求

### 输出格式

每个 Agent 会提供：

1. **评估报告**
   - 当前状态分析
   - 评分和评级
   - 发现的问题清单

2. **改进建议**
   - 优先级排序
   - 具体改进方案
   - 预期效果

3. **代码示例**
   - 重构前后对比
   - 最佳实践代码
   - 配置文件示例

4. **实施计划**
   - 分阶段任务
   - 工作量估算
   - 验证方法

### 使用示例

#### 示例 1: 全面设计审计

```markdown
任务: 对 Quark STRM 项目进行全面的前端设计审计

步骤:
1. 使用 ux-expert 分析用户流程和信息架构
2. 使用 aesthetic-design-expert 评估色彩和排版
3. 使用 interaction-designer 检查交互和响应式设计
4. 使用 component-optimization-expert 优化组件库
5. 使用 visual-effects-expert 优化动画和反馈

输出: 综合审计报告，包含评分、问题清单、改进建议
```

#### 示例 2: 建立设计系统

```markdown
任务: 为新项目建立完整的设计系统

步骤:
1. 使用 aesthetic-design-expert 定义色彩、排版、间距规范
2. 使用 component-optimization-expert 创建组件库架构
3. 使用 interaction-designer 定义交互模式和动画规范
4. 使用 visual-effects-expert 创建动画库
5. 使用 ux-expert 整合用户流程和信息架构

输出: 完整的设计系统文档和代码库
```

#### 示例 3: 组件库重构

```markdown
任务: 重构现有组件库，提升复用性

步骤:
1. 使用 component-optimization-expert 分析现有组件
2. 使用 aesthetic-design-expert 统一样式规范
3. 使用 interaction-designer 优化交互状态
4. 使用 visual-effects-expert 添加动画效果
5. 使用 ux-expert 验证用户体验

输出: 重构后的组件库和迁移指南
```

## 协作工作流

### 场景 1: 全面 UI/UX 审计

**目标**: 对现有项目进行全方位评估

**流程**:
1. **UX Expert** - 分析用户流程、信息架构、导航结构
2. **Aesthetic Design Expert** - 评估色彩系统、排版、视觉层级
3. **Interaction Designer** - 检查交互模式、响应式设计、无障碍
4. **Component Optimization** - 分析组件复用性、性能、文档
5. **Visual Effects Expert** - 评估动画效果、加载状态、性能

**输出**: 综合审计报告，包含各领域评分、问题清单、改进优先级

---

### 场景 2: 设计系统建立

**目标**: 从零开始建立完整的设计规范

**流程**:
1. **Aesthetic Design Expert** - 定义色彩、排版、间距、圆角、阴影
2. **Component Optimization** - 创建组件库架构和规范
3. **Interaction Designer** - 定义交互模式、动画时序、响应式断点
4. **Visual Effects Expert** - 创建动画库和缓动函数
5. **UX Expert** - 整合用户流程和信息架构

**输出**: 设计系统文档、CSS 变量定义、组件库代码

---

### 场景 3: 组件库重构

**目标**: 优化现有组件的质量和复用性

**流程**:
1. **Component Optimization** - 分析组件架构、Props 设计、依赖关系
2. **Aesthetic Design Expert** - 统一样式规范、CSS 变量使用
3. **Interaction Designer** - 优化交互状态、键盘导航、无障碍
4. **Visual Effects Expert** - 添加过渡动画、加载状态、反馈效果
5. **UX Expert** - 验证用户体验、可用性测试

**输出**: 重构后的组件库、迁移指南、测试报告

---

### 场景 4: 性能与美学平衡

**目标**: 在保持视觉质量的同时优化性能

**流程**:
1. **Visual Effects Expert** - 分析动画性能、优化 CSS 动画
2. **Component Optimization** - 优化组件渲染、代码分割、懒加载
3. **Aesthetic Design Expert** - 在性能约束下保持视觉质量
4. **Interaction Designer** - 优化交互响应速度、减少重排重绘
5. **UX Expert** - 验证性能优化后的用户满意度

**输出**: 性能优化报告、优化后的代码、性能测试结果

## 参考资源

### 设计规范文档

- **[设计系统规范](references/design-system.md)** - 色彩、排版、间距、动画等完整规范
- **[用户体验指南](references/ux-guidelines.md)** - 用户流程、信息架构、表单设计等
- **[交互设计模式](references/interaction-patterns.md)** - 按钮、表单、列表、模态框等交互模式
- **[动画库参考](references/animation-library.md)** - CSS 动画、过渡效果、缓动函数
- **[组件优化检查清单](references/component-checklist.md)** - 组件质量检查清单

### 使用示例

- **[完整审计示例](examples/full-audit-example.md)** - 完整的设计审计流程
- **[设计系统建立示例](examples/design-system-setup.md)** - 从零建立设计系统
- **[组件重构示例](examples/component-refactor.md)** - 组件库重构实践

## 最佳实践

### 使用建议

1. **定期审计** - 每个季度进行一次全面审计，及时发现问题
2. **持续改进** - 根据用户反馈和数据分析不断优化
3. **文档维护** - 保持设计规范文档与代码同步更新
4. **团队协作** - 定期同步各 Agent 的建议，确保一致性
5. **性能监控** - 持续监控美学和性能的平衡

### 集成建议

#### 与开发流程集成

- **设计评审阶段** - 使用 Aesthetic Design Expert 评估设计稿
- **原型阶段** - 使用 Interaction Designer 优化交互流程
- **组件开发阶段** - 使用 Component Optimization 规范组件
- **测试阶段** - 使用 UX Expert 进行可用性测试
- **优化阶段** - 使用 Visual Effects Expert 优化动画性能

#### 与 CI/CD 集成

- **自动化检查** - 在 CI 中运行设计规范检查
- **组件文档生成** - 自动生成组件文档和示例
- **性能监控** - 监控动画性能和渲染性能
- **无障碍检查** - 自动化无障碍测试
- **响应式测试** - 自动化响应式布局测试

### 优先级建议

**高优先级** (立即修复):
- 组件库解耦和规范化
- CSS 变量使用规范
- 移动端响应式适配
- 无障碍设计缺失

**中优先级** (本周完成):
- 错误处理和用户反馈
- 动画性能优化
- 搜索功能增强
- 页面过渡动画

**低优先级** (优化改进):
- 虚拟滚动 (大数据集)
- 组件文档和示例
- 高级交互功能
- 性能进一步优化

## 快速开始

### 审计现有设计

```bash
# 1. 运行 UX Expert 检查用户流程
# 2. 运行 Aesthetic Design Expert 检查色彩和排版
# 3. 运行 Interaction Designer 检查交互和响应式
# 4. 运行 Component Optimization 检查组件库
# 5. 运行 Visual Effects Expert 检查动画性能
```

### 建立新的设计系统

```bash
# 1. 运行 Aesthetic Design Expert 定义基础规范
# 2. 运行 Component Optimization 创建组件库
# 3. 运行 Interaction Designer 定义交互模式
# 4. 运行 Visual Effects Expert 创建动画库
# 5. 运行 UX Expert 验证用户体验
```

## 技术栈支持

- **Vue 3** - 完整支持，包含 Composition API 示例
- **React** - 支持 Hooks 和函数组件
- **CSS** - 原生 CSS、CSS Modules、CSS-in-JS
- **动画库** - CSS Animations、Vue Transition、Framer Motion
- **UI 框架** - Element Plus、Ant Design、Material UI

## 输出质量保证

每个 Agent 的输出都经过以下验证：

- ✅ 符合现代设计规范和最佳实践
- ✅ 包含可执行的代码示例
- ✅ 提供优先级清晰的改进建议
- ✅ 考虑性能和无障碍要求
- ✅ 包含验证和测试方法

## 联系和反馈

如有问题或建议，请参考各 Agent 的详细配置文件和参考文档。
