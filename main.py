from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------

app = FastAPI(title="Student Management API")

# ----------------------------------------------------
# Enable CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mahesh",
    port="5432"
)

# ----------------------------------------------------
# Pydantic Model
# ----------------------------------------------------

class Student(BaseModel):
    id: int
    name: str
    course: str

# ----------------------------------------------------
# GET All Students
# ----------------------------------------------------

@app.get("/students")
def get_students():

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, course
        FROM students
        ORDER BY id
    """)

    rows = cursor.fetchall()

    cursor.close()

    students = []

    for row in rows:
        students.append(
            {
                "id": row[0],
                "name": row[1],
                "course": row[2]
            }
        )

    return students

# ----------------------------------------------------
# POST Student
# ----------------------------------------------------

@app.post("/students")
def add_student(student: Student):

    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            VALUES (%s,%s,%s)
        """, (
            student.id,
            student.name,
            student.course
        ))

        conn.commit()

    except Exception as e:

        conn.rollback()
        cursor.close()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    cursor.close()

    return {
        "message": "Student Added Successfully"
    }

# ----------------------------------------------------
# PUT Student
# ----------------------------------------------------

@app.put("/students")
def update_student(student: Student):

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET
            name=%s,
            course=%s
        WHERE id=%s
    """, (
        student.name,
        student.course,
        student.id
    ))

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    cursor.close()

    return {
        "message": "Student Updated Successfully"
    }

# ----------------------------------------------------
# PATCH Student
# ----------------------------------------------------

@app.patch("/students")
def patch_student(student: Student):

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET
            name=%s,
            course=%s
        WHERE id=%s
    """, (
        student.name,
        student.course,
        student.id
    ))

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    cursor.close()

    return {
        "message": "Student Updated Successfully"
    }

# ----------------------------------------------------
# DELETE Student
# ----------------------------------------------------

@app.delete("/students/{id}")
def delete_student(id: int):

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM students
        WHERE id=%s
    """, (id,))

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    cursor.close()

    return {
        "message": "Student Deleted Successfully"
    }

# ----------------------------------------------------
# Root
# ----------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Student Management API Running..."
    }