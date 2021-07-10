## 用例运行
执行测试用例

1. 安装httprunner
`pip install HttpRunner==2.2.2`

2. 添加视图函数test_run
```python
@csrf_exempt
def test_run(request):
    """
    运行用例
    :param request:
    :return:
    """

    runner = HttpRunner(failfase=False)

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

```

3. views.py 导入函数
```
from httpapitest.utils import  get_time_stamp,timestamp_to_datetime
from httprunner.api import HttpRunner
from httpapitest.runner import run_test_by_type,run_by_single
import logging
import os,shutil
```
4. 创建要导入的函数
在utils.py 文件中添加dump_yaml_file，dump_python_file，get_time_stamp，timestamp_to_datetime
并导入
`import time,io,yaml,datetime`

```python
def dump_yaml_file(yaml_file, data):
    """ load yaml file and check file content format
    """
    with io.open(yaml_file, 'w', encoding='utf-8') as stream:
        yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8')


def dump_python_file(python_file, data):
    with io.open(python_file, 'w', encoding='utf-8') as stream:
        stream.write(data)

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp


def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime.datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary
```



在httpapitest添加runner.py文件
用例使用的是run_test_by_type,run_by_single，其它函数在批量运行时使用
```python
import os

from django.core.exceptions import ObjectDoesNotExist

from httpapitest.models import TestCase, Module, Project, DebugTalk
from httpapitest.utils import dump_python_file, dump_yaml_file


def run_by_single(index, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :return: dict
    """
    config = {
        'config': {
            'name': '',
            'base_url': '',
        }
    }
    testcase_list = []

    testcase_list.append(config)

    try:
        obj = TestCase.objects.get(id=index)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    request = eval(obj.request)
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_name

    config['config']['name'] = name

    
    testcase_dir_path = path
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        try:
            debugtalk = DebugTalk.objects.get(belong_project__project_name=project).debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)
    testcase_dir_path = os.path.join(path, project)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    testcase_dir_path = os.path.join(testcase_dir_path, module)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    for test_info in include:
        try:
            id = test_info[0]
            pre_request = eval(TestCase.objects.get(id=id).request)
            testcase_list.append(pre_request)

        except ObjectDoesNotExist:
            return testcase_list

    if request['test']['request']['url'] != '':
        testcase_list.append(request)

    dump_yaml_file(os.path.join(testcase_dir_path, name) +'.yml', testcase_list)



def run_by_batch(test_list, path, type=None):
    if type:
        for index in range(len(test_list) - 1):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, path)
            elif type == 'module':
                run_by_module(value, path)
    else:
        for index in range(len(test_list)):
            form_test = test_list[index].split('=')
            index = form_test[1]
            run_by_single(index, path)


def run_by_module(id, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :return: list
    """
    obj = Module.objects.get(id=id)
    test_index_list = TestCase.objects.filter(belong_module=obj).values_list('id')
    for index in test_index_list:
        run_by_single(index[0], path)


def run_by_project(id,  path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :return: list
    """
    obj = Project.objects.get(id=id)
    module_index_list = Module.objects.filter(belong_project=obj).values_list('id')
    for index in module_index_list:
        module_id = index[0]
        run_by_module(module_id, path)


def run_test_by_type(id, path, type):
    if type == 'project':
        run_by_project(id, path)
    elif type == 'module':
        run_by_module(id, path)
    else:
        run_by_single(id, path)

```

