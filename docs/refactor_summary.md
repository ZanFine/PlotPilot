# 人物与地点关系图重构 - 实施总结

## 改动概览

### 1. BiblePanel 简化 ✅
**文件**: `web-app/src/components/BiblePanel.vue`

**改动内容**:
- 移除了"人物"标签页（原 `characters` tab）
- 移除了"地点/势力"标签页（原 `locations` tab）
- 只保留"文风设定"和"时间线"两个标签页
- 更新了说明文字，引导用户到"叙事与知识"维护人物和地点
- 移除了相关的 `addChar`, `removeChar`, `addLoc`, `removeLoc` 方法
- 简化了 `stats` 计算，移除了 `namedChars` 和 `namedLocs`

**用户体验**:
- 界面更简洁，职责更清晰
- 统计信息显示提示："人物与地点请至「叙事与知识」维护"

---

### 2. 创建人物关系图组件 ✅
**文件**: `web-app/src/components/CharacterRelationGraph.vue`

**功能特性**:
- 只显示 `entity_type: 'character'` 的三元组
- 按重要程度着色：
  - **primary** (主角): 红色 `#ef4444`
  - **secondary** (重要配角): 橙色 `#f97316`
  - **minor** (次要人物): 蓝色 `#3b82f6`
- 节点形状：方形 (box)
- 支持节点点击事件（可扩展跳转到人物详情页）
- 提供"编辑三元组"按钮，跳转到知识页面

**数据格式**:
```json
{
  "subject": "张三",
  "predicate": "是朋友",
  "object": "李四",
  "entity_type": "character",
  "importance": "primary",
  "chapter_id": 1,
  "note": "主角"
}
```

---

### 3. 创建地点关系图组件 ✅
**文件**: `web-app/src/components/LocationRelationGraph.vue`

**功能特性**:
- 只显示 `entity_type: 'location'` 的三元组
- 按重要程度着色：
  - **core** (核心地点): 深绿 `#10b981`
  - **important** (重要地点): 浅绿 `#6ee7b7`
  - **normal** (一般地点): 灰色 `#9ca3af`
- 按地点类型显示不同形状：
  - **city** (城市): 圆形 (dot)
  - **region** (区域): 菱形 (diamond)
  - **building** (建筑): 方形 (box)
  - **faction** (势力): 星形 (star)
  - **realm** (领域): 三角形 (triangle)
- 支持节点点击事件（可扩展跳转到地点详情页）

**数据格式**:
```json
{
  "subject": "长安城",
  "predicate": "位于",
  "object": "大唐",
  "entity_type": "location",
  "location_type": "city",
  "importance": "core",
  "chapter_id": 1,
  "note": "{\"description\":\"帝国都城\",\"atmosphere\":\"庄严肃穆\"}"
}
```

---

### 4. 增强 KnowledgeTripleGraph 组件 ✅
**文件**: `web-app/src/components/KnowledgeTripleGraph.vue`

**新增功能**:
- 添加过滤下拉框：全部 / 人物 / 地点
- 根据 `entity_type` 和 `importance` 字段自动着色
- 人物节点显示为方形，地点节点显示为圆形
- 支持混合显示人物和地点关系（如"张三 -> 居住在 -> 长安城"）

**改进逻辑**:
- `getColorByType()`: 根据实体类型和重要程度返回颜色
- `filteredFacts`: 根据选择的过滤类型过滤三元组
- 节点 title 显示重要程度信息

---

## 数据结构设计

### 三元组扩展字段

```typescript
interface KnowledgeTriple {
  id: string
  subject: string
  predicate: string
  object: string
  chapter_id?: number
  note?: string

  // 新增字段
  entity_type?: 'character' | 'location'
  importance?: string  // 人物: primary/secondary/minor, 地点: core/important/normal
  location_type?: 'city' | 'region' | 'building' | 'faction' | 'realm'
}
```

### 人物三元组示例

```json
[
  {
    "subject": "张三",
    "predicate": "是朋友",
    "object": "李四",
    "entity_type": "character",
    "importance": "primary",
    "note": "主角"
  },
  {
    "subject": "李四",
    "predicate": "是师父",
    "object": "王五",
    "entity_type": "character",
    "importance": "secondary"
  }
]
```

### 地点三元组示例

```json
[
  {
    "subject": "长安城",
    "predicate": "位于",
    "object": "大唐",
    "entity_type": "location",
    "location_type": "city",
    "importance": "core"
  },
  {
    "subject": "朝廷",
    "predicate": "统治",
    "object": "长安城",
    "entity_type": "location",
    "location_type": "faction",
    "importance": "core"
  }
]
```

