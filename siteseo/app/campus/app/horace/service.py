from motor.motor_asyncio import AsyncIOMotorClient
from siteseo.app.campus.app.util.converter import read_json
from .model import CourseItem
from bson import ObjectId
from fastapi import HTTPException
from siteseo.app.campus.app.info.schema import UserResponse as Appuser
import datetime

async def horace_users(db: AsyncIOMotorClient):
    """
    Retrieve a list of all users from the MongoDB collection, limited to 1000 entries.

    Args:
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary containing a list of users.
    """
    user_collection = db.get_collection("user")
    return {'users': await user_collection.find({}).to_list(1000)}



async def a_user(id: str, db: AsyncIOMotorClient):
    """
    Retrieve a single user by their MongoDB ObjectId.

    Args:
    id (str): The ObjectId of the user as a string.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary representing the user document from MongoDB.

    Raises:
    HTTPException: An exception is raised if no user is found with the provided ID.
    """
    user_collection = db.get_collection("user")
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


# async def a_user(id: str, db: AsyncIOMotorClient):
#     user_collection = db.get_collection("user")
#     if (
#         user := await user_collection.find_one({"_id": ObjectId(id)})
#     ) is not None:
#         return user

#     raise HTTPException(status_code=404, detail=f"User {id} not found")


async def getby_username(email: str, db: AsyncIOMotorClient) -> dict:
    """
    Retrieve a user by their email address.

    Args:
    email (str): The email address of the user.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary representing the user document from MongoDB.

    Raises:
    HTTPException: An exception is raised if no user is found with the provided email.
    """
    user_collection = db.get_collection("user")
    user = await user_collection.find_one({"email": email})
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User with email {email} not found")


# async def getby_username(email: str, db: AsyncIOMotorClient ) -> Appuser:
#     user_collection = db.get_collection("user")
#     if(
#         user := await user_collection.find_one({"email": email})
#     ) is not None:
#         return user
#     raise HTTPException(status_code=404, detail=f"User {id} not found")

async def all_courses(db: AsyncIOMotorClient) -> list:
    """
    Retrieve all courses from the database.

    Args:
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    list: A list of dictionaries, each representing a course document from MongoDB.
    """
    course_collection = db.get_collection("course")
    courses = await course_collection.find().to_list(length=1000) 
    return courses

async def lte_courses(db: AsyncIOMotorClient) -> list:

    registration_collection = db.get_collection('registrations')
    post_collection = db.get_collection('posts')
    user_collection = db.get_collection('user')
    course_collection = db.get_collection('course')
    # Fetch all active courses that are not drafts
    cursor = course_collection.find({"draft": False})
    courses = await cursor.to_list(length=None)

    result = []
    for course in courses:
        # Count students registered in this course
        registrations = await registration_collection.count_documents({"courses": course["_id"]})
        
        # Get posts related to the course
        posts_cursor = post_collection.find({"course_id": course["_id"]})
        posts = await posts_cursor.to_list(length=None)  # You would map these to DTOs

        author_id = course.get("author", {}).id
        if author_id:
            author = await user_collection.find_one({"_id": ObjectId(author_id)})
            course_author = Appuser(id=(author["_id"]), email=author.get("email"), roles=author.get("roles"), first_name=author.get("firstname"), last_name=author.get("lastname"), status=(author.get("active"))) if author else None
            
        else:
            course_author = None
        print(author)

        course_item = CourseItem(
            id=course.get("_id"),
            course_name=course.get("courseName"),
            brief=course.get("brief"),
            updated_on=course.get("updatedOn"),
            thumbnail=course.get("thumbnail"),
            category=course.get("category"),
            total_steps=course.get("total_steps"),
            draft=course.get("draft"),
            students=registrations,
            author=course_author,
            posts=posts,  # Assuming direct mapping, otherwise you need transformation
            cost=course.get("price") - course.get("tax") if course.get("price") else None
        )
        # if au:
        #     author = au.get("id")
        #     course_item["author"] = author
        # else:
        #     None
        
        result.append(course_item)

    return result


async def free_courses(db: AsyncIOMotorClient) -> list:
    """
    Retrieve all courses that are free (price == 0).

    Args:
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    list: A list of dictionaries representing free course documents.
    """
    course_collection = db.get_collection("course")
    courses = await course_collection.find({"price": 0}).to_list(length=1000)
    return courses


