# ER 图

# ER 图说明文档

实体-关系图（Entity-Relationship Diagram, ER 图）用于描述系统中主要数据实体及其之间的关系，是数据库设计的重要组成部分。

---

## 一、ER 图作用

- 可视化系统数据结构与实体关系
- 理清表与表之间的主外键映射
- 作为系统开发与文档交付的重要设计资料

---

## 二、HotMeal 系统实体列表

| 实体名     | 描述             |
| ---------- | ---------------- |
| User       | 用户信息         |
| Category   | 菜品分类         |
| Dish       | 菜品详情         |
| Order      | 订单主表         |
| OrderItem  | 订单明细表       |
| DiningArea | 用餐区域         |
| MenuChat   | 用户 AI 聊天记录 |

---

## 三、实体关系描述

- 一个 `User` 可以创建多个 `Order`
- 一个 `Order` 可以包含多个 `OrderItem`
- 每个 `OrderItem` 对应一个 `Dish`
- 每个 `Dish` 属于一个 `Category`
- 一个 `Order` 可以关联一个 `DiningArea`
- 一个 `User` 可以产生多个 `MenuChat` 记录

---

## 四、推荐绘图工具

建议使用以下工具绘制 ER 图：

| 工具名称     | 官网地址                  | 说明               |
| ------------ | ------------------------- | ------------------ |
| draw.io      | https://app.diagrams.net  | 免费，支持离线使用 |
| dbdiagram.io | https://dbdiagram.io      | 支持导入 SQL / DSL |
| ProcessOn    | https://www.processon.com | 在线协作式绘图工具 |

---

## 五、图像文件保存建议

- 图片命名：`ER图.png`
- 存放路径：`/Docs/数据库设计/ER图.png`
- 可附源文件：`ER图.drawio` 或 `ER图.dbml`

---

## 六、示意结构（文字预览）

```
User ─────────────┐
                  ↓
               Order ──────┐
                            ↓
                        OrderItem ───── Dish ───── Category
                             ↓
                       DiningArea

User ─────────────→ MenuChat
```

> 注：箭头表示“拥有”或“关联”关系，具体关系请通过 ER 图工具绘制。

---

## 七、补充说明

如需生成 ER 图，请结合数据库建表语句或 models 目录下的 ORM 结构，导入至上述工具中绘制。图像完成后可嵌入论文、展示文档中使用。
