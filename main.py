import logging
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

logger = logging.getLogger(__name__)

@register("temperature_control", "Moan282", "DeepSeek 温度控制（斜杠命令版）", "v1.2.1", "https://github.com/Moan282/astrbot_plugin_temperature")
class TemperaturePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.temperature = 0.7
        # 尝试应用温度，但无论成败都不影响加载
        try:
            self._apply_temperature()
            logger.info(f"✅ 温度控制插件加载成功，当前温度 = {self.temperature}")
        except Exception as e:
            logger.warning(f"⚠️ 初始应用温度失败: {e}")

    def _apply_temperature(self):
        """将当前温度应用到 provider（静默执行）"""
        try:
            if hasattr(self.context, 'provider'):
                provider = self.context.provider
                if hasattr(provider, 'temperature'):
                    provider.temperature = self.temperature
                elif hasattr(provider, 'set_param'):
                    provider.set_param('temperature', self.temperature)
                elif hasattr(provider, 'default_params'):
                    provider.default_params['temperature'] = self.temperature
                elif hasattr(self.context, 'conf'):
                    self.context.conf['temperature'] = self.temperature
                else:
                    # 如果都不可用，尝试修改全局配置（如果有）
                    logger.warning("无法通过 provider 设置温度，插件仅提供查询/修改命令，实际生效需重启或手动配置")
            else:
                logger.warning("没有 provider 对象，温度可能无法自动应用")
        except Exception as e:
            logger.warning(f"应用温度时出错（不影响插件运行）: {e}")

    @filter.command("/温度查询")
    async def query_temp(self, event: AstrMessageEvent):
        yield event.make_result().message(f"🌡️ 当前 temperature = {self.temperature}")

    @filter.command("/温度更改")
    async def change_temp(self, event: AstrMessageEvent):
        msg = event.message_str.strip()
        parts = msg.split()
        if len(parts) < 2:
            yield event.make_result().message("❌ 用法：/温度更改 0.8（范围 0.0~1.0）")
            return
        try:
            val = float(parts[1])
            if not (0.0 <= val <= 1.0):
                yield event.make_result().message("❌ 温度必须在 0.0 到 1.0 之间")
                return
            self.temperature = val
            self._apply_temperature()
            yield event.make_result().message(f"✅ temperature 已设置为 {val}")
        except ValueError:
            yield event.make_result().message("❌ 请输入数字，例如 /温度更改 0.8")