async def courses_by_range(min_price: float, max_price: float, db: AsyncIOMotorClient) -> list:
    """
    Retrieve courses within a specified price range.

    Args:
    min_price (float): Minimum price of the course.
    max_price (float): Maximum price of the course.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    list: A list of dictionaries representing course documents within the price range.
    """
    course_collection = db.get_collection("course")
    courses = await course_collection.find({"price": {"$gte": min_price, "$lte": max_price}}).to_list(length=1000)
    return courses


async def next_lecture(course_id: str, db: AsyncIOMotorClient) -> dict:
    """
    Retrieve the next lecture of a specific course.

    Args:
    course_id (str): The unique identifier of the course.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary representing the next lecture document.
    """
    lecture_collection = db.get_collection("lectures")
    lecture = await lecture_collection.find_one({"course_id": course_id, "date": {"$gt": datetime.now()}})
    if lecture:
        return lecture
    raise HTTPException(status_code=404, detail=f"No upcoming lecture found for course {course_id}")

async def find_course_detail(course_id: str, db: AsyncIOMotorClient) -> dict:
    """
    Retrieve detailed information of a specific course by its ID.

    Args:
    course_id (str): The unique identifier of the course.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary representing the course document.

    Raises:
    HTTPException: An exception is raised if no course is found with the provided ID.
    """
    course_collection = db.get_collection("course")
    course = await course_collection.find_one({"_id": ObjectId(course_id)})
    if course:
        return course
    raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")



async def course_ids(db: AsyncIOMotorClient) -> list:
    """
    Retrieve all course IDs from the MongoDB collection.

    Args:
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    list: A list of course IDs.
    """
    try:
        course_collection = db.get_collection("course")
        cursor = course_collection.find({}, {'_id': 1})  # Only retrieve the _id field
        course_ids = [str(course['_id']) for course in await cursor.to_list(length=None)]
        return course_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def user_progress():
    pass

async def a_course(id: str, db: AsyncIOMotorClient):
    """
    Retrieve a specific course by its MongoDB ObjectId.

    Args:
    id (str): The ObjectId of the course as a string.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    dict: A dictionary representing the course document from MongoDB.

    Raises:
    HTTPException: An exception is raised if no course is found with the provided ID.
    """
    try:
        course_collection = db.get_collection("course")
        course = await course_collection.find_one({"_id": ObjectId(id)})
        if course:
            return course
        else:
            raise HTTPException(status_code=404, detail=f"Course with ID {id} not found")
    except Exception as e:
        # Catching a broader exception might be useful to handle unexpected errors,
        # such as connection issues or bad ID formats.
        raise HTTPException(status_code=500, detail=str(e))


async def by_author(user_id: str, db: AsyncIOMotorClient) -> list:
    """
    Retrieve all courses created by a specific author.

    Args:
    user_id (str): The unique identifier of the author.
    db (AsyncIOMotorClient): The database client used to interact with MongoDB.

    Returns:
    list: A list of dictionaries, each representing a course document.

    Raises:
    HTTPException: An exception is raised if there is an error in fetching data from the database.
    """
    try:
        course_collection = db.get_collection("course")
        # Assuming the courses collection has an 'author_id' field that is an ObjectId
        courses = await course_collection.find({"author_id": ObjectId(user_id)}).to_list(length=None)
        if not courses:
            # Optionally, you might want to handle the case where no courses are found
            # by either returning an empty list or raising an HTTPException.
            raise HTTPException(status_code=404, detail="No courses found for the given author")
        return courses
    except Exception as e:
        # This captures errors like incorrect ObjectId formatting and connection issues.
        raise HTTPException(status_code=500, detail=str(e))

async def all_for_edit():
    pass
async def find_course_detail_map(cid: str, db: AsyncIOMotorClient):
    course_collection = db.get_collection("course")
    course_document = await course_collection.find_one({"_id": ObjectId(cid)})
    if not course_document:
        raise HTTPException(status_code=404, detail="Course not found")
    
    curriculum_map = read_json(course_document['curriculum'])
    return {
        "course_name": course_document["course_name"],
        "curriculum": curriculum_map.dict()  # Serialize Pydantic model to dict
    }
