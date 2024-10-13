# import json
from django.http import JsonResponse
import cohere
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time
from django.shortcuts import render

cohere_client = cohere.Client('a8d3Ka6iKAOwT2wkKMhyrx0ewCRgE2IOBd4orXzQ')

def get_reviews(request):
    url = request.GET.get('page')
    
    if not url:
        return JsonResponse({'error': 'No page URL provided'}, status=400)

    if 'amazon.in' in url:
        reviews_data = extract_reviews(url)
    
    if reviews_data is None:
        return JsonResponse({'error': 'Failed to extract reviews'}, status=500)
    
    return JsonResponse(reviews_data, safe=False)


def get_reviews_url(product_url):
    # Extracting  product ID using regex
    match = re.search(r'/dp/([A-Z0-9]+)', product_url)
    if match:
        product_id = match.group(1)

        reviews_url = f"https://www.amazon.in/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        print('reviews_url',reviews_url)
        return reviews_url
    else:
        return None





def extract_reviews(url):
    reviews = []
    page_number = 1

    reviews_url = get_reviews_url(url) 
    print('reviews_url',reviews_url)
    if not reviews_url:
        return {'error': 'Invalid product URL'}
    while True:
        # Construct the URL for the current page
       
        page_url = f"{reviews_url}&pageNumber={page_number}"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(page_url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all review elements
            review_elements = soup.find_all(class_='a-section review aok-relative')

            if not review_elements:
                break

            for element in review_elements:
                review_info = {}

                title_element = element.find('a', {'data-hook': 'review-title'})
                title_span = title_element.find('span', class_=False)  
                review_info['title'] = title_span.get_text(strip=True) if title_span else None

                rating_element = element.find('i', {'data-hook': 'review-star-rating'})
                review_info['rating'] = rating_element.get_text(strip=True) if rating_element else None

                rating_element = element.find('span', {'data-hook': 'review-date'})
                review_info['date'] = rating_element.get_text(strip=True) if rating_element else None

                body_element = element.find('span', {'data-hook': 'review-body'})
                review_info['body'] = body_element.get_text(strip=True) if body_element else None

                reviewer_element = element.find('span', {'class': 'a-profile-name'})
                review_info['reviewer'] = reviewer_element.get_text(strip=True) if reviewer_element else None

 
                reviews.append(review_info)


            page_number += 1

    # Create the final structured output
    reviews_count = len(reviews)
    result = {
        'reviews_count': reviews_count,
        'reviews': reviews
    }
    return result



def enter_url(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'No URL provided'}, status=400)
        reviews_data = extract_reviews(url)
        if reviews_data is None:
            return JsonResponse({'error': 'Failed to extract reviews'}, status=500)
        return JsonResponse(reviews_data, safe=False)
    
    return render(request, 'review/index.html')

