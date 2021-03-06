/*提示 弹出*/
function myAlert(data) {
    $('#my-alert_print').text(data);
    $('#my-alert').modal({
        relatedTarget: this
    });
}


/*添加项目*/
function project_add(url) {
    // 使用jquery获取表单数据
    var data = $('#project_add').serializeJSON(); 

    // 对表单数据做校验
    if (data.project_name === '' ) {
        myAlert('项目名称不能为空')
        return
    }
    if (data.responsible_name === '') {
        myAlert('负责人不能为空')
        return
    }

    if (data.test_user === '') {
        myAlert('测试人员不能为空')
        return
    }

    if (data.dev_user === '') {
        myAlert('开发人员不能为空')
        return
    }

    if (data.dev_user === '') {
        myAlert('发布应用不能为空')
        return
    }
    // 使用jquery的ajax 提交表单
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('/httpapitest/') !== -1) {
                window.location.href = data;
            } else {
                myAlert(data);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function update_data_ajax(id, url) {
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
                if (data.indexOf('/httpapitest/') !== -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function del_data_ajax(id, url) {
    var data = {
        "id": id
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
                if (data.indexOf('/httpapitest/') !== -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);

    editor.setFontSize(17);

    editor.setReadOnly(false);

    editor.setOption("wrap", "free");

    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });


}

/*添加模块*/
function module_add(url) {
    // 使用jquery获取表单数据
    var m = $('#module_add').serializeJSON(); 

    // 对表单数据做校验
    if (m.module_name === '' ) {
        myAlert('模块名称不能为空')
        return
    }
    if (m.belong_project === '请选择') {
        myAlert('请选择项目，没有请先添加哦')
        return
    }

    if (m.test_user === '') {
        myAlert('测试人员不能为空')
        return
    }

    // 使用jquery的ajax 提交表单
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(m),
        contentType: "application/json",
        success: function (r) {
            if (r.indexOf('/httpapitest/') !== -1) {
                window.location.href = r;
            } else {
                myAlert(r);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}



function del_row(id) {
    var attribute = id;
    var chkObj = document.getElementsByName(attribute);
    var tabObj = document.getElementById(id);
    for (var k = 0; k < chkObj.length; k++) {
        if (chkObj[k].checked) {
            tabObj.deleteRow(k + 1);
            k = -1;
        }
    }
}

function add_row(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var cell_check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var cell_key = "<input type='text' name='test[][key]'  value='' style='" + style + "' />";
    var cell_value = "<input type='text' name='test[][value]'  value='' style='" + style + "' />";
    var cell_type = "<select name='test[][type]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>string</option><option>int</option><option>float</option><option>boolean</option></select>";
    var cell_comparator = "<select name='test[][comparator]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>equals</option> <option>contains</option> <option>startswith</option> <option>endswith</option> <option>regex_match</option> <option>type_match</option> <option>contained_by</option> <option>less_than</option> <option>less_than_or_equals</option> <option>greater_than</option> <option>greater_than_or_equals</option> <option>not_equals</option> <option>string_equals</option> <option>length_equals</option> <option>length_greater_than</option> <option>length_greater_than_or_equals</option> <option>length_less_than</option> <option>length_less_than_or_equals</option></select>";

    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);


    newTdObj0.innerHTML = cell_check
    newTdObj1.innerHTML = cell_key;
    if (id === 'variables' || id === 'data') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_type;
        newTdObj3.innerHTML = cell_value;
    } else if (id === 'validate') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_comparator;
        newTdObj3.innerHTML = cell_type;
        var newTdObj4 = myNewRow.insertCell(4);
        newTdObj4.innerHTML = cell_value;
    } else {
        newTdObj2.innerHTML = cell_value;
    }
}

function add_params(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var placeholder = '单个:["value1", "value2],  多个:[["name1", "pwd1"],["name2","pwd2"]]';
    var key = "<textarea  name='test[][key]'  placeholder='单个:key, 多个:key1-key2'  style='" + style + "' />";
    var value = "<textarea  name='test[][value]'  placeholder='" + placeholder + "' style='" + style + "' />";
    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);
    newTdObj0.innerHTML = check;
    newTdObj1.innerHTML = key;
    newTdObj2.innerHTML = value;
}

function show_module(module_info, id) {
    module_info = module_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

function auto_load(id, url, target, type) {
    var data = $(id).serializeJSON();
    if (id === '#belong_message' || id === '#form_message') {
        data = {
            "case": {
                "name": data,
                "type": type
            }
        }
    }
    if (id ==='#project') {
        data = {
            "crontab": {
                "name": data,
                "type": type
            }
        }
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
        
                show_module(data, target)
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function case_ajax(type, editor) {
    var url = $("#url").serializeJSON();
    var method = $("#method").serializeJSON();
    var dataType = $("#DataType").serializeJSON();
    var caseInfo = $("#form_message").serializeJSON();
    var variables = $("#form_variables").serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data  = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#form_request_data").serializeJSON();
    }
    var headers = $("#form_request_headers").serializeJSON();
    var extract = $("#form_extract").serializeJSON();
    var validate = $("#form_validate").serializeJSON();
    var parameters = $('#form_params').serializeJSON();
    var hooks = $('#form_hooks').serializeJSON();
    var include = [];
    var i = 0;
    $("ul#pre_case li a").each(function () {
        include[i++] = [$(this).attr('id'), $(this).text()];
    });
    caseInfo['include'] = include;
    const test = {
        "test": {
            "name": caseInfo,
            "parameters": parameters,
            "variables": variables,
            "request": {
                "url": url.url,
                "method": method.method,
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "extract": extract,
            "validate": validate,
            "hooks": hooks,
        }
    };
    if (type === 'edit') {
        url = '#';
    } else {
        url = '/httpapitest/case/add';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(test),
        contentType: "application/json",
        success: function (data) {
           
                if (data.indexOf('/httpapitest/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function copy_data_ajax(id, url) {
    var data = {
        "data": $(id).serializeJSON(),
        'mode': 'copy'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('/httpapitest/') !== -1) {
                window.location.href = data;
            } else {
                myAlert(data);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

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

/*添加计划任务*/
function task_add(url) {
    // 使用jquery获取表单数据
    var data = $('#task_add').serializeJSON(); 

    // 对表单数据做校验
    if (data.project === '请选择' ) {
        myAlert('请选择项目')
        return
    }
    if (data.name === '') {
        myAlert('名字不能为空')
        return
    }

    if (data.module === '') {
        myAlert('请选择模块')
        return
    }

    if (data.crontab_time === '') {
        myAlert('定时配置不可为空')
        return
    }

    // 使用jquery的ajax 提交表单
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('/httpapitest/') !== -1) {
                window.location.href = data;
            } else {
                myAlert(data);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}