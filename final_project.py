#!/usr/bin/env python
# coding: utf-8

# In[78]:


#import library we needed and the csv file 
import numpy as np
import pandas as pd
df = pd.read_csv('StudentsPerformance.csv')

#change the order of the column and change it to the form of array 
df = df[['gender','race/ethnicity','parental level of education','test preparation course','math score','reading score','writing score','lunch']]
data = np.array(df)


# In[79]:


#label encoding the data, change the data that is not in the form of digit into digit 
def change_value_to_number(array):
    
    for i in range(len(array)):
        if array[i][0] == 'female':
            array[i][0] = 0
        elif array[i][0] == 'male':
            array[i][0] = 1
        
    for i in range(len(array)):
        if array[i][1] == 'group A':
            array[i][1] = 0
        elif array[i][1] == 'group B':
            array[i][1] = 1
        elif array[i][1] == 'group C':
            array[i][1] = 2
        elif array[i][1] == 'group D':
            array[i][1] = 3
        elif array[i][1] == 'group E':
            array[i][1] = 4

    for i in range(len(array)):
        if array[i][2] == "bachelor's degree":
            array[i][2] = 0
        elif array[i][2] == 'some college':
            array[i][2] = 1
        elif array[i][2] == "master's degree":
            array[i][2] = 2
        elif array[i][2] == "associate's degree":
            array[i][2] = 3
        elif array[i][2] == "high school":
            array[i][2] = 4
        elif array[i][2] == "some high school":
            array[i][2] = 5

    for i in range(len(array)):
        if array[i][3] == 'completed':
            array[i][3] = 0
        elif array[i][3] == 'none':
            array[i][3] = 1
            
    for i in range(len(array)):
        if array[i][7] == 'standard':
            array[i][7] = 0
        elif array[i][7] == 'free/reduced':
            array[i][7] = 1
            
    array = np.asarray(array).astype('float32')
    
    return array


# In[80]:


#slice the first 800 data as training data
def slice_training_value(array):
    x_train = array[0:800,:7]
    y_train = []
    
    y_train_list = []
    for i in range(800):
        train_label = array[i][7]  #and take the data of the last column as label
        y_train_list.append(train_label)
        
    y_train = np.array(y_train_list) #trasforming the list into the form of array
    
    return x_train, y_train


# In[81]:


#slice the last 200 data as testing data
def slice_testing_value(array):
    x_test = array[801:1000,:7]
    y_test = []
    
    y_test_list = []
    for i in range(801,1000,1):
        test_label= array[i][7]  #and take the data of the last column as label
        y_test_list.append(test_label)
    
    y_test = np.array(y_test_list)  #trasforming the list into the form of array
    
    return x_test, y_test


# In[82]:


#use one hot encoding to encode the label data
from keras.utils import np_utils

def categorize_label(y_train, y_test):
    y_train = np_utils.to_categorical(y_train, 2)  #2 kind of outputs for the label, one for eating lunch normally ,and one for not
    y_test = np_utils.to_categorical(y_test, 2)
    
    return y_train, y_test 


# In[83]:


#import Keras and the functions we needed in this project
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from keras import losses

