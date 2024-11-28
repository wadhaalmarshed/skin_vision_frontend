import streamlit as st
import requests
import uuid
from io import BytesIO
from PIL import Image
from google.cloud import storage


# Google Cloud Storage and FastAPI configuration
BUCKET_NAME = "skin-vision-bucket"  # Replace with your GCS bucket name
FASTAPI_URL = "http://127.0.0.1:8002/predict"  # FastAPI endpoint

def upload_to_gcs(bucket_name, file, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, rewind=True)
    return destination_blob_name

def main():
    st.title("Skin Vision - Upload and Predict")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Generate a unique filename for the image
        file_id = str(uuid.uuid4())
        destination_blob_name = f"raw-images/{file_id}_{uploaded_file.name}"

        # Upload the image to Google Cloud Storage
        with st.spinner("Uploading to Google Cloud Storage..."):
            uploaded_filename = upload_to_gcs(BUCKET_NAME, uploaded_file, destination_blob_name)
        st.success("Upload successful!")

        # Call FastAPI for model prediction
        #with st.spinner("Running model inference..."):

        response = requests.post(FASTAPI_URL, files={"file": (uploaded_filename, uploaded_file, "image/png")})
        st.write(response)

        if response.status_code == 200:
            st.write(response)
            predictions = response.json()
            st.success("Inference completed!")
            # Display predictions in a readable format
            if predictions.get("predictions"):
                st.write("Predictions:")
                st.json(predictions["predictions"])
            else:
                st.write("No objects detected.")
        else:
            st.error("Failed to get predictions.")
            st.write(response.text)

if __name__ == "__main__":
    main()
