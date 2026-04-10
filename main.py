#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彩票记录与分析工具 - 手机App版
支持双色球和大乐透的购彩记录、自动对奖、中奖统计、随机选号
"""

import os
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional

import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp

# 导入自定义模块
from database import LotteryDatabase
from network import LotteryNetwork
from algorithm import RandomNumberGenerator
from core import LotteryCore, LotteryType, PrizeLevel


class LotteryApp(App):
    """主应用类"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.network = None
        self.core = None
        self.random_gen = None

    def build(self):
        """构建应用界面"""
        self.title = "彩票记录与分析工具"

        # 初始化组件
        self._init_components()

        # 创建主布局
        main_layout = TabbedPanel(do_default_tab=False)
        main_layout.tab_height = dp(50)

        # 创建各个功能选项卡
        tabs = [
            ("主页", self._create_home_tab()),
            ("购彩记录", self._create_record_tab()),
            ("随机选号", self._create_random_tab()),
            ("开奖查询", self._create_draw_tab()),
            ("统计分析", self._create_stat_tab()),
        ]

        for tab_name, tab_content in tabs:
            tab = TabbedPanelItem(text=tab_name)
            tab.add_widget(tab_content)
            main_layout.add_widget(tab)

        return main_layout

    def _init_components(self):
        """初始化各个组件"""
        try:
            # 初始化数据库
            self.db = LotteryDatabase()
            # 初始化网络模块
            self.network = LotteryNetwork()
            # 初始化核心逻辑
            self.core = LotteryCore(self.db, self.network)
            # 初始化随机数生成器
            self.random_gen = RandomNumberGenerator()

            # 尝试连接网络获取最新开奖信息
            Clock.schedule_once(lambda dt: self._load_initial_data(), 1)
        except Exception as e:
            print(f"初始化组件失败: {e}")

    def _load_initial_data(self):
        """加载初始数据"""
        # 这里可以加载一些初始数据，比如最新开奖信息
        pass

    def _create_home_tab(self) -> BoxLayout:
        """创建主页选项卡"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 应用标题
        title = Label(
            text="彩票记录与分析工具",
            font_size=dp(24),
            size_hint=(1, 0.2),
            color=(0.2, 0.4, 0.8, 1)
        )

        # 功能简介
        intro = Label(
            text="欢迎使用彩票管理工具！\n\n功能包括：\n• 购彩记录管理\n• 自动对奖与统计\n• 智能随机选号\n• 开奖信息查询\n• 盈亏分析报表",
            font_size=dp(16),
            size_hint=(1, 0.5),
            halign='left',
            valign='top'
        )
        intro.bind(size=intro.setter('text_size'))

        # 快速操作按钮
        quick_actions = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.3))

        quick_buttons = [
            ("快速选号", self._show_random_numbers),
            ("记录购彩", self._show_record_dialog),
            ("查询开奖", self._show_draw_query),
            ("查看统计", self._show_statistics),
        ]

        for text, callback in quick_buttons:
            btn = Button(text=text, size_hint=(1, 1))
            btn.bind(on_press=lambda instance, cb=callback: cb())
            quick_actions.add_widget(btn)

        layout.add_widget(title)
        layout.add_widget(intro)
        layout.add_widget(quick_actions)

        return layout

    def _create_record_tab(self) -> ScrollView:
        """创建购彩记录选项卡"""
        scroll = ScrollView(size_hint=(1, 1))

        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 添加记录按钮
        add_btn = Button(
            text="+ 添加购彩记录",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        add_btn.bind(on_press=lambda x: self._show_record_dialog())
        content.add_widget(add_btn)

        # 记录列表区域
        self.record_list = BoxLayout(orientation='vertical', spacing=dp(5))
        content.add_widget(self.record_list)

        # 初始加载记录
        self._load_records()

        scroll.add_widget(content)
        return scroll

    def _create_random_tab(self) -> BoxLayout:
        """创建随机选号选项卡"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 彩票类型选择
        type_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=dp(10))
        type_layout.add_widget(Label(text="彩票类型:", size_hint=(0.3, 1)))

        self.lottery_spinner = Spinner(
            text="双色球",
            values=("双色球", "大乐透"),
            size_hint=(0.7, 1)
        )
        type_layout.add_widget(self.lottery_spinner)
        layout.add_widget(type_layout)

        # 生成按钮
        generate_btn = Button(
            text="生成随机号码",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.4, 0.8, 1)
        )
        generate_btn.bind(on_press=self._generate_random_numbers)
        layout.add_widget(generate_btn)

        # 结果显示区域
        result_label = Label(
            text="生成的号码将显示在这里",
            font_size=dp(18),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        result_label.bind(size=result_label.setter('text_size'))
        self.random_result_label = result_label
        layout.add_widget(result_label)

        # 算法说明
        algorithm_info = Label(
            text="算法说明：\n模拟24人各写一个数字，计算平均值作为基础号，\n若超出上限则取余数。",
            font_size=dp(14),
            size_hint=(1, 0.3),
            halign='left',
            valign='top',
            color=(0.4, 0.4, 0.4, 1)
        )
        algorithm_info.bind(size=algorithm_info.setter('text_size'))
        layout.add_widget(algorithm_info)

        return layout

    def _create_draw_tab(self) -> ScrollView:
        """创建开奖查询选项卡"""
        scroll = ScrollView(size_hint=(1, 1))

        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 查询区域
        query_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))

        self.draw_type_spinner = Spinner(
            text="双色球",
            values=("双色球", "大乐透"),
            size_hint=(0.4, 1)
        )

        query_btn = Button(
            text="查询最新开奖",
            size_hint=(0.6, 1),
            background_color=(0.2, 0.4, 0.8, 1)
        )
        query_btn.bind(on_press=self._query_latest_draw)

        query_layout.add_widget(self.draw_type_spinner)
        query_layout.add_widget(query_btn)
        content.add_widget(query_layout)

        # 开奖结果显示区域
        self.draw_result_label = Label(
            text="开奖信息将显示在这里",
            font_size=dp(16),
            size_hint=(1, None),
            halign='left',
            valign='top'
        )
        self.draw_result_label.bind(
            size=self.draw_result_label.setter('text_size'),
            texture_size=self.draw_result_label.setter('size')
        )
        content.add_widget(self.draw_result_label)

        scroll.add_widget(content)
        return scroll

    def _create_stat_tab(self) -> ScrollView:
        """创建统计分析选项卡"""
        scroll = ScrollView(size_hint=(1, 1))

        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 统计标题
        stat_title = Label(
            text="统计分析",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(40),
            color=(0.2, 0.4, 0.8, 1)
        )
        content.add_widget(stat_title)

        # 统计结果显示区域
        self.stat_result_label = Label(
            text="统计信息将显示在这里\n\n请先添加购彩记录并查询开奖",
            font_size=dp(16),
            size_hint=(1, None),
            halign='left',
            valign='top'
        )
        self.stat_result_label.bind(
            size=self.stat_result_label.setter('text_size'),
            texture_size=self.stat_result_label.setter('size')
        )
        content.add_widget(self.stat_result_label)

        # 刷新按钮
        refresh_btn = Button(
            text="刷新统计数据",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        refresh_btn.bind(on_press=self._refresh_statistics)
        content.add_widget(refresh_btn)

        scroll.add_widget(content)
        return scroll

    # ===== 业务逻辑方法 =====

    def _show_random_numbers(self):
        """显示随机选号对话框"""
        self._generate_random_numbers(None)

    def _show_record_dialog(self):
        """显示添加购彩记录对话框"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # 彩票类型选择
        type_layout = BoxLayout(orientation='horizontal')
        type_layout.add_widget(Label(text="彩票类型:", size_hint=(0.3, 1)))
        record_type_spinner = Spinner(text="双色球", values=("双色球", "大乐透"), size_hint=(0.7, 1))
        type_layout.add_widget(record_type_spinner)
        content.add_widget(type_layout)

        # 号码输入
        number_layout = BoxLayout(orientation='vertical')
        number_layout.add_widget(Label(text="号码 (用逗号分隔):"))
        number_input = TextInput(multiline=False, hint_text="例: 01,07,13,19,24,31+12")
        number_layout.add_widget(number_input)
        content.add_widget(number_layout)

        # 金额输入
        amount_layout = BoxLayout(orientation='horizontal')
        amount_layout.add_widget(Label(text="投注金额:", size_hint=(0.3, 1)))
        amount_input = TextInput(text="2", multiline=False, input_filter='int', size_hint=(0.7, 1))
        amount_layout.add_widget(amount_input)
        content.add_widget(amount_layout)

        # 渠道输入（可选）
        channel_layout = BoxLayout(orientation='horizontal')
        channel_layout.add_widget(Label(text="购彩渠道:", size_hint=(0.3, 1)))
        channel_input = TextInput(text="手机App", multiline=False, size_hint=(0.7, 1))
        channel_layout.add_widget(channel_input)
        content.add_widget(channel_layout)

        # 错误信息标签
        error_label = Label(text="", size_hint=(1, None), height=dp(30), color=(1, 0, 0, 1))
        content.add_widget(error_label)

        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, None), height=dp(50))
        cancel_btn = Button(text="取消")
        save_btn = Button(text="保存", background_color=(0.2, 0.6, 0.2, 1))

        def save_record(instance):
            # 获取输入值
            lottery_type = record_type_spinner.text
            numbers = number_input.text.strip()
            amount_text = amount_input.text.strip()
            channel = channel_input.text.strip()

            # 验证输入
            if not numbers:
                error_label.text = "请输入号码"
                return

            if not amount_text:
                error_label.text = "请输入投注金额"
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    error_label.text = "投注金额必须大于0"
                    return
            except ValueError:
                error_label.text = "投注金额必须是数字"
                return

            # 验证号码格式（使用core模块）
            if self.core:
                valid, message, detail = self.core.validate_numbers(lottery_type, numbers)
                if not valid:
                    error_label.text = f"号码格式错误: {message}"
                    return
            else:
                # 基本验证
                if '+' not in numbers:
                    error_label.text = "号码格式错误，应包含'+'分隔"
                    return

            # 保存到数据库
            try:
                purchase_date = datetime.now().strftime("%Y-%m-%d")
                purchase_id = self.db.add_purchase(
                    purchase_date=purchase_date,
                    lottery_type=lottery_type,
                    numbers=numbers,
                    amount=amount,
                    channel=channel if channel else "手机App"
                )

                if purchase_id:
                    # 成功
                    popup.dismiss()
                    # 刷新记录列表
                    self._load_records()
                    # 显示成功消息
                    success_popup = Popup(
                        title="成功",
                        content=Label(text=f"购彩记录添加成功！\nID: {purchase_id}"),
                        size_hint=(0.6, 0.4)
                    )
                    success_popup.open()
                    Clock.schedule_once(lambda dt: success_popup.dismiss(), 2)
                else:
                    error_label.text = "保存失败，请重试"
            except Exception as e:
                error_label.text = f"保存失败: {str(e)}"

        def cancel(instance):
            popup.dismiss()

        save_btn.bind(on_press=save_record)
        cancel_btn.bind(on_press=cancel)

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(save_btn)
        content.add_widget(btn_layout)

        popup = Popup(
            title="添加购彩记录",
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()

    def _show_draw_query(self):
        """显示开奖查询"""
        # 切换到开奖查询选项卡
        pass

    def _show_statistics(self):
        """显示统计分析"""
        # 切换到统计分析选项卡
        pass

    def _generate_random_numbers(self, instance):
        """生成随机号码"""
        lottery_type = self.lottery_spinner.text
        try:
            if self.random_gen:
                numbers = self.random_gen.generate_numbers(lottery_type)
                display = numbers["display"]

                # 格式化显示
                if lottery_type == "双色球":
                    reds = numbers["numbers"]["red"]
                    blue = numbers["numbers"]["blue"][0]
                    result = f"红球: {', '.join(str(x).zfill(2) for x in reds)}\n蓝球: {str(blue).zfill(2)}"
                else:  # 大乐透
                    fronts = numbers["numbers"]["front"]
                    backs = numbers["numbers"]["back"]
                    result = f"前区: {', '.join(str(x).zfill(2) for x in fronts)}\n后区: {', '.join(str(x).zfill(2) for x in backs)}"

                # 添加算法说明
                result += f"\n\n(使用24人算法生成，种子: {numbers['seed']})"
            else:
                result = "随机数生成器未初始化"

            self.random_result_label.text = result
        except Exception as e:
            self.random_result_label.text = f"生成号码失败: {e}"

    def _query_latest_draw(self, instance):
        """查询最新开奖信息"""
        lottery_type = self.draw_type_spinner.text
        self.draw_result_label.text = f"正在查询{lottery_type}最新开奖信息..."

        try:
            # 使用网络模块获取开奖信息
            if self.network:
                draw_data = self.network.fetch_latest_draw(lottery_type)
                if draw_data:
                    # 格式化显示
                    if lottery_type == "双色球":
                        result = f"""双色球第{draw_data['draw_number']}期开奖结果：
开奖日期: {draw_data['draw_date']}
红球: {draw_data['numbers']}
奖池: {draw_data['prize_pool']:.2f}亿元
下一期开奖: {draw_data.get('next_draw_date', '待定')}
数据来源: {draw_data.get('source', '未知')}"""
                    else:  # 大乐透
                        result = f"""大乐透第{draw_data['draw_number']}期开奖结果：
开奖日期: {draw_data['draw_date']}
前区: {draw_data['numbers']}
奖池: {draw_data['prize_pool']:.2f}亿元
下一期开奖: {draw_data.get('next_draw_date', '待定')}
数据来源: {draw_data.get('source', '未知')}"""

                    self.draw_result_label.text = result
                else:
                    self.draw_result_label.text = f"获取{lottery_type}开奖信息失败"
            else:
                self.draw_result_label.text = "网络模块未初始化"
        except Exception as e:
            self.draw_result_label.text = f"查询开奖信息失败: {e}"


    def _refresh_statistics(self, instance):
        """刷新统计数据"""
        try:
            if self.core:
                # 获取统计报告
                stats = self.core.get_statistics_report()
                self.stat_result_label.text = stats
            else:
                self.stat_result_label.text = "核心模块未初始化，无法获取统计数据"
        except Exception as e:
            self.stat_result_label.text = f"获取统计数据失败: {e}\n\n请先添加购彩记录并查询开奖。"

    def _load_records(self):
        """加载购彩记录"""
        # 清空现有记录
        self.record_list.clear_widgets()

        try:
            if self.db:
                # 从数据库获取购彩记录
                purchases = self.db.get_purchases(limit=50)

                if not purchases:
                    # 没有记录，显示提示
                    empty_label = Label(
                        text="暂无购彩记录\n\n点击上方按钮添加记录",
                        font_size=dp(16),
                        size_hint=(1, None),
                        height=dp(100),
                        halign='center',
                        valign='middle'
                    )
                    empty_label.bind(size=empty_label.setter('text_size'))
                    self.record_list.add_widget(empty_label)
                    return

                for purchase in purchases:
                    # 格式化显示
                    date_str = purchase.get('purchase_date', '未知日期')
                    lottery_type = purchase.get('lottery_type', '未知类型')
                    numbers = purchase.get('numbers', '')
                    amount = purchase.get('amount', 0)

                    # 如果有中奖信息，添加标记
                    prize_level = purchase.get('prize_level')
                    if prize_level:
                        date_type = f"{date_str} {lottery_type} ✓"
                    else:
                        date_type = f"{date_str} {lottery_type}"

                    # 创建记录项
                    record_item = BoxLayout(
                        orientation='horizontal',
                        size_hint=(1, None),
                        height=dp(60),
                        padding=dp(5)
                    )

                    record_item.add_widget(Label(
                        text=date_type,
                        size_hint=(0.4, 1),
                        halign='left'
                    ))

                    record_item.add_widget(Label(
                        text=numbers,
                        size_hint=(0.4, 1),
                        halign='left'
                    ))

                    record_item.add_widget(Label(
                        text=f"{amount}元",
                        size_hint=(0.2, 1),
                        halign='right'
                    ))

                    self.record_list.add_widget(record_item)
            else:
                # 数据库未初始化
                error_label = Label(
                    text="数据库未初始化",
                    font_size=dp(16),
                    size_hint=(1, None),
                    height=dp(60),
                    halign='center'
                )
                error_label.bind(size=error_label.setter('text_size'))
                self.record_list.add_widget(error_label)
        except Exception as e:
            error_label = Label(
                text=f"加载记录失败: {e}",
                font_size=dp(14),
                size_hint=(1, None),
                height=dp(60),
                halign='center'
            )
            error_label.bind(size=error_label.setter('text_size'))
            self.record_list.add_widget(error_label)

    def on_stop(self):
        """应用退出时的清理工作"""
        if self.db:
            self.db.close()


if __name__ == '__main__':
    # 设置窗口大小（模拟手机屏幕）
    Window.size = (360, 640)

    # 运行应用
    LotteryApp().run()