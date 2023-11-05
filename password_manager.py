# import libraries
import streamlit as st
import sqlite3
import webbrowser
from user import User

# connection to database via sqlite3
conn = sqlite3.connect("pwd.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists pwd_mngr(app_name varchar(20) not null,
                                                 user_name varchar(50) not null,
                                                 pass_word varchar(50) not null,
                                                 email_address varchar(100) not null,
                                                 url varchar(255) not null,
                                                 primary key(app_name));""")

def insert_data(u):
    with conn:
        c.execute("INSERT INTO pwd_mngr VALUES (:app,:user,:pass,:email,:url)",
                  {'app':u.app,'user':u.username,'pass':u.password,'email':u.email,'url':u.url})
        
def get_cred_by_app(app):
    with conn:
        c.execute("SELECT app_name, user_name, pass_word, email_address, url FROM pwd_mngr WHERE app_name = :name;",{'name':app})
        return c.fetchone()

def remove_app_cred(app):
    with conn:
        c.execute("DELETE FROM pwd_mngr WHERE app_name = :name", {'name': app})

def update_password(app, new_pass_word):
    with conn:
        c.execute("UPDATE pwd_mngr SET pass_word = :pass WHERE app_name = :name",{'name': app,'pass': new_pass_word})

# title of app
st.title("Password Manager 🔐")

c.execute("SELECT COUNT(*) FROM pwd_mngr")
db_size = c.fetchone()[0]

c.execute("SELECT app_name FROM pwd_mngr")
app_names = c.fetchall()
app_names = [i[0] for i in app_names]

# sidebar menu
radio_option = st.sidebar.radio("Menu", options=["Home","Add Account","Update Password","Delete Account"])

# render pages based on the optino selected
if radio_option == "Home":
    st.subheader("Find Credentials")
    # process 1
    if db_size > 0:
        option = st.selectbox('Select Application', app_names) # To be added
        
        #Function to get credentials by taking the application name as an 
        #argument and display the data
        cred = get_cred_by_app(option)

        with st.container():
            st.text(f"Username")
            st.code(f"{cred[1]}",language="python")
            st.text_input('Password', value=cred[2], type="password")
            url = cred[4]
            if st.button('Launch',use_container_width=True):
                webbrowser.open_new_tab(url=url)

        with st.expander("Additional Details:"):
            st.text(f"email")
            st.code(f"{cred[3]}",language="python")
            st.text(f"URL")
            st.code(f"{cred[4]}",language="python")
        
    else:
        st.info('Database is Empty')

if radio_option == "Add Account":
    st.subheader("Add New Credentials")
    # Create a form for taking user inputs
    app_name = st.text_input("Application",'Twitter')
    user_name = st.text_input("User name",'tweety')
    pass_word = st.text_input("Password",'pass123', type='password')
    email = st.text_input("Email", 'tweety@xyz.com')
    url = st.text_input("Website", "twitter.com")

    if st.button("Save", use_container_width=True):
        try:
            data = User(app_name,user_name,pass_word,email,url)
            insert_data(data)
            st.success(f"{app_name}'s credential is added to the Database!")
        except:
            st.warning("Something went wrong! Try Again.")
    st.info(f"Available Credentials in Database: {db_size}")

if radio_option == "Update Password":
    st.subheader("Update Password")
    # Do ---
    if db_size > 0:

        # app_names to be populate from db
        up_app = st.selectbox("Select an Account you want to update", app_names)
        new_pass_1 = st.text_input("New Password", "new123", type="password")
        new_pass_2 = st.text_input("Confirm New Password", "new123", type="password")
        if new_pass_1 == new_pass_2:
            if st.button("Update", use_container_width=True):
                try:
                    update_password(up_app, new_pass_1)
                    st.success(f"{up_app}'s password is updated!")
                except:
                    st.info('Database is Empty. Go to Create to add Data')
        else:
            st.warning("Password don't match! Try Again")
    else:
        st.info("Database is Empty.")

if radio_option == "Delete Account":
    st.subheader("Delete Credentials")
    
    if db_size > 0:

        agree = st.checkbox("View Full Database")
        if agree:
            c.execute("SELECT app_name, email_address, url from pwd_mngr")
            results = c.fetchall()
            st.table(results)
            st.markdown("######")
            delt = st.selectbox("Select an Account you want to delete", app_names)
            st.markdown("######")
            if st.button("Delete", use_container_width=True):
                try:
                    remove_app_cred(delt)
                    st.success(f"{delt}'s Credential is removed from Database!")
                except:
                    st.info("Database is Empty. Go to Cread to add Data")
    else:
        st.info("Database is Empty")