4. 添加运行结果模板文件
创建文件report_template.html
```html
<!DOCTYPE html>
<html>


<head>
    <meta charset='utf-8'/>
    <meta name='description' content=''/>
    <meta name='robots' content='noodp, noydir'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'/>
    <meta id="timeStampFormat" name="timeStampFormat" content='MMM d, yyyy hh:mm:ss a'/>

    <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600' rel='stylesheet' type='text/css'>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <link href='http://extentreports.com/resx/dist/css/extent.css' type='text/css' rel='stylesheet'/>

    <title>{{ html_report_name }} - TestReport</title>

    <style type='text/css'>
        .node.level-1 ul {
            display: none;
        }

        .node.level-1.active ul {
            display: block;
        }

        .card-panel.environment th:first-child {
            width: 30%;
        }
    </style>
</head>

<body class='extent standard default hide-overflow dark'>
<div id='theme-selector' alt='切换主题，默认黑色' title='切换主题'>
    <span><i class='material-icons'>desktop_windows</i></span>
</div>

<nav>
    <div class="nav-wrapper">
        <a href="#!" class="brand-logo blue darken-3">Extent</a>

        <!-- slideout menu -->
        <ul id='slide-out' class='side-nav fixed hide-on-med-and-down'>
            <li class='waves-effect active'><a href='#!' view='test-view'
                                               onclick="configureView(0);chartsView('test');"><i class='material-icons'>dashboard</i></a>
            </li>
            <li class='waves-effect'><a href='#!' view='category-view' onclick="configureView(1)"><i
                    class='material-icons'>label_outline</i></a></li>
            <li class='waves-effect'><a href='#!' onclick="configureView(-1);chartsView('dashboard');"
                                        view='dashboard-view'><i class='material-icons'>track_changes</i></a></li>
        </ul>

        <!-- report name -->
        <span class='report-name'>Test Report: {{ html_report_name }}</span>

        <!-- report headline -->
        <span class='report-headline'></span>

        <!-- nav-right -->
        <ul id='nav-mobile' class='right hide-on-med-and-down nav-right'>
            <li>
                <a href='#!'>
                    <span class='label suite-start-time blue darken-3'>{{ time.start_datetime }}</span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>HttpRunner {{ platform.httprunner_version }} </span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>{{ platform.python_version }} </span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>{{ platform.platform }}</span>
                </a>
            </li>
        </ul>
    </div>
</nav>

<!-- container -->
<div class='container'>

    <div id='test-view' class='view'>

        <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- test toggle -->
                <div class='chip transparent'>
                    <a class='dropdown-button tests-toggle' data-activates='tests-toggle' data-constrainwidth='true'
                       data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>warning</i> Status
                    </a>
                    <ul id='tests-toggle' class='dropdown-content'>
                        <li status='pass'><a href='#!'>Pass <i class='material-icons green-text'>check_circle</i></a>
                        </li>
                        <li status='fail'><a href='#!'>Fail <i class='material-icons red-text'>cancel</i></a></li>
                        <li status="skip"><a href="#!">Skip <i class="material-icons cyan-text">redo</i></a></li>
                        <li class='divider'></li>
                        <li status='clear' clear='true'><a href='#!'>Clear Filters <i
                                class='material-icons'>clear</i></a></li>
                    </ul>
                </div>
                <!-- test toggle -->

                <!-- category toggle -->
                <div class='chip transparent'>
                    <a class='dropdown-button category-toggle' data-activates='category-toggle'
                       data-constrainwidth='false' data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>local_offer</i> Category
                    </a>
                    <ul id='category-toggle' class='dropdown-content'>
                        {% for test_suite_summary in details %}
                            <li><a href='#'>{{ test_suite_summary.name }}</a>
                            </li>
                        {% endfor %}


                        <li class='divider'></li>
                        <li class='clear'><a href='#!' clear='true'>Clear Filters</a></li>
                    </ul>
                </div>
                <!-- category toggle -->

                <!-- clear filters -->
                <div class='chip transparent hide'>
                    <a class='' id='clear-filters' alt='Clear Filters' title='Clear Filters'>
                        <i class='material-icons'>close</i> Clear
                    </a>
                </div>
                <!-- clear filters -->

                <!-- enable dashboard -->
                <div id='toggle-test-view-charts' class='chip transparent'>
                    <a class='pink-text' id='enable-dashboard' alt='Enable Dashboard' title='Enable Dashboard'>
                        <i class='material-icons'>track_changes</i> Dashboard
                    </a>
                </div>
                <!-- enable dashboard -->

                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input style="color: red" id='search-tests' type='text' class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>


        <div id='test-view-charts' class='subview-full'>

            <div id='test-view-charts' class='subview-full'>
                <div id='charts-row' class='row nm-v nm-h'>
                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Tests</div>
                            <div class='chart-box'>
                                <canvas id='parent-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                            <span class='tooltipped' data-position='top'><span
                                    class='strong'>{{ stat.teststeps.successes }}</span> test(s) passed</span>
                                <span class='tooltipped' data-position='top'><span
                                        class='strong'>{{ stat.teststeps.failures }}</span> test(s) failed</span>
                            </div>
                            <div class='block text-small'>
                            <span class='strong tooltipped' data-position='top'
                            >{{ stat.teststeps.errors }}</span>
                                test(s) errored
                                <span class='strong tooltipped' data-position='top'
                                >{{ stat.teststeps.skipped }}</span>
                                test(s) skipped
                            </div>
                        </div>
                    </div>

                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Suites</div>
                            <div class='chart-box'>
                                <canvas id='child-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                            <span id="pass_suites" class='tooltipped' data-position='top'>
                            </span>
                            </div>
                            <div class='block text-small'>
                                <span id="fail_suites" class='strong tooltipped' data-position='top'></span> suite(s)
                                failed
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Suites</h5>
                <ul id='test-collection' class='test-collection'>

                    {% for test_suite_summary in details %}
                        {% if test_suite_summary.success == True %}
                            <li class='test displayed active has-leaf pass' status='pass' bdd='true'
                                test-id='{{ test_suite_summary.name }}_{{ forloop.counter }}'>
                                {% else %}
                            <li class='test displayed active has-leaf fail' status='fail' bdd='false'
                                test-id='{{ test_suite_summary.name }}_{{ forloop.counter }}'>
                        {% endif %}
                        <div class='test-heading'>
                            <span class='test-name'>{{ test_suite_summary.name }}</span>
                            <span class='test-time'>baseurl: {{ test_suite_summary.base_url }}</span>
                            {% if test_suite_summary.success == True %}
                                <span class='test-status right pass'>pass</span>
                            {% else %}
                                <span class='test-status right fail'>fail</span>
                            {% endif %}


                        </div>
                        <div class='test-content hide'>
                            <div class='test-time-info'>
                                <span class='label start-time'>{{ test_suite_summary.time.start_at }}</span>
                                <span class='label end-time'>{{ test_suite_summary.time.duration|floatformat:3 }} seconds</span>
                            </div>
                            <div class='test-desc'>Pass: {{ test_suite_summary.stat.successes }} ;
                                Fail: {{ test_suite_summary.stat.failures }} ;
                                Error: {{ test_suite_summary.stat.errors }}
                                Skip: {{ test_suite_summary.stat.skipped }} ;
                            </div>
                            <div class='test-attributes'>
                                <div class='category-list'>
                                    <span class='category label white-text'>{{ test_suite_summary.name }}</span>
                                    <span class='category label white-text'>base_url: {{ test_suite_summary.base_url }}</span>
                                </div>
                            </div>
                            <ul class='collapsible node-list' data-collapsible='accordion'>
                                {% for record in test_suite_summary.records %}
                                    {% if  record.status == 'success' %}
                                        <li class='node level-1 leaf pass' status='pass'
                                            test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>
                                            {% elif record.status == 'failure' %}
                                        <li class='node level-1 leaf fail' status='fail'
                                            test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>
                                            {% elif record.status == 'error' %}
                                        <li class='node level-1 leaf error' status='error'
                                            test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>
                                            {% elif record.status == 'skipped' %}
                                        <li class='node level-1 leaf skip' status='skip'
                                            test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>
                                    {% endif %}
                                <div class='collapsible-header'>
                                    <div class='node-name'>{{ record.name }}</div>
                                    <span class='node-time'>{{ record.start_timestamp }}</span>
                                    <span class='node-duration'>response_time: {{ record.meta_datas.stat.response_time_ms }} ms</span>
                                    {% if  record.status == 'success' %}
                                        <span class='test-status right pass'>pass</span>
                                    {% elif record.status == 'failure' %}
                                        <span class='test-status right fail'>fail</span>
                                    {% elif record.status == 'error' %}
                                        <span class='test-status right error'>error</span>
                                    {% elif record.status == 'skipped' %}
                                        <span class='test-status right skip'>skip</span>
                                    {% endif %}

                                </div>
                                <div class='collapsible-body'>
                                    <div class='category-list right'>
                                        <span class='category label white-text'>{{ test_suite_summary.name }}</span>
                                        <span class='category label white-text'>{{ record.name }}</span>
                                    </div>
                                    <div class='node-steps'>
                                    {% for step in record.meta_datas.data %}
                                        <table class='bordered table-results'>
                                            <thead>
                                            <tr>
                                                <th>Status</th>
                                                <th>Params</th>
                                                <th>Details</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            <tr class='info' status='info'>
                                                <td class='status info' title='info' alt='info'><i
                                                        class='material-icons'>low_priority</i></td>
                                                <td class='timestamp'>url</td>
                                                <td class='step-details'>{{ step.request.url }}</td>
                                            </tr>
                                            <tr class='info' status='info'>
                                                <td class='status info' title='info' alt='info'><i
                                                        class='material-icons'>low_priority</i></td>
                                                <td class='timestamp'>method</td>
                                                <td class='step-details'>{{ step.request.method }}</td>
                                            </tr>
                                            <tr class='info' status='info'>
                                                <td class='status info' title='info' alt='info'><i
                                                        class='material-icons'>low_priority</i></td>
                                                <td class='timestamp'>status_code</td>
                                                <td class='step-details'>{{ step.response.status_code }}</td>
                                            </tr>
                                            {% for key, value in step.request.items %}
                                                {% if key != 'url' and key != 'method' and key != 'start_timestamp' %}
                                                    <tr class='log' status='debug'>
                                                        <td class='status debug' title='debug' alt='debug'><i
                                                                class='material-icons'>low_priority</i></td>
                                                        <td class='timestamp'>{{ key }}</td>
                                                        <td class='step-details'>
                                                            {% if key == "headers" %}
                                                                {% for header_key, header_value in value.items %}
                                                                    <div>
                                                                        <strong>{{ header_key }}</strong>: {{ header_value }}
                                                                    </div>
                                                                {% endfor %}
                                                            {% else %}
                                                                {{ value }}
                                                            {% endif %}
                                                        </td>
                                                    </tr>
                                                {% endif %}
                                            {% endfor %}

                                            {% for key, value in step.response.items %}
                                                {% if key != "content" and key != "json" and key != "elapsed_ms" and key != "response_time_ms" and key != "content_size" and key != "content_type" and key != "status_code" and key != "reason" and key != "ok" and key != "encoding" and key != "url" %}
                                                    <tr class='log' status='debug'>
                                                        <td class='status debug' title='debug' alt='debug'><i
                                                                class='material-icons'>low_priority</i></td>
                                                        <td class='timestamp'>{{ key }}</td>
                                                        <td class='step-details'>
                                                            {% if key == "headers" %}
                                                                {% for header_key, header_value in value.items %}
                                                                    <div>
                                                                        <strong>{{ header_key }}</strong>: {{ header_value }}
                                                                    </div>
                                                                {% endfor %}
                                                            {% elif key == "text" %}
                                                                {% if  record.meta_datas.response.content_type == 'image' %}
                                                                    <img src="{{ record.meta_datas.response.content }}"/>
                                                                {% else %}
                                                                    <pre>{{ record.meta_datas.response.text }}</pre>
                                                                {% endif %}
                                                            {% else %}
                                                                {{ value }}
                                                            {% endif %}
                                                        </td>
                                                    </tr>
                                                {% endif %}
                                            {% endfor %}

                                            <tr class='log' status='pass'>
                                                <td class='status pass' title='pass' alt='pass'><i
                                                        class='material-icons'>low_priority</i></td>
                                                <td class='timestamp'>Validators</td>
                                                <td class='step-details'>
                                                    {% for validator in record.meta_datas.validators %}
                                                        <div>
                                                            <strong>{{ validator.comparator }}:</strong>[ {{ validator.expect }}
                                                            ,&nbsp;&nbsp;{{ validator.check_value }} ]
                                                        </div>
                                                    {% endfor %}
                                                </td>
                                            </tr>

                                            <tr class='info' status='info'>
                                                <td class='status info' title='info' alt='info'><i
                                                        class='material-icons'>low_priority</i></td>
                                                <td class='timestamp'>Statistics</td>
                                                <td class='step-details'>
                                                    <div>
                                                        content_size(bytes): {{ record.meta_datas.stat.content_size }}
                                                    </div>
                                                    <div>
                                                        response_time(ms): {{ record.meta_datas.stat.response_time_ms }}
                                                    </div>
                                                    <div>
                                                        elapsed(ms): {{ record.meta_datas.stat.elapsed_ms }}
                                                    </div>
                                                </td>
                                            </tr>


                                            {% if record.attachment %}
                                                <tr class='log' status='fail'>
                                                    <td class='status fail' title='fail' alt='fail'><i
                                                            class='material-icons'>cancel</i></td>
                                                    <td class='timestamp'>exception:</td>
                                                    <td class='step-details'>
                                                        <pre>{{ record.attachment }}</pre>
                                                    </td>
                                                </tr>
                                            {% endif %}
                                            </tbody>
                                        </table>
                                    {% endfor %}
                                    </div>
                                    
                                </div>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                    {% endfor %}
                </ul>
            </div>
        </div>
        <!-- subview left -->

        <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='test-name'></h5>

                <div id='step-filters' class="right">
                    <span class="blue-text" status="info" alt="info" title="info"><i
                            class="material-icons">info_outline</i></span>
                    <span class="green-text" status="pass" alt="pass" title="pass"><i class="material-icons">check_circle</i></span>
                    <span class="red-text" status="fail" alt="fail" title="fail"><i
                            class="material-icons">cancel</i></span>
                    <span class="red-text text-darken-4" status="fatal" alt="fatal" title="fatal"><i
                            class="material-icons">cancel</i></span>
                    <span class="pink-text text-lighten-1" status="error" alt="error" title="error"><i
                            class="material-icons">error</i></span>
                    <span class="orange-text" alt="warning" status="warning" title="warning"><i
                            class="material-icons">warning</i></span>
                    <span class="teal-text" status="skip" alt="skip" title="skip"><i
                            class="material-icons">redo</i></span>
                    <span status="clear" alt="Clear filters" title="Clear filters"><i
                            class="material-icons">clear</i></span>
                </div>
            </div>
        </div>
    </div>
    <!-- subview right -->
    <!-- test view -->
    <div id='category-view' class='view hide'>

        <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input tyle="color: red;" id='search-tests' type='text'
                               class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>

        <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Categories</h5>
                <ul id='category-collection' class='category-collection'>

                    <li class='category displayed active'>
                        <div class='category-heading'>
                            <span class='category-name'>All Suites</span>
                            <span class='category-status right'>
							    <span class='label pass'>{{ stat.successes }} </span>
                                {% if stat.failures != 0 %}
                                    <span class='label fail'>{{ stat.failures }}</span>
                                {% endif %}
                                {% if stat.errors != 0 %}
                                    <span class='label blue lighten-1'>{{ stat.errors }}</span>
                                {% endif %}
                                {% if stat.skipped != 0 %}
                                    <span class='label yellow darken-2'>{{ stat.skipped }}</span>
                                {% endif %}
                                </span>
                        </div>
                        <div class='category-content hide'>
                            <div class='category-status-counts'>
                                <span class='label green accent-4 white-text'>Passed: {{ stat.successes }}</span>
                                <span class='label red lighten-1 white-text'>Failed: {{ stat.failures }}</span>
                                <span class='label blue lighten-1 white-text'>Errored: {{ stat.errors }}</span>
                                <span class="label yellow darken-2 white-text">Skipped: {{ stat.skipped }}</span>
                            </div>

                            <div class='category-tests'>
                                <table class='bordered table-results'>
                                    <thead>
                                    <tr>
                                        <th>Timestamp</th>
                                        <th>TestName</th>
                                        <th>Status</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {% for test_suite_summary in details %}
                                        <tr style="border: 1px solid #49cc90; background-color: rgba(73, 204, 144, .1)">
                                            <td>{{ test_suite_summary.time.start_at }}</td>
                                            <td class='linked'
                                                test-id='{{ test_suite_summary.name }}_{{ forloop.counter }}'>{{ test_suite_summary.name }}</td>
                                            {% if test_suite_summary.success == True %}
                                                <td><span class='test-status pass'>pass</span></td>
                                            {% else %}
                                                <td><span class='test-status fail'>fail</span></td>
                                            {% endif %}

                                        </tr>
                                        {% for record in test_suite_summary.records %}
                                            {% if record.name !=  test_suite_summary.name %}
                                                <tr>
                                                    <td>{{ record.meta_datas.request.start_timestamp }}</td>
                                                    <td class='linked'
                                                        test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>{{ record.name }}</td>
                                                    {% if record.status == 'success' %}
                                                        <td><span class='test-status pass'>pass</span></td>
                                                    {% elif record.status == 'failure' %}
                                                        <td><span class='test-status fail'>fail</span></td>
                                                    {% elif record.status == 'error' %}
                                                        <td><span class='test-status error'>error</span></td>
                                                    {% elif record.status == 'skipped' %}
                                                        <td><span class='test-status' style="color: #fbc02d">skip</span>
                                                        </td>
                                                    {% endif %}
                                                </tr>
                                            {% endif %}
                                        {% endfor %}
                                    {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </li>

                    {% for test_suite_summary in details %}
                        <li class='category displayed active'>
                            <div class='category-heading'>
                                <span class='category-name'>{{ test_suite_summary.name }}</span>
                                <span class='category-status right'>
							    <span class='label pass'>{{ test_suite_summary.stat.successes }} </span>
                                    {% if test_suite_summary.stat.failures != 0 %}
                                        <span class='label fail'>{{ test_suite_summary.stat.failures }}</span>
                                    {% endif %}
                                    {% if test_suite_summary.stat.errors != 0 %}
                                        <span class='label blue lighten-1'>{{ test_suite_summary.stat.errors }}</span>
                                    {% endif %}
                                    {% if test_suite_summary.stat.skipped != 0 %}
                                        <span class='label yellow darken-2'>{{ test_suite_summary.stat.skipped }}</span>
                                    {% endif %}
                                </span>
                            </div>
                            <div class='category-content hide'>
                                <div class='category-status-counts'>
                                    <span class='label green accent-4 white-text'>Passed: {{ test_suite_summary.stat.successes }}</span>
                                    <span class='label red lighten-1 white-text'>Failed: {{ test_suite_summary.stat.failures }}</span>
                                    <span class='label blue lighten-1 white-text'>Errored: {{ stat.errors }}</span>
                                    <span class="label yellow darken-2 white-text">Skipped: {{ test_suite_summary.stat.skipped }}</span>
                                </div>

                                <div class='category-tests'>
                                    <table class='bordered table-results'>
                                        <thead>
                                        <tr>
                                            <th>Timestamp</th>
                                            <th>TestName</th>
                                            <th>Status</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {% for record in test_suite_summary.records %}
                                            <tr>
                                                <td>{{ record.meta_datas.request.start_timestamp }}</td>
                                                <td class='linked'
                                                    test-id='{{ test_suite_summary.name }}_{{ record.name }}_{{ forloop.counter }}'>{{ record.name }}</td>
                                                {% if record.status == 'success' %}
                                                    <td><span class='test-status pass'>pass</span></td>
                                                {% elif record.status == 'failure' %}
                                                    <td><span class='test-status fail'>fail</span></td>
                                                {% elif record.status == 'error' %}
                                                    <td><span class='test-status error'>error</span></td>
                                                {% elif record.status == 'skipped' %}
                                                    <td><span class='test-status' style="color: #fbc02d">skip</span>
                                                    </td>
                                                {% endif %}
                                            </tr>
                                        {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='category-name'></h5>
            </div>
        </div>
    </div>
    <!-- category view -->

    <div id='dashboard-view' class='view hide'>
        <div class='card-panel transparent np-v'>
            <h5>Dashboard</h5>

            <div class='row'>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Pass
                        <div class='panel-lead'>{{ stat.teststeps.successes }}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Fail
                        <div class='panel-lead'>{{ stat.teststeps.failures }}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Error
                        <div class='panel-lead'>{{ stat.teststeps.errors }}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Skip
                        <div class='panel-lead'>{{ stat.teststeps.skipped }}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Start
                        <div class='panel-lead'>{{ time.start_datetime }}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Time Taken
                        <div class='panel-lead'>{{ time.duration|floatformat:3 }} seconds</div>
                    </div>
                </div>
                <div class='col s4'>
                    <div class='card-panel'>
                        <span class='right label cyan white-text'>Categories</span>
                        <p>&nbsp;</p>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Passed</th>
                                <th>Failed</th>
                                <th>Errored</th>
                                <th>Skipped</th>
                            </tr>
                            <tr>
                                <td>All Suites</td>
                                <td class="pass">{{ stat.successes }}</td>
                                <td class="fail">{{ stat.failures }}</td>
                                <td class="error">{{ stat.errors }}</td>
                                <td class="skip">{{ stat.skipped }}</td>
                            </tr>

                            {% for test_suite_summary in details %}
                                <tr>
                                    <td>{{ test_suite_summary.name }}</td>
                                    <td class="pass">{{ test_suite_summary.stat.successes }}</td>
                                    <td class="fail">{{ test_suite_summary.stat.failures }}</td>
                                    <td class="error">{{ test_suite_summary.stat.errors }}</td>
                                    <td class="skip">{{ test_suite_summary.stat.skipped }}</td>
                                </tr>
                            {% endfor %}
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- dashboard view -->
    <!-- testrunner-logs view -->
    <!-- container -->
</div>
<script>
    var test_suite_success = 0;
    {%for test_suite_summary in details %}
        {% if test_suite_summary.success == True %}
            test_suite_success = test_suite_success + 1;
        {% endif %}

    {% endfor %}

    var statusGroup = {
        passParent: {{ stat.teststeps.successes }},
        failParent: {{ stat.teststeps.failures }},
        fatalParent: 0,
        errorParent: {{ stat.teststeps.errors }},
        warningParent: 0,
        skipParent: {{ stat.teststeps.skipped }},
        exceptionsParent: 0,

        passChild: test_suite_success,
        failChild: {{ details|length }} -test_suite_success,
        fatalChild: 0,
        errorChild: 0,
        warningChild: 0,
        skipChild: 0,
        infoChild: 0,
        exceptionsChild: 0,

        passGrandChild: 0,
        failGrandChild: 0,
        fatalGrandChild: 0,
        errorGrandChild: 0,
        warningGrandChild: 0,
        skipGrandChild: 0,
        infoGrandChild: 0,
        exceptionsGrandChild: 0,
    };

    document.getElementById('pass_suites').innerHTML = "<span class='strong'>" + test_suite_success + "</span> suite(s) passed";//找到id为'myId'的标签内插入html变量的值
    document.getElementById('fail_suites').innerText = {{ details|length }} -test_suite_success;//找到id为'myId'的标签替换它的内容为html的值

</script>

<script src='http://extentreports.com/resx/dist/js/extent.js' type='text/javascript'></script>


<script type='text/javascript'>
    $(window).off("keydown");
</script>
</body>

</html>

```

