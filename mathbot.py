import os
import discord
from discord.ext import commands
import operator
import ast
from dotenv import load_dotenv

# --- 安全運算邏輯 (取代 eval()) ---
load_dotenv()
TOKEN = os.getenv('MATHBOT_TOKEN')
print("mathbot token get: ", TOKEN)


# 定義安全允許的運算符號
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}

class Calculator:
    """用於安全地解析和計算數學表達式的類別。"""
    def evaluate(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise TypeError("不允許的常數類型。")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise TypeError("不允許的運算符號。")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ValueError("除數不能為零。")
            return ALLOWED_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return operator.neg(self.evaluate(node.operand))
            raise TypeError("不允許的一元運算符號。")
        raise TypeError("運算式包含不允許的元素。")

    def safe_calculate(self, expression):
        node = ast.parse(expression, mode='eval').body
        return self.evaluate(node)


# --- Discord Bot 設定 ---
BOT_PREFIX = '$'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'MathBot 已登入為: {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f'{BOT_PREFIX}calc'
    ))

@bot.command(name='calc', help='計算數學表達式。例如: $calc 15 * (5 + 2) / 3')
async def calculate_command(ctx, *, expression: str):
    expression = expression.replace(" ", "")
    try:
        calculator = Calculator()
        result = calculator.safe_calculate(expression)
        result_str = f'{result:.4f}' if isinstance(result, float) else str(result)
        await ctx.send(f'**數學計算結果**\n輸入: `{expression}`\n答案: **`{result_str}`**')
    except (TypeError, ValueError) as e:
        await ctx.send(f'⚠️ **計算錯誤**：{e}')
    except Exception:
        await ctx.send(f'❌ **輸入格式無效**。請檢查您的數學表達式。')


# --- 提供給 main.py 用的 async 啟動函數 ---
async def run_bot():
    token = os.getenv('MATHBOT_TOKEN')
    if not token:
        raise ValueError("MATHBOT_TOKEN 沒有設定！")
    await bot.start(token)  # ⚠️ 注意：這裡改成 await，不使用 bot.run()


# --- 保留獨立運行的功能 ---
if __name__ == '__main__':
    import asyncio
    asyncio.run(run_bot())
