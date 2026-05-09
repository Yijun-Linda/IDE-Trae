# 更新可视化文件计划

## 背景
用户手动修改了 `SUBMISSION_POST.md`，需要同步更新两个 HTML 可视化文件以保持一致性。

## SUBMISSION_POST.md 的关键变化

### 1. 步骤示例调整
- **原步骤**（7步）：拿大杯外卖杯 → 不加冰 → 加燕麦奶 → 加半糖糖浆 → 萃取倒入 → 打奶泡 → 盖上出杯
- **新步骤**（6步）：拿大杯外卖杯 → 不加冰 → 加燕麦奶 → 加半糖糖浆 → 萃取倒入 → 盖上出杯
- **变化**：移除了"打奶泡"步骤，最后一步从"盖上，出杯"改为"盖上出杯"

### 2. AI模型变更
- 原：通义千问 API
- 新：GLM 5.1 API

### 3. 小票文案微调
- 底部提示从"5分钟后自动出下一杯"改为"5分钟后出下一杯"

---

## 更新任务

### 任务1：更新 comparison_visualization.html
**文件路径**：`d:\tuzizhang99\vibe-muse\IDE-Trae\materials\comparison_visualization.html`

**具体修改**：
1. 第287行：将 `盖盖出杯` 改为 `盖上出杯`
2. 第290行：将 `5分钟后自动出下一杯` 改为 `5分钟后出下一杯`

### 任务2：更新 architecture_diagram.html
**文件路径**：`d:\tuzizhang99\vibe-muse\IDE-Trae\materials\architecture_diagram.html`

**具体修改**：
1. 第306行：将 `通义千问 API` 改为 `GLM 5.1 API`

---

## 验证清单

- [ ] comparison_visualization.html 第287行已更新为"盖上出杯"
- [ ] comparison_visualization.html 第290行已更新为"5分钟后出下一杯"
- [ ] architecture_diagram.html 第306行已更新为"GLM 5.1 API"
- [ ] 两个HTML文件在浏览器中正常显示