5. 修改case_lit.html
```js
# 找到
post('#', {'id': index})
# 修改为
post('{%url 'test_run' %}', {'id': index})
```
6. 添加url

`path('test/test_run', views.test_run, name='test_run'),`

7. commons.js 添加
```js
function post(url, params) {
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in params) {
        var opt = document.createElement("input");
        opt.name = x;
        opt.value = params[x];
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}
```
测试用例运行


## 批量运行

### 用例批量运行
1. 添加批量运行视图
```python
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
```


### 测试用例批量运行
在views.py中导入
`from httpapitest.runner import run_by_batch`

修改module_list.html模板
```
# 找到下面语句
post('#', obj)
#修改为
post('{% url 'test_batch_run' %}', obj)             
```

添加url
`path('test/test_batch_run', views.test_batch_run, name='test_batch_run'),`

测试用例批量运行

### 模块批量运行功能
修改module_list.html模板

两个运行button
```
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-bug"
                         onclick="run_test('batch','{% url 'test_batch_run' %}', 'module')">运行
                </button>


                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '运行', trigger: 'hover focus'}"
                                            onclick="run_test('{{ module.id }}', '{% url 'test_run' %}', 'module')"
                                            >
                                        <span class="am-icon-bug"></span>
                                    </button>


```

script 部分                                
```js     
        function run_test(mode,url, type) {
            if (mode === 'batch') {
                if ($("input:checked").size() === 0) {
                    myAlert("请至少选择一个模块运行！");
                    return;
                }
            }
            $('#select_env').modal({
                relatedTarget: this,
                onConfirm: function () {
                    var data = {
                        "id": $("#module_list").serializeJSON(),
                        "type": type,
                        'report_name': $('#report_name').val()
                    };
                    if (mode !== 'batch') {
                        data["id"] = mode;
                    }
                    if ($('#mode').val() === 'true') {
                        if (mode === 'batch') {
                            var json2map = JSON.stringify(data['id']);
                            var obj = JSON.parse(json2map);
                            obj['type'] = data['type'];
                            post('{% url 'test_batch_run' %}', obj);
                        } else {
                            post('{% url 'test_run' %}', data);
                        }
                    } else {
                        $.ajax({
                            type: 'post',
                            url: url,
                            data: JSON.stringify(data),
                            contentType: "application/json",
                            success: function (data) {
                                myAlert(data);
                            },
                            error: function () {
                                myAlert('Sorry，服务器可能开小差啦, 请重试!');
                            }
                        });
                    }
                },
                onCancel: function () {
                }
            });
        }
```

