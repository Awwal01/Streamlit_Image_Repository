import streamlit as st

from stmshopify_security import make_hashes, check_hashes

import sqlite3
from pathlib import Path
from PIL import Image
import glob
import os

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

def create_usertable():
    c.execute('''CREATE TABLE IF NOT EXISTS
                userstable(username TEXT PRIMARY KEY,
                password TEXT NOT NULL)''')

def add_userdata(username, password:str):
    if (password == '') or (username == ''):
        return st.error('please add a valid password and username')
    password = make_hashes(password)
    c.execute('''INSERT INTO userstable(username, 
                        password)
                        VALUES(?,?)''', 
                        (username, password))
                    
    conn.commit()

def login_user(username, password):
    hashed_password = make_hashes(password)
    password = check_hashes(password, hashed_password)
    c.execute('''SELECT * FROM userstable
                 WHERE username=? AND password=?''',
             (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def upload_image():
    types = ['jpeg', 'jpg', 'png']
    uploaded_images = st.file_uploader('upload private image', 
                                    type=types,
                                    accept_multiple_files=True)
    return uploaded_images
        
def save_images(uploaded_images, choice, username):
    current_folder = os.path.dirname(__file__)
    if choice == 'private':
        save_path = Path(current_folder, f'private/{username}')
    else:
        save_path = Path(current_folder, 'public')

    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    for image in uploaded_images:
        if image is not None:
            data = image.read()
        st.info('Ensure the file name is unique')
        with open(os.path.join(save_path, image.name), 'wb') as f:
            f.write(image.getbuffer())
            st.success(f'saved {image.name}')
    st.success('done')

def view_images(username, choice):
    view_type = ['view private images', 'view public image']
    view = st.selectbox('view images', view_type)
    
    current_folder = os.path.dirname(__file__)
    if choice == 'private':
        image_folder = current_folder + f'/private/{username}/*'
        images = glob.glob(image_folder)
        image = st.selectbox('select image to view', images)
    else:
        image_dir = current_folder + '/public/*'
        images = glob.glob(image_dir)
        image = st.selectbox('select image to view', images)
    st.info(str(len(images))+f' images in this {choice} repository')

    if len(images) > 0:
        image = Image.open(image)
        st.image(image, use_column_width=True)
        
