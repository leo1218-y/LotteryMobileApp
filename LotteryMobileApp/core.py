#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心逻辑模块
处理彩票规则、对奖计算、统计分析等核心业务逻辑
"""

import json
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional, Set, Any
from enum import Enum

from database import LotteryDatabase, LotteryType, PrizeLevel
from network import LotteryNetwork


class LotteryCore:
    """彩票核心逻辑类"""

    def __init__(self, db: LotteryDatabase, network: LotteryNetwork = None):
        self.db = db
        self.network = network if network else LotteryNetwork()

        # 彩票规则定义
        self.lottery_rules = {
            "双色球": {
                "name": "双色球",
                "red_range": (1, 33),
                "red_count": 6,
                "blue_range": (1, 16),
                "blue_count": 1,
                "price": 2.0,  # 每注价格
                "draw_days": [2, 4, 7],  # 每周二、四、日开奖
            },
            "大乐透": {
                "name": "大乐透",
                "front_range": (1, 35),
                "front_count": 5,
                "back_range": (1, 12),
                "back_count": 2,
                "price": 2.0,  # 基本投注价格
                "price_add": 3.0,  # 追加投注价格
                "draw_days": [1, 3, 6],  # 每周一、三、六开奖
            }
        }

    # ===== 号码验证与解析 =====

    def validate_numbers(self, lottery_type: str, numbers_str: str) -> Tuple[bool, str, Dict]:
        """验证号码格式是否正确"""
        try:
            if lottery_type == "双色球":
                return self._validate_ssq_numbers(numbers_str)
            elif lottery_type == "大乐透":
                return self._validate_dlt_numbers(numbers_str)
            else:
                return False, "不支持的彩票类型", {}
        except Exception as e:
            return False, f"号码解析失败: {str(e)}", {}

    def _validate_ssq_numbers(self, numbers_str: str) -> Tuple[bool, str, Dict]:
        """验证双色球号码"""
        # 格式: "01,02,03,04,05,06+07" 或 "1,2,3,4,5,6+7"
        if '+' not in numbers_str:
            return False, "号码格式错误，应包含'+'分隔红蓝球", {}

        red_blue = numbers_str.split('+')
        if len(red_blue) != 2:
            return False, "号码格式错误，应有且仅有一个'+'", {}

        red_str, blue_str = red_blue[0], red_blue[1]

        # 解析红球
        red_parts = red_str.split(',')
        if len(red_parts) != 6:
            return False, "红球数量应为6个", {}

        red_numbers = []
        for num_str in red_parts:
            try:
                num = int(num_str.strip())
                if num < 1 or num > 33:
                    return False, f"红球号码{num}超出范围(1-33)", {}
                red_numbers.append(num)
            except ValueError:
                return False, f"红球号码'{num_str}'不是有效数字", {}

        # 检查红球重复
        if len(set(red_numbers)) != 6:
            return False, "红球号码有重复", {}

        # 解析蓝球
        try:
            blue_number = int(blue_str.strip())
            if blue_number < 1 or blue_number > 16:
                return False, f"蓝球号码{blue_number}超出范围(1-16)", {}
        except ValueError:
            return False, f"蓝球号码'{blue_str}'不是有效数字", {}

        # 返回成功结果
        numbers_detail = {
            "red": sorted(red_numbers),
            "blue": blue_number,
            "display": f"{','.join(str(x).zfill(2) for x in sorted(red_numbers))}+{str(blue_number).zfill(2)}"
        }

        return True, "号码格式正确", numbers_detail

    def _validate_dlt_numbers(self, numbers_str: str) -> Tuple[bool, str, Dict]:
        """验证大乐透号码"""
        # 格式: "01,02,03,04,05+01,02" 或 "1,2,3,4,5+1,2"
        if '+' not in numbers_str:
            return False, "号码格式错误，应包含'+'分隔前后区", {}

        front_back = numbers_str.split('+')
        if len(front_back) != 2:
            return False, "号码格式错误，应有且仅有一个'+'", {}

        front_str, back_str = front_back[0], front_back[1]

        # 解析前区
        front_parts = front_str.split(',')
        if len(front_parts) != 5:
            return False, "前区数量应为5个", {}

        front_numbers = []
        for num_str in front_parts:
            try:
                num = int(num_str.strip())
                if num < 1 or num > 35:
                    return False, f"前区号码{num}超出范围(1-35)", {}
                front_numbers.append(num)
            except ValueError:
                return False, f"前区号码'{num_str}'不是有效数字", {}

        # 检查前区重复
        if len(set(front_numbers)) != 5:
            return False, "前区号码有重复", {}

        # 解析后区
        back_parts = back_str.split(',')
        if len(back_parts) != 2:
            return False, "后区数量应为2个", {}

        back_numbers = []
        for num_str in back_parts:
            try:
                num = int(num_str.strip())
                if num < 1 or num > 12:
                    return False, f"后区号码{num}超出范围(1-12)", {}
                back_numbers.append(num)
            except ValueError:
                return False, f"后区号码'{num_str}'不是有效数字", {}

        # 检查后区重复
        if len(set(back_numbers)) != 2:
            return False, "后区号码有重复", {}

        # 返回成功结果
        numbers_detail = {
            "front": sorted(front_numbers),
            "back": sorted(back_numbers),
            "display": f"{','.join(str(x).zfill(2) for x in sorted(front_numbers))}+{','.join(str(x).zfill(2) for x in sorted(back_numbers))}"
        }

        return True, "号码格式正确", numbers_detail

    # ===== 开奖查询与更新 =====

    def update_latest_draw(self, lottery_type: str) -> Tuple[bool, str, Optional[Dict]]:
        """更新最新开奖信息"""
        try:
            draw_data = self.network.fetch_latest_draw(lottery_type)
            if not draw_data:
                return False, "获取开奖信息失败", None

            # 保存到数据库
            success = self.db.add_draw_result(
                draw_date=draw_data["draw_date"],
                lottery_type=lottery_type,
                draw_number=draw_data["draw_number"],
                numbers=draw_data["numbers"],
                prize_pool=draw_data.get("prize_pool"),
                sales_amount=draw_data.get("sales_amount"),
                next_draw_date=draw_data.get("next_draw_date")
            )

            if success:
                return True, "开奖信息更新成功", draw_data
            else:
                return False, "保存开奖信息到数据库失败", draw_data

        except Exception as e:
            return False, f"更新开奖信息异常: {str(e)}", None

    def check_and_update_draws(self):
        """检查并更新所有彩票类型的开奖信息"""
        results = {}
        for lottery_type in ["双色球", "大乐透"]:
            success, message, data = self.update_latest_draw(lottery_type)
            results[lottery_type] = {
                "success": success,
                "message": message,
                "has_data": data is not None
            }
        return results

    # ===== 对奖计算 =====

    def check_prize(self, purchase_numbers: str, draw_numbers: str,
                    lottery_type: str) -> Tuple[bool, Optional[str], Optional[float]]:
        """对奖计算，返回是否中奖、奖级、奖金"""
        try:
            # 解析号码
            if lottery_type == "双色球":
                return self._check_ssq_prize(purchase_numbers, draw_numbers)
            elif lottery_type == "大乐透":
                return self._check_dlt_prize(purchase_numbers, draw_numbers)
            else:
                return False, None, None
        except Exception as e:
            print(f"对奖计算异常: {e}")
            return False, None, None

    def _check_ssq_prize(self, purchase_numbers: str, draw_numbers: str) -> Tuple[bool, Optional[str], Optional[float]]:
        """双色球对奖计算"""
        # 解析购买的号码
        purchase_valid, purchase_msg, purchase_detail = self._validate_ssq_numbers(purchase_numbers)
        if not purchase_valid:
            return False, None, None

        # 解析开奖号码
        draw_valid, draw_msg, draw_detail = self._validate_ssq_numbers(draw_numbers)
        if not draw_valid:
            return False, None, None

        # 计算匹配数量
        red_match = len(set(purchase_detail["red"]) & set(draw_detail["red"]))
        blue_match = 1 if purchase_detail["blue"] == draw_detail["blue"] else 0

        # 根据匹配数量确定奖级
        prize_level = None

        if red_match == 6 and blue_match == 1:
            prize_level = "一等奖"
        elif red_match == 6 and blue_match == 0:
            prize_level = "二等奖"
        elif red_match == 5 and blue_match == 1:
            prize_level = "三等奖"
        elif (red_match == 5 and blue_match == 0) or (red_match == 4 and blue_match == 1):
            prize_level = "四等奖"
        elif (red_match == 4 and blue_match == 0) or (red_match == 3 and blue_match == 1):
            prize_level = "五等奖"
        elif (red_match == 2 and blue_match == 1) or (red_match == 1 and blue_match == 1) or (red_match == 0 and blue_match == 1):
            prize_level = "六等奖"

        if prize_level:
            # 获取奖金金额
            prize_rule = self.db.get_prize_rule("双色球", prize_level)
            if prize_rule:
                # 如果是浮动奖金（一等奖、二等奖），返回0
                if prize_rule["is_floating"]:
                    prize_amount = 0.0  # 浮动奖金，实际金额未知
                else:
                    prize_amount = prize_rule["min_amount"]  # 固定奖金
            else:
                prize_amount = 0.0

            return True, prize_level, prize_amount
        else:
            return False, None, None

    def _check_dlt_prize(self, purchase_numbers: str, draw_numbers: str) -> Tuple[bool, Optional[str], Optional[float]]:
        """大乐透对奖计算"""
        # 解析购买的号码
        purchase_valid, purchase_msg, purchase_detail = self._validate_dlt_numbers(purchase_numbers)
        if not purchase_valid:
            return False, None, None

        # 解析开奖号码
        draw_valid, draw_msg, draw_detail = self._validate_dlt_numbers(draw_numbers)
        if not draw_valid:
            return False, None, None

        # 计算匹配数量
        front_match = len(set(purchase_detail["front"]) & set(draw_detail["front"]))
        back_match = len(set(purchase_detail["back"]) & set(draw_detail["back"]))

        # 根据匹配数量确定奖级
        prize_level = None

        if front_match == 5 and back_match == 2:
            prize_level = "一等奖"
        elif front_match == 5 and back_match == 1:
            prize_level = "二等奖"
        elif front_match == 5 and back_match == 0:
            prize_level = "三等奖"
        elif front_match == 4 and back_match == 2:
            prize_level = "四等奖"
        elif front_match == 4 and back_match == 1:
            prize_level = "五等奖"
        elif front_match == 3 and back_match == 2:
            prize_level = "六等奖"
        elif front_match == 4 and back_match == 0:
            prize_level = "七等奖"
        elif (front_match == 3 and back_match == 1) or (front_match == 2 and back_match == 2):
            prize_level = "八等奖"
        elif (front_match == 3 and back_match == 0) or (front_match == 2 and back_match == 1) or \
             (front_match == 1 and back_match == 2) or (front_match == 0 and back_match == 2):
            prize_level = "九等奖"

        if prize_level:
            # 获取奖金金额
            prize_rule = self.db.get_prize_rule("大乐透", prize_level)
            if prize_rule:
                # 如果是浮动奖金（一等奖、二等奖），返回0
                if prize_rule["is_floating"]:
                    prize_amount = 0.0  # 浮动奖金，实际金额未知
                else:
                    prize_amount = prize_rule["min_amount"]  # 固定奖金
            else:
                prize_amount = 0.0

            return True, prize_level, prize_amount
        else:
            return False, None, None

    def check_all_unchecked_purchases(self, lottery_type: str = None) -> Dict[str, Any]:
        """检查所有未对奖的购彩记录"""
        purchases = self.db.get_unchecked_purchases(lottery_type)
        results = {
            "total": len(purchases),
            "checked": 0,
            "won": 0,
            "total_prize": 0.0,
            "details": []
        }

        for purchase in purchases:
            # 查找对应的开奖结果
            draw = self.db.get_draw_by_date(purchase["lottery_type"], purchase.get("available_draw_date"))

            if draw:
                won, prize_level, prize_amount = self.check_prize(
                    purchase["numbers"], draw["numbers"], purchase["lottery_type"]
                )

                if won:
                    # 更新数据库
                    self.db.update_purchase_prize(
                        purchase["id"], prize_level, prize_amount, draw["draw_date"]
                    )

                    results["won"] += 1
                    results["total_prize"] += prize_amount if prize_amount else 0

                    results["details"].append({
                        "purchase_id": purchase["id"],
                        "lottery_type": purchase["lottery_type"],
                        "numbers": purchase["numbers"],
                        "won": True,
                        "prize_level": prize_level,
                        "prize_amount": prize_amount
                    })
                else:
                    # 标记为已检查但未中奖
                    self.db.cursor.execute("""
                        UPDATE purchases SET checked = 1 WHERE id = ?
                    """, (purchase["id"],))
                    self.db.conn.commit()

                    results["details"].append({
                        "purchase_id": purchase["id"],
                        "lottery_type": purchase["lottery_type"],
                        "numbers": purchase["numbers"],
                        "won": False
                    })
            else:
                # 没有找到对应的开奖结果
                results["details"].append({
                    "purchase_id": purchase["id"],
                    "lottery_type": purchase["lottery_type"],
                    "numbers": purchase["numbers"],
                    "won": False,
                    "error": "未找到对应开奖结果"
                })

            results["checked"] += 1

        return results

    # ===== 统计分析 =====

    def calculate_statistics(self, lottery_type: str = None) -> Dict[str, Any]:
        """计算统计信息"""
        total_investment = self.db.get_total_investment(lottery_type)
        total_prize = self.db.get_total_prize(lottery_type)
        prize_counts = self.db.get_prize_counts(lottery_type)
        win_rate = self.db.get_win_rate(lottery_type)

        net_profit = total_prize - total_investment

        # 计算各奖级详细统计
        prize_details = []
        all_prize_rules = self.db.get_all_prize_rules(lottery_type)

        for rule in all_prize_rules:
            level = rule["prize_level"]
            count = prize_counts.get(level, 0)
            amount = rule["min_amount"] if not rule["is_floating"] else "浮动"

            prize_details.append({
                "level": level,
                "count": count,
                "amount": amount,
                "is_floating": bool(rule["is_floating"])
            })

        # 计算日期范围
        today = datetime.now().strftime("%Y-%m-%d")

        return {
            "statistic_date": today,
            "lottery_type": lottery_type,
            "total_investment": total_investment,
            "total_prize": total_prize,
            "net_profit": net_profit,
            "win_rate": win_rate,
            "prize_counts": prize_counts,
            "prize_details": prize_details,
            "summary": {
                "total_tickets": self._count_total_tickets(lottery_type),
                "winning_tickets": self._count_winning_tickets(lottery_type),
                "avg_investment_per_ticket": total_investment / self._count_total_tickets(lottery_type) if self._count_total_tickets(lottery_type) > 0 else 0,
                "avg_prize_per_winning": total_prize / self._count_winning_tickets(lottery_type) if self._count_winning_tickets(lottery_type) > 0 else 0,
            }
        }

    def _count_total_tickets(self, lottery_type: str = None) -> int:
        """统计总票数"""
        query = "SELECT COUNT(*) FROM purchases"
        params = []

        if lottery_type:
            query += " WHERE lottery_type = ?"
            params.append(lottery_type)

        self.db.cursor.execute(query, params)
        return self.db.cursor.fetchone()[0] or 0

    def _count_winning_tickets(self, lottery_type: str = None) -> int:
        """统计中奖票数"""
        query = "SELECT COUNT(*) FROM purchases WHERE checked = 1 AND prize_level IS NOT NULL"
        params = []

        if lottery_type:
            query += " AND lottery_type = ?"
            params.append(lottery_type)

        self.db.cursor.execute(query, params)
        return self.db.cursor.fetchone()[0] or 0

    def get_statistics_report(self, lottery_type: str = None) -> str:
        """生成统计报告文本"""
        stats = self.calculate_statistics(lottery_type)

        if lottery_type:
            title = f"{lottery_type}统计报告"
        else:
            title = "综合统计报告"

        report = f"""{title} (截至{stats['statistic_date']})
{'-' * 40}
累计投入: {stats['total_investment']:.2f}元
累计中奖: {stats['total_prize']:.2f}元
净盈亏: {stats['net_profit']:+.2f}元
中奖率: {stats['win_rate']:.2f}%