测试模块运行

### 项目批量运行
修改project_list.html
两个运行按钮
```html
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-bug"
                         onclick="run_test('batch','{% url 'test_batch_run' %}', 'project')">运行
                </button>

                <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '运行', trigger: 'hover focus'}"
                                            onclick="run_test('{{ project.id }}', '{% url 'test_run' %}', 'project')"
                                            >
                                        <span class="am-icon-bug"></span>
                                    </button>
```

script 部分                                
```js     
        function run_test(mode,url, type) {
            if (mode === 'batch') {
                if ($("input:checked").size() === 0) {
                    myAlert("请至少选择一个模块运行！");
                    return;
                }
            }
            $('#select_env').modal({
                relatedTarget: this,
                onConfirm: function () {
                    var data = {
                        "id": $("#module_list").serializeJSON(),
                        "type": type,
                        'report_name': $('#report_name').val()
                    };
                    if (mode !== 'batch') {
                        data["id"] = mode;
                    }
                    if ($('#mode').val() === 'true') {
                        if (mode === 'batch') {
                            var json2map = JSON.stringify(data['id']);
                            var obj = JSON.parse(json2map);
                            obj['type'] = data['type'];
                            post('{% url 'test_batch_run' %}', obj);
                        } else {
                            post('{% url 'test_run' %}', data);
                        }
                    } else {
                        $.ajax({
                            type: 'post',
                            url: url,
                            data: JSON.stringify(data),
                            contentType: "application/json",
                            success: function (data) {
                                myAlert(data);
                            },
                            error: function () {
                                myAlert('Sorry，服务器可能开小差啦, 请重试!');
                            }
                        });
                    }
                },
                onCancel: function () {
                }
            });
        }
```
添加运行窗口

