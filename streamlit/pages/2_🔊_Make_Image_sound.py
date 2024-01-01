import streamlit as st
from PIL import Image
import io
import base64
import requests
from PIL import Image
from PIL import Image, PngImagePlugin
from streamlit_option_menu import option_menu
from pororo import Pororo
from langdetect import detect
import openai
import os

## Title
st.title('AI 그림 일기 생성')

## Header/Subheader
st.markdown("* * *")
st.header('음성에 해당하는 그림 생성')
st.markdown("* * *")

dat=st.date_input('날짜') 
date=f"{dat}"
nowtime=date[0:4]+date[5:7]+date[8:10]


st.subheader("음성 파일을 업로드 해주세요")

openai.api_key = 'Enter your OpenAI api key'
steps = st.slider('     <속도-----------------------------------------------------퀄리티>', 10, 100, 35)
col1, col2 = st.columns(2)

with col1:
    checkbox1 = st.checkbox('유화풍')
with col2:
    checkbox2 = st.checkbox('현실풍')
uploaded_file = st.file_uploader("업로드")#업로드 받기


#Speech Recognition(asr), Summarization(summ), Translation(trans)
summ1 = Pororo(task="summarization", model="abstractive", lang="ko")
summ2 = Pororo(task='summarization', model='bullet', lang='ko')
trans = Pororo(task='translation', lang='multi')


if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format='audio/mp3')   # 받은 파일 보여주기
    
    
#----------------------------------------------------------------------------------------------------------------------------    
    # 저장 경로 
    save_path='/home/sangwon/grad_design/result_image/'+nowtime+'.png'#결과 사진 저장 경로
    sound_path="/home/sangwon/grad_design/input_audio/"+nowtime+".wav"# 사운드 파일 저장 경로
    save_text="/home/sangwon/grad_design/input_audio2text/"+nowtime+".txt"
#---------------------------------------------------------------------------------------------------------------------------- 

    if (os.path.exists(sound_path)):
        ""
    else:
        with open(sound_path, mode='bx') as f:      #업로드 파일 저장
            f.write(audio_bytes)       
        
        
    # audio2text
    audio_file = open(sound_path, 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)
    text = transcript['text']
    print(f'text : {text}')
    file = open(save_text, "w") 
    file.write(text)
    file.close()
    
    
    # text2img Pipeline
    if (detect(text)=='en'):
        ko_res = trans(text, src='en', tgt='ko')
        print(f'ko_res : {ko_res}')
        ko_res = summ1(ko_res, beam=20)
        print(f'ko_key1 : {ko_res}')
        ko_key = summ2(ko_res, beam=20)
        print(f'ko_key2 : {ko_key}')
        ko_key_sum=''
        for i in range(len(ko_key)):
            ko_key_sum+=f'{ko_key[i]},'
        print(f'ko_key_sum : {ko_key_sum}')
        en_key = trans(ko_key_sum, src='ko', tgt='en')
        print(f'en_key : {en_key}')
        
        
    elif (detect(text)=='ko'):
        ko_res = text
        print(f'ko_res : {ko_res}')
        ko_key = summ2(ko_res, beam=20)
        print(f'ko_key : {ko_key}')
        ko_key_sum=''
        for i in range(len(ko_key)):
            ko_key_sum+=f'{ko_key[i]},'
        print(f'ko_key_sum : {ko_key_sum}')
        en_key = trans(ko_key_sum, src='ko', tgt='en')
        print(f'en_key : {en_key}')
    if checkbox1==True:
        en_key="<lora:oil painting:0.6>, oil painting, "+en_key
    elif checkbox2==True:
        en_key="realistic,"+en_key

    chat_response = "(masterpiece,highest quality), " + en_key
    

    # sd_webui address
    url = "http://127.0.0.1:7860"

    print(f"{chat_response}")

    if st.button("만들기", key='message'):
        payload = {
        "prompt": chat_response,
        "negative_prompt": "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation. tattoo, watermark, text, sketch, 3d, vector art, bad hands, low quality, human, letterbox, letter, face",
        "seed": -1,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "denoising_strength": 0.45,
        "enable_hr": True,
        "hr_scale": 1.5,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
        "hr_second_pass_steps": 10,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "send_images": True,
        "save_images": False,
        }

        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

        r = response.json()

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            
            png_payload = {
                "image" : "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
            
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save(save_path, pnginfo=pnginfo)

        
        ##Show image
        img = Image.open(save_path)
        st.image(img, caption="Result Image")
    
    