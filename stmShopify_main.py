import streamlit as st
from stmshopify_security import make_hashes

from stmShopify_functions import create_usertable, add_userdata
from stmShopify_functions import login_user, upload_image
from stmShopify_functions import view_images, save_images

import glob
from PIL import Image

def main():
    st.title('Shopify Inspired Image repository')
    menu = ['Home', 'Login', 'SignUp']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')

    # elif choice == 'Login':
    #     st.subheader('Login Section')

    username = st.sidebar.text_input('User Name', 
                                    max_chars=30)
    password = st.sidebar.text_input('Password', 
                                    type='password')

    if st.sidebar.checkbox('Login'):
        create_usertable()
        hashed_password = make_hashes(password)
        result = login_user(username, password)
        if result:
            st.success(f'Logged In as {username}')
            task = st.selectbox('Task', ['Add Image',
                                         'View Image',
                                        'Analytics', 
                                        'Profile'])
            if task == 'Add Image':
                st.subheader('Add Your Image')
                uploaded_images = upload_image()
                permission = ['private', 'public']
                choice = st.radio('permission', 
                                    permission)
                if st.button('save image'):
                    save_images(uploaded_images, 
                                choice, 
                                username)

            elif task == 'View Image':
                permission = ['private', 'public']
                choice = st.radio('permission', 
                                    permission)

                view_images(username, choice)
                

            elif task == 'Analytics':
                st.subheader('Analytics')
            else:
                st.subheader(f'{username} profile')
        else:
            st.warning('Incorrect Username/password')


    elif choice == 'SignUp':
        st.subheader('Create a New Account')
        new_user = st.text_input('Username', key='1')
        new_password = st.text_input('Password', type='password', key='2')
        
        if st.button('Signup'):
            create_usertable()
            if not add_userdata(new_user, new_password):
                st.success('Your account has been created')
                st.info('Go to login in sidebar > menu')


if __name__ == '__main__':
    main()