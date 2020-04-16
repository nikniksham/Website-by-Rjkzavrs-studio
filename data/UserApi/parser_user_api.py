from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('age', required=True, type=int)
parser.add_argument('nickname', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('password', required=True, type=str)
