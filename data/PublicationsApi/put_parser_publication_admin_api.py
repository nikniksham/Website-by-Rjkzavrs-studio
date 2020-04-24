from flask_restful import reqparse

put_parser_admin = reqparse.RequestParser()
put_parser_admin.add_argument('id', type=int)
put_parser_admin.add_argument('header', type=str)
put_parser_admin.add_argument('body', type=str)
put_parser_admin.add_argument('availability_status', type=int)
