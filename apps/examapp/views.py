from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import User, UserManager, Thought, ThoughtManager
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):

    return render(request, 'examapp/index.html')

def register(request):
    print('in register')
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print('***Number of Errors',len(errors))
        return redirect('/')
    password = request.POST['pw']
    pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    current_user = User.objects.create(first_name = request.POST['fn'], last_name = request.POST['ln'], email= request.POST['email'], password = pwhash)
    request.session['current_user_id'] = current_user.id

    return redirect('/thoughts')

def login(request):
    print('in login')
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:

        current_user = User.objects.filter(email = request.POST['email_log'])
        request.session['current_user_id'] = current_user[0].id

        return redirect('/thoughts')



def dashboard(request):
    # Security measures
    if 'current_user_id' not in request.session: 
        return redirect('/')
    current_user = User.objects.get(id = request.session['current_user_id'])
    
    Thought.objects.annotate(like_count=Count('users_who_like')).order_by('-like_count')
    context = {
        'all_thoughts': Thought.objects.annotate(like_count=Count('users_who_like')).order_by('-like_count').all(),
        'current_user': User.objects.get(id = request.session['current_user_id']),
        # 'uploaded_wishes': Wish.objects.filter(uploaded_by = current_user).filter(granted = False),
        # 'granted_wishes': Wish.objects.filter(granted = True),
    
    }
    Thought.objects.annotate(like_count=Count('users_who_like')).order_by('-like_count')
    print('in wishes')
 
    print(User.objects.filter(id = request.session['current_user_id'])[0].first_name)




    return render(request, 'examapp/dashboard.html', context)

def new(request):
    context = {
        'current_user': User.objects.get(id = request.session['current_user_id'])
    }

    return render(request, 'examapp/newwish.html', context)

def createwish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('wishes/new')
    current_user = User.objects.get(id = request.session['current_user_id'])
    Wish.objects.create(item = request.POST['item'], desc = request.POST['desc'], uploaded_by = current_user, location = request.POST['loc'])
    
    return redirect('/thoughts')

def newthought(request):
    errors = Thought.objects.thought_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/thoughts')
    current_user = User.objects.get(id = request.session['current_user_id'])
    Thought.objects.create(desc = request.POST['desc'], uploaded_by = current_user)

    return redirect('/thoughts')

def removewish(request, wishid):
    Wish.objects.get(id = wishid).delete()
    
    return redirect('/thoughts')

def grant_wish(request, wishid):
    current_wish = Wish.objects.get(id = wishid)
    current_wish.granted = True
    current_wish.save()
    return redirect('/thoughts')

def edit_wish(request, wishid):
    context = {
        'current_user': User.objects.get(id = request.session['current_user_id']),
        'current_wish': Wish.objects.get(id = wishid),

    }

    
    return render(request, 'examapp/editwish.html', context)

def completeedit(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'wishes/edit/{request.POST["wishid"]}')
    print(request.POST)
    wish = Wish.objects.get(id = request.POST['wishid'])
    wish.item = request.POST['item']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect('/thoughts')

def logout(request):
    request.session.clear()
    return redirect('/')

def stats(request):
    context = {
        'current_user': User.objects.get(id = request.session['current_user_id']),
        'all_wishes': Wish.objects.filter(granted = True),
        'your_granted_wishes': Wish.objects.filter(granted = True).filter(uploaded_by = request.session['current_user_id']),
        'your_pending_wishes': Wish.objects.filter(granted = False).filter(uploaded_by = request.session['current_user_id']),
    }

    return render(request, 'examapp/stats.html', context)

def like(request, thoughtid):
    current_thought = Thought.objects.get(id = thoughtid)
    current_user = User.objects.get(id = request.session['current_user_id'])
    current_thought.users_who_like.add(current_user)
    return redirect(f'/thoughts/{thoughtid}')

def unlike(request, thoughtid):
    current_thought = Thought.objects.get(id = thoughtid)
    current_user = User.objects.get(id = request.session['current_user_id'])
    current_thought.users_who_like.remove(current_user)
    return redirect(f'/thoughts/{thoughtid}')

def details(request, thoughtid):
    #Security measures
    if 'current_user_id' not in request.session: 
        return redirect('/')
    current_thought = Thought.objects.get(id = thoughtid)
    context = {
        'current_thought' : Thought.objects.get(id = thoughtid),
        'current_user': User.objects.get(id = request.session['current_user_id']),
        'liked_by': current_thought.users_who_like.all(),
    }

    return render(request, 'examapp/thoughts.html', context)

def delete(request, thoughtid):
    current_thought = Thought.objects.get(id = thoughtid)
    current_thought.delete()

    return redirect('/thoughts')