import random
import re
import pandas as pd
import numpy as np
import joblib

class Forecast:

    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.lower()
        self.list_of_ingredients = self.list_of_ingredients.split(',')
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]

    def preprocess(self):
        df = pd.read_csv('epi_r_clean.csv')
        groceries = df.columns[2:]
        vector = pd.DataFrame(data = np.zeros((1, len(groceries))), columns=groceries)
        for i in list(groceries):
            if i in self.list_of_ingredients:
                vector[i] = 1.0
        self.vector = vector
        return self.vector
        
    def predict_rating_category(self):
        model = joblib.load('best_RandomForestClassifier_cl_3.joblib')
        rating_cat = model.predict(self.vector)
        if rating_cat == 'great':
            text = 'Вкусное. Отличный выбор продуктов!'
        if rating_cat == 'so-so':
            text = 'Нормальное. Но может пересмотрим что-то в списке продуктов?'
        if rating_cat == 'bad':
            text = 'Невкусное. Хоть конкретно Вам может быть и понравится блюдо из этих ингридиентов, но, на наш взгляд, это плохая идея - готовить блюдо из них. Хотели предупредить.'
        rating_cat = rating_cat
        return rating_cat, text

class NutritionFacts:
    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.lower()
        self.list_of_ingredients = self.list_of_ingredients.split(',')
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]
        
    def retrieve(self):
        df = pd.read_csv('df_nutrition.csv')
        for i in self.list_of_ingredients:
            if i == self.list_of_ingredients[0]:
                nutr = df.loc[df['food_product'] == i]
                df_nutr = nutr
            else:
                nutr = df.loc[df['food_product'] == i]
                df_nutr = pd.concat([df_nutr, nutr])
        df_nutr.reset_index(drop=True, inplace=True)
        for x in range(len(df_nutr)):
            df_nutr['pr_daily_norm'][x] =  round(df_nutr['pr_daily_norm'][x], 0)
            df_nutr['nutrition'][x] = df_nutr['nutrition'][x].split(',')[0]
        df_nutr = df_nutr.loc[df_nutr['pr_daily_norm'] > 0]
        df_nutr = df_nutr.sort_values(by=['food_product', 'pr_daily_norm'], ascending=False)
        df_nutr.drop(columns=['value'], inplace=True)
        df_nutr.reset_index(drop=True, inplace=True)
        self.facts = df_nutr
        return self.facts

class SimilarRecipes:
    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.lower()
        self.list_of_ingredients = self.list_of_ingredients.split(',')
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]
    
    def find_all(self):
        df = pd.read_csv('df_recipes.csv')
        df = df.loc[df['val'] - len(self.list_of_ingredients) <= 5]
        for i in self.list_of_ingredients:
            if i == self.list_of_ingredients[0]:
                df_rec = df.loc[df[i] == 1]
                df_recipes = df_rec
            else:
                df_rec = df.loc[df[i] == i]
                df_recipes = pd.concat([df_recipes, df_rec])
        df_recipes = df_recipes.drop_duplicates(keep='first')
        df_recipes.reset_index(drop=True, inplace=True)
        df_recipes['ing'] = df_recipes['val']
        df_recipes['ing_n'] = df_recipes['val']
        for x in range(len(df_recipes)):
            df_recipes['ing'][x] = 0
            for y in self.list_of_ingredients:
                df_recipes['ing'][x] = df_recipes['ing'][x] + df_recipes[y][x]
            df_recipes['ing_n'][x] = df_recipes['val'][x] - df_recipes['ing'][x]
        df_recipes = df_recipes.sort_values(by = ['ing', 'ing_n'], ascending=[False, True])
        self.n = df_recipes['ing'][0]
        self.indexes = df_recipes
        return self.indexes, self.n

    def top_similar(self):
        text_with_recipes = self.indexes
        text_with_recipes = text_with_recipes.loc[text_with_recipes['ing_n'] <= 5]
        text_with_recipes.reset_index(drop=True, inplace=True)
        return text_with_recipes