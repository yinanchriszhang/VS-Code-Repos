from tkinter import Tk, Entry, Button, StringVar, LEFT, END
import ast
import csv
from datetime import datetime
from pathlib import Path


def safe_eval(expr: str):
	"""Evaluate a math expression safely using AST.

	Allowed nodes: Expression, BinOp, UnaryOp, Constant/Num, operators + - * / % ** // and parentheses.
	"""
	allowed_nodes = (
		ast.Expression,
		ast.BinOp,
		ast.UnaryOp,
		ast.Constant,
		ast.Load,
		ast.Expr,
	)

	allowed_ops = (
		ast.Add,
		ast.Sub,
		ast.Mult,
		ast.Div,
		ast.Mod,
		ast.Pow,
		ast.FloorDiv,
		ast.UAdd,
		ast.USub,
	)

	node = ast.parse(expr, mode="eval")

	for n in ast.walk(node):
		if isinstance(n, ast.BinOp):
			if not isinstance(n.op, allowed_ops):
				raise ValueError("Disallowed operator")
		elif isinstance(n, ast.UnaryOp):
			if not isinstance(n.op, allowed_ops):
				raise ValueError("Disallowed unary operator")
		elif isinstance(n, ast.Call):
			raise ValueError("Function calls not allowed")
		# allow space and operator nodes
		elif isinstance(n, (ast.Expression, ast.Constant, ast.Expr, ast.Load)):
			continue
		elif isinstance(n, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv, ast.UAdd, ast.USub)):
			continue
		else:
			raise ValueError(f"Disallowed expression: {type(n).__name__}")

	return eval(compile(node, "<ast>", mode="eval"))


LOG_FILE = Path("Calculator - Agent Build\calculator_log.csv")


def log_entry(expression: str, result, filename: Path | str | None = None):
	"""Append a log row with timestamp, input expression, and result to CSV."""
	if filename is None:
		filename = LOG_FILE
	# ensure parent dir exists
	fpath = Path(filename)
	first = not fpath.exists()
	with fpath.open("a", newline="", encoding="utf-8") as fh:
		writer = csv.writer(fh)
		if first:
			writer.writerow(["timestamp", "expression", "result"])
		writer.writerow([datetime.utcnow().isoformat(), expression, str(result)])


class Calculator:
	def __init__(self, master):
		self.master = master
		master.title("Calculator")

		self.value = StringVar()
		self.entry = Entry(master, textvariable=self.value, justify=LEFT, font=(None, 18))
		self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

		buttons = [
			('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
			('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
			('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
			('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
		]

		for (text, r, c) in buttons:
			action = (lambda x=text: self.on_button(x))
			b = Button(master, text=text, width=5, height=2, command=action, font=(None, 14))
			b.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

		clear = Button(master, text='C', width=5, height=2, command=self.clear, font=(None, 14))
		clear.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

		back = Button(master, text='⌫', width=5, height=2, command=self.backspace, font=(None, 14))
		back.grid(row=5, column=2, padx=3, pady=3, sticky="nsew")

		plusminus = Button(master, text='±', width=5, height=2, command=self.plusminus, font=(None, 14))
		plusminus.grid(row=5, column=3, padx=3, pady=3, sticky="nsew")

		master.bind('<Return>', lambda e: self.on_button('='))
		master.bind('<BackSpace>', lambda e: self.backspace())
		master.bind('<Escape>', lambda e: self.clear())

	def on_button(self, char):
		if char == '=':
			expr = self.value.get()
			try:
				result = safe_eval(expr)
				self.value.set(str(result))
				try:
					log_entry(expr, result)
				except Exception:
					# non-fatal: logging failure should not break UI
					pass
			except Exception:
				self.value.set('Error')
		else:
			self.entry.insert(END, char)

	def clear(self):
		self.value.set('')

	def backspace(self):
		s = self.value.get()
		self.value.set(s[:-1])

	def plusminus(self):
		s = self.value.get()
		if not s:
			return
		try:
			v = safe_eval(s)
			self.value.set(str(-v))
		except Exception:
			self.value.set('Error')


def self_test():
	tests = {
		'1+1': 2,
		'2*3+4': 10,
		'2**3': 8,
		'10/4': 2.5,
	}
	for expr, expect in tests.items():
		val = safe_eval(expr)
		if abs(val - expect) > 1e-9:
			return False
	return True


def main():
	root = Tk()
	calc = Calculator(root)
	root.mainloop()


if __name__ == '__main__':
	main()

