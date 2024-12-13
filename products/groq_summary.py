from groq import Groq
from products.models import Product
import os
API_KEY = os.getenv('API_KEY')
print(API_KEY)
client = Groq(api_key=API_KEY)

def chat(prompt, question):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""{prompt}"""
            },
            {
                "role": "user",
                "content": f"""{question}"""
            }
        ],
        temperature=1,
        max_tokens=4048,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    return result

def get_product_insights():
    products = Product.objects.all()

    question = []
    for product in products:
        question.append(
            f"Name: {product.name}, Price: {product.price}, Rating: {product.rating}, Description: {product.description}"
        )

    question_text = "\n".join(question)

    prompt = (
        "You are a data analyst for an e-commerce website where different products are listed. "
        "You will be provided with some of its catalog data, and you need to provide insights in a summary format. "
        "The data is in the sequence of name, price, rating, and description."
    )

    result = chat(prompt, question_text[0:2000])
    result = result.replace("*", "")
    return result
