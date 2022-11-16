from django.shortcuts import render, redirect, get_object_or_404
from .models import Posting, Comment
from .forms import PostingForm, CommentForm
# [코드 작성] django.contrib.auth.decorators 에서 login_required 데코레이션 추가

# [코드 작성] django.views.decorators.http 에서 require_POST 데코레이션 추가


# Create your views here.
def index(request):
    return render(request, 'page/index.html')

# [Read] 전체 글 목록 보기
def posting_list(request):
    postings = Posting.objects.all()
    context = {
        'postings': postings,
    }
    return render(request, 'page/posting_list.html', context)

# [Create] 글 작성하기
def posting_create(request):
    # [코드 작성] 웹 페이지에 로그인이 되어있는 경우만 글 쓰기가 가능하도록 조건문 작성
    
    if request.method == 'POST':
        posting_form = PostingForm(request.POST)
        
        if posting_form.is_valid():
            # [코드 작성] posting_form을 임시저장
            # [코드 작성] posting_form의 author에 작성자 객체 추가

            posting_form.save()
            return redirect('page:posting_list')
    else:
        posting_form = PostingForm()
    
    context = {
        'posting_type': '글쓰기',
        'posting_form': posting_form,
    }
    return render(request, 'page/posting_form.html', context)
    # [코드 작성] 로그인이 되어있지 않은 경우 로그인 페이지로 돌아가도록 처리
    

# [Read & Create] 작성글 보기 & 댓글 작성
def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.posting = posting
            # [코드 작성] comment_form의 author에 작성자 객체 추가

            comment_form.save()
            return redirect('page:posting_detail', posting_id)
    else :
        comment_form = CommentForm()
    
    comments = posting.comment_list.all()

    context = {
        'posting': posting,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'page/posting_detail.html', context)

# [Update] 작성글 수정
# [코드 작성] login_required 데코레이션 추가

def posting_update(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    # [코드 작성] 글(posting) 작성자(author)가 로그인한 사람(request.user)과 같을 경우에만 글 수정이 가능하도록 조건문 작성

    if request.method == 'POST':
        posting_form = PostingForm(request.POST, instance=posting)

        if posting_form.is_valid():
            posting_form.save()
            return redirect('page:posting_detail', posting_id)
    else:
        posting_form = PostingForm(instance=posting)

    context = {
        'posting_type': '글수정',
        'posting': posting,
        'posting_form': posting_form,
    }
    return render(request, 'page/posting_form.html', context)
    # [코드 작성] posting_id에 해당하는 페이지로 redirect


# [Delete] 작성글 삭제
# [코드 작성] login_required 데코레이션 추가

# [코드 작성] require_POST 데코레이션 추가

def posting_delete(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    # [코드 작성] 글(posting) 작성자(author)가 로그인한 사람(request.user)과 같을 경우에만 글 수정이 가능하도록 조건문 작성
    
    posting.delete()
    return redirect('page:posting_list')
    # [코드 작성] posting_id에 해당하는 페이지로 redirect
    

# [Delete] 댓글 삭제
# [코드 작성] login_required 데코레이션 추가

# [코드 작성] require_POST 데코레이션 추가

def comment_delete(request, posting_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # [코드 작성] 댓글(comment) 작성자(author)가 로그인한 사람(request.user)과 같을 경우에만 글 수정이 가능하도록 조건문 작성
    
    comment.delete()
    # [코드 작성] posting_id에 해당하는 페이지로 redirect
    