```html
<div class="am-modal am-modal-confirm" tabindex="-1" id="select_env">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <form class="form-horizontal">
                <div class="form-group">
                    <label class="control-label col-sm-3" for="report_name"
                           style="font-weight: inherit; font-size: small ">报告名称：</label>
                    <div class="col-sm-8">
                        <input name="report_name" type="text" id="report_name" class="form-control"
                               placeholder="默认时间戳命名" value="" readonly>
                    </div>
                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">执行方式:</label>
                    <div class="col-sm-8">
                        <select class="form-control" id="mode" name="mode">
                            <option value="true">同步(执行完立即返回报告)</option>
                            <option value="false">异步(后台执行，完毕后可查看报告)</option>
                        </select>
                    </div>
                </div>
            </form>
            </form>

            <div class="am-modal-moduleter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>
```

## 测试报告

1. 在modules.py 中添加 模型TestReports
```python
class TestReports(BaseTable):
    class Meta:
        verbose_name = "测试报告"
        db_table = 'TestReports'

    report_name = models.CharField(max_length=40, null=False)
    start_at = models.CharField(max_length=40, null=True)
    status = models.BooleanField()
    testsRun = models.IntegerField()
    successes = models.IntegerField()
    reports = models.TextField()
```

2. 添加视图函数
```python
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
```
views.py 新增导入
```python
from httpapitest.models import TestReports
from django.utils.safestring import mark_safe
```

