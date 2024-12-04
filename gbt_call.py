from openai import OpenAI
import os


def AI_response(dict_):
    client = OpenAI(
        api_key=os.getenv("openai_key") # replace with real one or .env
    )

    try:

        #PICK the best prompt
        query = f"""
        Given the following dictionary of detected skin issues and their occurrences: {dict_}, craft a user-friendly response providing a prioritized list of skincare products.
        The response should:
        Prioritize addressing the most frequent issue (e.g., 50 pimples), followed by less frequent ones (e.g., eczema and scars).
        Recommend specific skincare products for each issue, including multi-purpose options that can address more than one concern.
        For each product, explain why it was chosen, detailing key ingredients and how they address the respective issue.
        Provide tips on how to integrate the products into a skincare routine, including layering and precautions.
        Include a general reminder to consult a dermatologist for personalized advice or if issues persist.
        """
        # Create a streaming chat completion
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="gpt-4o-mini",
            stream=True,
        )

        # Collect and return the streamed response
        response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            response += content
            print(content, end="")  # Print in real-time if needed
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"
