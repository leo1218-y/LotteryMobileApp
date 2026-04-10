#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机选号算法模块
实现基于24人算法的智能随机选号
"""

import random
import time
from typing import List, Tuple, Dict, Optional, Any


class RandomNumberGenerator:
    """随机数生成器类"""

    def __init__(self, seed: int = None):
        """初始化生成器"""
        if seed is None:
            seed = int(time.time() * 1000) % 1000000
        random.seed(seed)
        self.seed = seed

        # 算法参数
        self.num_people = 24  # 24个人
        self.min_number = -500  # 每人可写的最小数字
        self.max_number = 500   # 每人可写的最大数字

        # 彩票规则
        self.lottery_rules = {
            "双色球": {
                "red": {
                    "count": 6,
                    "range": (1, 33),
                    "description": "红球"
                },
                "blue": {
                    "count": 1,
                    "range": (1, 16),
                    "description": "蓝球"
                }
            },
            "大乐透": {
                "front": {
                    "count": 5,
                    "range": (1, 35),
                    "description": "前区"
                },
                "back": {
                    "count": 2,
                    "range": (1, 12),
                    "description": "后区"
                }
            }
        }

    def generate_numbers(self, lottery_type: str) -> Dict[str, Any]:
        """生成随机号码"""
        if lottery_type not in self.lottery_rules:
            raise ValueError(f"不支持的彩票类型: {lottery_type}")

        rules = self.lottery_rules[lottery_type]
        result = {
            "lottery_type": lottery_type,
            "seed": self.seed,
            "numbers": {},
            "display": "",
            "algorithm_steps": []
        }

        if lottery_type == "双色球":
            # 生成红球
            red_numbers = self._generate_unique_numbers(
                "red", rules["red"]["count"], rules["red"]["range"]
            )
            result["numbers"]["red"] = red_numbers
            result["algorithm_steps"].append(self._get_last_algorithm_steps())

            # 生成蓝球
            blue_numbers = self._generate_unique_numbers(
                "blue", rules["blue"]["count"], rules["blue"]["range"]
            )
            result["numbers"]["blue"] = blue_numbers
            result["algorithm_steps"].append(self._get_last_algorithm_steps())

            # 格式化显示
            red_display = ','.join(str(x).zfill(2) for x in sorted(red_numbers))
            blue_display = str(blue_numbers[0]).zfill(2)
            result["display"] = f"{red_display}+{blue_display}"

        elif lottery_type == "大乐透":
            # 生成前区
            front_numbers = self._generate_unique_numbers(
                "front", rules["front"]["count"], rules["front"]["range"]
            )
            result["numbers"]["front"] = front_numbers
            result["algorithm_steps"].append(self._get_last_algorithm_steps())

            # 生成后区
            back_numbers = self._generate_unique_numbers(
                "back", rules["back"]["count"], rules["back"]["range"]
            )
            result["numbers"]["back"] = back_numbers
            result["algorithm_steps"].append(self._get_last_algorithm_steps())

            # 格式化显示
            front_display = ','.join(str(x).zfill(2) for x in sorted(front_numbers))
            back_display = ','.join(str(x).zfill(2) for x in sorted(back_numbers))
            result["display"] = f"{front_display}+{back_display}"

        return result

    def _generate_unique_numbers(self, number_type: str, count: int,
                                 number_range: Tuple[int, int]) -> List[int]:
        """生成一组不重复的随机号码"""
        numbers = []
        attempts = 0
        max_attempts = 100  # 防止无限循环

        while len(numbers) < count and attempts < max_attempts:
            # 为每个位置生成一个号码
            base_number = self._generate_single_number(number_range)

            # 确保不重复
            if base_number not in numbers:
                numbers.append(base_number)

            attempts += 1

        # 如果尝试次数过多仍未生成足够的不重复号码，使用备用方法
        if len(numbers) < count:
            needed = count - len(numbers)
            all_possible = list(range(number_range[0], number_range[1] + 1))
            remaining = [x for x in all_possible if x not in numbers]

            if len(remaining) >= needed:
                extra = random.sample(remaining, needed)
                numbers.extend(extra)
            else:
                # 如果可能的值不够，允许重复
                while len(numbers) < count:
                    numbers.append(self._generate_single_number(number_range))

        return sorted(numbers)

    def _generate_single_number(self, number_range: Tuple[int, int]) -> int:
        """使用24人算法生成单个号码"""
        min_val, max_val = number_range
        limit = max_val  # 上限

        # 步骤1: 24个人各写一个数字
        people_numbers = []
        for i in range(self.num_people):
            # 每个人写一个数字，范围在min_number到max_number之间
            number = random.randint(self.min_number, self.max_number)
            people_numbers.append(number)

        # 步骤2: 计算24个数字的总和
        total = sum(people_numbers)

        # 步骤3: 计算平均值并取整
        average = total / self.num_people
        base_number = int(round(average))

        # 步骤4: 处理超出范围的情况
        if base_number > limit:
            remainder = base_number % limit
            if remainder == 0:
                final_number = limit
            else:
                final_number = remainder
        elif base_number < 1:
            # 处理负数或0的情况
            abs_number = abs(base_number)
            remainder = abs_number % limit
            if remainder == 0:
                final_number = limit
            else:
                final_number = remainder
        else:
            final_number = base_number

        # 确保在有效范围内
        final_number = max(1, min(final_number, limit))

        # 保存算法步骤详情（用于调试和显示）
        self.last_algorithm_steps = {
            "people_numbers": people_numbers,
            "total": total,
            "average": average,
            "base_number": base_number,
            "limit": limit,
            "final_number": final_number,
            "calculation": f"{total} ÷ {self.num_people} = {average:.2f} → {base_number} → {final_number}"
        }

        return final_number

    def _get_last_algorithm_steps(self) -> Dict[str, Any]:
        """获取上一次算法步骤详情"""
        return getattr(self, 'last_algorithm_steps', {})

    def generate_multiple_sets(self, lottery_type: str, count: int = 5) -> List[Dict[str, Any]]:
        """生成多组随机号码"""
        sets = []
        for i in range(count):
            # 每次使用不同的种子
            new_seed = self.seed + i + 1
            generator = RandomNumberGenerator(new_seed)
            numbers = generator.generate_numbers(lottery_type)
            numbers["set_number"] = i + 1
            sets.append(numbers)
        return sets

    def get_algorithm_explanation(self) -> str:
        """获取算法说明"""
        explanation = """24人算法说明：

