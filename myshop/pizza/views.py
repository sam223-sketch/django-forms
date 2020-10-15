from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza 

# Create your views here.
def home(request):
	return render(request, 'home.html')

def order(request):
	multiple_form = MultiplePizzaForm()
	# Using submitted data in form
	if request.method == 'POST':
		filled_form = PizzaForm(request.POST)
		if filled_form.is_valid():
			created_pizza = filled_form.save()
			created_pizza_pk = created_pizza.id
			#return message to the user after making a order
			note = 'Thanks for Ordering %s %s and %s' %(filled_form.cleaned_data['size'],
			filled_form.cleaned_data['topping1'],
			filled_form.cleaned_data['topping2'],)
			filled_form = PizzaForm()
		else:
			created_pizza_pk = None
			note = 'Pizza order failed. Enter all details. Try again.'
		return render(request, 'order.html', {'created_pizza_pk':created_pizza_pk,'pizzaform':filled_form, 'note':note, 'multiple_form':multiple_form})
	else:

		form = PizzaForm()
		return render(request, 'order.html', {'pizzaform':form, 'multiple_form':multiple_form})


def pizzas(request):
	number_of_pizzas = 2
	filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
	if filled_multiple_pizza_form.is_valid():
		number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
	PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
	formset = PizzaFormSet()
	if request.method == 'POST':
		filled_formset = PizzaFormSet(request.POST)
		if filled_formset.is_valid():
			for form in filled_formset:
				print(form.cleaned_data['topping1'])
			note = 'Pizzas have been ordered'

		else:
			note = 'Order was not created'
		return render(request, 'pizzas.html', {'note':note, 'formset':formset})

	else:
		return render(request, 'pizzas.html', {'formset':formset})

def edit_order(request, pk):
	pizza = Pizza.objects.get(pk=pk)
	form = PizzaForm(instance=pizza)
	if request.method == 'POST':
		filled_form = PizzaForm(request.POST,instance=pizza)
		if filled_form.is_valid():
			filled_form.save()
			form = filled_form
			note = 'Order has been updated.'
			return render(request, 'edit_order.html', {'note':note, 'pizzaform':form,'pizza':pizza})
	return render(request, 'edit_order.html', {'pizzaform':form,'pizza':pizza})
