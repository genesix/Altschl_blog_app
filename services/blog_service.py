from services.user_service import read_users
import csv
import time


current_time = time.ctime()
fieldnames = ['id', 'author', 'title', 'content', 'time_created']

#reads the blog from csv file - blog.csv into a dictionary in memory - blogs
def read_blogs_dict():
    blogs ={}
    with open("database/blog.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            blogs[row['title']] = row['content']
    return blogs
    
#reads from csv file - blog.csv into a list in memory    
def read_blogs():
    blogs =[]
    with open("database/blog.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            blogs.append(row)
    return blogs


def write_blog_header():
    with open('database/blog.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        

#writes blog from memory into blog.csv file
def write_blogs(author: str, title: str, content: str):
    users = read_users()
    with open('database/blog.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        for user in users:
            if user['username'] == author:   
                writer.writerow({
                    'id': user['id'],
                    'author': author,
                    'title': title,
                    'content': content,
                    'time_created': current_time
        })
    blog = {'id': user['id'], 'author': author, 'title': title, 'content': content, 'time-created': current_time}
    return blog 

def read_blogs_by_id():
    blogs_dict = {}
    with open('database/blog.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            blog_id = int(row['id'])
            del row['id']
            blogs_dict[blog_id] = row
    return blogs_dict

#function that edits blog contents or titles
def title_edit(new_title, id):
    blogs = read_blogs()
    for blog in blogs:
        if blog['id'] == str(id):
            blog['title'] = new_title
    with open('database/blog.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for blog in blogs:
            writer.writerow(blog)
            
        
#function that edits blog contents
def content_edit(new_content, id):
    blogs = read_blogs()
    for blog in blogs:
        if blog['id'] == str(id):
            blog['content'] = new_content
    with open('database/blog.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for blog in blogs:
            writer.writerow(blog)
            
#function that deletes a blog
def blog_delete(title):
    blogs = read_blogs()
    for blog in blogs:
        if blog['title'] == title:
            del[blog]
        with open('database/blog.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            for blog in blogs:
                writer.writerow(blog)
            