# accounts/context_processors.py (新規作成)
from .forms import CustomLoginForm

def login_form_context(request):
    return {
        'login_form': CustomLoginForm()
    }