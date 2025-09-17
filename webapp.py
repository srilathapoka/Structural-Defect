import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt


#lets configure the model
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')



st.sidebar.title('UPLOAD YOUR IMAGE HERE')

uploaded_image=st.sidebar.file_uploader('Here',type=['jpeg','jpg','png'])
if uploaded_image:
    image=Image.open(uploaded_image)
    st.sidebar.subheader(':blue[UPLOADED IMAGE]')
    st.sidebar.image(image)



#create main page
st.title(':red[STRUCTURAL DEFECTS] :green[AI assited structure defect identifier in construction business]')  
tips='''To use the application folow the steps below
* upload the image
* Click on the button to generate summary
* Click download to save the report generated'''
st.write(tips)
pre_title=st.text_input('Report Title:',None)
prep_by=st.text_input('Report Prepared by:',None)
prep_for=st.text_input('Report Prepared for:',None)

prompt=f'''Assume you are a structuratal engineer.the user has provided on image of a structure.you
need to identify the structural defects in the image and generate a report.the report should contain the following:

It should with the title, prepared by and prepared for details. Provided by user. also use
{pre_title} as title, {prep_by} as prepared by, {prep_for} as prepared for the same.
also mention the current date from{dt.datetime.now().date()}.


* Identify and classify the defect for eg:crack,spalling,corrosion,honeycombing,etc.
* there could more than one defects in the image.identify all the defects separately
* for each defect identified,provide a short description of the defect and its potential impact on the
* for each measure the severity of the defect as low,medium or high.Also mention if the defect is inevitable or avoidable.
* Also mention the time before this effect leads to permament damage to the structure
* provide a short term and long solution anlong with their estimated cost and time to implement
* what precuationary measures can be taken to avoid such defects in future.
* The report generated should be in the word format.
* Show the data in bullet points and tabular format whereever possible.
* make sure that the report does not exceeds 3 pages'''

if st.button('Generate Report'):
    if uploaded_image is None:
        st.error('please upload an image first.')
    else:
        with st.spinner('Generating Report...'):
            response=model.generate_content([prompt,image],generation_config={'temperature':0.2})
            st.write(response.text)
        st.download_button(
            label='Download Report',
            data=response.text,
            file_name='Structurak_defect_report.text',
            mime='text/plain')            