from fastapi import APIRouter


router = APIRouter()

@router.get("/about")
def about():
    return{
    "name": "Your Name",
    "email":"Your@gmail.com",
    "my_features": {
        "Version History": "Tracks previous note versions and allows restoration."
    }


    }



