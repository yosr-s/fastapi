from tortoise import fields , models
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(models.Model):
    id = fields.IntField(pk=True)
    todo = fields.CharField(max_length=250)
    due_date = fields.CharField(max_length=250)
    description = fields.TextField()

    class PydanticMeta:
        pass

    def __str__(self):
        return self.todo


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)