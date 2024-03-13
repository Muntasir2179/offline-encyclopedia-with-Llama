from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# importing custom classes and helper functions
import os
from dashboard.settings import BASE_DIR
from .text_processor import get_document_chunks
from .chromadb_operations import ChromadbOperations
from .llama_response import response


# creating object for performing vector operations
vector_operations = ChromadbOperations()

# Create your views here.

def login_function(request):
    if request.method == 'GET':
        # if authenticated user tries to access the login url again then redirect to home page
        if request.user.is_authenticated:
            return redirect('index')
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request=request, template_name='login.html', context=context)
    else:
        # if user send a POST request with credentials
        error_message = None
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                vector_operations.create_vector_storage()
                return redirect('index')
        else:
            username = request.POST.get('username')
            all_user = User.objects.all()
            error_message = "No user exit with this username"
            for single_user in all_user:
                if username == single_user.username:
                    error_message = "Password doesn't match"

            context = {
                "form": form,
                "error_message": error_message
            }
            return render(request=request, template_name='login.html', context=context)


def signup_function(request):
    if request.method == 'GET':
        # if authenticated user tries to access the signup url again then redirect to home page
        if request.user.is_authenticated:
            return redirect('index')
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request=request, template_name='signup.html', context=context)
    
    # if user send a POST request with credentials
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # forming error messages
        error_messages = check_user_credentials({
            'username': request.POST.get('username'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2')
        })
        context = {
                'form': form,
                'error_messages': error_messages
        }
        if len(error_messages.keys()) == 0:
            if form.is_valid():
                user = form.save()
                if user is not None:
                    return redirect('login')
        else:
            return render(request=request, template_name='signup.html', context=context)


def logout_function(request):
    # deleting vector stores before logged out
    vector_operations.delete_vector_storage()
    logout(request=request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    return render(request=request, template_name='home.html', context={'current_user': request.user})


@login_required(login_url='login')
def upload(request):
    if request.method == "GET":  # if user requests for upload page
        return render(request=request, template_name='upload.html', context={'current_user': request.user})
    else:
        # if user send a POST request with uploaded files
        os.makedirs(name=str(BASE_DIR / "uploads"), exist_ok=True)  # making 'uploads' directory if not exists
        uploaded_files = request.FILES.getlist('files')   # fetching the uploaded files
        # saving each file into the 'uploads' directory
        for uploaded_file in uploaded_files:
            with open(f'uploads/{uploaded_file.name}', 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            destination.close()
        
        # if some files are there in 'uploads' directory then insert them into vector database
        if len(os.listdir(path=BASE_DIR / "uploads")) != 0:
            text_chunks = get_document_chunks(path=BASE_DIR / "uploads")   # splitting documents into smaller chunks
            vector_operations.insert_data(texts_chunks=text_chunks)   # inserting into vector database

            # listing all the files in 'uploads' folder and deleting those uploaded files
            file_list = os.listdir(BASE_DIR / 'uploads')
            if len(file_list) != 0:
                for file_name in file_list:
                    os.remove(os.path.join(BASE_DIR / 'uploads', file_name))
        
        return render(request=request, template_name='chat.html', context={'current_user': request.user})


@login_required(login_url='login')
def chat(request):
    context = {
        'current_user': request.user
    }
    
    # if user has send a POST request with a query
    if request.method == 'POST':
        query_text = request.POST.get('query')  # fetching the query
        knowledge_base = vector_operations.query(query_text=query_text)  # performing vector search to find context or knowledge base for Llama
        query_response = response(context=knowledge_base, question=query_text)   # invoking the query and knowledge base into Llama
        context['query_response'] = query_response if query_response is not None else "No response"  # fetching the Llama response
        context['query_text'] = query_text
    return render(request=request, template_name='chat.html', context=context)


@login_required(login_url='login')
def chat_with_custom_knowledge(request):
    context = {
        'current_user': request.user
    }
    if request.method == "POST":
        query_text = request.POST.get('response_query')
        # performing vector search to find context or knowledge base for Llama
        custom_knowledge_base = vector_operations.query_on_custom_knowledge_base(query_text=query_text)
        query_response = response(context=custom_knowledge_base, question=query_text)  # invoking the query and custom knowledge base context into Llama
        context['query_response'] = query_response if query_response is not None else "No response" 
        context['query_text'] = query_text
    return render(request=request, template_name='chat.html', context=context)


# function for checking user credentials and generate valid error message
def check_user_credentials(user_info):
    username = user_info['username']
    password1 = user_info['password1']
    password2 = user_info['password2']

    all_user = User.objects.all()
    error_messages = {}
    for single_user in all_user:
        if username == single_user.username:
            error_messages['username_error_msg'] = "Username is taken"

    if password1 != password2:
        error_messages['password_error_msg'] = "Password doesn't match"
    else:
        if len(password1) < 8:
            error_messages['password_error_msg'] = "Minimum password length is 8"
    
    return error_messages