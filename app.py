import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from google.cloud import storage
import base64
from gbt_call import AI_response


FASTAPI_URL = "http://127.0.0.1:8000/predict"  # FastAPI endpoint


#CSS & HTML
st.write("""
    <style>
    .stApp {
    background-color: #D6C1B3;
        }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header(("About Us"))
st.sidebar.markdown((
    "Welcome to SkinVision  –  your personal skin care assistant that’s here to help you achieve your healthiest, happiest skin. We believe that skincare should be simple, accessible, and tailored just for you. That’s why we’ve created an intelligent platform that helps you understand your skin’s unique needs, and offers personalized recommendations."
))

st.sidebar.header(("Privacy Policy & Terms of Use for Uploaded Pictures"))

def show_privacy_popup():
    if "agreed_to_terms" not in st.session_state or not st.session_state.agreed_to_terms:
        with st.expander("Privacy Policy (Click to read)", expanded=True):
            st.write("""
                ### Privacy Policy

                By using this application, you agree to our Terms and Conditions and Privacy Policy.

                - We collect and process your data to provide better service.
                - Your data is used exclusively for this application.

                Please read the full Privacy Policy for more details.

                **Terms and Conditions:**
                By agreeing, you accept all terms listed.
            """)

def main():

    with st.columns(3)[1]:
        st.image("skinvision-logo.png")

    st.markdown("""
    <h1 style="text-align: center;font-size: 23px;">Skin Vision - AI-powered insights for flawless skin</h1>
    """, unsafe_allow_html=True)

    # Space at the top for better visual separation
    st.markdown("<br>", unsafe_allow_html=True)

    # Display Privacy Policy and Terms of Use
    st.write("#### Privacy Policy & Terms of Use for Uploaded Pictures")

    if "agreed_to_terms" not in st.session_state or not st.session_state.agreed_to_terms:
        st.write("Please review and agree to the Privacy Policy & Terms of Use to proceed.")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Read Privacy Policy"):
            show_privacy_popup()

        st.markdown("<br>", unsafe_allow_html=True)

        agreement = st.checkbox("I agree to the Privacy Policy")

        if agreement:
            st.session_state.agreed_to_terms = True
            st.sidebar.success("You have agreed to the Privacy Policy.")
        else:
            if "agreed_to_terms" in st.session_state and st.session_state.agreed_to_terms:
                st.sidebar.warning("You have already agreed to the Privacy Policy.")

        if "agreed_to_terms" in st.session_state and st.session_state.agreed_to_terms:
            st.write("Thank you for agreeing to the terms! You can now proceed with the app.")
            st.write("You can now use the features of the Skin Vision app.")
        else:
            st.stop()

    else:
        st.write("You have already agreed to the terms! You can now proceed with the app.")
        st.write("You can now use the features of the Skin Vision app.")

        option = st.radio("Select an option", ("Use Webcam", "Upload Picture"))

        if option == "Use Webcam":
            enable = st.checkbox("Enable camera")
            picture = st.camera_input("Take a picture", disabled=not enable)

            if picture:
                image = picture

        elif option == "Upload Picture":
            uploaded_file = st.file_uploader("Upload an image", type=["jpg"])

            if uploaded_file:
                image = uploaded_file

        if 'image' in locals():
            img = Image.open(image)
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG")
            img_buffer.seek(0)

            response = requests.post(FASTAPI_URL, files={"file": ("filename.jpg", img_buffer, "image/jpg")})
            response_dict = response.json()
            base64_img = response_dict["image"]
            image_data = base64.b64decode(base64_img)

            if response.status_code == 200:

                # If you want to show two images side by side (example with "Captured Image" and "Uploaded Image")
                if 'image' in locals():
                # Create two columns for side-by-side display
                    col1, col2 = st.columns(2)

                    # Image 1 in the first column
                    with col1:

                        if 'uploaded_file' in locals() and uploaded_file:
                         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                        elif 'picture' in locals() and picture:
                         st.image(picture, caption="Captured Image", use_container_width=True)

                    # Image 2 in the second column (just an example - you can put another image or similar)
                    with col2:
                        st.image(Image.open(BytesIO(image_data)), caption="Processed Image", use_container_width=True)

                st.success("First Stage Completed!")
                if st.button("Get More Insight !"):
                    html_content = ""
                    for key, value in response_dict["class"].items():
                        html_content += f"""
                        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 5px;">
                            <strong>{key}:</strong> {value}
                        </div>
                        """
                    st.markdown(html_content, unsafe_allow_html=True)

                    st.write(AI_response(response_dict["class"]))  # Assuming AI_response is your function to handle inference output


if __name__ == "__main__":
    main()
