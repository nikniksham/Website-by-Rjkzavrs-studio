from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=int)
put_parser.add_argument('header', type=str)
put_parser.add_argument('body', type=str)
