from google.cloud import storage
from fastapi import FastAPI, File, UploadFile
import streamlit as st
import uuid

BUCKET_NAME = "skin-vision-bucket"

# Initialize Google Cloud Storage client
def upload_to_gcs(bucket_name, file, destination_blob_name):
   """Uploads a file to Google Cloud Storage."""
   client = storage.Client()
   bucket = client.bucket(bucket_name)

#    print(bucket_name)

   blob = bucket.blob(destination_blob_name)
   blob.upload_from_file(file, rewind=True)
   return f"File uploaded to GCS: {destination_blob_name}"

# Streamlit App
def main():
   st.title("Skin Vision - File Upload Test")

   # File uploader
   uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

   if uploaded_file is not None:
       # Generate a unique filename using UUID
       file_id = str(uuid.uuid4())
       destination_blob_name = f"raw-images/{file_id}_{uploaded_file.name}"

       # Upload to GCS
       with st.spinner("Uploading to Google Cloud Storage..."):
           gcs_url = upload_to_gcs(BUCKET_NAME, uploaded_file, destination_blob_name)

       # Display success message
       st.success("Upload successful!")
       st.write(gcs_url)

if __name__ == "__main__":
   main()
