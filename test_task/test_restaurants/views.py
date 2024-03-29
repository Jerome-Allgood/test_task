from django.contrib.auth import logout, login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from .forms import SignupForm, LoginForm, UserForm, RestaurantForm
from .models import Restaurant, CustomUser, PreOrder, Reserved


class HomeView(ListView):
    model = Restaurant
    template_name = 'home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        rest = sorted(Restaurant.objects.all(),
                      key=lambda restaurant: restaurant.total_order_count,
                      reverse=True)
        context['sorted_restaurants'] = rest
        return context


class RestaurantDetailView(DetailView):
    queryset = Restaurant.objects.all()
    template_name = 'restaurant_detail_view.html'

    def post(self, request, pk):
        user = request.user
        restaurant = Restaurant.objects.get(id=request.POST['restaurant'])
        new_order = PreOrder.objects.create(
            user=user,
            restaurant=restaurant
        )
        new_order.save()
        return redirect('/')


def sign_up(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = CustomUser.objects.create_user(**cd)
                user.save()
                login(request, user)
            except IntegrityError as i:
                return render(request, 'signup.html',
                              {'form': form, 'error': i})
        return redirect('/')
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                email=cd['email'],
                password=cd['password']
            )
            if user:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


class ProfileView(TemplateView):
    template_name = 'profile.html'


class MyOrders(ListView):

    def get(self, request, *args, **kwargs):
        pre_orders = PreOrder.objects.filter(user=request.user).filter(
            status='new')
        reserves = Reserved.objects.filter(preorder__user=request.user)
        return render(request, 'my_orders.html', {'pre_orders': pre_orders,
                                                  'reserves': reserves
                                                  })


class AllOrders(ListView):
    def get(self, request, *args, **kwargs):
        pre_orders = PreOrder.objects.all()
        return render(request, 'all_orders.html', {'pre_orders': pre_orders})

    def post(self, request):
        reserves = Reserved.objects.filter(
            preorder__restaurant=request.POST['restaurant'])
        restaurant_tables = Restaurant.objects.get(
            id=request.POST['restaurant']).tables
        if reserves.count() < restaurant_tables:
            pre_order = PreOrder.objects.get(id=request.POST['pre_order_id'])
            pre_order.status = 'confirmed'
            pre_order.save()
            new_reserve = Reserved.objects.create(
                preorder=pre_order
            )
            new_reserve.save()
        pre_orders = PreOrder.objects.all()
        return render(request, 'all_orders.html', {'pre_orders': pre_orders})


class AllReserves(ListView):
    def get(self, request, *args, **kwargs):
        reserves = Reserved.objects.all()
        return render(request, 'all_reserves.html', {'reserves': reserves})

    def post(self, request):
        reserve = Reserved.objects.get(id=request.POST['reserve_id'])
        reserve.delete()
        reserves = Reserved.objects.all()
        return render(request, 'all_reserves.html', {'reserves': reserves})


class CreatePreorder(FormView):
    form_class = UserForm
    restaurant_form_class = RestaurantForm
    template_name = 'create_preorder.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        restaurant_choice_form = self.restaurant_form_class
        return render(request, self.template_name,
                      {'form': form, 'restaurant_form': restaurant_choice_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        restaurant_choice_form = self.restaurant_form_class(request.POST)
        if form.is_valid() and restaurant_choice_form.is_valid():
            new_user = CustomUser.objects.create(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                phone=form.cleaned_data['phone']
            )
            new_user.save()
            new_preorder = PreOrder.objects.create(
                user=new_user,
                restaurant=restaurant_choice_form.cleaned_data['restaurant'],
            )
            new_preorder.save()
            return render(request, 'all_orders.html')
