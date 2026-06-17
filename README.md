# Temperature Control Plugin for AstrBot

一个用于 **AstrBot** 的插件，允许你动态查询和修改 **DeepSeek API** 的 `temperature` 参数，无需重启机器人。

## ✨ 功能

- 查询当前 temperature 值
- 实时更改 temperature（范围 0.0 ~ 1.0）
- 更改后自动应用到后续对话
- 通过斜杠命令快速操作

## 📦 安装方式

### 方法一：通过 GitHub 导入（推荐）

1. 打开 AstrBot 管理后台 → 插件管理
2. 选择 **GitHub 导入**
3. 输入仓库地址:https://github.com/Moan282/astrbot_plugin_temperature
4. 点击安装，重启 AstrBot 即可

### 方法二：手动安装

1. 下载本仓库的 ZIP 压缩包并解压
2. 将解压后的 `temperature_control` 文件夹放入 AstrBot 的 `addons/` 目录下
3. 重启 AstrBot

## 🛠️ 使用方法

在 QQ 群或私聊中发送以下命令（需要机器人有管理员权限或已开启命令响应）：

| 命令 | 说明 | 示例 |
|------|------|------|
| `/温度查询` | 查询当前 temperature 值 | `/温度查询` → 回复 `🌡️ 当前 temperature = 0.7` |
| `/温度更改 <数值>` | 修改 temperature 为指定值（0.0 ~ 1.0） | `/温度更改 0.85` → 回复 `✅ temperature 已设置为 0.85` |

### 温馨提示
- `temperature` 值越高，回复随机性越强（更“放飞”），越低则越稳定（更“保守”）。
- 建议范围：`0.7` 适合日常聊天，`0.9` 以上适合创意型或娱乐型对话。

## ⚙️ 原理说明

插件启动时会尝试通过 AstrBot 的 `context.provider` 或 `context.conf` 接口设置 temperature 值。当您通过命令更改时，插件会更新内存中的值并立即应用（无需重启）。

> **注意**：如果您的 AstrBot 版本较旧，可能无法实时生效，此时建议重启机器人或通过配置文件修改。

## 🔧 兼容性

- 已在 AstrBot v4.26.x 上测试通过
- 支持 DeepSeek API 及其他兼容 OpenAI API 的提供商（需适配）

## 🐛 问题反馈

如有 Bug 或建议，请在 GitHub 仓库中提交 Issue，或直接联系作者 [Moan282](https://github.com/Moan282)。

## 📜 许可证

MIT License
