#!/usr/bin/python3
#NOTICE: this code was generously provided by my friend https://github.com/Patrolin/

from collections import UserList
import operator


class Zaliby(UserList):
	MAX = 2 << 14

	def __init__(self, code: str):
		super().__init__()
		self.code = code
		self.number_stack = []
		self.pointer = 0
		self.pointer_stack = []

	def __iter__(self):
		while self.pointer < len(self.code):
			char = self.code[self.pointer]

			# NUMBERS
			if char in set('0123456789'):
				self.number_stack.append(char)
			else:
				if self.number_stack:
					self.append(int(''.join(self.number_stack)))
					self.number_stack.clear()

				# OPERATORS
				if char in set('+-*/<='):
					b = self.pop()
					self.append(
						{
						 '+': operator.add,
						 '-': operator.sub,
						 '*': operator.mul,
						 '/': operator.floordiv,
						 '<': operator.lt,
						 '=': operator.eq
						}.get(char)(self.pop(), b) % Zaliby.MAX
					)
				elif char == ';':
					self.append(self[-1])
				# OUTPUT
				elif char == '.':
					yield self.pop()

				# WHILE
				elif char == '[':
					self.pointer_stack.append(self.pointer)
					self.pointer_stack.append(self.code.index(']', self.pointer))
				elif char == '@':
					if self.pop() == 0:
						self.pointer = self.pointer_stack[-1]
						self.pointer_stack.pop()
						self.pointer_stack.pop()
				elif char == ']':
					self.pointer = self.pointer_stack[-2]

				# TERNARY
				elif char == '?':
					if self.pop() == 0:
						self.pointer = self.code.index(':', self.pointer)
				elif char == ':':
					self.pointer = self.code.index('!', self.pointer)

			self.pointer += 1


if __name__ == '__main__':
	for output in Zaliby('10 [;110 < @ ;. 10 +]'):
		print(output)