3. 添加report_list.html模板
[report_list.html](./Chapter-12/code/hat/templates/report_list.html)
[report_view.html](./Chapter-12/code/hat/templates/report_view.html)
4. 添加url
```
path('report/list', views.report_list, name='report_list'),
path('report/delete', views.report_delete, name='report_delete'),
path('report/view/<int:id>', views.report_view, name='report_view'),
```

## 添加异步执行功能
1. 添加异步运行所需要的tasks.py文件

[tasks.py](./Chapter-12/code/hat/httpapitest/tasks.py)

在utils.py中添加函数add_test_reports,并导入TestReports和 os, platform
```python
def add_test_reports(summary, report_name=None):
    """
    定时任务或者异步执行报告信息落地
    :param start_at: time: 开始时间
    :param report_name: str: 报告名称，为空默认时间戳命名
    :param kwargs: dict: 报告结果值
    :return:
    """
    
    
    print("xxx")
    separator = '\\' if platform.system() == 'Windows' else '/'

    time_stamp = int(summary["time"]["start_at"])
    summary['time']['start_at'] = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    report_name = report_name if report_name else summary['time']['start_datetime']
    summary['html_report_name'] = report_name

    report_path = os.path.join(os.getcwd(), "reports{}{}.html".format(separator,time_stamp))
    #runner.gen_html_report(html_report_template=os.path.join(os.getcwd(), "templates{}extent_report_template.html".format(separator)))

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_reports = {
        'report_name': report_name,
        'status': summary.get('success'),
        'successes': summary.get('stat').get('testcases').get('success'),
        'testsRun': summary.get('stat').get('testcases').get('total'),
        'start_at': summary['time']['start_at'],
        'reports': reports
    }

    TestReports.objects.create(**test_reports)
    return report_path

```
安装模块celery

