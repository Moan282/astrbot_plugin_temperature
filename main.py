from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("temperature_control", "Moan282", "DeepSeek 温度控制（斜杠命令版）", "v1.2.0", "https://github.com/Moan282/astrbot_plugin_temperature")
class TemperaturePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.temperature = 0.7
        self._apply_temperature()
        self.context.logger.info(f"✅ 温度控制插件加载成功，当前温度 = {self.temperature}")

    def _apply_temperature(self):
        """将当前温度应用到 provider"""
        try:
            if hasattr(self.context, 'provider'):
                provider = self.context.provider
                if hasattr(provider, 'temperature'):
                    provider.temperature = self.temperature
                elif hasattr(provider, 'set_param'):
                    provider.set_param('temperature', self.temperature)
                elif hasattr(provider, 'default_params'):
                    provider.default_params['temperature'] = self.temperature
                else:
                    if hasattr(self.context, 'conf'):
                        self.context.conf['temperature'] = self.temperature
            self.context.logger.info(f"🌡️ 已应用 temperature = {self.temperature}")
        except Exception as e:
            self.context.logger.warning(f"⚠️ 应用温度失败: {e}")

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