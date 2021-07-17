from django.shortcuts import render

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from httpapitest.models import Project, DebugTalk, Module, TestCase, TestReports
from httpapitest.utils import case_logic
from httpapitest.utils import  get_time_stamp,timestamp_to_datetime
from httprunner.api import HttpRunner
from httpapitest.runner import run_test_by_type,run_by_single
from httpapitest.runner import run_by_batch
from httpapitest.tasks import main_hrun,test
from django.utils.safestring import mark_safe
import logging
import os,shutil
from django_celery_beat.models import PeriodicTask
from httpapitest.utils import task_logic, get_total_values
from httpapitest.models import UserInfo
from django.shortcuts import redirect

# Create your views here.
def index(request):
    project_length = Project.objects.count()
    module_length = Module.objects.count()
    test_length = TestCase.objects.count()
    

    total = get_total_values()
    manage_info = {
        'project_length': project_length,
        'module_length': module_length,
        'test_length': test_length,
        'total': total
    }

    
    return render(request, 'index.html', manage_info)


@csrf_exempt
def project_add(request):

    # 处理ajax提交的表单
    if request.is_ajax():
        project = json.loads(request.body.decode('utf-8'))
        if project.get('project_name') == '':
            msg = '项目名称不能为空'
            return HttpResponse(msg)
        if project.get('responsible_name') == '':
            msg = '负责人不能为空'
            return HttpResponse(msg)
        if project.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        if project.get('dev_user') == '':
            msg = '开发人员不能为空'
            return HttpResponse(msg)
        if project.get('publish_app') == '':
            msg = '发布应用不能为空'
            return HttpResponse(msg)
        if Project.objects.filter(project_name=project.get('project_name')):
            msg = "项目已经存在"
            return HttpResponse(msg)
        else:
            p = Project()
            p.project_name = project.get('project_name')
            p.responsible_name = project.get('responsible_name')
            p.test_user = project.get('test_user')
            p.dev_user = project.get('dev_user')
            p.publish_app = project.get('publish_app')
            p.simple_desc = project.get('simple_desc')
            p.other_desc = project.get('other_desc')
            p.save()
            d = DebugTalk()
            d.belong_project = p
            d.save()
            return HttpResponse(reverse('project_list'))
    # 显示项目添加页面
    if request.method == 'GET':
        return render(request, 'project_add.html')
    else:
        return HttpResponse("xxxxxxxxxxxxxx")

@csrf_exempt
def project_list(request):
    if request.method == 'GET':
        all_projects = Project.objects.all().order_by("-update_time")
        project_name = request.GET.get('project','All')
        info = {'belong_project': project_name}
        if project_name != 'All':
            rs = Project.objects.filter(project_name=project_name)
        else:
            rs = all_projects
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        projects = paginator.get_page(page)
        context_dict = {'projects': projects, 'all_projects': all_projects,'info': info}
        return render(request,"project_list.html",context_dict)

@csrf_exempt
def project_edit(request):
    if request.is_ajax():
        project = json.loads(request.body.decode('utf-8'))
        if project.get('project_name') == '':
            msg = '项目名称不能为空'
            return HttpResponse(msg)
        if project.get('responsible_name') == '':
            msg = '负责人不能为空'
            return HttpResponse(msg)
        if project.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        if project.get('dev_user') == '':
            msg = '开发人员不能为空'
            return HttpResponse(msg)
        if project.get('publish_app') == '':
            msg = '发布应用不能为空'
            return HttpResponse(msg)
        else:
            p = Project.objects.get(project_name=project.get('project_name'))
            p.responsible_name = project.get('responsible_name')
            p.test_user = project.get('test_user')
            p.dev_user = project.get('dev_user')
            p.publish_app = project.get('publish_app')
            p.simple_desc = project.get('simple_desc')
            p.other_desc = project.get('other_desc')
            p.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('project_list'))
        else:
            return HttpResponse(msg)

@csrf_exempt
def project_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        project_id = data.get('id')
        project = Project.objects.get(id=project_id)
        project.delete()
        return HttpResponse(reverse('project_list'))



