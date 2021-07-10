from django.shortcuts import render

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from httpapitest.models import Project, DebugTalk, Module, TestCase
from httpapitest.utils import case_logic


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
        if 'case' in data.keys():
            project = data["case"]["name"]["project"]
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



