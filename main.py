import ast
import operator
import re
import sqlite3
from datetime import datetime

DB_NAME = "pyclaw.db"

# Chỉ cho phép các phép tính an toàn
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    """Tính biểu thức số học mà không dùng eval()."""
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Chỉ hỗ trợ số.")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError("Phép toán không được hỗ trợ.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if op_type is ast.Pow and abs(right) > 10:
                raise ValueError("Số mũ quá lớn.")

            result = OPERATORS[op_type](left, right)

            if abs(result) > 10**100:
                raise ValueError("Kết quả quá lớn.")

            return result

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError("Toán tử không được hỗ trợ.")
            return OPERATORS[op_type](evaluate(node.operand))

        raise ValueError("Biểu thức không hợp lệ.")

    return evaluate(tree)


# ---------- Giải phương trình bậc 1 và bậc 2 ----------

def poly_add(p, q, sign=1):
    result = dict(p)
    for degree, coef in q.items():
        result[degree] = result.get(degree, 0.0) + sign * coef
    return result


def poly_mul(p, q):
    result = {}
    for d1, c1 in p.items():
        for d2, c2 in q.items():
            result[d1 + d2] = result.get(d1 + d2, 0.0) + c1 * c2
    return result


def check_degree(poly):
    for degree, coef in poly.items():
        if degree > 2 and abs(coef) > 1e-12:
            raise ValueError("Chỉ hỗ trợ phương trình bậc 1 và bậc 2.")
    return poly