@csrf_exempt
def debugtalk_edit(request, id):
    if request.method == "GET":
        d = DebugTalk.objects.get(pk=id)
        context_dict = {'debugtalk': d.debugtalk, 'id': d.id }
        return render(request, "debugtalk_edit.html",context_dict)

    if request.is_ajax():
        d = DebugTalk.objects.get(pk=id)
        content = json.loads(request.body.decode('utf-8'))
        d.debugtalk = content["debugtalk"]
        d.save()
        return HttpResponse("debugtalk edit success")


@csrf_exempt
def module_add(request):
    if request.method == 'GET':
        projects = Project.objects.all().order_by("-update_time")
        context_dict = {'projects': projects}
        return render(request, 'module_add.html',context_dict)
    if request.is_ajax():
        module = json.loads(request.body.decode('utf-8'))
        if module.get('module_name') == '':
            msg = '模块名称不能为空'
            return HttpResponse(msg)
        if module.get('belong_project') == '请选择':
            msg = '请选择项目，没有请先添加哦'
            return HttpResponse(msg)
        if module.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        p = Project.objects.get(project_name=module.get('belong_project'))
        if Module.objects.filter(module_name=module.get('module_name'), belong_project=p):
            msg = "模块已经存在"
            return HttpResponse(msg)
        else:
            m = Module()
            m.module_name = module.get('module_name')
            p = Project.objects.get(project_name=module.get('belong_project'))
            m.belong_project = p
            m.test_user = module.get('test_user')
            m.simple_desc = module.get('simple_desc')
            m.other_desc = module.get('other_desc')
            m.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('module_list'))
          
        else:
            return HttpResponse(msg)

@csrf_exempt
def module_list(request):
    if request.method == 'GET':
        module = request.GET.get("module", "")
        if module:
            rs = Module.objects.filter(module_name__contains=module).order_by("-update_time")
        else:
            rs = Module.objects.all().order_by("-update_time")
        info = {'module': module}
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'modules': objects,'info': info }
        return render(request,"module_list.html",context_dict)

@csrf_exempt
def module_edit(request):
    if request.is_ajax():
        module = json.loads(request.body.decode('utf-8'))
        
        if module.get('module_name') == '':
            msg = '模块名称不能为空'
            return HttpResponse(msg)
        if module.get('belong_project') == '请选择':
            msg = '请选择项目，没有请先添加哦'
            return HttpResponse(msg)
        if module.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        p = Project.objects.get(project_name=module.get('belong_project'))
        if module.get('module_name') != Module.objects.get(id=module.get('index')).module_name and \
            Module.objects.filter(module_name=module.get('module_name'), belong_project=p).count()>0:
            msg = "模块已经存在"
            return HttpResponse(msg)
        else:
            m = Module.objects.get(id=module.get('index'))
            m.module_name = module.get('module_name')
            m.belong_project = p
            m.test_user = module.get('test_user')
            m.simple_desc = module.get('simple_desc')
            m.other_desc = module.get('other_desc')
            m.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('module_list'))
        else:
            return HttpResponse(msg)
    

@csrf_exempt
def module_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        project_id = data.get('id')
        module = Module.objects.get(id=project_id)
        module.delete()
        return HttpResponse(reverse('module_list'))

@csrf_exempt
def case_add(request):
    if request.method == 'GET':
        context_dict = {
            'projects': Project.objects.all().values('project_name').order_by('-create_time')
        }
        return render(request, 'case_add.html', context_dict)
    if request.is_ajax():
        testcase = json.loads(request.body.decode('utf-8'))
        msg = case_logic(**testcase)
        if msg == 'ok':
            return HttpResponse(reverse('case_list'))
        else:
            return HttpResponse(msg)

