from fastapi import FastAPI, HTTPException, status, Form
from typing import Annotated
from routers.users import router as user_router, UserCreate
from routers.blog import router as blog_router
from services.user_service import write_user, write_header, read_users, logged_in, read_logged_users, write_logged_in_header
from services.blog_service import read_blogs, write_blog_header



app = FastAPI()

app.include_router(user_router, tags=['User'])
app.include_router(blog_router,  tags=['Blog'])


@app.get('/', status_code=status.HTTP_200_OK)
async def get_blogs():
    return read_blogs()

@app.get('/About', status_code=status.HTTP_200_OK)
async def about():
    return {
        'About': """Welcome to Collins' blog. Enjoy our wealth of information on different topics, ranging from tech to socials.Create an account to share your experiences with our millions of readers and users. """
        }
    
@app.get('/Contact', status_code=status.HTTP_200_OK)
async def contact():
    return {
        'Contact Us': 
            {
                'twitter': "@Genelinx",
            }
    }

write_header()
write_logged_in_header()
write_blog_header()


@app.post('/create-account',  status_code=status.HTTP_201_CREATED)
async def create_account(user: UserCreate):
    users_list = read_users()
    for data in users_list:
        if data['username'] == user.username:
            return {f'message: account already exists'}
    write_user(user.firstname, user.lastname, user.username, user.email, user.password)
    return{f'message: user account created!'}
    

#login
@app.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    users_list = read_users()
    logged_in_users = read_logged_users()
    for users in users_list:
        if username in  logged_in_users.keys():
            return{f'message: user already logged in'}
        elif users['username'] == username:
            logged_in(username, password)
            return {f'message: Logged in successfully'}
    raise HTTPException(status_code=400, detail="Invalid credentials")
    
