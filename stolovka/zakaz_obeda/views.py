from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



# Create your views here.

def register(request):
    """Страница регистрации"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """Страница входа"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')


def home(request):
    """Главная страница - управление столовой"""
    #works_list = Work.objects.all().select_related('author', 'genre').prefetch_related('tools').order_by('-created_at')
    
    #paginator = Paginator(works_list, 10)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {
       # 'page_obj': page_obj,
      #  'works': page_obj.object_list
    })


@login_required
def profile(request):
    """Личный кабинет пользователя (редирект на публичный профиль)"""
    return redirect('user_profile', username=request.user.username)


def user_profile(request, username):
    """Публичный профиль пользователя"""
    profile_user = get_object_or_404(User, username=username)
    #_list = User.objects.filter(author=profile_user).order_by('-created_at')
    
    paginator = Paginator(works_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'is_own_profile': request.user == profile_user,
        'page_obj': page_obj,
        'works': page_obj.object_list
    })