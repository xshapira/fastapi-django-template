from random import randrange

from fastapi import HTTPException, Response, status

from api.main import APIRouter
from posts.schemas import Post

router = APIRouter()

db = []


@router.get("")
def test():
    return {"hello": "world"}


def find_post(id):
    return [p for p in db if p["id"] == id]


def find_index_post(id):
    for i, p in enumerate(db):
        if p["id"] == id:
            return i


@router.get("")
def get_posts():
    return {"data": db}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10001)
    db.append(post_dict)
    return {"data": post_dict}


@router.get("/{id}")
def get_post(id: int):
    if post := find_post(id):
        return {"post_details": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    db[index] = post_dict
    return {"data": post_dict}


# @router.post("/programmers", status_code=status.HTTP_201_CREATED)
# def create_programmer(programmer: ProgrammerSchema):
#     user = Programmer.objects.create(**programmer.dict())
#     return user


# @router.post("/programmers", status_code=status.HTTP_201_CREATED)
# def create_programmer(programmer: ProgrammerSchema):
#     user = Programmer.objects.create(
#         name=programmer.name,
#         password=programmer.password,
#         age=programmer.age,
#         company=Company.objects.get(id=programmer.company),
#     )
#     return user


# @router.get("/programmers/{id}")
# def get_programmer(id: int):
#     return Programmer.objects.get(id=id)
