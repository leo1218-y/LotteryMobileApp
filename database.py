#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模块
使用SQLite存储彩票记录、开奖结果等数据
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Any
from enum import Enum


class LotteryType(Enum):
    """彩票类型枚举"""
    SSQ = "双色球"  # 双色球
    DLT = "大乐透"  # 大乐透


class PrizeLevel(Enum):
    """奖级枚举"""
    # 双色球奖级
    SSQ_1 = ("一等奖", 6, 1, 0)      # 6红+1蓝
    SSQ_2 = ("二等奖", 6, 0, 0)      # 6红
    SSQ_3 = ("三等奖", 5, 1, 0)      # 5红+1蓝
    SSQ_4 = ("四等奖", 5, 0, 0)      # 5红 或 4红+1蓝
    SSQ_5 = ("五等奖", 4, 1, 0)      # 4红+1蓝 或 4红
    SSQ_6 = ("六等奖", 2, 1, 0)      # 1红+1蓝 或 0红+1蓝

    # 大乐透奖级
    DLT_1 = ("一等奖", 5, 2, 0)      # 5+2
    DLT_2 = ("二等奖", 5, 1, 0)      # 5+1
    DLT_3 = ("三等奖", 5, 0, 0)      # 5+0
    DLT_4 = ("四等奖", 4, 2, 0)      # 4+2
    DLT_5 = ("五等奖", 4, 1, 0)      # 4+1
    DLT_6 = ("六等奖", 3, 2, 0)      # 3+2
    DLT_7 = ("七等奖", 4, 0, 0)      # 4+0
    DLT_8 = ("八等奖", 3, 1, 0)      # 3+1 或 2+2
    DLT_9 = ("九等奖", 3, 0, 0)      # 3+0 或 2+1 或 1+2 或 0+2

    def __init__(self, name_cn, red_match, blue_match, prize_amount):
        self.name_cn = name_cn
        self.red_match = red_match  # 红球/前区匹配数
        self.blue_match = blue_match  # 蓝球/后区匹配数
        self.prize_amount = prize_amount  # 奖金金额（0表示浮动）