def parse_poly(expression):
    """Biến biểu thức theo x thành đa thức {bậc: hệ số}, không dùng eval()."""
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return {0: float(node.value)}
            raise ValueError("Chỉ hỗ trợ số.")

        if isinstance(node, ast.Name):
            if node.id == "x":
                return {1: 1.0}
            raise ValueError(f"Chỉ hỗ trợ ẩn x, không hiểu '{node.id}'.")

        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)
            if isinstance(node.op, ast.USub):
                return {d: -c for d, c in value.items()}
            if isinstance(node.op, ast.UAdd):
                return value
            raise ValueError("Toán tử không được hỗ trợ.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Add):
                return poly_add(left, right, 1)
            if isinstance(node.op, ast.Sub):
                return poly_add(left, right, -1)
            if isinstance(node.op, ast.Mult):
                return check_degree(poly_mul(left, right))
            if isinstance(node.op, ast.Div):
                if set(right) - {0}:
                    raise ValueError("Chỉ được chia cho một số.")
                divisor = right.get(0, 0.0)
                if divisor == 0:
                    raise ZeroDivisionError("chia cho 0")
                return {d: c / divisor for d, c in left.items()}
            if isinstance(node.op, ast.Pow):
                if set(right) - {0}:
                    raise ValueError("Số mũ phải là số nguyên 0, 1 hoặc 2.")
                exponent = right.get(0, 0.0)
                if exponent not in (0, 1, 2):
                    raise ValueError("Số mũ phải là số nguyên 0, 1 hoặc 2.")
                result = {0: 1.0}
                for _ in range(int(exponent)):
                    result = poly_mul(result, left)
                return check_degree(result)

        raise ValueError("Phương trình không hợp lệ.")

    return evaluate(tree)


def prepare_side(text):
    """Chuẩn hóa: 2x^2 -> 2*x**2, 3(x+1) -> 3*(x+1)."""
    text = text.lower().replace(",", ".").replace("^", "**")
    text = re.sub(r"(\d|\))\s*x", r"\1*x", text)
    text = re.sub(r"x\s*\(", "x*(", text)
    text = re.sub(r"(\d|\))\s*\(", r"\1*(", text)
    return text.strip()


def fmt(number):
    number = round(number, 10)
    if number == 0:
        number = 0.0
    return f"{number:.6g}"


def sign_fmt(number):
    """Định dạng có dấu: '+ 5' hoặc '- 5'."""
    return f"{'-' if round(number, 10) < 0 else '+'} {fmt(abs(number))}"


def solve_equation(equation):
    if equation.count("=") != 1:
        raise ValueError("Phương trình cần đúng một dấu '='.")

    left, right = equation.split("=")
    if not left.strip() or not right.strip():
        raise ValueError("Hai vế của phương trình không được để trống.")

    expression = f"({prepare_side(left)}) - ({prepare_side(right)})"
    poly = parse_poly(expression)

    a = round(poly.get(2, 0.0), 10)
    b = round(poly.get(1, 0.0), 10)
    c = round(poly.get(0, 0.0), 10)

    if a != 0:
        delta = b * b - 4 * a * c
        header = (
            f"Phương trình bậc 2: {fmt(a)}x² {sign_fmt(b)}x {sign_fmt(c)} = 0\n"
        )
        header += f"Delta = {fmt(delta)}\n"
        if delta < 0:
            return header + "Delta < 0: phương trình vô nghiệm (trong số thực)."
        if delta == 0:
            return header + f"Nghiệm kép: x = {fmt(-b / (2 * a))}"
        root = delta ** 0.5
        x1 = (-b - root) / (2 * a)
        x2 = (-b + root) / (2 * a)
        return header + f"Hai nghiệm: x1 = {fmt(x1)}, x2 = {fmt(x2)}"

    if b != 0:
        return (
            f"Phương trình bậc 1: {fmt(b)}x {sign_fmt(c)} = 0\n"
            f"Nghiệm: x = {fmt(-c / b)}"
        )

    if c == 0:
        return "Phương trình có vô số nghiệm."
    return "Phương trình vô nghiệm."


# ---------- Cơ sở dữ liệu ----------

def setup_database():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_message(role, content):
    with sqlite3.connect(DB_NAME) as db:
        db.execute(
            """
            INSERT INTO messages (role, content, created_at)
            VALUES (?, ?, ?)
            """,
            (role, content, datetime.now().isoformat(timespec="seconds")),
        )


def show_history():
    with sqlite3.connect(DB_NAME) as db:
        rows = db.execute(
            """
            SELECT role, content, created_at
            FROM messages ORDER BY id DESC LIMIT 10
            """
        ).fetchall()

    if not rows:
        print("Chưa có lịch sử trò chuyện.\n")
        return

    print("\n--- 10 tin nhắn gần nhất ---")
    for role, content, created_at in reversed(rows):
        print(f"[{created_at}] {role}: {content}")
    print()


# ---------- Trả lời ----------

def reply(message):
    text = message.strip()
    lower = text.lower()

    if lower in ("xin chao", "xin chào", "chào", "chao", "hello", "hi"):
        return "Chào bạn! Mình là PyClaw Assistant. Gõ 'help' để xem lệnh."

    if lower == "help":
        return (
            "Các lệnh có sẵn:\n"
            "- help: xem hướng dẫn\n"
            "- gio: xem giờ hiện tại\n"
            "- tinh <biểu thức>: tính toán, ví dụ tinh 12 * (3 + 2)\n"
            "- giai <phương trình>: giải phương trình bậc 1, bậc 2,\n"
            "    ví dụ giai 2x + 6 = 0 hoặc giai x^2 - 5x + 6 = 0\n"
            "- lichsu: xem lịch sử\n"
            "- thoat: kết thúc chương trình"
        )

    if lower == "gio":
        return datetime.now().strftime("Bây giờ là %H:%M:%S, ngày %d/%m/%Y.")

    if lower.startswith("tinh "):
        expression = text[5:].strip()
        try:
            return f"Kết quả: {calculate(expression)}"
        except (ValueError, SyntaxError, ZeroDivisionError,
                OverflowError) as error:
            return f"Không tính được: {error}"

    if lower.startswith("giai "):
        equation = text[5:].strip()
        try:
            return solve_equation(equation)
        except (ValueError, SyntaxError, ZeroDivisionError,
                OverflowError) as error:
            return f"Không giải được: {error}"

    return (
        "Mình chưa hiểu yêu cầu này. Hãy nhập 'help' để xem "
        "các lệnh hiện có."
    )


def main():
    setup_database()

    print("=" * 40)
    print("       PYCLAW ASSISTANT")
    print("=" * 40)
    print("Nhập 'help' để xem hướng dẫn.")
    print("Nhập 'thoat' để kết thúc.\n")

    while True:
        try:
            message = input("Bạn: ").strip()
        except (EOFError, OSError):
            print("\nKhông nhận được dữ liệu nhập từ terminal.")
            print("Hãy chạy lại bằng Terminal của VS Code.")
            break

        if not message:
            continue

        if message.lower() in ("thoat", "exit", "quit"):
            print("PyClaw đã kết thúc.")
            break

        if message.lower() == "lichsu":
            show_history()
            continue

        save_message("user", message)
        answer = reply(message)
        save_message("assistant", answer)
        print(f"PyClaw: {answer}\n")


if __name__ == "__main__":
    main()