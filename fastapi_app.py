from fastapi import FastAPI, HTTPException, UploadFile
from io import BytesIO
from PIL import Image
from google.cloud import storage
import os
import uuid
import torch  # Use YOLOv8 from ultralytics

# Initialize FastAPI app
app = FastAPI()

# Google Cloud Storage bucket and model configuration
BUCKET_NAME = "skin-vision-bucket"  # Replace with your GCS bucket name
MODEL_BLOB_NAME = "models/best.pt"  # Path to your model in GCS
LOCAL_MODEL_PATH = "/tmp/best.pt"  # Temporary path for the model

# Initialize the model variable
model = None

def get_gcs_client():
    """Initialize Google Cloud Storage client."""
    return storage.Client()

def download_model_from_gcs():
    """
    Download the model from Google Cloud Storage if not already available locally.
    """
    if not os.path.exists(LOCAL_MODEL_PATH):
        client = get_gcs_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_BLOB_NAME)
        blob.download_to_filename(LOCAL_MODEL_PATH)
        print(f"Model downloaded from GCS to {LOCAL_MODEL_PATH}")

@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event to download the model and load it.
    """
    global model
    print("Starting up...")
    download_model_from_gcs()  # Download model from GCS
    model = torch.hub.load('ultralytics/yolov8', 'custom', path=LOCAL_MODEL_PATH)
    print("Model loaded successfully!")

@app.get("/")
def root():
    return {"ok":True}


@app.post("/predict/")
async def predict(file: UploadFile):

    image_bytes = file.file.read()
    image = Image.open(BytesIO(image_bytes))

    predict = model.predict(image)

    # img_buffer = BytesIO()
    # uploaded_file.save(img_buffer, format="PNG")
    # img_buffer.seek(0)


    return {"ok":predict}

    """
    Predict endpoint: Processes an image from GCS and returns model predictions.
    Args:
        filename (str): Name of the image file in GCS.
    Returns:
        dict: Model predictions.
    """
    # try:
    #     # Generate a temporary local path for the image
    #     local_image_path = f"/tmp/{uuid.uuid4()}.jpg"

    #     # Download the image from GCS to a temporary local path
    #     client = get_gcs_client()
    #     bucket = client.bucket(BUCKET_NAME)
    #     blob = bucket.blob(filename)
    #     blob.download_to_filename(local_image_path)
    #     print(f"Downloaded image {filename} from GCS to {local_image_path}")

    #     # Run inference using YOLOv8 (no need for preprocessing)
    #     results = model(local_image_path)  # Inference directly from image file path

    #     # Format the results as a list of dictionaries
    #     predictions = results.pandas().xyxy[0].to_dict(orient="records")

    #     # Cleanup: delete the temporary image file
    #     os.remove(local_image_path)

    #     return {"predictions": predictions}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
