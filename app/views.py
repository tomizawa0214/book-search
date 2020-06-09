from django.views.generic import View
from django.shortcuts import render
import json
import requests
from .forms import SearchForm

SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1025176530386995193'

def get_api_data(params):
  api = requests.get(SEARCH_URL, params=params).text
  result = json.loads(api)
  items = result['Items']
  return items

class IndexView(View):
  def get(self, request, *args, **kwargs):
    form = SearchForm(request.POST or None)

    return render(request, 'app/index.html', {
      'form': form
    })

  def post(self, request, *args, **kwargs):
    form = SearchForm(request.POST or None)

    if form.is_valid():
      keyword = form.cleaned_data['title']
      params = {
        'title': keyword,
        'hits': 28,
      }
      items = get_api_data(params)
      book_data = []
      for i in items:
        item = i['Item']
        title = item['title']
        image = item['largeImageUrl']
        isbn = item['isbn']
        query = {
          'title': title,
          'image': image,
          'isbn': isbn
        }
        book_data.append(query)

      return render(request, 'app/book.html', {
        'book_data': book_data,
        'keyword': keyword
      })
    
    return render(request, 'app/index.html', {
      'form': 'form'
    })