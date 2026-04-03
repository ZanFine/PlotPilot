# 地点/城市结构设计

## 数据模型

### 地点实体 (Location Entity)
存储在知识三元组系统中，通过 `entity_type: 'location'` 标识

```typescript
interface LocationTriple {
  id: string
  subject: string           // 地点名称
  predicate: string         // 关系类型
  object: string            // 目标地点/势力
  entity_type: 'location'
  importance: 'core' | 'important' | 'normal'  // 重要程度
  location_type: 'city' | 'region' | 'building' | 'faction' | 'realm'
  chapter_id?: number       // 首次出现章节
  note?: string            // 备注说明

  // 扩展属性（存储在 note 的 JSON 中）
  metadata?: {
    description: string    // 地点描述
    atmosphere: string     // 氛围特征
    ruler?: string        // 统治者/归属势力
    population?: string   // 规模/人口
    significance: string  // 剧情意义
  }
}
```

## 地点类型 (location_type)

1. **city** - 城市
   - 例：长安城、洛阳、江南水乡

2. **region** - 区域/国家
   - 例：大唐、西域、江湖

3. **building** - 建筑/场所
   - 例：皇宫、客栈、藏书阁

4. **faction** - 势力/组织
   - 例：朝廷、魔教、商会

5. **realm** - 虚构领域
   - 例：仙界、魔域、秘境

## 关系类型 (predicate)

### 地理关系
- `位于` - 地点包含关系
  - 例：`长安城 -> 位于 -> 大唐`
- `毗邻` - 地点相邻
  - 例：`洛阳 -> 毗邻 -> 长安城`
- `通往` - 交通连接
  - 例：`丝绸之路 -> 通往 -> 西域`

### 势力关系
- `统治` - 势力控制地点
  - 例：`朝廷 -> 统治 -> 长安城`
- `对立于` - 势力冲突
  - 例：`魔教 -> 对立于 -> 朝廷`
- `结盟` - 势力合作
  - 例：`商会 -> 结盟 -> 朝廷`
- `隶属于` - 从属关系
  - 例：`地方帮派 -> 隶属于 -> 魔教`

### 功能关系
- `是...的据点` - 势力基地
  - 例：`黑风寨 -> 是魔教的据点 -> 魔教`
- `是...的发源地` - 历史渊源
  - 例：`昆仑山 -> 是剑宗的发源地 -> 剑宗`

## 重要程度着色方案

### core (核心地点) - 深绿色 #10b981
- 主要剧情发生地
- 多次出现的关键场景
- 例：主角居住的城市、最终决战地

### important (重要地点) - 浅绿色 #6ee7b7
- 重要剧情节点
- 关键转折发生地
- 例：重要会面地点、宝物所在地

### normal (一般地点) - 灰色 #9ca3af
- 过场地点
- 背景设定
- 例：路过的城镇、提及的远方国度

## 三元组示例

### 示例 1：城市层级关系
```json
[
  {
    "subject": "长安城",
    "predicate": "位于",
    "object": "大唐",
    "entity_type": "location",
    "location_type": "city",
    "importance": "core",
    "note": "{\"description\":\"帝国都城，繁华鼎盛\",\"atmosphere\":\"庄严肃穆\",\"ruler\":\"皇帝\",\"significance\":\"主角成长地，多次重要剧情发生地\"}"
  },
  {
    "subject": "大唐",
    "predicate": "毗邻",
    "object": "西域",
    "entity_type": "location",
    "location_type": "region",
    "importance": "important"
  }
]
```

### 示例 2：势力与地点关系
```json
[
  {
    "subject": "朝廷",
    "predicate": "统治",
    "object": "长安城",
    "entity_type": "location",
    "location_type": "faction",
    "importance": "core"
  },
  {
    "subject": "魔教",
    "predicate": "对立于",
    "object": "朝廷",
    "entity_type": "location",
    "location_type": "faction",
    "importance": "core"
  },
  {
    "subject": "黑风寨",
    "predicate": "是魔教的据点",
    "object": "魔教",
    "entity_type": "location",
    "location_type": "building",
    "importance": "important"
  }
]
```

### 示例 3：人物与地点关联
```json
[
  {
    "subject": "张三",
    "predicate": "居住在",
    "object": "长安城",
    "entity_type": "character",
    "importance": "primary",
    "note": "主角"
  },
  {
    "subject": "李四",
    "predicate": "统治",
    "object": "魔教",
    "entity_type": "character",
    "importance": "primary",
    "note": "反派"
  }
]
```

## 前端展示

### 地点关系图页面
- 只显示 `entity_type: 'location'` 的三元组
- 节点颜色根据 `importance` 字段映射
- 节点形状根据 `location_type` 区分：
  - city: 圆形
  - region: 六边形
  - building: 方形
  - faction: 菱形
  - realm: 星形

### 人物关系图页面
- 只显示 `entity_type: 'character'` 的三元组
- 可以显示人物与地点的关联（虚线边）

### 综合关系图页面
- 显示所有三元组
- 人物和地点用不同颜色系区分
- 支持过滤和搜索

## 数据迁移

### 从旧 Bible 数据迁移
```javascript
// 旧格式
{
  locations: [
    { name: "长安城", description: "帝国都城，繁华鼎盛" }
  ]
}

// 转换为三元组
{
  subject: "长安城",
  predicate: "是",
  object: "城市",
  entity_type: "location",
  location_type: "city",
  importance: "normal",
  note: JSON.stringify({
    description: "帝国都城，繁华鼎盛"
  })
}
```

## API 端点

### 获取地点列表
```
GET /api/v1/novels/{novel_id}/locations
```

### 获取地点关系图
```
GET /api/v1/novels/{novel_id}/knowledge?entity_type=location
```

### 创建/更新地点三元组
```
POST /api/v1/novels/{novel_id}/knowledge/triples
PUT /api/v1/novels/{novel_id}/knowledge/triples/{triple_id}
```
