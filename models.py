from flask import jsonify, request
import json
class User:
    def __init__(self, card_id, firstname, lastname,username, password):
        self._id = card_id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)