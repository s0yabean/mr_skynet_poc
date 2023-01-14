import streamlit as st
import os
import pandas as pd
import requests
import json
import numpy as np
from io import StringIO
from PIL import Image

def main(): 
    st.title("Skynet")
    st.subheader("Masterfully communicate with anyone.")
    st.markdown("Upload someone's photo/ text and instantly speak their language.")

    with st.form(key='my_form'):
        name = st.text_input(label = "Name:",
                          value = "John")
        text = st.text_area(label = "Text:", height=120, max_chars=200)
        uploaded_file = st.file_uploader(label = "Upload Face Photo:", type=['jpg','png','jpeg'])
        category = st.selectbox(label = "What do you want to say?",
                          options = ["How to sell", "How to date", "How to coach", "How to lead", "(Show All)"])

        if len(text) < 15 and len(text) != 0:
            st.warning("text is too short to make prediction.")

        submitted = st.form_submit_button(label='Submit')
    if submitted:
        if len(text) == 0 and uploaded_file is None:
            st.warning("No text or image uploaded, prediction cannot be made.")
        else: 
            if len(text) > 0:
                text_result = text_api(text)
            else:
                text_result = [0.0, 0.0, 0.0, 0.0]

            if uploaded_file is not None:
                save_uploadedfile(uploaded_file)
                img_result = image_api(uploaded_file)
                os.remove("temp_images" + "/" + uploaded_file.name)
            else:
                img_result = [0.0, 0.0, 0.0, 0.0]

            result = [x + y for x, y in zip(text_result, img_result)]
            insights = ""
            if category == "How to sell":
                st.subheader(category + " " + name + "?")
                insights = insights_sell(np.argmax(result))
                st.markdown(insights)
                st.markdown("More advanced sales advice at www.themindreader.ai")
            elif category == "How to date":
                st.subheader(category + " " + name + "?")
                insights = insights_date(np.argmax(result))
                st.markdown(insights)
                st.markdown("More advanced dating advice at www.readhermind.ai")
            elif category == "How to coach":
                st.subheader(category + " " + name + "?")
                insights = insights_coach(np.argmax(result))
                st.markdown(insights)
                st.markdown("This is a suitable coaching product: https://www.amazon.sg/Wise-Master-Builder-Leadership-Tool/dp/1945102136")
            elif category == "How to lead":
                st.subheader(category + " " + name + "?")
                insights = insights_lead(np.argmax(result))
                st.markdown(insights)
                st.markdown("This is a suitable leadership product: https://www.amazon.sg/Wise-Master-Builder-Leadership-Tool/dp/1945102136")
            else:
                st.subheader("How to sell" + " " + name + "?")
                st.markdown(insights_sell(np.argmax(result)))
                st.markdown("More advanced sales advice at www.themindreader.ai")
                st.subheader("How to date" + " " + name + "?")
                st.markdown(insights_date(np.argmax(result)))
                st.markdown("More advanced dating advice at www.readhermind.ai")
                st.subheader("How to coach" + " " + name + "?")
                st.markdown(insights_coach(np.argmax(result)))
                st.markdown("This is a suitable coaching product: https://www.amazon.sg/Wise-Master-Builder-Leadership-Tool/dp/1945102136")
                st.subheader("How to lead" + " " + name + "?")
                st.markdown(insights_lead(np.argmax(result)))
                st.markdown("This is a suitable leadership product: https://www.amazon.sg/Wise-Master-Builder-Leadership-Tool/dp/1945102136")
                
product_html = """<html>
<head>
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}

.price {
  color: grey;
  font-size: 22px;
}

.card button {
  border: none;
  outline: 0;
  padding: 12px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}

.card button:hover {
  opacity: 0.7;
}
</style>
</head>
<body>

<h2 style="text-align:center">Product Card</h2>

<div class="card">
  <img src="https://unsplash.com/photos/pFPehlRo_yA" alt="Denim Jeans" style="width:100%">
  <h1>Tailored Jeans</h1>
  <p class="price">$19.99</p>
  <p>Some text about the jeans. Super slim and comfy lorem ipsum lorem jeansum. Lorem jeamsun denim lorem jeansum.</p>
  <p><button>Add to Cart</button></p>
</div>

</body>
</html>"""

