import streamlit as st

# # Function to display the Privacy Policy
# def show_privacy_policy():
#     privacy_policy = """
#     # SkinVision Privacy Policy

#     At **SkinVision**, we take your privacy and the security of your personal information seriously. This Privacy Policy explains how we handle and protect the pictures you upload while using our services, as well as how we use the data generated through our app.

#     ## 1. What We Collect
#     When you upload a photo to SkinVision, we collect the image file for the purpose of analyzing your skin's features, such as pores, acne, dark circles, and other skin conditions. We may also collect other data related to your skin analysis and the recommendations provided (e.g., skin type, routine preferences).

#     ## 2. How We Use Your Photos
#     - **Analysis:** The uploaded pictures are processed by our machine learning model to generate insights about your skin. These insights are used to provide you with personalized skincare recommendations.
#     - **Temporary Use:** Your photo will only be used for analysis during the session and will not be stored permanently on our servers unless explicitly stated.
#     - **Improvement of Service:** To improve our algorithms and provide more accurate results, we may use a limited set of anonymized images for training purposes. In this case, the images will be fully anonymized, meaning they will not be tied to any personal information or identifiable characteristics.
#     - **No Third-Party Sharing:** We do not share your uploaded photos or any other personal data with third-party companies for marketing or any other purposes unless required by law.

#     ## 3. Data Retention
#     - **Temporary Data Storage:** Photos are temporarily stored for the duration of your session and automatically deleted once the analysis is complete and the results are generated.
#     - **User-Controlled Deletion:** You have the ability to delete your uploaded photos from our system at any time by following the instructions in the app or contacting our support team.

#     ## 4. Data Security
#     We take the security of your data very seriously and use industry-standard encryption protocols to protect your uploaded photos and other personal information. While we strive to ensure the safety of your data, please be aware that no system is 100% secure, and we cannot guarantee the complete protection of your data from unauthorized access.

#     ## 5. User Rights and Control
#     As a user, you have the following rights concerning your personal data:
#     - **Access:** You can request access to any data we have collected about you, including uploaded photos and generated insights.
#     - **Correction:** If any information is incorrect or needs updating, you can contact us to correct it.
#     - **Deletion:** You can request that your photos and data be deleted from our system at any time.
#     - **Withdrawal of Consent:** You have the right to withdraw your consent for us to use your uploaded photos and personal data, though doing so may limit some features of the app (such as receiving personalized recommendations).

#     ## 6. Children’s Privacy
#     SkinVision is not intended for use by individuals under the age of 16. If we become aware that a child under 16 has uploaded a photo or shared personal data, we will take steps to delete the information as soon as possible.

#     ## 7. Changes to This Policy
#     We may update this Privacy Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. We will notify you of significant changes by updating the date at the top of this page or through other communication channels, where applicable.

#     ## 8. Contact Us
#     If you have any questions about how we handle your uploaded photos or if you wish to exercise your rights as described in this Privacy Policy, please contact us at:

#     **SkinVision Team**
#     Email: [support@skinvision.com]
#     Address: [Insert physical address, if applicable]
#     Phone: [Insert phone number, if applicable]
#     """

#     st.markdown(privacy_policy)

# # Home page of the app
# def home_page():
#     st.title("Welcome to SkinVision")

#     st.write(
#         "SkinVision is an intelligent app that analyzes your skin and provides personalized skincare routines."
#     )

#     # Button to navigate to Privacy Policy page
#     if st.button("Read Privacy Policy"):
#         st.session_state.page = "Privacy Policy"  # Change to Privacy Policy page
#         st.experimental_rerun()

# # Page after the user agrees to the Privacy Policy
# def privacy_policy_page():
#     st.title("Privacy Policy")

#     show_privacy_policy()

#     # Add checkbox for agreement
#     agreement = st.checkbox("I agree to the Privacy Policy")

#     # Session state to track whether user has agreed
#     if agreement:
#         st.session_state.agreed_to_terms = True
#         st.success("Thank you for agreeing to the Privacy Policy! You may now proceed.")
#         st.session_state.page = "Home"  # Go back to the home page after agreeing
#         st.experimental_rerun()
#     else:
#         st.session_state.agreed_to_terms = False

# # Main app logic
# def main():
#     # Initialize session state if not set
#     if 'agreed_to_terms' not in st.session_state:
#         st.session_state.agreed_to_terms = False

#     if 'page' not in st.session_state:
#         st.session_state.page = "Home"  # Default page

#     # Page navigation logic based on session state
#     if st.session_state.page == "Home":
#         home_page()
#     elif st.session_state.page == "Privacy Policy":
#         privacy_policy_page()
#     else:
#         home_page()

# if __name__ == "__main__":
#     main()

import streamlit as st

# Function to display the privacy policy and handle agreement
def show_privacy_popup():
    # Check if the user has agreed to the terms before
    if "agreed_to_terms" not in st.session_state or not st.session_state.agreed_to_terms:
        # Show the privacy policy pop-up (using an expander for simplicity)
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

            # Agree button
            agree_button = st.button("I Agree")
            if agree_button:
                # Store that the user has agreed to the terms
                st.session_state.agreed_to_terms = True
                st.success("You have successfully agreed to the terms and conditions.")
            else:
                st.warning("Please agree to the terms to continue.")

    else:
        # User has already agreed, proceed with the app
        st.write("Thank you for agreeing to the terms and conditions! You may now proceed with the app.")

# Main logic
def main():
    st.title("Skin Vision App")
    show_privacy_popup()

if __name__ == "__main__":
    main()