`pip install celery==4.3.0`

在views.py 导入from httpapitest.tasks import main_hrun


2. 修改settings.py 添加celery相关配置
[settings.py](./Chapter-12/code/hat/hat/settings.py)
```
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  #注意这里的127.0.0.1 应该为你redis服务的ip
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler' # 定时任务
CELERY_TASK_RESULT_EXPIRES = 7200  # celery任务执行结果的超时时间，
CELERYD_CONCURRENCY = 1 if DEBUG else 10 # celery worker的并发数 也是命令行-c指定的数目 根据服务器配置实际更改 一般25即可
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会死掉
```

3. 在hat目录中新增celery.py 文件

[celery.py](./Chapter-12/code/hat/hat/celery.py)

该文件用来启动celery 进程

```
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hat.settings')

app = Celery('hat')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```
在同目录下的__init__.py 添加以下内容
```
from .celery import app as celery_app

__all__ = ('celery_app',)
```

4. 安装gevent，redis 模块
```
pip install gevent
pip install redis
```
5. 启动redis

6. 启动celery

`celery -A  hat  worker --loglevel=info  -P gevent`

打开模块列表,执行模块选择异步

## redis
## redis
Redis 是一个高性能的key-value数据库。
Redis 以下三个特点：

+ Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
+ Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，hash等数据结构的存储。
+ Redis支持数据的备份，即master-slave模式的数据备份。

### redis数据结构

+ STRING：字符串、整数或浮点数
+ LIST：列表，可存储多个相同的字符串
+ SET：集合，存储不同元素，无序排列
+ HASH：散列表，存储键值对之间的映射，无序排列


### redis-cli

```
127.0.0.1:6379> info
# Server
redis_version:6.0.9
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:11509227cb1fdf31
redis_mode:standalone
os:Linux 3.10.0-1160.el7.x86_64 x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:8.3.0

```

### redis 字符串
Redis 字符串数据类型的相关命令用于管理 redis 字符串值
```
127.0.0.1:6379> set name jiaminqiang
OK
127.0.0.1:6379> get name
"jiaminqiang"
127.0.0.1:6379> set name 贾敏强
OK
127.0.0.1:6379> get name
"\xe8\xb4\xbe\xe6\x95\x8f\xe5\xbc\xba"

```

### redis hash
Redis hash 是一个 string 类型的 field（字段） 和 value（值） 的映射表，hash 特别适合用于存储对象。

