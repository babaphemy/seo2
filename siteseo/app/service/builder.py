from app.db.models import Webbuilder
from app.db.schema import WebbuilderRequest
def builder_builder(db, builder: WebbuilderRequest) -> Webbuilder:
    new_builder = Webbuilder(
        id = builder.id,
        content = builder.content,
        product_id = builder.product_id,
        is_live = True
    )
    db.add(new_builder)
    db.commit()
    db.refresh(new_builder)
    return new_builder