class LotteryDatabase:
    """彩票数据库管理类"""

    def __init__(self, db_path: str = "lottery.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._init_database()

    def _init_database(self):
        """初始化数据库表结构"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # 创建彩票记录表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_date TEXT NOT NULL,
                lottery_type TEXT NOT NULL,
                numbers TEXT NOT NULL,
                amount REAL NOT NULL,
                channel TEXT,
                draw_date TEXT,
                prize_level TEXT,
                prize_amount REAL,
                checked INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建开奖结果表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS draws (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                draw_date TEXT NOT NULL,
                lottery_type TEXT NOT NULL,
                draw_number TEXT NOT NULL,
                numbers TEXT NOT NULL,
                prize_pool REAL,
                sales_amount REAL,
                next_draw_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(draw_date, lottery_type)
            )
        """)

        # 创建奖金规则表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prize_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lottery_type TEXT NOT NULL,
                prize_level TEXT NOT NULL,
                red_match INTEGER NOT NULL,
                blue_match INTEGER NOT NULL,
                min_amount REAL,
                max_amount REAL,
                is_floating INTEGER DEFAULT 0,
                description TEXT,
                UNIQUE(lottery_type, prize_level)
            )
        """)

        # 创建统计缓存表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                statistic_date TEXT NOT NULL,
                lottery_type TEXT,
                total_investment REAL DEFAULT 0,
                total_prize REAL DEFAULT 0,
                net_profit REAL DEFAULT 0,
                win_rate REAL DEFAULT 0,
                prize_counts TEXT,  -- JSON格式存储各奖级次数
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(statistic_date, lottery_type)
            )
        """)

        # 初始化奖金规则数据
        self._init_prize_rules()

        self.conn.commit()

    def _init_prize_rules(self):
        """初始化奖金规则数据"""
        # 检查是否已有数据
        self.cursor.execute("SELECT COUNT(*) FROM prize_rules")
        count = self.cursor.fetchone()[0]
        if count > 0:
            return

        # 双色球奖金规则（示例，实际金额为浮动）
        ssq_rules = [
            ("双色球", "一等奖", 6, 1, 0, 0, 1, "6红+1蓝"),
            ("双色球", "二等奖", 6, 0, 0, 0, 1, "6红"),
            ("双色球", "三等奖", 5, 1, 3000, 3000, 0, "5红+1蓝"),
            ("双色球", "四等奖", 5, 0, 200, 200, 0, "5红 或 4红+1蓝"),
            ("双色球", "五等奖", 4, 1, 10, 10, 0, "4红+1蓝 或 4红"),
            ("双色球", "六等奖", 2, 1, 5, 5, 0, "1红+1蓝 或 0红+1蓝"),
        ]

        # 大乐透奖金规则（示例）
        dlt_rules = [
            ("大乐透", "一等奖", 5, 2, 0, 0, 1, "5+2"),
            ("大乐透", "二等奖", 5, 1, 0, 0, 1, "5+1"),
            ("大乐透", "三等奖", 5, 0, 10000, 10000, 0, "5+0"),
            ("大乐透", "四等奖", 4, 2, 3000, 3000, 0, "4+2"),
            ("大乐透", "五等奖", 4, 1, 300, 300, 0, "4+1"),
            ("大乐透", "六等奖", 3, 2, 200, 200, 0, "3+2"),
            ("大乐透", "七等奖", 4, 0, 100, 100, 0, "4+0"),
            ("大乐透", "八等奖", 3, 1, 15, 15, 0, "3+1 或 2+2"),
            ("大乐透", "九等奖", 3, 0, 5, 5, 0, "3+0 或 2+1 或 1+2 或 0+2"),
        ]

        all_rules = ssq_rules + dlt_rules

        for rule in all_rules:
            self.cursor.execute("""
                INSERT OR IGNORE INTO prize_rules
                (lottery_type, prize_level, red_match, blue_match, min_amount, max_amount, is_floating, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, rule)

        self.conn.commit()

    # ===== 彩票记录操作 =====

    def add_purchase(self, purchase_date: str, lottery_type: str, numbers: str,
                     amount: float, channel: str = "") -> int:
        """添加购彩记录"""
        self.cursor.execute("""
            INSERT INTO purchases
            (purchase_date, lottery_type, numbers, amount, channel, checked)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (purchase_date, lottery_type, numbers, amount, channel, 0))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_purchases(self, lottery_type: str = None, limit: int = 100) -> List[Dict]:
        """获取购彩记录列表"""
        query = "SELECT * FROM purchases"
        params = []

        if lottery_type:
            query += " WHERE lottery_type = ?"
            params.append(lottery_type)

        query += " ORDER BY purchase_date DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        rows = self.cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def get_unchecked_purchases(self, lottery_type: str = None) -> List[Dict]:
        """获取未对奖的购彩记录"""
        query = """
            SELECT p.*, d.draw_date as available_draw_date
            FROM purchases p
            LEFT JOIN draws d ON p.lottery_type = d.lottery_type
                AND d.draw_date >= p.purchase_date
            WHERE p.checked = 0
        """
        params = []

        if lottery_type:
            query += " AND p.lottery_type = ?"
            params.append(lottery_type)

        query += " ORDER BY p.purchase_date"

        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        rows = self.cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def update_purchase_prize(self, purchase_id: int, prize_level: str,
                              prize_amount: float, draw_date: str):
        """更新购彩记录的中奖信息"""
        self.cursor.execute("""
            UPDATE purchases
            SET prize_level = ?, prize_amount = ?, draw_date = ?, checked = 1
            WHERE id = ?
        """, (prize_level, prize_amount, draw_date, purchase_id))
        self.conn.commit()

    # ===== 开奖结果操作 =====

    def add_draw_result(self, draw_date: str, lottery_type: str, draw_number: str,
                        numbers: str, prize_pool: float = None, sales_amount: float = None,
                        next_draw_date: str = None):
        """添加开奖结果"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO draws
                (draw_date, lottery_type, draw_number, numbers, prize_pool, sales_amount, next_draw_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (draw_date, lottery_type, draw_number, numbers, prize_pool,
                  sales_amount, next_draw_date))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"添加开奖结果失败: {e}")
            return False

    def get_latest_draw(self, lottery_type: str) -> Optional[Dict]:
        """获取最新一期开奖结果"""
        self.cursor.execute("""
            SELECT * FROM draws
            WHERE lottery_type = ?
            ORDER BY draw_date DESC
            LIMIT 1
        """, (lottery_type,))

        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def get_draw_by_date(self, lottery_type: str, date: str) -> Optional[Dict]:
        """根据日期获取开奖结果"""
        self.cursor.execute("""
            SELECT * FROM draws
            WHERE lottery_type = ? AND draw_date = ?
            LIMIT 1
        """, (lottery_type, date))

        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    # ===== 奖金规则操作 =====

    def get_prize_rule(self, lottery_type: str, prize_level: str) -> Optional[Dict]:
        """获取奖金规则"""
        self.cursor.execute("""
            SELECT * FROM prize_rules
            WHERE lottery_type = ? AND prize_level = ?
            LIMIT 1
        """, (lottery_type, prize_level))

        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def get_all_prize_rules(self, lottery_type: str = None) -> List[Dict]:
        """获取所有奖金规则"""
        query = "SELECT * FROM prize_rules"
        params = []

        if lottery_type:
            query += " WHERE lottery_type = ?"
            params.append(lottery_type)

        query += " ORDER BY lottery_type, red_match DESC, blue_match DESC"

        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        rows = self.cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    # ===== 统计操作 =====

    def update_statistics(self, statistic_date: str, lottery_type: str = None,
                          total_investment: float = 0, total_prize: float = 0,
                          net_profit: float = 0, win_rate: float = 0,
                          prize_counts: Dict = None):
        """更新统计信息"""
        prize_counts_json = json.dumps(prize_counts) if prize_counts else "{}"

        self.cursor.execute("""
            INSERT OR REPLACE INTO statistics
            (statistic_date, lottery_type, total_investment, total_prize,
             net_profit, win_rate, prize_counts)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (statistic_date, lottery_type, total_investment, total_prize,
              net_profit, win_rate, prize_counts_json))
        self.conn.commit()

    def get_statistics(self, start_date: str = None, end_date: str = None,
                       lottery_type: str = None) -> List[Dict]:
        """获取统计信息"""
        query = "SELECT * FROM statistics WHERE 1=1"
        params = []

        if start_date:
            query += " AND statistic_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND statistic_date <= ?"
            params.append(end_date)

        if lottery_type:
            query += " AND lottery_type = ?"
            params.append(lottery_type)

        query += " ORDER BY statistic_date DESC"

        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        rows = self.cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    # ===== 通用统计查询 =====

    def get_total_investment(self, lottery_type: str = None) -> float:
        """获取总投入金额"""
        query = "SELECT SUM(amount) FROM purchases WHERE 1=1"
        params = []

        if lottery_type:
            query += " AND lottery_type = ?"
            params.append(lottery_type)

        self.cursor.execute(query, params)
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def get_total_prize(self, lottery_type: str = None) -> float:
        """获取总中奖金额"""
        query = "SELECT SUM(prize_amount) FROM purchases WHERE checked = 1"
        params = []

        if lottery_type:
            query += " AND lottery_type = ?"
            params.append(lottery_type)

        self.cursor.execute(query, params)
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def get_prize_counts(self, lottery_type: str = None) -> Dict[str, int]:
        """获取各奖级中奖次数"""
        query = """
            SELECT prize_level, COUNT(*) as count
            FROM purchases
            WHERE checked = 1 AND prize_level IS NOT NULL
        """
        params = []

        if lottery_type:
            query += " AND lottery_type = ?"
            params.append(lottery_type)

        query += " GROUP BY prize_level"

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()

        counts = {}
        for prize_level, count in results:
            counts[prize_level] = count

        return counts

    def get_win_rate(self, lottery_type: str = None) -> float:
        """计算中奖率"""
        query_total = "SELECT COUNT(*) FROM purchases"
        query_win = "SELECT COUNT(*) FROM purchases WHERE checked = 1 AND prize_level IS NOT NULL"
        params = []

        if lottery_type:
            query_total += " WHERE lottery_type = ?"
            query_win += " AND lottery_type = ?"
            params.append(lottery_type)

        self.cursor.execute(query_total, params)
        total = self.cursor.fetchone()[0]

        self.cursor.execute(query_win, params)
        win = self.cursor.fetchone()[0]

        if total == 0:
            return 0.0
        return win / total * 100

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # 测试数据库功能
    db = LotteryDatabase("test.db")

    # 测试添加购彩记录
    purchase_id = db.add_purchase(
        purchase_date="2023-10-28",
        lottery_type="双色球",
        numbers="01,07,13,19,24,31+12",
        amount=2.0,
        channel="手机App"
    )
    print(f"添加购彩记录成功，ID: {purchase_id}")

    # 测试获取记录
    purchases = db.get_purchases(limit=5)
    print(f"获取到 {len(purchases)} 条购彩记录")

    # 测试统计信息
    total_investment = db.get_total_investment()
    print(f"总投入: {total_investment}")

    db.close()