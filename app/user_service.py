from bson import ObjectId
from pymongo import MongoClient
from .config import Config
from .user import UserSchema

class UserService:
    def __init__(self):
        client = MongoClient(Config.MONGO_URI)
        self.db = client.userdb
        self.users_collection = self.db.users
        self.user_schema = UserSchema()
        self.users_schema = UserSchema(many=True)

    def create_user(self, user_data):
        validated_data = self.user_schema.load(user_data)        
        existing_user = self.users_collection.find_one({'email': validated_data['email']})
        if existing_user:
            raise ValueError('Email already exists')
        result = self.users_collection.insert_one(validated_data)
        validated_data['id'] = str(result.inserted_id)
        
        return {
            'user' : self.user_schema.dump(validated_data),
            'message' : 'User created successfully.'
        }

    def get_all_users(self):
        users = list(self.users_collection.find())
        return self.users_schema.dump([
            {**user, 'id': str(user['_id'])} for user in users
        ])

    def get_user_by_id(self, user_id):
        try:
            user = self.users_collection.find_one({'_id': ObjectId(user_id)})
            if not user:
                return None
            user['id'] = str(user['_id'])
            return self.user_schema.dump(user)
        except Exception:
            return None

    def update_user(self, user_id, user_data):
        try:
            validated_data = self.user_schema.load(user_data, partial=True)            
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)}, 
                {'$set': validated_data}
            )
            
            if result.modified_count == 0:
                return None
            
            return {
                'user' : self.get_user_by_id(user_id),
                'message' : 'User updated successfully.'
            }
            
        except Exception as e:
            raise ValueError(str(e))

    def delete_user(self, user_id):
        try:
            result = self.users_collection.delete_one({'_id': ObjectId(user_id)})
            return {'message':'User deleted successfully.'}
        except Exception:
            return False