```shell
127.0.0.1:6379> HMSET student name jia age 18
OK
127.0.0.1:6379> hgetall student
1) "name"
2) "jia"
3) "age"
4) "18"
127.0.0.1:6379> hget student name
"jia"
127.0.0.1:6379> hget student age
"18"
```

### redis list
Redis列表是简单的字符串列表，按照插入顺序排序。
```
127.0.0.1:6379> lpush names jia
(integer) 1
127.0.0.1:6379> lpush names li
(integer) 2
127.0.0.1:6379> lpush names wang
(integer) 3
127.0.0.1:6379> llen names
(integer) 3
127.0.0.1:6379> lrange 0 2
(error) ERR wrong number of arguments for 'lrange' command
127.0.0.1:6379> lrange names 0 2
1) "wang"
2) "li"
3) "jia"
127.0.0.1:6379> lpop names
"wang"
127.0.0.1:6379> lrange names 0 2
1) "li"
2) "jia"
127.0.0.1:6379> llen names
(integer) 2
127.0.0.1:6379> rpop names
"jia"
127.0.0.1:6379> lrange names 0 2
1) "li"
127.0.0.1:6379> rpush names zhang
(integer) 2
127.0.0.1:6379> lrange names 0 2
1) "li"
2) "zhang"
```

### redis set
Redis 的 Set 是 String 类型的无序集合。集合成员是唯一的，这就意味着集合中不能出现重复的数据。
```
127.0.0.1:6379> sadd numbers 1
(integer) 1
127.0.0.1:6379> sadd numbers 2
(integer) 1
127.0.0.1:6379> sadd numbers 3
(integer) 1
127.0.0.1:6379> smembers numbers
1) "1"
2) "2"
3) "3"
127.0.0.1:6379> sadd numbers 3
(integer) 0
127.0.0.1:6379> smembers numbers
1) "1"
2) "2"
3) "3"

127.0.0.1:6379> spop numbers 1
1) "1"
127.0.0.1:6379> smembers numbers
1) "2"
2) "3"
127.0.0.1:6379> spop numbers 3
1) "2"
2) "3"
```

### 通用命令
1. 查看key类型
` type student`
2. 删除key
`type student`
3. 判断key是否存在
```
127.0.0.1:6379> set name jia
OK
127.0.0.1:6379> exists name
(integer) 1
127.0.0.1:6379> del name
(integer) 1
127.0.0.1:6379> exists name
(integer) 0
```
4. 列出所有key
```
127.0.0.1:6379> keys *
1) "names"
```

## celery

Celery 是一个简单、灵活且可靠的，处理大量消息的分布式系统，并且提供维护这样一个系统的必需工具。是一个专注于实时处理的任务队列，同时也支持任务调度。


任务队列用作跨线程或机器分配工作的机制。 任务队列的输入是为一个任务。任务队列通过消息系统borker实现。客户端往broker中加任务，worker进程不断监视broker中的任务队列以执行新的任务


支持的常见broker
+ redis
+ rabbitmq
+ zookeeper

编写tasks.py
```
from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

@app.task
def add(x, y):
    return x + y
```


client.py
```
from tasks import add
add.delay(2,3) 
```

启动 redis
执行client.py 生成一个要执行的任务
`python client.py`
查看redis key
```
127.0.0.1:6379> keys *
1) "celery"
2) "_kombu.binding.celery"
```
查看key类型
```
127.0.0.1:6379> type celery
list
127.0.0.1:6379> type "_kombu.binding.celery"
set
```
查看key 的value
```
127.0.0.1:6379> lrange celery 0 -1
1) "{\"body\": \"W1syLCAzXSwge30sIHsiY2FsbGJhY2tzIjogbnVsbCwgImVycmJhY2tzIjogbnVsbCwgImNoYWluIjogbnVsbCwgImNob3JkIjogbnVsbH1d\", \"content-encoding\": \"utf-8\", \"content-type\": \"application/json\", \"headers\": {\"lang\": \"py\", \"task\": \"tasks.add\", \"id\": \"d0ac9482-bb5f-4b4d-8b70-625cd88aad0d\", \"shadow\": null, \"eta\": null, \"expires\": null, \"group\": null, \"retries\": 0, \"timelimit\": [null, null], \"root_id\": \"d0ac9482-bb5f-4b4d-8b70-625cd88aad0d\", \"parent_id\": null, \"argsrepr\": \"(2, 3)\", \"kwargsrepr\": \"{}\", \"origin\": \"gen15684@LAPTOP-PHMJ1QN6\"}, \"properties\": {\"correlation_id\": \"d0ac9482-bb5f-4b4d-8b70-625cd88aad0d\", \"reply_to\": \"7d107092-94b4-35c8-bb26-20063dc7944d\", \"delivery_mode\": 2, \"delivery_info\": {\"exchange\": \"\", \"routing_key\": \"celery\"}, \"priority\": 0, \"body_encoding\": \"base64\", \"delivery_tag\": \"3526616e-1efc-4eae-867d-1715c8751531\"}}"

127.0.0.1:6379> smembers "_kombu.binding.celery"
1) "celery\x06\x16\x06\x16celery"
```


celery 为一个任务队列列表 等待执行的任务都在这个列表里
_kombu.binding.celery 默认的任务队列名称默认为 celery



启动worker

`celery -A tasks worker --loglevel=info  -P eventlet`


