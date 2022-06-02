from sanic import Sanic
from sanic import response

app = Sanic(__name__)

in_memory_student_db = [
    {
        "name": "Manan Gyanchandani",
        "college": "IIITG",
        "roll": 1,
        "email": "manan.co.in@gmail.com",
        "phone": 9999999999,
        "subjects": ["DBMS", "OS", "OOPS"],
        "friends": ["F1", "F2", "F3"],
    }
]


@app.get("/")
async def get_student(request):
    id_ = request.args.get("id")
    if id_:
        if int(id_) in range(len(in_memory_student_db)):
            return response.json(in_memory_student_db[int(id_)])
        else:
            return response.json(
                {
                    "status": "error",
                    "message": f"data with id {id_} not found. Try with different id!!!",
                }
            )
    return response.json(in_memory_student_db)


@app.post("/")
async def post_student(request):
    student = request.json
    in_memory_student_db.append(student)
    return response.json(student)


@app.put("/<id_:int>")
async def update_student(request, id_):
    student = request.json
    if id_ in range(len(in_memory_student_db)):
        in_memory_student_db[id_] = student
    else:
        return response.json({"error": "No Student with given id"})
    return response.json(student)


@app.delete("/<id_:int>")
async def delete_student(request, id_):
    if id_ in range(len(in_memory_student_db)):
        del in_memory_student_db[id_]
    else:
        return response.json({"error": "No Student with given id"})
    return response.json({"message": "Deleted student successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
