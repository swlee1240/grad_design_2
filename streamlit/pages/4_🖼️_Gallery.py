import streamlit as st
import os
from PIL import Image
import random

# Streamlit 앱 제목 설정
st.title(":sunflower:   일기장   :blossom:")

# 모든 파일 목록 가져오기
input_txt_path="/home/sangwon/grad_design/input_text"
input_img_path="/home/sangwon/grad_design/input_photo"
input_sound_path="/home/sangwon/grad_design/input_audio"
output_img_path="/home/sangwon/grad_design/result_image"
sound2txt_path="/home/sangwon/grad_design/input_audio2text"


input_txt_files = os.listdir(input_txt_path)
input_img_files = os.listdir(input_img_path)
input_sound_files = os.listdir(input_sound_path)

# 파일 이름에 따라 정렬
all_files = input_txt_files + input_img_files + input_sound_files 
#+ output_img_files

for file_name in sorted(all_files, reverse=True):
    
    filename=file_name.split(".")[0]
    date=filename[0:4]+"년"+filename[4:6]+"월"+filename[6:8]+"일"
    
    txt_path0 = input_txt_path+"/"+file_name
    input_img_path0 = input_img_path+"/"+file_name
    sound_path = input_sound_path+"/"+file_name
    
    output_img_path0=output_img_path+"/"+filename+".png"
    sound2txt_path0 = sound2txt_path+"/"+filename+".txt"
    
   
    # 텍스트 파일 불러오기
    if os.path.exists(txt_path0)&os.path.exists(output_img_path0):
        
        st.header(date)
        col1, col2 = st.columns(2)
    
        with col1:
            with open(txt_path0, "r", encoding='UTF8') as txt_file:# 서버에선, encoding='UTF8'이거 없어도 될듯
                text_content = txt_file.read()
            st.write(text_content)
        with col2:
                
            output_image = Image.open(output_img_path0)
            st.image(output_image,"", use_column_width=True)
    

    # 이미지 파일 불러오기
    if os.path.exists(input_img_path0)&os.path.exists(output_img_path0):
        st.header(date)
        col1, col2 = st.columns(2)
        with col1:
            image = Image.open(input_img_path0)
            st.image(image, "", use_column_width=True)
        with col2:
            output_image = Image.open(output_img_path0)
            st.image(output_image, "", use_column_width=True)


    # 사운드 파일 불러오기
    if os.path.exists(sound_path)&os.path.exists(sound2txt_path0)&os.path.exists(output_img_path0):
        st.header(date)
        col1, col2 = st.columns(2)
        with col1:
            
            audio = open(sound_path, 'rb').read()
            st.audio(audio, format='audio/mp3')
            
            
            with open(sound2txt_path0, "r", encoding='UTF8') as sound2txt_file:# 서버에선, encoding='UTF8'이거 없어도 될듯
                sound2text_content = sound2txt_file.read()
            #st.markdown(f"## {file_name}")
            st.markdown("##### 오디오 >> 텍스트")
            st.write(sound2text_content)
            
        with col2:
            
            output_image = Image.open(output_img_path0)
            st.markdown(" ")
            st.image(output_image, "", use_column_width=True)