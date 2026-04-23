# Story-0.1.1: 云打印机API对接

## 关联信息
- 所属版本：v0.1
- 关联文档：mvp.md#五、技术栈
- 前置依赖：无
- 优先级：P0（阻塞后续所有开发）

## 任务描述

对接主流云打印机厂商API，实现基础打印功能。需要支持至少2家厂商作为备选方案。

### 目标厂商
1. **易联云**（首选）- 支持美团/饿了么直连
2. **飞鹅云**（备选）- API文档完善，稳定性好

### 核心功能
1. 打印机设备绑定与验证
2. 文本打印（基础小票格式）
3. 打印状态查询
4. 异常处理（打印失败回退）

## 认知约束

### 结构同构性思维
- 将打印机API的复杂响应结构同构为简洁的内部接口
- 统一封装：无论底层是易联云还是飞鹅，上层调用方式一致

### 极限推演思维
- 边界条件：当打印机离线时如何优雅降级？
- 异常条件：当API限流时如何处理？
- 极端条件：当网络完全中断时如何回退到原始模式？

### 可验证性
- 所有API调用必须有dry-run模式
- 打印前生成预览，确认后再发送
- 记录每次调用的输入输出日志

## 完成标准

### 功能标准
- [ ] 易联云API基础对接完成
- [ ] 飞鹅云API基础对接完成（备选）
- [ ] 统一打印机接口封装
- [ ] 支持打印纯文本小票

### 验证标准
- [ ] 提供打印测试脚本（tests/test_printer.py）
- [ ] dry-run模式验证通过
- [ ] 异常场景测试通过（离线、限流、超时）
- [ ] 代码覆盖率 > 80%

### 文档标准
- [ ] API对接文档（docs/dev0.1/0.1.1-printer-api.md）
- [ ] 使用示例代码
- [ ] 故障排查指南

## 相关文件

- 代码路径：src/printer/
  - `__init__.py` - 包初始化
  - `base.py` - 抽象基类
  - `yilianyun.py` - 易联云实现
  - `feie.py` - 飞鹅云实现
  - `factory.py` - 工厂模式创建实例
- 测试路径：tests/test_printer.py
- 文档路径：docs/dev0.1/0.1.1-printer-api.md

## 技术细节

### 易联云API要点
- 接口地址：https://open-api.10ss.net/
- 认证方式：sign签名（md5）
- 关键接口：
  - `addprinter` - 添加打印机
  - `print` - 打印文本
  - `queryPrinterStatus` - 查询状态

### 飞鹅云API要点
- 接口地址：https://api.feieyun.com/
- 认证方式：USER + UKEY
- 关键接口：
  - `print` - 打印订单
  - `queryOrderState` - 查询订单状态

### 统一接口设计
```python
class BasePrinter(ABC):
    @abstractmethod
    def print_ticket(self, content: str, dry_run: bool = False) -> dict:
        """打印小票，返回订单ID和状态"""
        pass
    
    @abstractmethod
    def query_status(self, order_id: str) -> dict:
        """查询打印状态"""
        pass
    
    @abstractmethod
    def is_online(self) -> bool:
        """检查打印机是否在线"""
        pass
```

## 状态
- [x] 待开始 / [ ] 进行中 / [ ] 已完成

## 备注

### 风险与应对
| 风险 | 应对措施 |
|------|---------|
| 易联云API文档不清晰 | 准备飞鹅云作为备选，同步调研 |
| 打印机设备未到位 | 先用沙盒环境/模拟器测试 |
| API调用频率限制 | 实现指数退避重试机制 |

### 依赖项
- 需要申请易联云/飞鹅云开发者账号
- 需要获取测试打印机设备号
