전자공학과 종합설계과제(2) 수행 코드입니다.

![algorithm](https://github.com/swlee1240/grad_design_2/assets/129383630/8d0b5b73-2f89-478b-be9b-ee68fb0a323b)

위 사진은 코드의 기본적인 알고리즘입니다.
text, image, audio와 같은 다양한 형태의 일기를 입력받아 해당 내용에 대한 그림 일기를 출력해주는 알고리즘입니다.


github에는 업로드 하지 않았지만 이미지 생성으로는 stable-diffusion-webui를 활용했습니다.
zavychromaxl_v21 모델을 사용했고, 유화풍에는 oil painting Lora를 사용했습니다.


**반드시 필요한 설정들은 아래와 같습니다**
1) python 3.8
2) torch 1.8.0

-> 위 조건을 만족해야 자연어처리 모델 Pororo의 OCR 기능을 정상적으로 활용할 수 있습니다. (Pororo 공식 문서에서는 torch 1.6.0을 권장하지만 현재는 에러가 뜹니다.)




아래는 데모 사진들입니다.

1. 텍스트로 입력받기

![1](https://github.com/swlee1240/grad_design_2/assets/129383630/48eec33e-0cc9-4a2a-9ed6-ca68e7f22487)
![2](https://github.com/swlee1240/grad_design_2/assets/129383630/1eb85066-f4d6-4974-a576-f0695b595520)

2. 오디오로 입력받기

(오늘은 친구들과 함께 식당에서 피자를 먹었던 날이다. 친구들과 오랜만에 만나기로 한 특별한 날이었다. 그곳은 아늑한 분위기와 맛있는 피자로 유명한 곳이었다. 피자가 나오기를 기다리는 동안 친구들과 이야기를 나눴다. 오랜만에 만난 친구들의 얼굴은 더욱 반가웠다.)

![3](https://github.com/swlee1240/grad_design_2/assets/129383630/7623b23f-55a4-4ca0-98da-e1ef591da59c)
![4](https://github.com/swlee1240/grad_design_2/assets/129383630/4f62ea91-b60d-47f1-9f5d-89b6680332c4)

3. 이미지(일기장을 찍은 사진)로 입력받기

![5](https://github.com/swlee1240/grad_design_2/assets/129383630/c184d976-b5ea-43e5-9e69-a095f6a6fab1)
![6](https://github.com/swlee1240/grad_design_2/assets/129383630/13fdb95e-e65f-4125-ad46-0542233e2b50)

