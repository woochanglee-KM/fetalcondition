import copy
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model, layers
from tensorflow.keras import layers

#모델 정의 및 불러오기
def conv_auto_model():
    n_steps = 5750
    n_features = 1
    input_layer = layers.Input(shape=(n_steps, n_features))
    pad_check = tf.cast(input_layer != 0, dtype=tf.float32)
    h = layers.Masking(mask_value=0)(input_layer)

    h = layers.Conv1D(filters=32, kernel_size=20,
                      activation="relu", name='conv_1')(h)
    h = layers.Conv1D(filters=16, kernel_size=20,
                      activation="relu", name='conv_2')(h)

    h = layers.Conv1DTranspose(
        filters=16, kernel_size=20, activation="relu", name='conv_3')(h)
    h = layers.Conv1DTranspose(
        filters=32, kernel_size=20, activation="relu", name='conv_4')(h)
    h = layers.Conv1DTranspose(
        filters=1, kernel_size=1, activation="relu", name='conv_5')(h)

    h = pad_check*h
    model = Model(input_layer, h)
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse')

    # 모델 불러오기
    model.load_weights("./model/pred_fetal_condition.h5")
    return(model)

#비정상스코어 & 태아상태 도출
def forecasting_condition(model,data):
    #데이터 전처리
    def padding(data):
        length=len(data)
        if len(data)>5750:
            data=data[(length-5750):length]
        elif len(data)<5750:
#            if len(data)==0:
#                data = np.concatenate((data, np.repeat(0, 5750-len(data)))).tolist()
#            elif np.unique(data)[0]==0:
#                data=[0.01]
#                data = np.concatenate((data, np.repeat(0, 5750-len(data)))).tolist()
#            else:
            data = np.concatenate((data, np.repeat(0, 5750-len(data)))).tolist()                
        else:
            data=data
        return(data)
        
    #0패딩
    data=padding(data)

    # 데이터표준화
    data_max = 190
    data_min = 0
    data_std = (np.array(data)-data_min)/(data_max-data_min)
    data_std = data_std.reshape(1, len(data), 1)

    # 모델예측(표준화풀기)
    data_pred = model.predict(data_std)
    data_pred = data_pred*(data_max-data_min)+data_min
    data_pred = data_pred.reshape(data_pred.shape[1])

    #비정상스코어
    score=max(data-data_pred)
    
    # 태아상태
    if score < 10:
        if score==0:
            state='비정상'
        else:        
            state = '정상'
    else:
        state = '비정상'
    return(score, state)

# 기초태아심박동율 & 정서안정지수 산출
def emotional_stability_index(data):
    if len(data)==0:
        a=0;b=20
    else:
        if data==[0]:
            a,b=0,[0]
        else:
            #기초태아심박동율
            a=pd.Series(data)
            a = a.loc[a != 0] #0제외
            a = a.loc[(a >= a.quantile(q=0.1)) & (a <= a.quantile(q=0.9))]# 분위수를 기준으로 80%영역을 가져옴
            a = int(a.mean())# 평균값 도출
            
            # 태아 정서안정 지수
            b = abs(a-120)
            b = int(b)
            conditionlist = [
            (b == 0),
            ((0 < b) & (b <= 10)),
            ((10 < b) & (b <= 20)),
            ((20 < b) & (b <= 30)),
            ((30 < b) & (b <= 40)),
            ((40 < b) & (b <= 50)),
            ((50 < b) & (b <= 60)),
            ((60 < b) & (b <= 70)),
            (b < 60)]
            choicelist = [100, 90, 80, 70, 60, 50, 40, 30, 20]
            b = np.select(conditionlist, choicelist, default=0)
            b = b.tolist()
    return a, b