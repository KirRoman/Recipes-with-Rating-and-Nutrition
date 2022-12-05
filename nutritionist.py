import recipes
import pandas as pd
pd.options.mode.chained_assignment = None
import re
print("Ingredients List Example: apple, bean, cookie, fruit, lentil, tomato")
list_of_ingredients = input("Please write name of the ingredient in English, do not use numbers or special characters: ")
list_of_ingr = list_of_ingredients.lower()
list_of_ingr = list_of_ingr.split(',')
list_of_ingr = [x.strip(' ') for x in list_of_ingr]
df = pd.read_csv('epi_r_clean.csv')
groceries = df.columns[2:]
if len(list_of_ingr) <= 1:
    print("Слишком мало продуктов. Введите 2 продукта и более")
elif len(list_of_ingr) > 1:
    a = 0
    for i in list_of_ingr:
        if i not in list(groceries):
            print("К сожелению, не знаю такой продукт:", i)
        else: a = a + 1
    if a < len(list_of_ingr):
        print("Попробуйте выбрать что-нибудь из списка:", list(groceries))
    if a == len(list_of_ingr):
        recipe = recipes.Forecast(list_of_ingredients)
        recipe.preprocess()
        rating_cat, text = recipe.predict_rating_category()
        print('\n' + 'I. НАШ ПРОГНОЗ' + '\n' + text + '\n')
        nutrition = recipes.NutritionFacts(list_of_ingredients)
        facts = nutrition.retrieve()
        print("II. ПИЩЕВАЯ ЦЕННОСТЬ")
        for n in list_of_ingr:
            print('\n' + n + '\n')
            for nn in range(len(facts)):
                if facts['food_product'][nn] == n:
                    print(facts['nutrition'][nn], ' - ',facts['pr_daily_norm'][nn], '% of Daily Value')
        similarrecipe = recipes.SimilarRecipes(list_of_ingredients)
        indexes,n = similarrecipe.find_all()
        text_with_recipes = similarrecipe.top_similar()
        print('\n' + 'III. ТОП-3 ПОХОЖИХ РЕЦЕПТА:' + '\n')
        if n < len(list_of_ingr):
            print('Из введённых Вами продуктов рецепта не нашлось, могу предложить следующие рецепты с максимальным количеством этих продуктов: ')
            if len(text_with_recipes) >= 3:
                print(f"- {text_with_recipes['title'][0]}, рейтинг {text_with_recipes['rating'][0]} URL: {text_with_recipes['url'][0]}")
                print(f"- {text_with_recipes['title'][1]}, рейтинг {text_with_recipes['rating'][1]} URL: {text_with_recipes['url'][1]}")
                print(f"- {text_with_recipes['title'][2]}, рейтинг {text_with_recipes['rating'][2]} URL: {text_with_recipes['url'][2]}")
            else:
                print('похожие рецепты не найдены введите другой список продуктов')
        if n == len(list_of_ingr) & int(text_with_recipes['ing_n'][0]) == 0 & len(text_with_recipes) >= 1:
            print('Вот рецепт со всеми введёнными продуктами: ')
            print(f"- {text_with_recipes['title'][0]}, рейтинг {text_with_recipes['rating'][0]} URL: {text_with_recipes['url'][0]}")