### 跨类型关联示例

```json
[
  {
    "subject": "张三",
    "predicate": "居住在",
    "object": "长安城",
    "entity_type": "character",
    "importance": "primary"
  },
  {
    "subject": "李四",
    "predicate": "统治",
    "object": "魔教",
    "entity_type": "character",
    "importance": "primary"
  }
]
```

---

## 使用指南

### 1. 在页面中使用组件

```vue
<template>
  <div>
    <!-- 人物关系图 -->
    <CharacterRelationGraph :slug="novelSlug" />

    <!-- 地点关系图 -->
    <LocationRelationGraph :slug="novelSlug" />

    <!-- 综合知识图谱（支持过滤） -->
    <KnowledgeTripleGraph :slug="novelSlug" />
  </div>
</template>

<script setup>
import CharacterRelationGraph from '@/components/CharacterRelationGraph.vue'
import LocationRelationGraph from '@/components/LocationRelationGraph.vue'
import KnowledgeTripleGraph from '@/components/KnowledgeTripleGraph.vue'
</script>
```

### 2. 添加人物三元组

在"叙事与知识"页面添加三元组时，需要包含以下字段：

```json
{
  "subject": "人物名称",
  "predicate": "关系类型",
  "object": "目标人物/地点",
  "entity_type": "character",
  "importance": "primary",  // primary/secondary/minor
  "chapter_id": 1,
  "note": "备注信息"
}
```

### 3. 添加地点三元组

```json
{
  "subject": "地点名称",
  "predicate": "关系类型",
  "object": "目标地点",
  "entity_type": "location",
  "location_type": "city",  // city/region/building/faction/realm
  "importance": "core",  // core/important/normal
  "chapter_id": 1,
  "note": "备注信息"
}
```

---

## 后续工作

### 待实现功能

1. **后端 API 支持**
   - 在 `triples` 表中添加 `entity_type`, `importance`, `location_type` 字段
   - 更新 `SqliteKnowledgeRepository` 支持新字段
   - 创建 API 端点支持按类型查询三元组

2. **前端编辑界面**
   - 在"叙事与知识"页面添加实体类型选择器
   - 添加重要程度选择器
   - 添加地点类型选择器

3. **详情页面**
   - 创建人物详情页：显示人物信息、关系网络、出场章节
   - 创建地点详情页：显示地点信息、相关人物、相关事件

4. **数据迁移**
   - 编写迁移脚本，将旧的 Bible 人物和地点数据转换为三元组
   - 为现有三元组自动推断 `entity_type`

---

## 颜色方案总结

### 人物节点
- 🔴 **主角** (primary): `#ef4444` 红色
- 🟠 **重要配角** (secondary): `#f97316` 橙色
- 🔵 **次要人物** (minor): `#3b82f6` 蓝色

### 地点节点
- 🟢 **核心地点** (core): `#10b981` 深绿
- 🟢 **重要地点** (important): `#6ee7b7` 浅绿
- ⚪ **一般地点** (normal): `#9ca3af` 灰色

### 默认节点
- 🟣 **未分类**: `#6366f1` 紫色

---

## 测试清单

- [ ] BiblePanel 只显示"文风设定"和"时间线"两个标签
- [ ] 统计信息显示提示文字
- [ ] CharacterRelationGraph 正确过滤人物三元组
- [ ] 人物节点按重要程度着色
- [ ] LocationRelationGraph 正确过滤地点三元组
- [ ] 地点节点按重要程度着色
- [ ] 地点节点按类型显示不同形状
- [ ] KnowledgeTripleGraph 过滤器正常工作
- [ ] 混合显示人物和地点关系
- [ ] 节点点击事件触发
- [ ] "编辑三元组"按钮跳转正确

---

## 文件清单

### 修改的文件
- `web-app/src/components/BiblePanel.vue`
- `web-app/src/components/KnowledgeTripleGraph.vue`

### 新增的文件
- `web-app/src/components/CharacterRelationGraph.vue`
- `web-app/src/components/LocationRelationGraph.vue`
- `docs/location_structure_design.md`
- `docs/refactor_summary.md` (本文件)

---

## 设计理念

1. **职责分离**: BiblePanel 专注于文风和时间线，人物和地点通过三元组系统管理
2. **可视化优先**: 关系图作为主要展示方式，直观展示实体间的关系
3. **颜色编码**: 通过颜色快速识别实体的重要程度
4. **灵活扩展**: 三元组系统支持任意类型的关系，易于扩展
5. **数据统一**: 所有关系数据存储在知识图谱中，避免数据冗余

---

完成时间: 2026-04-02
