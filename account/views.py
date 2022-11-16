from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('page:index')
    else:
        form = UserCreationForm()
    context = {
        # [코드 작성] 화면에 '회원가입' 임을 알려줄 수 있도록 type 전달

        'form': form,
    }
    return render(request, 'account/form.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('page:index')
    else:
        form = AuthenticationForm()
    context = {
        # [코드 작성] 화면에 '로그인' 임을 알려줄 수 있도록 type 전달

        'form': form,
    }
    return render(request, 'account/form.html', context)

# [코드 작성] auth_logout 함수를 이용한 로그아웃 기능 구현

