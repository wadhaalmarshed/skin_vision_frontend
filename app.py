import streamlit as st
import requests
import uuid
from io import BytesIO
from PIL import Image
from google.cloud import storage


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
    st.write(response)
    st.write(type(response))
    if response.status_code == 200:
                st.write(response.status_code)
                prediction_img=response.content
                #history=response.content
                #st.write(history)
                # img_buffer=BytesIO()
                # prediction_img=prediction_img.save(img_buffer, format="JPEG")
                # img_buffer.seek(0)
                # prediction_img=img_buffer.read()
                st.image(Image.open(BytesIO(prediction_img)))


                st.success("Inference completed!")
                # Display predictions in a readable format


        # file_id = str(uuid.uuid4())
        # destination_blob_name = f"raw-images/{file_id}_{image.name}"

        # with st.spinner("Uploading to Google Cloud Storage..."):
        #         picture = upload_to_gcs(BUCKET_NAME, prediction_img, destination_blob_name)
        #         st.success("Upload successful!")

    # Upload image through Streamlit


    # if uploaded_file is not None and not enable:
    #     # Display the uploaded image
    #     st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    #     img = Image.open(uploaded_file)
    #     img_buffer = BytesIO()
    #     img.save(img_buffer, format="JPEG")
    #     img_buffer.seek(0)

    #     response = requests.post(FASTAPI_URL, files={"file": ("filename.jpg", img_buffer, "image/jpg")})
    #     st.write(response)

    #     if response.status_code == 200:
    #             st.write(response)
    #             predictions = response.json()
    #             st.success("Inference completed!")
    #             # Display predictions in a readable format
    #             if predictions.get("predictions"):
    #                 st.write("Predictions:")
    #                 st.json(predictions["predictions"])
    #             else:
    #                 st.write("No objects detected.")

        # # Generate a unique filename for the image
        # file_id = str(uuid.uuid4())
        # destination_blob_name = f"raw-images/{file_id}_{uploaded_file.name}"

        # # Upload the image to Google Cloud Storage
        # with st.spinner("Uploading to Google Cloud Storage..."):
        #     uploaded_filename = upload_to_gcs(BUCKET_NAME, uploaded_file, destination_blob_name)
        #     st.success("Upload successful!")



if __name__ == "__main__":
    main()
