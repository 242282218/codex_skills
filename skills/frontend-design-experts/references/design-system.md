# 设计系统规范

## 色彩系统

### 主色调
- 主色: #667EEA (紫蓝)
- 成功: #4FACE (蓝)
- 警告: #FA7099 (粉)
- 危险: #EF4444 (红)
- 信息: #F093FB (紫)

### 中性色
- 背景主: #FFFFFF / #1F2937 (深色)
- 背景次: #F9FAFB / #111827 (深色)
- 文字主: #111827 / #F9FAFB (深色)
- 文字次: #6B7280 / #D1D5DB (深色)
- 边框: #E5E7EB / #374151 (深色)

### 渐变
- 主渐变: linear-gradient(135deg, #667EEA 0%, #764BA2 100%)
- 成功渐变: linear-gradient(135deg, #4FACE 0%, #00D4FF 100%)
- 警告渐变: linear-gradient(135deg, #FA7099 0%, #F093FB 100%)

## 排版系统

### 字体
- 主字体: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
- 等宽字体: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace

### 字号
- H1: 32px / 1.2 / 700
- H2: 28px / 1.3 / 600
- H3: 24px / 1.4 / 600
- H4: 20px / 1.5 / 600
- Body: 14px / 1.6 / 400
- Small: 12px / 1.5 / 400
- Tiny: 11px / 1.4 / 400

## 间距系统

基础单位: 4px

- xs: 4px
- sm: 8px
- md: 12px
- lg: 16px
- xl: 20px
- 2xl: 24px
- 3xl: 32px
- 4xl: 40px

## 圆角系统

- sm: 4px
- md: 8px
- lg: 12px
- xl: 16px
- 2xl: 20px
- full: 9999px

## 阴影系统

- sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
- md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
- lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)
- xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)

## 动画规范

### 时长
- 快速: 150ms (反馈、悬停)
- 标准: 300ms (过渡、打开)
- 缓慢: 500ms (进入、离开)

### 缓动函数
- 标准: cubic-bezier(0.4, 0, 0.2, 1)
- 进入: cubic-bezier(0.34, 1.56, 0.64, 1)
- 离开: cubic-bezier(0.4, 0, 0.6, 1)
- 弹性: cubic-bezier(0.68, -0.55, 0.265, 1.55)

## 响应式断点

- xs: 0px
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

## 无障碍规范

- 最小触摸目标: 44x44px
- 最小文字大小: 12px
- 对比度: WCAG AA (4.5:1 for text)
- 焦点指示器: 2px solid outline
- 键盘导航: Tab 顺序合理
