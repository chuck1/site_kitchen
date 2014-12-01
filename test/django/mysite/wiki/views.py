from django.shortcuts import render

import markdown

# Create your views here.

def index(request):
	context = {}
	return render(request, 'wiki/index.html', context)

def page(request, page):

	context = {}

	try:
		with open('/home/chuck/git/wiki_school/' + page + '.md', 'r') as f:
			text = f.read()
	except:
		context['text'] = repr(page) + ' not found'
	else:
		html = markdown.markdown(text)

		context['text'] = html

	return render(request, 'wiki/page.html', context)

