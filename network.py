#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络模块
负责从网络获取开奖信息
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class LotteryNetwork:
    """彩票网络接口管理类"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = self._create_session()

        # 定义数据源（备用多个数据源）
        self.data_sources = {
            "双色球": [
                {
                    "name": "500彩票网",
                    "url": "https://kaijiang.500.com/ssq.shtml",
                    "type": "html",
                    "enabled": True
                },
                {
                    "name": "中彩网",
                    "url": "https://www.zhcw.com/kjxx/ssq/",
                    "type": "html",
                    "enabled": True
                },
                {
                    "name": "模拟数据源",
                    "url": "simulate",
                    "type": "simulate",
                    "enabled": True
                }
            ],
            "大乐透": [
                {
                    "name": "500彩票网",
                    "url": "https://kaijiang.500.com/dlt.shtml",
                    "type": "html",
                    "enabled": True
                },
                {
                    "name": "中彩网",
                    "url": "https://www.zhcw.com/kjxx/dlt/",
                    "type": "html",
                    "enabled": True
                },
                {
                    "name": "模拟数据源",
                    "url": "simulate",
                    "type": "simulate",
                    "enabled": True
                }
            ]
        }

        # 用户代理列表，随机选择以避免被屏蔽
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        ]

    def _create_session(self) -> requests.Session:
        """创建带有重试机制的会话"""
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def get_random_user_agent(self) -> str:
        """获取随机用户代理"""
        return random.choice(self.user_agents)

    def fetch_latest_draw(self, lottery_type: str) -> Optional[Dict]:
        """获取最新一期开奖信息"""
        if lottery_type not in self.data_sources:
            return None

        data_sources = self.data_sources[lottery_type]

        # 按顺序尝试各个数据源
        for source in data_sources:
            if not source["enabled"]:
                continue

            try:
                if source["type"] == "simulate":
                    result = self._simulate_draw_data(lottery_type)
                elif source["type"] == "html":
                    result = self._fetch_from_website(source["url"], lottery_type)
                else:
                    continue

                if result:
                    print(f"从 {source['name']} 获取数据成功")
                    return result

            except Exception as e:
                print(f"数据源 {source['name']} 失败: {e}")
                continue

        # 所有数据源都失败，返回模拟数据
        print("所有数据源失败，返回模拟数据")
        return self._simulate_draw_data(lottery_type)

    def _fetch_from_website(self, url: str, lottery_type: str) -> Optional[Dict]:
        """从网站获取开奖信息"""
        try:
            headers = {
                "User-Agent": self.get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }

            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                return None

            # 这里需要根据具体网站的HTML结构解析
            # 由于不同网站结构不同，这里返回模拟数据
            # 实际项目中应该实现针对每个网站的解析器
            return self._parse_html_response(response.text, lottery_type)

        except Exception as e:
            print(f"网页请求失败: {e}")
            return None

    def _parse_html_response(self, html: str, lottery_type: str) -> Optional[Dict]:
        """解析HTML响应（占位符，实际需要根据网站结构实现）"""
        # 这里应该实现具体的HTML解析逻辑
        # 由于不同网站结构不同，这里暂时返回模拟数据
        return self._simulate_draw_data(lottery_type)

    def _simulate_draw_data(self, lottery_type: str) -> Dict:
        """生成模拟的开奖数据（当网络请求失败时使用）"""
        now = datetime.now()
        draw_date = now.strftime("%Y-%m-%d")

        # 生成模拟期号
        year = now.year % 100
        month_day = now.strftime("%m%d")
        draw_number = f"{year}{month_day}"

        if lottery_type == "双色球":
            # 生成6个不重复的红球（1-33）和1个蓝球（1-16）
            red_balls = random.sample(range(1, 34), 6)
            blue_ball = random.randint(1, 16)

            numbers = {
                "red": sorted(red_balls),
                "blue": blue_ball,
                "display": f"{','.join(str(x).zfill(2) for x in sorted(red_balls))}+{str(blue_ball).zfill(2)}"
            }

            # 模拟奖池金额（5-30亿）
            prize_pool = random.uniform(5, 30) * 100000000

        elif lottery_type == "大乐透":
            # 生成5个不重复的前区（1-35）和2个不重复的后区（1-12）
            front_balls = random.sample(range(1, 36), 5)
            back_balls = random.sample(range(1, 13), 2)

            numbers = {
                "front": sorted(front_balls),
                "back": sorted(back_balls),
                "display": f"{','.join(str(x).zfill(2) for x in sorted(front_balls))}+{','.join(str(x).zfill(2) for x in sorted(back_balls))}"
            }

            # 模拟奖池金额（3-15亿）
            prize_pool = random.uniform(3, 15) * 100000000

        else:
            numbers = {"display": ""}
            prize_pool = 0

        # 模拟下一期开奖日期（通常是当前日期+2或+3天）
        next_draw_date = (now + timedelta(days=random.randint(2, 3))).strftime("%Y-%m-%d")

        # 模拟销售额（1-5亿）
        sales_amount = random.uniform(1, 5) * 100000000

        return {
            "draw_date": draw_date,
            "lottery_type": lottery_type,
            "draw_number": draw_number,
            "numbers": numbers["display"],
            "numbers_detail": numbers,
            "prize_pool": round(prize_pool, 2),
            "sales_amount": round(sales_amount, 2),
            "next_draw_date": next_draw_date,
            "source": "simulate",
            "timestamp": time.time()
        }

    def fetch_draw_by_date(self, lottery_type: str, date: str) -> Optional[Dict]:
        """根据日期获取开奖信息"""
        # 这里应该调用相应的API或爬虫
        # 暂时返回模拟数据
        data = self._simulate_draw_data(lottery_type)
        data["draw_date"] = date

        # 调整期号基于日期
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        year = date_obj.year % 100
        month_day = date_obj.strftime("%m%d")
        data["draw_number"] = f"{year}{month_day}"

        return data

    def fetch_draw_history(self, lottery_type: str, limit: int = 10) -> List[Dict]:
        """获取历史开奖记录"""
        history = []

        now = datetime.now()
        for i in range(limit):
            draw_date = (now - timedelta(days=i * 2)).strftime("%Y-%m-%d")
            draw_data = self.fetch_draw_by_date(lottery_type, draw_date)
            if draw_data:
                history.append(draw_data)

        return history

    def check_connectivity(self) -> bool:
        """检查网络连接"""
        try:
            test_urls = [
                "https://www.baidu.com",
                "https://www.google.com",
                "https://www.zhcw.com"
            ]

            for url in test_urls:
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code == 200:
                        return True
                except:
                    continue

            return False
        except:
            return False

    def get_data_source_status(self) -> Dict[str, List[Dict]]:
        """获取数据源状态"""
        status = {}
        for lottery_type, sources in self.data_sources.items():
            status[lottery_type] = []
            for source in sources:
                source_status = source.copy()
                source_status["test_url"] = source["url"] if source["type"] != "simulate" else "N/A"
                status[lottery_type].append(source_status)

        return status


# 测试代码
if __name__ == "__main__":
    network = LotteryNetwork()

    print("测试网络连接...")
    if network.check_connectivity():
        print("网络连接正常")
    else:
        print("网络连接失败，将使用模拟数据")

    print("\n测试获取双色球最新开奖...")
    ssq_data = network.fetch_latest_draw("双色球")
    if ssq_data:
        print(f"开奖日期: {ssq_data['draw_date']}")
        print(f"期号: {ssq_data['draw_number']}")
        print(f"号码: {ssq_data['numbers']}")
        print(f"奖池: {ssq_data['prize_pool']:.2f}元")
        print(f"数据源: {ssq_data['source']}")

    print("\n测试获取大乐透最新开奖...")
    dlt_data = network.fetch_latest_draw("大乐透")
    if dlt_data:
        print(f"开奖日期: {dlt_data['draw_date']}")
        print(f"期号: {dlt_data['draw_number']}")
        print(f"号码: {dlt_data['numbers']}")
        print(f"奖池: {dlt_data['prize_pool']:.2f}元")
        print(f"数据源: {dlt_data['source']}")

    print("\n数据源状态:")
    status = network.get_data_source_status()
    for lottery_type, sources in status.items():
        print(f"\n{lottery_type}:")
        for source in sources:
            print(f"  - {source['name']}: {'启用' if source['enabled'] else '禁用'} ({source['type']})")