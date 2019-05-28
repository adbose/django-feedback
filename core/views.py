from django.shortcuts import render
from .models import Question

from django.views.generic import TemplateView
from .forms import UserRegistrationForm, FeedbackForm#, QuizForm

# # Create your views here.


class RegistrationPageView(TemplateView):
    def get(self, request):
        form = UserRegistrationForm()
        print("Empty User Registration Form...")
        print(form)

        return render(request, template_name='core/register.html', context={'form': form})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        print("#####")
        print("Registration form with data...")
        print(form)
        print("#####")
        if form.is_valid():
            print("form is valid")
            user = form.save()

            print("#####")
            print("User __str__")
            print(user)

            print("#####")
            print("Registration form Raw POST request ")
            print(request.POST)

            user_dict = dict(form.data)
            del user_dict['csrfmiddlewaretoken']
            # saving the user dictionary to the session
            request.session['user_dict'] = user_dict
            print("#####")
            print("User dictionary saved in session without csrfmiddlewaretoken...")
            print(user_dict)

        else:
            print("form is invalid")
        return render(request, template_name='core/registration_submitted.html', context={'user': user})



class FeedbackView(TemplateView):
    def get(self, request):
        # form = FeedbackForm()
        ques = Question.objects.all()
        # request.session['ques'] = ques
        print("#####")
        print("Raw printing all the questions from the database as a Queryset... (it's basically a list")
        print("#####")
        print(ques)
        print("Printing all the questions with options on the console")
        print("##########")
        for que in ques:
            print(que.id)
            print(que.question)
            print(que.optiona)
            print(que.optionb)
            print(que.optionc)
            print(que.optiond)
            print("##########")

        return render(request, template_name='core/feedback.html', context={'ques': ques})
        # return render(request, template_name='core/feedback.html', context={'form': form, 'ques': ques})

    def post(self, request):
        data = request.POST
        print("#####")
        print("Printing the raw feedback POST request as a Querydict...")
        print(data)

        # retrieving the questions from the session
        # ques = request.session['ques']

        print("#####")
        ques = Question.objects.all()
        print("Printing the questions retrieved from the database as a Queryset...")
        print(ques)

        # retrieving the user from the session
        user_dict = request.session['user_dict']
        data_dict = dict(data)
        del data_dict['csrfmiddlewaretoken']

        print("#####")
        print("Printing the response data as a dictionary without csrf middleware token")
        print(data_dict)
        print("#####")

        response = {}
        response["Full Name"] = user_dict["full_name"][0]
        response["Email"] = user_dict["email"][0]

        qna_dict = {}
        for key in data_dict.keys():
            if key != 'csrfmiddlewaretoken':
                qna_dict[str(ques[int(key)-1])] = data_dict[key][0]

        response["Feedback"] = [qna_dict]
        print(response)

        import json
        response_json = json.dumps(response)
        print("#####")
        print("Converting the response dictionary into JSON string...")
        print(response_json)
        # import ipdb;ipdb.set_trace()
        # if form.is_valid():
        #     response = form.save()
        #     print("form is valid")
        #     print(response)
        #
        # else:
        #     print("form is invalid")
        f = open("media/download/feedback_response.json", "w")
        f.write(response_json)
        f.close()
        return render(request, template_name='core/feedback_submitted.html', context={})


from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.conf import settings
import os

def download(request):
    response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('feedback_submitted.json')

    path = os.path.join(settings.MEDIA_ROOT, 'download/')
    response['X-Sendfile'] = smart_str(path)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


# from django.http import HttpResponse
# from django.conf import settings
# import os
#
# def download(request):
#     file_path = os.path.join(settings.BASE_DIR, 'media\\download\\feedback_submitted.json')
#     print(file_path)
#     json_data = open(file_path, "r").read()
#     return HttpResponse(json_data, content_type="application/json")


# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404
#
#
# def download(request, path='download/feedback_submitted.json'):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/json")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404