def insights_coach(index):
    if index == 0:
        return """Coach step by step, fine print and details of any statistics you use from large organizations."""
    if index == 1:
        return """Coach with a light-hearted and fun approach, being open to jump between light and serious topics."""
    if index == 2:
        return "Coach with empathy, holding space and sharing your own story, beliefs and challenges you overcame."
    if index == 3:
        return "Coach with social proof, academic theories, acheivements and prestige and why your recommendations are the most logical choice."

def insights_lead(index):
    if index == 0:
        return """Lead with regulations, safety, conservative-ness."""
    if index == 1:
        return """Lead with fun, happiness and comfort."""
    if index == 2:
        return "Lead with empathy and a personal touch."
    if index == 3:
        return "Lead with knowledge, expertise and connections."

def insights_date(index):
    if index == 0:
        return """Use appropriate language to introduce yourself. It is better for you to err on the side of looking 'boring' than being inappropriate.
Do not use crass jokes or insuinate anything inappropriate in your texts before you get to know your date.
Share facts about yourself and don't come across dodgy or too vague.
When asking the other party out, set definitive dates and times and ensure you book a good location so that your plans are not thwarted."""
    if index == 1:
        return """Come across as fun and flirtraous - they're always up for a good time.
Don't get too serious with them, just joke along and make them feel you're gonna be fun to be with.
Use reverse psychology to get their interest in you after a few exchanges.
Be spontaneous with the setting of a date - it can be a few hour's notice up to a few days. They like feeling kept on their toes with you."""
    if index == 2:
        return "Get to know them personally and ask about what hobbies, organisations and causes they support."
    if index == 3:
        return "Get to the point and share what theories or frameworks you use in relationships and dating."

def insights_sell(index):
    if index == 0:
        return """Social proof is crucial for them – hence things like reviews, recommendations,
endorsements, certifications help them decide. Having a conservative outlook, they make
safer choices and avoid risks, uncertainty and ambiguity. If you are an experienced salesperson, you’re likely to get their respect
and trust with more ease.
If not, you’ll find it harder to convince them, especially if you’re selling big -
ticket items, because your experience is such a significant factor for them."""
    if index == 1:
        return """The environment for them is crucial – they must be brought into the mood to purchase
through great ambiences – like great smelling coffee, comfortable seats, and pleasant sights. In essence, creating
a delightful experience is crucial for the sales process. They are by nature risk -
takers and tend to take more adventurous options rather than
conservative ones. Most importantly, they want to achieve more freedom, more options,
more flexibility in their lives with the purchase they make. If you can position your offering to give them as such, you’ll have
a high chance of sealing the deal."""
    if index == 2:
        return """Be friendly, sincere, and genuinely interested in them.
Appreciate them for taking the time to meet you.
Share about your story and invite them to share about themselves –
take significant time for this, and do not jump to business too quickly.
Show sincerity and interest in them personally."""
    if index == 3:
        return """Prepare yourself mentally. Ensure logical coherency in your proposals.
Think about the counterpoints to your own arguments and prepare your justifications.
Power - dress."""

x_api_key = st.secrets["x-api-key"]
image_api_url = st.secrets["image-api"]
text_api_url = st.secrets["text-api"]

def text_api(text):
    url = text_api_url
    header = {"x-api-key" : x_api_key}
    return requests.post(url, headers=header, json=json.dumps({"text": text})).json()["prediction"]

def image_api(uploaded_file):
    filename = "temp_images" + "/" + uploaded_file.name
    files = {'file': (filename, open(filename, 'rb'), 'application/octet-stream')}
    upload_files_url = image_api_url
    headers = {"x-api-key" : x_api_key}
    return requests.post(upload_files_url, files=files, headers=headers).json()["prediction"]

def save_uploadedfile(uploadedfile):
     with open(os.path.join("temp_images",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())

if __name__ == '__main__':
    main()
