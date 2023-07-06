from django.forms import *
from .models import *

from froala_editor.widgets import FroalaEditor



class BlogForm(ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content'] 
        
        
        
class Blog_comment(ModelForm):

    class Meta:
        model = BlogComment
        fields = ['comment']