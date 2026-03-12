# 动画库参考

## 基础过渡

### 淡入淡出
```css
.fade-enter-active,
.fade-leave-active {
  transition: opacity 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
```

### 滑动
```css
.slide-enter-active,
.slide-leave-active {
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
  transform: translateY(20px);
}

.slide-leave-to {
  transform: translateY(-20px);
}
```

### 缩放
```css
.scale-enter-active,
.scale-leave-active {
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.scale-enter-from,
.scale-leave-to {
  transform: scale(0.95);
}
```

## 微交互

### 按钮悬停
```css
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.btn:active {
  transform: translateY(0);
}
```

### 加载动画
```css
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### 脉冲动画
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

## 缓动函数库

### 标准缓动
- ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
- ease-in: cubic-bezier(0.4, 0, 1, 1)
- ease-out: cubic-bezier(0, 0, 0.2, 1)

### 弹性缓动
- bounce-in: cubic-bezier(0.68, -0.55, 0.265, 1.55)
- bounce-out: cubic-bezier(0.34, 1.56, 0.64, 1)

### 背弹缓动
- back-in: cubic-bezier(0.6, -0.28, 0.735, 0.045)
- back-out: cubic-bezier(0.175, 0.885, 0.32, 1.275)

## 页面过渡

### 淡入淡出过渡
```vue
<Transition name="fade">
  <component :is="currentComponent" />
</Transition>
```

### 滑动过渡
```vue
<Transition name="slide-left">
  <component :is="currentComponent" />
</Transition>
```

## 列表动画

### 列表进入
```css
.list-enter-active {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-move {
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

## 性能优化

### 使用 transform 和 opacity
- 避免改变 width/height
- 避免改变 position
- 使用 will-change 提示
- 使用 GPU 加速

### 禁用动画
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