各奖级中奖次数:
"""

        for detail in stats["prize_details"]:
            count = detail["count"]
            if count > 0:
                amount = detail["amount"]
                amount_str = f"{amount}元" if isinstance(amount, (int, float)) else amount
                report += f"{detail['level']}: {count}次 ({amount_str})\n"

        report += f"""
汇总信息:
总票数: {stats['summary']['total_tickets']}张
中奖票数: {stats['summary']['winning_tickets']}张
平均每票投入: {stats['summary']['avg_investment_per_ticket']:.2f}元
平均每注奖金: {stats['summary']['avg_prize_per_winning']:.2f}元
{'-' * 40}
建议: 理性购彩，量力而行"""

        return report

    # ===== 工具方法 =====

    def get_next_draw_date(self, lottery_type: str) -> Optional[str]:
        """获取下一期开奖日期"""
        latest_draw = self.db.get_latest_draw(lottery_type)
        if latest_draw and latest_draw.get("next_draw_date"):
            return latest_draw["next_draw_date"]

        # 如果没有下一期日期，根据开奖规则计算
        rules = self.lottery_rules.get(lottery_type)
        if not rules:
            return None

        # 简单实现：假设明天开奖
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return tomorrow

    def get_lottery_types(self) -> List[str]:
        """获取支持的彩票类型列表"""
        return list(self.lottery_rules.keys())

    def get_lottery_info(self, lottery_type: str) -> Optional[Dict]:
        """获取彩票详细信息"""
        return self.lottery_rules.get(lottery_type)


# 测试代码
if __name__ == "__main__":
    # 创建数据库和网络对象
    db = LotteryDatabase("test_core.db")
    network = LotteryNetwork()
    core = LotteryCore(db, network)

    print("测试号码验证...")
    test_numbers = [
        ("双色球", "01,07,13,19,24,31+12", True),
        ("双色球", "1,7,13,19,24,31+12", True),
        ("双色球", "01,01,13,19,24,31+12", False),  # 重复
        ("大乐透", "01,07,13,19,24+01,12", True),
        ("大乐透", "1,7,13,19,24+1,12", True),
    ]

    for lottery_type, numbers, expected in test_numbers:
        valid, message, detail = core.validate_numbers(lottery_type, numbers)
        status = "通过" if valid == expected else "失败"
        print(f"{lottery_type} - {numbers}: {message} ({status})")

    print("\n测试对奖计算...")
    # 测试双色球对奖
    purchase_ssq = "01,07,13,19,24,31+12"
    draw_ssq_win = "01,07,13,19,24,31+12"  # 一等奖
    draw_ssq_lose = "02,08,14,20,25,32+11"  # 不中奖

    won, level, amount = core.check_prize(purchase_ssq, draw_ssq_win, "双色球")
    print(f"双色球一等奖测试: {'中奖' if won else '未中奖'} - 奖级: {level}, 奖金: {amount}")

    won, level, amount = core.check_prize(purchase_ssq, draw_ssq_lose, "双色球")
    print(f"双色球不中奖测试: {'中奖' if won else '未中奖'}")

    # 测试大乐透对奖
    purchase_dlt = "01,07,13,19,24+01,12"
    draw_dlt_win = "01,07,13,19,24+01,12"  # 一等奖
    draw_dlt_lose = "02,08,14,20,25+02,11"  # 不中奖

    won, level, amount = core.check_prize(purchase_dlt, draw_dlt_win, "大乐透")
    print(f"大乐透一等奖测试: {'中奖' if won else '未中奖'} - 奖级: {level}, 奖金: {amount}")

    won, level, amount = core.check_prize(purchase_dlt, draw_dlt_lose, "大乐透")
    print(f"大乐透不中奖测试: {'中奖' if won else '未中奖'}")

    print("\n测试统计计算...")
    stats = core.calculate_statistics()
    print(f"总投入: {stats['total_investment']:.2f}元")
    print(f"总奖金: {stats['total_prize']:.2f}元")
    print(f"净盈亏: {stats['net_profit']:+.2f}元")
    print(f"中奖率: {stats['win_rate']:.2f}%")

    print("\n测试统计报告生成...")
    report = core.get_statistics_report()
    print(report)

    db.close()