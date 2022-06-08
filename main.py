import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.bell import api as bell
from backend.classroom import api as classroom
from backend.core.settings import settings
from backend.course import api as course
from backend.group import api as group
from backend.schedule_item import api as schedule_item
from backend.teacher import api as teacher
from backend.type_schedule_item import api as type_schedule_item

settings.configure_logging()

app = FastAPI(**settings.fastapi_kwargs)

if settings.allowed_hosts:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.on_event("startup")
async def startup_event():
    print("Starting up...")


app.include_router(bell.router)
app.include_router(classroom.router)
app.include_router(course.router)
app.include_router(group.router)
app.include_router(teacher.router)
app.include_router(schedule_item.router)
app.include_router(type_schedule_item.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # noqa
