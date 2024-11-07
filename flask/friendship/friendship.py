from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from models import FriendshipModel  # Alterei para usar a importação do modelo correto

class FriendshipRequest(BaseModel):
    user_id: int
    friend_id: int


Friendship_Pydantic = pydantic_model_creator(FriendshipModel, name="Friendship")
FriendshipIn_Pydantic = pydantic_model_creator(FriendshipModel, name="FriendshipIn", exclude_readonly=True)
