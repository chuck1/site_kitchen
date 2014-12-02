from django.shortcuts import render

import markdown

# Create your views here.

def index(request):
	context = {}
	return render(request, 'wiki/index.html', context)

def page(request, page):

	context = {}

	filename = '/home/chuck/git/wiki/' + page + '.md'
	
	try:
		with open(filename, 'r') as f:
			text = f.read()
	except:
		context['text'] = repr(filename) + ' not found'
	else:
		html = markdown.markdown(text)

		context['text'] = html

	return render(request, 'wiki/page.html', context)