步骤：
1. 模拟24个人，每人写一个数字（范围：-500到500）
2. 将24个数字相加得到总和
3. 总和除以24得到平均值，取整作为基础号码
4. 如果基础号码超出该位置的上限：
   - 计算基础号码除以上限的余数
   - 如果余数为0，则取上限值
   - 否则取余数作为最终号码
5. 如果基础号码在范围内，直接使用

特点：
- 每个号码位置独立计算
- 算法具有随机性但又有一定规律
- 可重复生成相同的种子会产生相同结果

示例：
假设红球上限为33，24人数字之和为100：
平均值 = 100 ÷ 24 ≈ 4.17 → 取整为4 → 4在1-33范围内 → 最终号码为4

假设蓝球上限为16，24人数字之和为500：
平均值 = 500 ÷ 24 ≈ 20.83 → 取整为21 → 21超出1-16范围
余数 = 21 % 16 = 5 → 最终号码为5
"""
        return explanation

    def get_detailed_algorithm_info(self, lottery_type: str, number_set: Dict[str, Any]) -> str:
        """获取详细的算法信息"""
        info = f"彩票类型: {lottery_type}\n"
        info += f"随机种子: {number_set.get('seed', self.seed)}\n"
        info += f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        info += "生成的号码:\n"
        info += f"  {number_set['display']}\n\n"

        if "algorithm_steps" in number_set:
            info += "算法步骤详情:\n"

            if lottery_type == "双色球":
                # 红球步骤
                if len(number_set["algorithm_steps"]) > 0:
                    red_steps = number_set["algorithm_steps"][0]
                    info += f"\n红球生成步骤:\n"
                    info += f"  24人数字: {red_steps['people_numbers'][:6]}... (共24个)\n"
                    info += f"  总和: {red_steps['total']}\n"
                    info += f"  平均值: {red_steps['average']:.2f}\n"
                    info += f"  基础号码: {red_steps['base_number']}\n"
                    info += f"  上限: {red_steps['limit']}\n"
                    info += f"  最终号码: {red_steps['final_number']}\n"
                    info += f"  计算过程: {red_steps['calculation']}\n"

                # 蓝球步骤
                if len(number_set["algorithm_steps"]) > 1:
                    blue_steps = number_set["algorithm_steps"][1]
                    info += f"\n蓝球生成步骤:\n"
                    info += f"  24人数字: {blue_steps['people_numbers'][:6]}... (共24个)\n"
                    info += f"  总和: {blue_steps['total']}\n"
                    info += f"  平均值: {blue_steps['average']:.2f}\n"
                    info += f"  基础号码: {blue_steps['base_number']}\n"
                    info += f"  上限: {blue_steps['limit']}\n"
                    info += f"  最终号码: {blue_steps['final_number']}\n"
                    info += f"  计算过程: {blue_steps['calculation']}\n"

            elif lottery_type == "大乐透":
                # 类似处理大乐透
                pass

        return info


# 测试代码
if __name__ == "__main__":
    print("测试随机数生成器...")
    print("-" * 50)

    # 创建生成器
    generator = RandomNumberGenerator(123456)
    print(f"随机种子: {generator.seed}")

    # 测试双色球
    print("\n生成双色球号码:")
    ssq_numbers = generator.generate_numbers("双色球")
    print(f"号码: {ssq_numbers['display']}")
    print(f"红球: {ssq_numbers['numbers']['red']}")
    print(f"蓝球: {ssq_numbers['numbers']['blue']}")

    # 测试大乐透
    print("\n生成大乐透号码:")
    dlt_numbers = generator.generate_numbers("大乐透")
    print(f"号码: {dlt_numbers['display']}")
    print(f"前区: {dlt_numbers['numbers']['front']}")
    print(f"后区: {dlt_numbers['numbers']['back']}")

    # 测试多组生成
    print("\n生成5组双色球号码:")
    multiple_sets = generator.generate_multiple_sets("双色球", 5)
    for i, number_set in enumerate(multiple_sets, 1):
        print(f"第{i}组: {number_set['display']}")

    # 显示算法说明
    print("\n" + "=" * 50)
    print("算法说明:")
    print(generator.get_algorithm_explanation())

    # 显示详细算法信息
    print("\n详细算法信息:")
    detailed_info = generator.get_detailed_algorithm_info("双色球", ssq_numbers)
    print(detailed_info[:500] + "...")  # 只显示前500字符