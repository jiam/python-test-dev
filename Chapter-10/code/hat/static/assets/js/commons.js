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