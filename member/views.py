from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from member.models import Member


def join(request):
    returnPage = 'member/join.html'

    if request.method == 'GET':
        return render(request, returnPage)
    elif request.method == 'POST':
        # 폼으로 전송된 데이터들을 dict형태에 저장
        form = request.POST.dict()
        # print(form, form['userid']) # 전송된 데이터 확인

        # 유효성 검사 1/2, 3/4/5
        error = ''      # 검사 결과 저장용 변수
        if not (form['userid'] and form['passwd'] and form['repasswd']\
                and form['name'] and form['email']):
            error ='<li>입력값이 누락되었습니다!</li>'
        elif form['passwd'] != form['repasswd']:
            error = '<li>비밀번호가 일치하지 않습니다!</li>'
        else:   # 입력한 회원정보를 Member 객체에 담음
            member = Member(
                userid=form['userid'], passwd=make_password(form['passwd']), repasswd=form['repasswd']
                , name=form['name'], email=form['email']
            )
            # Member 객체에 담은 회원정보를 member테이블에 저장
            member.save()

            # 회원가입 성공 시 joinok.html을 띄움
            returnPage='member/joinok.html'
        # 유효성 검사를 실패하는 경우 오류내용을 join.html에 표시하기 위해 dict 변수에 저장
        # 또한, 이미 입력했던 회원정보를 다시join.html에 입력하기 위해 form이라는 dict변수 생성
        context = {'form':form, 'error':error}
        return render(request, returnPage, context)

def login(request):
    return render(request,'member/login.html')

def myinfo(request):
    return render(request,'member/myinfo.html')

