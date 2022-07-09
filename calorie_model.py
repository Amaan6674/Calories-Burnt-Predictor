# import library
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

# load the data
data = pd.read_csv("calorie.csv")
print(data.head())

# understand the data
print(data.isnull().sum())

# features and target
features = data.drop(columns=['User_ID','Calories'])
target = data['Calories']

new_features = pd.get_dummies(features, drop_first=True)
print(new_features)

print(features.head())
print(target.head())


# train and test
x_train,x_test,y_train,y_test = train_test_split(new_features,target,test_size=0.2,random_state=5)


# model
model = RandomForestRegressor()
model.fit(x_train,y_train)


# performance
y_pred = model.predict(x_test)
score = model.score(x_test,y_test)
print(score)

'''
age = int(input("Enter Age: "))
h = int(input("Enter Height: "))
w = float(input("Enter Weight: "))
dur = float(input("Enter Duration: "))
hr = float(input("Enter Heart Rate: "))
bt = float(input("Enter Body Temp: "))
g = int(input("Enter 1 for Male or 0 for Female: "))

d = [[age,h,w,dur,hr,bt,g]]

res = model.predict(d)
print("Res = " ,res)




# save the model

with open("calorie.model", "wb" ) as f:
	pickle.dump(model,f)
'''

