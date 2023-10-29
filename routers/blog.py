from pydantic import BaseModel
from fastapi import APIRouter, status, HTTPException, Form
from services.user_service import read_logged_users
from services.blog_service import write_blogs, read_blogs_dict, write_blog_header, read_blogs_by_id, title_edit, content_edit, blog_delete
from typing import Annotated
import time
import csv


class BlogCreate(BaseModel):
    author: str
    title: str
    content: str

class BlogTitle(BaseModel):
    title: str
    
class BlogContent(BaseModel):
    content: str
    
class BlogDelete(BaseModel):
    author: str
    
router = APIRouter()

write_blog_header()

@router.post("/create-blog", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate):
    users = read_logged_users()
    blogs = read_blogs_dict()
    if blog.title in blogs.keys():
        raise HTTPException(status_code=409, detail="Blog already exists")
    if blog.author in users.keys():
       Blog =  write_blogs(blog.author, blog.title, blog.content)
       return {'post': Blog}
    raise HTTPException(status_code=403, detail="Unauthorized")


@router.put("/edit-blog-title/{id}", status_code=status.HTTP_200_OK)
async def edit_title(id: int, post: BlogTitle, username):
    blogs = read_blogs_by_id()
    logged_users = read_logged_users()
    for blog in blogs.values():
        if blog['author'] in logged_users.keys() and blog['author'] == username:
            title_edit(post.title, id)
            blogs_edited = read_blogs_by_id()
            blog_edited = blogs_edited[id]
            last_edited = time.ctime()
            return {'post': blog_edited,  'last-edited': last_edited}
    raise HTTPException(status_code=403, detail="Unauthorized")

@router.put("/edit-blog-content/{id}", status_code=status.HTTP_200_OK)
async def edit_content(id: int, post: BlogContent, username):
    blogs = read_blogs_by_id()
    logged_users = read_logged_users()
    for blog in blogs.values():
        if blog['author'] in logged_users.keys() and blog['author'] == username:
            content_edit(post.content, id)
            blogs_edited = read_blogs_by_id()
            blog_edited = blogs_edited[id]
            last_edited = time.ctime()
            return {'post': blog_edited,  'last-edited': last_edited}
    raise HTTPException(status_code=403, detail="Unauthorized")
            
                       

@router.delete("/delete-blog/{title}", status_code=status.HTTP_200_OK)
async def delete_blog(title: str, blog: BlogDelete, username):
    blogs = read_blogs_by_id()
    if blog.author == username:
        for post in blogs.values():
                if post['title'] == title:
                    blog_delete(title)
                    return {'message': 'Blog deleted'}
        raise HTTPException(status_code=404, detail="Blog not found")
    raise HTTPException(status_code=403, detail="Unauthorized")    
