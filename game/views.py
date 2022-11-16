from django.shortcuts import render, redirect, get_object_or_404
from random import *
from .models import Weapon, Character
from .forms import WeaponForm, CharacterForm

# Create your views here.
win = 0
draw = 0
lose = 0

def weapon_generate():
    # 무기는 자유롭게 변경 가능
    weapons = {
        '주먹도끼': 1,
        '가벼운 물총': 3,
        '낡은 검': 5,
        '수상한 막대기': 7,
        '수학의 정석': 9,
    }

    if Weapon.objects.all().count() == 0:
        for weapon in weapons:
            Weapon.objects.create(
                name = weapon,
                power = weapons[weapon],
            )

def game_list(request):
    weapon_generate()
    return render(request, 'game/game_list.html')

def rsp_select(request):
    global win, draw, lose
    context = {
        'win': win,
        'draw': draw,
        'lose': lose,
    }
    return render(request, 'game/rsp_select.html', context)

def rsp_result(request, pick):
    global win, draw, lose
    rsp = ['가위', '바위', '보']
    com = choice(rsp)

    if pick == com:
        result = '무승부'
        draw += 1
    elif (pick == '가위' and com == '보') or (pick == '바위' and com == '가위') or (pick == '보' and com == '바위'):
        result = '승리'
        win += 1
    else :
        result = '패배'
        lose += 1

    context = {
        'pick': pick,
        'com': com,
        'result': result,
        'win': win,
        'draw': draw,
        'lose': lose,
    }
    return render(request, 'game/rsp_result.html', context)

def rsp_reset(request):
    global win, draw, lose
    win, draw, lose = 0, 0, 0
    return redirect('game:rsp_select')

def weapon_create(request):
    if request.method == 'POST':
        weapon_form = WeaponForm(request.POST)
        
        if weapon_form.is_valid():
            weapon_form.save()
            return redirect('game:weapon_list')
    else:
        weapon_form = WeaponForm()
    
    context = {
        'weapon_form': weapon_form,
    }
    return render(request, 'game/weapon_form.html', context)

def weapon_list(request):
    weapons = Weapon.objects.all()
    context = {
        'weapons': weapons,
    }
    return render(request, 'game/weapon_list.html', context)

def adventure_home(request):
    # 로그인 한 경우
    if request.user.is_authenticated:
        # 생성한 캐릭터가 없을 경우
        # filter를 이용하여 로그인 한 유저와 연결되어 있는 캐릭터 객체가 있는지 찾음
        if Character.objects.filter(user=request.user).count() == 0:
            if request.method == 'POST':
                character_form = CharacterForm(request.POST)
                character_form = character_form.save(commit=False)
                character_form.user = request.user
                character_form.save()
                return redirect('game:adventure_home')
            else:
                character_form = CharacterForm()
            context = {
                'character_form': character_form,
            }
            return render(request, 'game/character_form.html', context)
        # 생성한 캐릭터가 있는 경우
        else:
            character = get_object_or_404(Character, user=request.user)
            # 무기를 얻지 못한 경우
            if character.weapon == None:
                # 무기 랜덤 선택
                # order_by('?')를 이용하여 랜덤하게 정렬 후 첫번째 항목을 가져옴
                random_weapon = Weapon.objects.order_by('?')[0]
                context = {
                    'random_weapon': random_weapon,
                }
                return render(request, 'game/adventure_new.html', context)
            # 무기를 얻은 경우
            else:
                context = {
                    'character': character,
                }
                return render(request, 'game/adventure_home.html', context)
    # 로그인 하지 않은 경우
    else:
        return redirect('account:login')

def weapon_get(request):
    character = get_object_or_404(Character, user=request.user)

    weapon_id = request.POST.get('random-weapon')
    selected_weapon = get_object_or_404(Weapon, id=weapon_id)

    new_weapon = Weapon.objects.create(
        name = selected_weapon.name,
        power = selected_weapon.power
    )
    
    # [미션] 생성된 캐릭터 객체의 weapon 필드에 new_weapon 객체를 넣어주기
    
    # [미션] character 객체를 저장(save)하는 코드 작성
    
    return redirect('game:adventure_home')
