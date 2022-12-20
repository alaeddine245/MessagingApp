from flask import jsonify, request
import json
class User:
    def __init__(self, card_id, firstname, lastname,email, password):
        self.card_id = card_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)