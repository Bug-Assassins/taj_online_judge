from include_module import *
from django.db import IntegrityError
from django.conf import settings
import zipfile
import random
import os
import traceback

# File Created By Ashish Kedia, ashish1294@gmail.com
# Created on 16th Jan, 2015
# Modified on 20th Jan, 2015

'''Experience is what you get when you didn't get what you wanted.
And experience is often the most valuable thing you have to offer.
- Randy Pausch, The Last Lecture'''

def problem_list(request) :

    return secure_render(request, 'problem_view.html', json_obj)
    
def problem_view(request, probid) :

    print "Problem View !!"

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
        json_obj['author'] = prob.author.name
        json_obj['allow_c'] = prob.allow_c
        json_obj['allow_java'] = prob.allow_java
        json_obj['time_limit_c'] = prob.c_time_limit
        json_obj['time_limit_java'] = prob.java_time_limit
        json_obj['memory_limit_c'] = prob.c_mem_limit
        json_obj['memory_limit_java'] = prob.java_mem_limit

        if request.session['id'] == prob.author_id or request.session['type'] == user.ADMIN :
            json_obj['allow_edit'] = True
        else :
            json_obj['allow_edit'] = False

        return secure_render(request, 'problem_view.html', json_obj)

    except ObjectDoesNotExist as e :
        traceback.print_exc()
        return HttpResponseRedirect("/problems/err/1")
    '''except Exception as e :
        traceback.print_exc()
        return HttpResponseRedirect("/error/3")'''

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

            print 'CHecking list = ', request.POST.getlist('langcheck[]')
            print "ANother Test = ", request.POST['langcheck[]']
            for x in request.POST.getlist('langcheck[]') :
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

            if problem.objects.filter(id = json_obj['id'])

            pr = problem(id = json_obj['id'], name = json_obj['name'], statement = json_obj['probstate'], \
                comment = json_obj['comment'], author_id = request.session['id'], is_judge = \
                json_obj['booljudge'], allow_c = json_obj['ccheck'], allow_java = json_obj['javacheck'], \
                c_time_limit = json_obj['ctimelim'], java_time_limit = json_obj['jtimelim'], c_mem_limit = \
                json_obj['cmemlim'], java_mem_limit = json_obj['jmemlim'])

            pr.save()

            print "final count = ", problem.objects.all().count()

            # Uploading Input File Here
            if json_obj['error'] == '' :
                input_file = request.FILES['taj_testcaseupload']
                output_file = request.FILES['taj_outputupload']

                temp1 = str(random.randint(1, 100000000))
                temp2 = str(random.randint(1, 100000000))

                ra = os.path.join(settings.TEMP_FILE_PATH, temp1 + input_file.name)
                rb = os.path.join(settings.TEMP_FILE_PATH, temp2 + output_file.name)

                temp_zip_input = open(ra, 'w')
                temp_zip_output = open(rb, 'w')

                for chunk in input_file.chunks() :
                    temp_zip_input.write(chunk)
                temp_zip_input.close()

                for chunk in output_file.chunks() :
                    temp_zip_output.write(chunk)
                temp_zip_output.close()

                zin = zipfile.ZipFile(ra, "r")
                zop = zipfile.ZipFile(rb, "r")

                # Checking File Format is correct. Each Input File should have corresponding output 
                inlist = sorted(zin.namelist())
                oplist = sorted(zop.namelist())

                if len(inlist) != len (oplist) :
                    raise InputOutputZipException('')
                for i, inf in enumerate(inlist) :
                    if inf != oplist[i] :
                        raise InputOutputZipException('')
                    inp = os.path.splitext(inf)
                    op = os.path.splitext(oplist[i])
                    if len(inp) < 2 or len(op) < 2:
                        raise InputOutputZipException('')
                    if inp[1] != '.txt' and inp[1] != '.in' :
                        raise InputOutputZipException('')
                    if op[1] != '.txt' and op[1] != '.out' :
                        raise InputOutputZipException('')

                # Deleting Old Contents. Creating Required Directory Structure
                par_dir = os.path.join(settings.TESTCASE_DIR, json_obj['id'])
                if not os.path.exists(par_dir):
                    os.makedirs(par_dir)
                os.system('rm -rf '+ par_dir + '/*')
                in_dir = os.path.join(par_dir, "input")
                op_dir = os.path.join(par_dir, "output")
                os.makedirs(in_dir)
                os.makedirs(op_dir)

                for inf in inlist :
                    zin.extract(inf, in_dir)
                    zop.extract(inf, op_dir)

                # Deleting the temporary files
                os.remove(ra)
                os.remove(rb)

                return HttpResponseRedirect('/success/1')

        except IntegrityError as ie :
            json_obj['error'] = "Problem Already Exist !!"
        except (zipfile.BadZipfile, zipfile.LargeZipFile) as e :
            json_obj['error'] = "Invalid Archive Selected !!"
        except InputOutputZipException as ioe :
            json_obj['error'] = "Improper Files in Input - Output Archive"
        except (ValueError, KeyError) as fe :
            # To catch Exceptions Like When Form Field is deleted and form is submitted
            json_obj['error'] = "Invalid Arguments Passed"
        except IOError :
            json_obj['error'] = "Unable to Store Test Cases. Contact Developer!!"
        except OSError as e :
            json_obj['error'] = "System Unavailable for Test Case Upload !!"
        #except :
         #   json_obj['error'] = "Unable to Add Problem at the moment !!"
          #  traceback.print_exc()
        finally :
            if json_obj['error'] != '' :
                p = problem.objects.filter(id = json_obj['id'])
                for pr in p :
                    pr.delete()

    else :
        json_obj['id'] = ''
        json_obj['name']  = ''
        json_obj['probstate'] = ''
        json_obj['error'] = ''
        json_obj['booljudge'] = True
        json_obj['ccheck'] = True
        json_obj['javacheck'] = True
        json_obj['cmemlim'] = settings.DEFAULT_C_MEM_LIMIT
        json_obj['ctimelim'] = settings.DEFAULT_C_TIME_LIMIT
        json_obj['jmemlim'] = settings.DEFAULT_JAVA_MEM_LIMIT
        json_obj['jtimelim'] = settings.DEFAULT_JAVA_TIME_LIMIT

    print "Final Error = " + json_obj['error']
    return secure_render(request, 'problem_add.html', json_obj)