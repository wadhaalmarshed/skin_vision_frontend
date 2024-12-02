import streamlit as st
import requests
import uuid
from io import BytesIO
from PIL import Image
from google.cloud import storage
import base64
from gbt_call import AI_response



# Google Cloud Storage and FastAPI configuration
BUCKET_NAME = "skin-vision-bucket"
FASTAPI_URL = "http://127.0.0.1:8000/predict"  # FastAPI endpoint

def upload_to_gcs(bucket_name, file, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, rewind=True)
    return destination_blob_name

def main():

    st.markdown("""
    <style>
    body {
    background-color: #D6C1B3;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.columns(3)[1]:
        st.image("skinvision-logo.png")

    st.markdown("""
    <h1 style="text-align: center;font-size: 23px;">Skin Vision - Empowering Your Skin Journey with Smart Insights</h1>
    """, unsafe_allow_html=True)

    # Take image through Webcam
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    image=None

    if picture:
        st.image(picture)
        image=picture

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        image=uploaded_file


    if image:
        img = Image.open(image)
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        response = requests.post(FASTAPI_URL, files={"file": ("filename.jpg", img_buffer, "image/jpg")})
        response_dict = response.json()
        base64_img = response_dict["image"]
        image_data = base64.b64decode(base64_img)


        if response.status_code == 200:

                    st.image(Image.open(BytesIO(image_data)))
                    st.success("Inference completed!")
                    if st.button("Click Me"):
                        st.write(response_dict["class"])
                        st.write(AI_response(response_dict["class"]))





if __name__ == "__main__":
    main()
