from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('header', required=True, type=str)
parser.add_argument('body', required=True, type=str)
