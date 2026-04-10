#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置文件
"""

import os
import json
from datetime import datetime


class AppConfig:
    """应用配置类"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件"""
        default_config = {
            "app": {
                "name": "彩票记录与分析工具",
                "version": "1.0.0",
                "author": "Claude Code",
                "description": "彩票购彩记录、对奖、统计与随机选号工具"
            },
            "database": {
                "path": "lottery.db",
                "auto_backup": True,
                "backup_days": 7
            },
            "network": {
                "timeout": 10,
                "retry_times": 3,
                "use_simulate_data": False
            },
            "algorithm": {
                "num_people": 24,
                "min_number": -500,
                "max_number": 500
            },
            "ui": {
                "window_width": 360,
                "window_height": 640,
                "theme": "light",
                "font_size": 16
            },
            "statistics": {
                "auto_refresh": True,
                "refresh_interval": 300  # 5分钟
            },
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 如果配置文件存在，加载它
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置（用户配置覆盖默认配置）
                    self._merge_configs(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}，使用默认配置")

        return default_config

    def _merge_configs(self, default: dict, user: dict):
        """递归合并配置"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_configs(default[key], value)
            else:
                default[key] = value

    def save_config(self):
        """保存配置文件"""
        try:
            # 更新最后运行时间
            self.config["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config

        # 遍历到最后一层
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_app_info(self) -> dict:
        """获取应用信息"""
        return self.config.get("app", {})

    def get_database_config(self) -> dict:
        """获取数据库配置"""
        return self.config.get("database", {})

    def get_network_config(self) -> dict:
        """获取网络配置"""
        return self.config.get("network", {})

    def get_algorithm_config(self) -> dict:
        """获取算法配置"""
        return self.config.get("algorithm", {})

    def get_ui_config(self) -> dict:
        """获取界面配置"""
        return self.config.get("ui", {})

    def update_last_run(self):
        """更新最后运行时间"""
        self.set("last_run", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.save_config()


# 全局配置实例
config = AppConfig()


if __name__ == "__main__":
    # 测试配置功能
    print("应用信息:")
    app_info = config.get_app_info()
    for key, value in app_info.items():
        print(f"  {key}: {value}")

    print("\n数据库配置:")
    db_config = config.get_database_config()
    for key, value in db_config.items():
        print(f"  {key}: {value}")

    print("\n测试配置获取:")
    print(f"  app.name: {config.get('app.name')}")
    print(f"  database.path: {config.get('database.path')}")
    print(f"  ui.window_width: {config.get('ui.window_width')}")

    # 测试设置配置
    config.set("ui.theme", "dark")
    print(f"\n设置ui.theme为: {config.get('ui.theme')}")

    # 测试保存
    if config.save_config():
        print("配置保存成功")
    else:
        print("配置保存失败")