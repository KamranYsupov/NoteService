from .mixins import TagSchemaMixin


class TagSchema(TagSchemaMixin):
    id: id: uuid.UUID
    

class CreateTagSchema(TagSchemaMixin):
    pass