from django.db.models import F
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from board.models import Board
from member.models import Member

# Create your views here.
# 게시판 목록보기 처리


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def board(request):
    # bdlist = Board.objects.values('id','title','userid','regdate','views')\
    #     .order_by('-id')

    # Board와 Member 테이블은 userid <-> id칼럼 기준으로 inner join 수행
    bdlist = Board.objects.select_related('member')

    # join된 member 테이블의 userid 확인
    # bdlist.get(0).member.userid

    context ={'bds': bdlist}

    return render(request, 'board/board.html',context)


# 게시판 본문보기 처리
def view(request):
    if request.method == 'GET':
        form =request.GET.dict()
        # print(form['bno'])

        # 본문글에 대한 조회수 증가
        # update board set views = views + 1
        # where id = ???
        # b=Board.objects.get(id=form['bno'])
        # b.views = b.views + 1
        # b.save()
        Board.objects.filter(id=form['bno']).update(views=F('views')+1)


        # select * from board inner join member
        # using(id) where id = ???
        bd = Board.objects.select_related('member')\
            .get(id=form['bno'])

    elif request.method == 'POST':
        pass

    context={'bd':bd}
    return render(request,'board/view.html', context)

# 게시판 글쓰기 처리
# get: board/write.html
# post: 작성한 글을 db에 저장, 'board/list.html'로 이동
def write(request):
    returnPage = 'board/write.html'
    form=''
    error=''

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        form = request.POST.dict()

        # 유효성 검사1
        if not (form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요!'
        else:
            # 입력한 게시글을 Board 객체에 담음
            # bd =board/ board=Board(나는 오른쪽)
            board = Board(title=form['title'],
                          contents=form['contents'],
                          # 새 글을 작성한 회원에 대한 정보는
                          # 회원 테이블에 존재하는 회원 번호(id)를 조회해서
                          # userid 속성에 저장
                          member=Member.objects.get(pk=form['memberid'])
                          )
            board.save()    # Board 객체에 담은 게시글을 테이블에 저장

            returnPage='board/board.html'

    context = {'form': form, 'error': error}
    return render(request, returnPage, context)

# 본문글 삭제하기
def remove(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # delete from board where bno = ??
        Board.objects.filter(id=form['bno']).delete();
    return redirect('/board')

# 본문글 수정하기
def modify(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # select * from board where bno = ???
        bd = Board.objects.get(id=form['bno'])

    elif request.method == 'POST':
        form = request.POST.dict()

        # update board set title = ???, contents = ???
        # where bno = ???
        # b = Board.objects.get(id=form['bno'])
        # b.title = form['title']
        # b.contents = form['contents']
        # b.save()

        Board.objects.filter(id=form['bno'])\
            .update(title=form['title'], contents=form['contents'])

        return redirect('/view?bno=' + form['bno'])
    context = {'bd': bd}
    return render(request, 'board/modify.html', context)