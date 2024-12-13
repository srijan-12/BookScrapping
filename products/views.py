from django.core.paginator import Paginator
from django.shortcuts import render
from products.models import Product
from .groq_summary import get_product_insights

def product_list(request):
    # Get all products
    product_list = Product.objects.all()

    # Create a paginator object, splitting the product list into 12 products per page
    paginator = Paginator(product_list, 12)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the products for the current page
    page_obj = paginator.get_page(page_number)

    # Call the Groq API to get insights
    prompt = (
        "You are a data analyst for an e-commerce website where different products are listed. "
        "You will be provided with some of its catalog data, and you need to provide insights in a summary format. "
        "The data is in the sequence of name, price, rating, and description."
    )
    
    question = []
    for product in page_obj:
        question.append(
            f"Name: {product.name}, Price: {product.price}, Rating: {product.rating}, Description: {product.description}"
        )
    question_text = "\n".join(question)
    
    result = get_product_insights()
    # insights_list = result.split(".")

    # Render the template with paginated products and Groq insights
    return render(request, 'product_list.html', {
        'page_obj': page_obj,
        'insights': result,
    })
