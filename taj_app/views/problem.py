from include_module import *
from settings import SUBMISSION_DIR, TEMP_FILE_PATH
import zipfile

# File Created By Ashish Kedia, ashish1294@gmail.com
# Created on 16th Jan, 2015
# Modified on 16th Jan, 2015

'''Experience is what you get when you didn't get what you wanted.
And experience is often the most valuable thing you have to offer.
- Randy Pausch, The Last Lecture'''

def problem_list(request) :

    return secure_render(request, 'problem_view.html', json_obj)
    
def problem_view(request, probid) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    json_obj = {}

    try :
        prob = problem.objects.get(id = probid)
        json_obj['name'] = prob.name
        json_obj['comment'] = prob.comment
        json_obj['statement'] = prob.statement
        json_obj['time_added'] = prob.added_at
        json_obj['is_judge'] = prob.is_judge
        json_obj['author'] = prob.author
        json_obj['allow_c'] = prob.allow_c
        json_obj['allow_java'] = prob.allow_java
        json_obj['time_limit_c'] = prob.c_time_limit
        json_obj['time_limit_java'] = prob.java_time_limit
        json_obj['memory_limit_c'] = prob.c_mem_limit
        json_obj['memory_limit_java'] = probjava_mem_limit
        return secure_render(request, 'problem_view.html', json_obj)
    except ObjectDoesNotExist as e :
        return HttpResponseRedirect("/problems/err/1")
    except Exception as e :
        return HttpResponseRedirect("/error/1")

'''def check_add_prob_form(request) :

    if 'probid' not in request.POST :
        return False, 'Please Enter Problem ID'
    else :


     and 'probname' in r and 'probstate' in request.POST \
    and 'comment' in request.POST and 'booljudge' in request.POST and 'langcheck' in request.POST \
    and 'cmemlim' in request.POST
'''

class InputOutputZipException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def problem_add(request) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    if request.session['type'] == user.STUDENT :
        return HttpResponseRedirect("/error/1")

    json_obj = {'error' : ''}

    if 'taj_add_prob_submit' in request.POST :
        try :
            json_obj['id'] = str(request.POST['probid']).strip()
            if json_obj['id'] == '' and json_obj['error'] == '' :
                json_obj['error'] = 'Please Enter a Problem ID'

            json_obj['name'] = str(request.POST['probname']).strip()
            if json_obj['name'] == '' and json_obj['error'] == '' :
                json_obj['error'] = 'Please Enter a Problem Name'

            json_obj['probstate'] = str(request.POST['probstate']).strip()
            if json_obj['probstate'] == '' and json_obj['error'] == '' :
                json_obj['error'] = 'Please ENter a Problem Statement'

            json_obj['comment'] = str(request.POST['comment']).strip()
            json_obj['booljudge'] = bool(int(request.POST['booljudge']))

            json_obj['ccheck'] = False
            json_obj['javacheck'] = False

            for x in request.POST['langcheck'] :
                if x == 'C' :
                    json_obj['ccheck'] = True
                elif x == 'Java' :
                    json_obj['javacheck'] = True
                else :
                    raise Exception('')

            json_obj['cmemlim'] = int(request.POST['cmemlim'])
            json_obj['ctimelim'] = int(request.POST['ctimelim'])
            json_obj['jmemlim'] = int(request.POST['jmemlim'])
            json_obj['jtimelim'] = int(request.POST['jtimelim'])

            # Uploading Input File Here
            input_file = request.FILES['taj_testcaseupload']
            output_file = request.FILES['taj_outputupload']

            temp_zip_input = open(TEMP_FILE_PATH + input_file.name)
            temp_zip_output = open(TEMP_FILE_PATH + output_file.name)

            for chunk in input_file.chunks() :
                temp_zip_input.write(chunk)
            temp_zip_input.close()

            for chunk in output_file.chunks() :
                temp_zip_output.write(chunk)
            temp_zip_output.close()

            zin = zipfile.ZipFile(TEMP_FILE_PATH + input_file.name)
            zop = zipfile.ZipFile(TEMP_FILE_PATH + output_file.name)

            # Checking File Format is correct. Each Input File should have corresponding output 
            inlist = sort(zin.namelist())
            oplist = sort(zop.namelist())

            if len(inlist) != len (oplist) :
                raise InputOutputZipException('')
            for i, inf in enumerate(inlist) :
                if inf != oplist[i] :
                    raise InputOutputZipException('')

            
        except zipfile.BadZipfile, zipfile.LargeZipFile as e :
            json_obj['error'] = "Invalid Archive Selected !!"
        except InputOutputZipException as ioe :
            json_obj['error'] = "Improper Files in Input - Output Archive"
        except ValueError, KeyError as fe :
            # To catch Exceptions Like When Form Field is deleted and form is submitted
            json_obj['error'] = "Invalid Arguments Passed"
        except Exception as e:



    else :
        json_obj['id'] = ''
        json_obj['name']  = ''
        json_obj['statement'] = ''
        json_obj['error'] = ''
        json_obj['is_judge'] = True
        json_obj['ccheck'] = True
        json_obj['javacheck'] = True
        json_obj['cmemlim'] = ''
        json_obj['ctimelim'] = ''
        json_obj['jmemlim'] = ''
        json_obj['jtimelim'] = ''

    return secure_render(request, 'problem_add.html', json_obj)