import streamlit as st
from io import BytesIO
from PIL import Image
from rembg import remove

MAX_FILE_SIZE = 5 * 1024 * 1024


st.markdown("### Build an image background remover in Streamlit")
img_upload = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


def convert_img(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    byte_img = buffer.getvalue()
    return byte_img


def fixed_img(img):
    col1.write("original img :camera:")
    col1.image(img)
    read_img = Image.open(img)
    fixed_img = remove(read_img)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed_img)
    st.download_button("Download image", convert_img(fixed_img), "download_img.png")


col1, col2 = st.columns(2)

if img_upload:
    if img_upload.size > MAX_FILE_SIZE:
        st.error("Too large to upload")
    fixed_img(img_upload)
