###############################################################
# Advent of Code 2022                                         #
# Day 07 https://adventofcode.com/2021/day/07                 #
# Puzzle input at https://adventofcode.com/2022/day/07/input  #
###############################################################

import enum
from collections import deque
import logging
from dsplot.graph import Graph


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [line.strip() for line in fs]
    return input

class Node:
    def __init__(self, node_name, size=0):
        self.children = []
        self.parent = None
        self.name = node_name
        self.size = size

    def __str__(self):
        return f'{self.name} (size {self.size})'

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class FileTree:
    def __init__(self):
        self.rootNode = None
        self.curNode = None

    def descend_to_child_node(self, node_name):
        self.curNode = next(child for child in self.curNode.children if child.name==node_name)

    def add_node(self, child_name, size=0):
        new_node = Node(node_name=child_name, size=size)
        self.curNode.add_child(new_node)
        # print(f'Adding node {self.nodeList[child_name]} to {self.curNode}')

    def add_root_node(self, node_name):
        self.rootNode = Node(node_name)
        self.curNode = self.rootNode
        # print(f'Setting {node_name} as root node!')

    def go_one_node_up(self):
        self.curNode = self.curNode.parent
        # print(f'stepping up one node to node {self.curNode}')

    def traverseTree(self, limit=70_000_000):
        result_list = {}
        nodes_to_visit = deque()
        nodes_to_visit.append(self.rootNode)
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            nodes_to_visit += current_node.children
            if (current_node.size <= limit) & ~(len(current_node.children) == 0):
                result_list[current_node.name] = current_node.size
                logging.info(f'Node {current_node} with parent {current_node.parent}')
        return result_list

    def createTreeDict(self):
        result_list = {}
        nodes_to_visit = deque()
        nodes_to_visit.append(self.rootNode)
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            nodes_to_visit += current_node.children
            result_list[current_node.name] = [c.name for c in current_node.children]
        return result_list

    def recursivelySumUpDirSize(self):

        def digDeeper(node):
            if len(node.children) == 0:
                return node.size
            for child in node.children:
                node.size += digDeeper(child)
            return node.size

        digDeeper(self.rootNode)


class TokenType(enum.Enum):
    CHANGE_TO_ROOT = 11
    CHANGE_TO_DIRECTORY = 12
    CHANGE_DIRECTORY_UP = 13
    LIST_DIRECTORY = 21
    DIRECTORY_NAME = 31
    FILE_NAME = 32
    EOF = 99


class Token:
    def __init__(self, tokenText, tokenKind):
        self.tokenText = tokenText
        self.tokenKind = tokenKind

    def __repr__(self):
        return f'{self.tokenText}\t({self.tokenKind})'


class Lexer:
    def __init__(self, src):
        self.source = src
        self.source_generator = (i for line in self.source for i in line.split(' '))

    def get_token(self):
        try:
            nextChar = next(self.source_generator)
            if nextChar == "$":
                nextChar = next(self.source_generator)
                if nextChar == "cd":
                    nextChar = next(self.source_generator)
                    if nextChar == "/":
                        token = Token(nextChar, TokenType.CHANGE_TO_ROOT)
                    elif nextChar == "..":
                        token = Token(nextChar, TokenType.CHANGE_DIRECTORY_UP)
                    else:
                        token = Token(nextChar, TokenType.CHANGE_TO_DIRECTORY)
                elif nextChar == "ls":
                    token = Token(nextChar, TokenType.LIST_DIRECTORY)
            elif nextChar == "dir":
                nextChar = next(self.source_generator)
                token = Token(nextChar, TokenType.DIRECTORY_NAME)
            elif nextChar.isdigit():
                token = Token((nextChar, next(self.source_generator)), TokenType.FILE_NAME)
            return token
        except StopIteration:
            return Token(None, TokenType.EOF)


class Parser:
    def __init__(self, lexer, file_tree):
        self.lexer = lexer
        self.curToken = None
        self.curDirectory = None
        self.FileTree = file_tree

    def nextToken(self):
        self.curToken = self.lexer.get_token()

    def program(self):
        self.nextToken()
        while True:
            if self.curToken.tokenKind == TokenType.CHANGE_TO_ROOT:
                self.curDirectory = self.curToken.tokenText
                self.FileTree.add_root_node(self.curDirectory)
                logging.info(f'changing to root {self.curDirectory}')
                self.nextToken()
            elif self.curToken.tokenKind == TokenType.CHANGE_TO_DIRECTORY:
                self.curDirectory = self.curToken.tokenText
                logging.info(f'changing to directory {self.curDirectory}')
                self.FileTree.descend_to_child_node(self.curDirectory)
                self.nextToken()
            elif self.curToken.tokenKind == TokenType.CHANGE_DIRECTORY_UP:
                self.curDirectory = self.curToken.tokenText
                self.FileTree.go_one_node_up()
                logging.info(f'changing to upper directory {self.FileTree.curNode}')
                self.nextToken()
            elif self.curToken.tokenKind == TokenType.LIST_DIRECTORY:
                logging.info(f'list directory {self.curDirectory}')
                self.nextToken()
                while self.curToken.tokenKind in [TokenType.DIRECTORY_NAME, TokenType.FILE_NAME]:
                    if self.curToken.tokenKind == TokenType.FILE_NAME:
                        size, name = self.curToken.tokenText
                    else:
                        size, name = ('0', self.curToken.tokenText)
                    size = int(size)
                    self.FileTree.add_node(name, size)
                    logging.info(f'appending {name} with size {size} to {self.curDirectory}')
                    self.nextToken()
            elif self.curToken.tokenKind == TokenType.EOF:
                break


def solve_part_i(input):
    myLexer = Lexer(input)
    myFileTree = FileTree()
    myParser = Parser(myLexer, myFileTree)
    myParser.program()
    myParser.FileTree.recursivelySumUpDirSize()
    graph = Graph(myParser.FileTree.createTreeDict(), directed=True)
    print(myParser.FileTree.createTreeDict())
    graph.plot()
    result = sum(i for _, i in myParser.FileTree.traverseTree(100_000).items())
    return result


def solve_part_ii(input):
    myLexer = Lexer(input)
    myFileTree = FileTree()
    myParser = Parser(myLexer, myFileTree)
    myParser.program()
    myParser.FileTree.recursivelySumUpDirSize()
    print(f'Total file system size is {myParser.FileTree.rootNode.size}')
    print(f'Missing file size is {70_000_000 - myParser.FileTree.rootNode.size}')
    result = min([i for _, i in myParser.FileTree.traverseTree().items() if i > (70_000_000 - myParser.FileTree.rootNode.size)])
    return result


if __name__ == "__main__":
    filename = "input_day07.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
#    print(solve_part_ii(read_input(filename)))
    