#designing the training models
def analyzing_data(x_train, x_test, y_train, y_test):
    model = Sequential()
    
    model.add(Dense(units = 7, activation='relu'))
    model.add(Dense(units = 1000, activation='relu'))
    model.add(Dense(units = 1000, activation='relu'))
    model.add(Dense(units = 1000, activation='relu'))
    model.add(Dense(units = 2, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size = 20, epochs = 200)

    result = model.evaluate(x_test, y_test)
    
    #print out the result of loss and accuracy for training
    print('Total loss',result[0])
    print('Acc:',result[1])
    
    #save the models to prepare for predicting the users result
    model.save('analyze.ann')


# In[84]:


#import the library we needed for creating GUI
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

#import load_model to use the model we trained before
from keras.models import load_model

#creating main window
menu = tk.Tk()
menu.title('高中學生用餐行為分析及預測系統')
menu.geometry('1000x1200')
menu.configure(bg = 'light blue')

#define the button when user click the "確定" button
def name_button_event():
    
    #define the button when user click the "我知道了!" button
    def confirm_button_event():
        
        #define the button when user click the "確認填寫無誤，開始分析資料" button
        def finish_button_event():
            
            #tell the user that the data analyzing is starting, and show the label when analyzing is finished
            processing = tk.Label(menu, text = "資料分析完成，請點進右方按鈕觀看預測結果。", bg = 'light blue', font = ("微軟正黑體",16))
            processing.grid(row = 12, column = 0,padx = 0, pady = 0)
            
            analyze_button = tk.Button(menu, width = 12, text = '開始預測!', font = ('微軟正黑體',18),bg = 'red', command = analyze_button_event)
            analyze_button.grid(row = 10, column = 1, padx = 50, pady = 0, ipady = 8)
            
            #put the csv file into the model for training, and starts training it
            array = change_value_to_number(data)
            x_train, y_train = slice_training_value(array)
            x_test, y_test = slice_testing_value(array)
            y_train, y_test = categorize_label(y_train, y_test)
            analyzing_data(x_train, x_test, y_train, y_test)

        #define the button when user click the "開始預測!" button
        def analyze_button_event():
            
            #show the prediction for user in the form of messagebox
            def pop_up():
                if lunch.get() == 0:
                    truth = "有吃午餐"
                else:
                    truth = "沒吃午餐"
                
                #show the predicting result and the fact 
                if predict[0][1] > predict[0][0]:
                    messagebox.showinfo("預測結果", "我預測您沒在吃午餐!\n您實際上的結果為:" + truth)
                else:
                    messagebox.showinfo("預測結果", "我預測您有在吃午餐!\n您實際上的結果為:" + truth)
            
            #put the data of the user entered into the training model we have trained before
            model = load_model('analyze.ann')
            gender_val = int(gender.get())
            ethnic_val = int(ethnic.get())
            education_val = int(education.get())
            preparation_val = int(preparation.get())
            math_val = int(math.get())
            reading_val = int(reading.get())
            writing_val = int(writing.get())
            enter = np.array([gender_val,ethnic_val,education_val,preparation_val,math_val,reading_val,writing_val])
           
            #change the form of the data entered to fit the shape for predicting
            temp = np.zeros(7)
            temp = temp.reshape(1,7)
            for i in range(7):
                temp[0,i] = enter[i]
            
            #starts predicting
            predict = model.predict(temp)
            pop_up()
         
        #validate that the data user entered are digits
        def validate(P):
            if str.isdigit(P) or P == '':
                return True
            else:
                return False
            
        welcome3.grid_remove()
        welcome4.grid_remove()
        confirm.grid_remove()
        
        #create a form and prompt the user to enter his/her personal information
        problem1 = tk.Label(menu, text = "問題1: 請問您的性別是?",bg = 'light blue',  font = ('微軟正黑體',14))
        problem1.grid(row = 0, column = 0,padx = 0, pady = 30)
        
        gender = tk.IntVar() 
        female = tk.Radiobutton(menu, text = '女性', variable = gender, value = 0, bg = 'light blue', font = ('微軟正黑體',14))
        female.grid(row = 0, column = 1,padx = 0, pady = 0)
        male = tk.Radiobutton(menu, text = '男性', variable = gender, value = 1, bg = 'light blue', font = ('微軟正黑體',14))
        male.grid(row = 0, column = 2,padx = 0, pady = 0)
       
        problem2 = tk.Label(menu, text = "問題2: 請問您的國籍是?", bg = 'light blue', font = ('微軟正黑體',14))
        problem2.grid(row = 1, column = 0,padx = 0, pady = 30)
        
        ethnic = tk.IntVar()
        american = tk.Radiobutton(menu, text = '白人', variable = ethnic, value = 0, bg = 'light blue', font = ('微軟正黑體',14))
        american.grid(row = 1, column = 1,padx = 0, pady = 0)
        latins = tk.Radiobutton(menu, text = '拉丁人', variable = ethnic, value = 1, bg = 'light blue', font = ('微軟正黑體',14))
        latins.grid(row = 1, column = 2,padx = 0, pady = 0)
        african = tk.Radiobutton(menu, text = '非裔', variable = ethnic, value = 2, bg = 'light blue', font = ('微軟正黑體',14))
        african.grid(row = 1, column = 3,padx = 0, pady = 0)
        asian = tk.Radiobutton(menu, text = '亞裔', variable = ethnic, value = 3, bg = 'light blue', font = ('微軟正黑體',14))
        asian.grid(row = 2, column = 1,padx = 0, pady = 0)
        others = tk.Radiobutton(menu, text = '其他', variable = ethnic, value = 4, bg = 'light blue', font = ('微軟正黑體',14))
        others.grid(row = 2, column = 2,padx = 0, pady = 0)
        
        problem3 = tk.Label(menu, text = "問題3: 請問您父母的最高學歷是?", bg = 'light blue', font = ('微軟正黑體',14))
        problem3.grid(row = 3, column = 0,padx = 0, pady = 30)
        
        education = tk.IntVar()
        bachelors = tk.Radiobutton(menu, text = '學士畢業', variable = education, value = 0, bg = 'light blue', font = ('微軟正黑體',14))
        bachelors.grid(row = 3, column = 1,padx = 0, pady = 0)
        college = tk.Radiobutton(menu, text = '大學(未畢)', variable = education, value = 1, bg = 'light blue', font = ('微軟正黑體',14))
        college.grid(row = 3, column = 2,padx = 0, pady = 0)
        master = tk.Radiobutton(menu, text = '碩士畢業', variable = education, value = 2, bg = 'light blue', font = ('微軟正黑體',14))
        master.grid(row = 3, column = 3,padx = 0, pady = 0)
        association = tk.Radiobutton(menu, text = '專科', variable = education, value = 3, bg = 'light blue', font = ('微軟正黑體',14))
        association.grid(row = 4, column = 1,padx = 0, pady = 0)
        high_school = tk.Radiobutton(menu, text = '高中', variable = education, value = 4, bg = 'light blue', font = ('微軟正黑體',14))
        high_school.grid(row = 4, column = 2,padx = 0, pady = 0)
        others = tk.Radiobutton(menu, text = '國中以下', variable = education, value = 5, bg = 'light blue', font = ('微軟正黑體',14))
        others.grid(row = 4, column = 3,padx = 0, pady = 0)
        
        problem4 = tk.Label(menu, text = "問題4: 請問您考試前有復習的習慣嗎?", bg = 'light blue', font = ('微軟正黑體',14))
        problem4.grid(row = 5, column = 0,padx = 0, pady = 30)
        
        preparation = tk.IntVar()
        prepared = tk.Radiobutton(menu, text = '有', variable = preparation, value = 0, bg = 'light blue', font = ('微軟正黑體',14))
        prepared.grid(row = 5, column = 1,padx = 0, pady = 0)
        none = tk.Radiobutton(menu, text = '沒有', variable = preparation, value = 1, bg = 'light blue', font = ('微軟正黑體',14))
        none.grid(row = 5, column = 2,padx = 0, pady = 0)
        
        problem5 = tk.Label(menu, text = "問題5: 請問您最後的數學成績是?", bg = 'light blue', font = ('微軟正黑體',14))
        problem5.grid(row = 6, column = 0,padx = 0, pady = 30)
        
        cmd = (menu.register(validate), '%P')
        math = tk.IntVar()
        math_score = tk.Entry(menu, width = 25, textvariable=math,bg = 'light grey', validate='key', validatecommand=cmd)
        math_score.grid(row = 6, column = 1, padx = 0, pady = 0)
        
        problem6 = tk.Label(menu, text = "問題6: 請問您最後的國文成績是?", bg = 'light blue', font = ('微軟正黑體',14))
        problem6.grid(row = 7, column = 0,padx = 0, pady = 30)
        
        reading = tk.IntVar()
        reading_score = tk.Entry(menu, width = 25, textvariable=reading, bg = 'light grey', validate='key', validatecommand=cmd)
        reading_score.grid(row = 7, column = 1, padx = 0, pady = 0)
        
        problem6 = tk.Label(menu, text = "問題7: 請問您最後的寫作成績是?", bg = 'light blue', font = ('微軟正黑體',14))
        problem6.grid(row = 8, column = 0,padx = 0, pady = 30)
        
        writing = tk.IntVar()
        writing_score = tk.Entry(menu, width = 25, textvariable=writing, bg = 'light grey', validate='key', validatecommand=cmd)
        writing_score.grid(row = 8, column = 1, padx = 0, pady = 0)
        
        problem7 = tk.Label(menu, text = "最後，在預測開始前，\n請告訴我您平常有吃午餐的習慣嗎?", bg = 'light blue', font = ('微軟正黑體',14))
        problem7.grid(row = 9, column = 0,padx = 0, pady = 30)
        
        lunch = tk.IntVar()
        yes = tk.Radiobutton(menu, text = '有', variable = lunch, value = 0, bg = 'light blue', font = ('微軟正黑體',14))
        yes.grid(row = 9, column = 1,padx = 0, pady = 0)
        no = tk.Radiobutton(menu, text = '沒有/吃很少', variable = lunch, value = 1, bg = 'light blue', font = ('微軟正黑體',14))
        no.grid(row = 9, column = 2,padx = 0, pady = 0)
        
        finish_button = tk.Button(menu, width = 30, text = '確認填寫無誤，開始分析資料', bg = 'light green', font = ('微軟正黑體',14), command = finish_button_event)
        finish_button.grid(row = 10, column = 0, padx = 50, pady = 0)
        
        waiting = tk.Label(menu, text = "按下按鈕後，請稍待片刻，\n資料分析將需要2分鐘左右的時間。", bg = 'light blue', font = ('微軟正黑體',12))
        waiting.grid(row = 11, column = 0,padx = 0, pady = 0)
        
        
    #confirm that user has entered his/her name
    if name.get() != '':
        your_name = name.get()
    
    welcome.grid_remove()
    welcome2.grid_remove()
    name.grid_remove()
    name_button.grid_remove()
    img_label.grid_remove()
    
    #introducing the predicting system for user 
    welcome3 = tk.Label(menu, text = your_name+",歡迎!\n    接下來我們會問幾個與您相關的問題，請依照自身情況填寫資料。", bg = 'light blue', font = ('微軟正黑體',20))
    welcome3.grid(row = 0, column = 0, padx = 100, pady = 75)
    
    welcome4 = tk.Label(menu, text = "此預測器將會對1000名高中生的個人資料\n進行深度學習的分析，\n    並根據分析產生預測模型，\n進而從您的資料產生預測結果。", bg = 'light blue', font = ('微軟正黑體',18))
    welcome4.grid(row = 1, column = 0, padx = 0, pady = 50)
    
    confirm = tk.Button(menu, width = 30, text = '我知道了!', bg = 'light green', font = ('微軟正黑體',16), command = confirm_button_event)
    confirm.grid(row = 2, column = 0, padx = 0, pady = 0)
    
#welcoming the user    
welcome = tk.Label(menu, text = '歡迎來到用餐行為分析暨預測系統!\n本系統將根據您的相關資料預測您的午餐用餐狀況:)', bg = 'light blue', font = ('微軟正黑體',25))
welcome.grid(row = 0, column = 0, padx = 140, pady = 200)

#import the meme, and show it at the button of the window
img_file = Image.open("school_lunch.jpg")
img_file = img_file.resize((300, 340),Image.ANTIALIAS)
image = ImageTk.PhotoImage(img_file)
img_label = tk.Label(menu, image = image, bg = 'light blue') 
img_label.grid(row = 4, column = 0, padx = 0, pady = 0, ipady = 10)

#prompt the user to enter his/her name
welcome2 = tk.Label(menu, text = '請在此輸入您的姓名:', bg = 'light blue', font = ('微軟正黑體',20))
welcome2.grid(row = 1, column = 0, padx = 0, pady = 0)


var = tk.StringVar()
name = tk.Entry(menu, width = 25, textvariable=var, bg = 'light grey', font = ('微軟正黑體',18))
name.grid(row = 2, column = 0, padx = 0, pady = 0, ipady = 10)


name_button = tk.Button(menu, width = 10, text = '確定', bg = 'light green', font = ('微軟正黑體',16), command = name_button_event)
name_button.grid(row = 3, column = 0, padx = 0, pady = 0)

menu.mainloop()

