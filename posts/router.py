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
