from django.shortcuts import render

def startView(request):
    template_file='mychat/start.html'
    
    options={
        
    }
    
    return render(request, template_file, options)


def createUser(request):
    template_file='mychat/createuser.html'
    
    options={
        
    }
    
    return render(request, template_file, options)