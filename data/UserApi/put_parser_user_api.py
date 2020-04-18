from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=int)
put_parser.add_argument('surname', type=str)
put_parser.add_argument('name', type=str)
put_parser.add_argument('age', type=int)
put_parser.add_argument('nickname', type=str)
put_parser.add_argument('email', type=str)
put_parser.add_argument('background_image_id', type=str)
