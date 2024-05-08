import streamlit as st
import hashlib
import io

def hash_text(text, hash_type):
    # Hash the input text using the specified hash function
    if hash_type == "MD5":
        return hashlib.md5(text.encode()).hexdigest()
    elif hash_type == "SHA-1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif hash_type == "SHA-256":
        return hashlib.sha256(text.encode()).hexdigest()
    elif hash_type == "SHA-512":
        return hashlib.sha512(text.encode()).hexdigest()

def hash_file(file, hash_type):
    # Hash the contents of the input file using the specified hash function
    if hash_type == "MD5":
        hasher = hashlib.md5()
    elif hash_type == "SHA-1":
        hasher = hashlib.sha1()
    elif hash_type == "SHA-256":
        hasher = hashlib.sha256()
    elif hash_type == "SHA-512":
        hasher = hashlib.sha512()

    # Read the file contents
    file_contents = file.read()

    # Calculate the hash
    hasher.update(file_contents)

    return hasher.hexdigest()

# Streamlit app
st.title("Hashing Functions")

# Ask the user to input text or upload a file
option = st.radio("Choose input method:", ("Text", "File"))

if option == "Text":
    # Ask the user to input text
    text = st.text_input("Enter text to hash:")
    if text:
        # Ask the user to select the hash function
        hash_type = st.selectbox("Choose a hash function:", ("MD5", "SHA-1", "SHA-256", "SHA-512"))

        # Hash the text using the selected hash function
        hashed_text = hash_text(text, hash_type)

        # Display the hash value
        st.write("Hash value:", hashed_text)
elif option == "File":
    # Ask the user to upload a file
    file = st.file_uploader("Upload a file to hash:", type=["txt", "pdf", "docx", "csv", "xlsx"])
    if file:
        # Ask the user to select the hash function
        hash_type = st.selectbox("Choose a hash function:", ("MD5", "SHA-1", "SHA-256", "SHA-512"))

        # Hash the file contents using the selected hash function
        hashed_file = hash_file(io.BytesIO(file.read()), hash_type)

        # Display the hash value
        st.write("Hash value:", hashed_file)