@csrf_exempt
def module_search_ajax(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        if 'test' in data.keys():
            project = data["test"]["name"]["project"]
        if 'config' in data.keys():
            project = data["config"]["name"]["project"]
        if 'case' in data.keys():
            project = data["case"]["name"]["project"]
        if 'upload' in data.keys():
            project = data["upload"]["name"]["project"]
        if 'crontab' in data.keys():
            project = data["crontab"]["name"]["project"]
        if  project != "All" and project != "请选择":
            p = Project.objects.get(project_name=project)
            modules = Module.objects.filter(belong_project=p)
            modules_list = ['%d^=%s' % (m.id, m.module_name) for m in modules ]
            modules_string = 'replaceFlag'.join(modules_list)
            return HttpResponse(modules_string)
        else:
            return HttpResponse('')

@csrf_exempt
def case_search_ajax(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        if 'case' in data.keys():
            project = data["case"]["name"]["project"]
            module = data["case"]["name"]["module"]
        if   project != "请选择" and module != "请选择":
            m = Module.objects.get(id=module)
            cases = TestCase.objects.filter(belong_project=project, belong_module=m)
            case_list = ['%d^=%s' % (c.id, c.name) for c in cases ]
            case_string = 'replaceFlag'.join(case_list)
            return HttpResponse(case_string)
        else:
            return HttpResponse('')

@csrf_exempt
def case_list(request):
    if request.method == 'GET':
        case = request.GET.get('name','')
        if case:
            rs = TestCase.objects.filter(name__contains=case).order_by("-update_time")
        else:
            rs = TestCase.objects.all().order_by("-update_time")
        info = {'case':case}        
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'case': objects, 'info':info,}
        return render(request,"case_list.html",context_dict)


@csrf_exempt
def case_edit(request, id):
    if request.method == 'GET':
        case = TestCase.objects.get(id=id)
        case_request = eval(case.request)
        case_include = eval(case.include)
        context_dict = {
            'project': Project.objects.all().values('project_name').order_by('-create_time'),
            'info': case,
            'request': case_request['test'],
            'include': case_include
        }
        return render(request, 'case_edit.html', context_dict)

    if request.is_ajax():
        case_list = json.loads(request.body.decode('utf-8'))
        msg = case_logic(type=False, **case_list)
        if msg == 'ok':
            return HttpResponse(reverse('case_list'))
        else:
            return HttpResponse(msg)

@csrf_exempt
def case_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        case_id = data.get('id')
        case = TestCase.objects.get(id=case_id)
        case.delete()
        return HttpResponse(reverse('case_list'))

@csrf_exempt
def case_copy(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        config_id = data['data']['index']
        name = data['data']['name']
        case = TestCase.objects.get(id=config_id)
        belong_module = case.belong_module
        if TestCase.objects.filter(name=name, belong_module=belong_module).count() > 0:
            return HttpResponse("用例名称重复")
        else:
            case.name = name
            case.id = None
            case.save()
            return HttpResponse(reverse('case_list'))


@csrf_exempt
def test_run(request):
    """
    运行用例
    :param request:
    :return:
    """

    runner = HttpRunner(failfast=False)

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        id = kwargs.pop('id')
        type = kwargs.pop('type')
        run_test_by_type(id, testcase_dir_path, type)
        report_name = kwargs.get('report_name', None)
        main_hrun.delay(testcase_dir_path, report_name)
        return HttpResponse('用例执行中，请稍后查看报告即可,默认时间戳命名报告')
    else:
        id = request.POST.get('id')
        type = request.POST.get('type', 'test')

        run_test_by_type(id, testcase_dir_path, type)
        
        runner.run(testcase_dir_path)
        #shutil.rmtree(testcase_dir_path)
        summary = timestamp_to_datetime(runner._summary, type=False)
        #print(summary)

        return render(request,'report_template.html', summary)


@csrf_exempt
def test_batch_run(request):
    """
    批量运行用例
    :param request:
    :return:
    """

    runner = HttpRunner(failfast=False)

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        test_list = kwargs.pop('id')
        print(test_list)
        type = kwargs.pop('type')
        report_name = kwargs.get('report_name', None)
        run_by_batch(test_list, testcase_dir_path, type=type)
        main_hrun.delay(testcase_dir_path, report_name)
        return HttpResponse('用例执行中，请稍后查看报告即可,默认时间戳命名报告')
    else:
        type = request.POST.get('type', None)
        test_list = request.body.decode('utf-8').split('&')
        run_by_batch(test_list, testcase_dir_path, type=type)

        runner.run(testcase_dir_path)

        #shutil.rmtree(testcase_dir_path)
        summary = timestamp_to_datetime(runner.summary, type=False)
        print(summary)
        return render(request,'report_template.html', summary)

def report_list(request):
    if request.method == "GET":
        rs = TestReports.objects.all().order_by("-update_time")
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'report': objects }
        return render(request,"report_list.html",context_dict)

@csrf_exempt
def report_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        report_id = data.get('id')
        report = TestReports.objects.get(id=report_id)
        report.delete()
        return HttpResponse(reverse('report_list'))

def report_view(request, id):
    """
    查看报告
    :param request:
    :param id: str or int：报告名称索引
    :return:
    """
    reports = TestReports.objects.get(id=id).reports
    return render(request, 'report_view.html', {"reports": mark_safe(reports)})

@csrf_exempt
def task_add(request):
    """
    添加任务
    :param request:
    :return:
    """

    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        msg = task_logic(**kwargs)
        if msg == 'ok':
            return HttpResponse(reverse('task_list'))
        else:
            return HttpResponse(msg)
    elif request.method == 'GET':
        info = {
            'project': Project.objects.all().order_by('-create_time')
        }
        return render(request, 'task_add.html', info)

def task_list(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        info = {'name': name}
        if name:
            rs = PeriodicTask.objects.filter(name=name).order_by('-date_changed')
        else:
            rs = PeriodicTask.objects.all().order_by('-date_changed')
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'task': objects, 'info': info}
        return render(request,"task_list.html",context_dict)


@csrf_exempt
def task_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        task_id = data.get('id')
        task = PeriodicTask.objects.get(id=task_id)
        task.delete()
        return HttpResponse(reverse('task_list'))

@csrf_exempt
def task_set(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        task_id = data.get('id')
        mode = data.get('mode')
        task = PeriodicTask.objects.get(id=task_id)
        task.enabled = mode
        task.save()
        return HttpResponse(reverse('task_list'))



def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            logging.info('{username} 登录成功'.format(username=username))
            request.session["login_status"] = True
            request.session["now_account"] = username
            return redirect('index')
        else:
            logging.info('{username} 登录失败, 请检查用户名或者密码'.format(username=username))
            return render(request, 'login.html', {'msg': '账号或密码不正确'})
    elif request.method == 'GET':
        return render(request, 'login.html')

@csrf_exempt
def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.decode('utf-8'))
        try:
            username = user_info.get('account')
            password = user_info.get('password')
            email = user_info.get('email')
    
            if UserInfo.objects.filter(username__exact=username).filter(status=1).count() > 0:
                logging.debug('{username} 已被其他用户注册'.format(username=username))
                msg = '该用户名已被注册，请更换用户名'
            if UserInfo.objects.filter(email__exact=email).filter(status=1).count() > 0:
                logging.debug('{email} 昵称已被其他用户注册'.format(email=email))
                msg = '邮箱已被其他用户注册，请更换邮箱'
            else:
                UserInfo.objects.create(username=username, password=password, email=email)
                logging.info('新增用户：{user_info}'.format(user_info=user_info))
                msg =  'ok'
        except Exception as e:
            logging.error('信息输入有误：{user_info}'.format(user_info=user_info))
            msg =  e
        if msg == 'ok':
            return HttpResponse('恭喜您，账号已成功注册')
        else:
            return HttpResponse(msg)
    elif request.method == 'GET':
        return render(request, "register.html")


def logout(request):
    """
    注销登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        logging.info('{username}退出'.format(username=request.session['now_account']))
        del request.session['now_account']
        del request.session['login_status']
        return redirect(login)