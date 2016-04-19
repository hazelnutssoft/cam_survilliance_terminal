$(document).ready(function(){
    var opts = {
      lines: 12,            // The number of lines to draw
      length: 7,            // The length of each line
      width: 5,             // The line thickness
      radius: 10,           // The radius of the inner circle
      scale: 1.0,           // Scales overall size of the spinner
      corners: 1,           // Roundness (0..1)
      color: '#000',        // #rgb or #rrggbb
      opacity: 1/4,         // Opacity of the lines
      rotate: 0,            // Rotation offset
      direction: 1,         // 1: clockwise, -1: counterclockwise
      speed: 1,             // Rounds per second
      trail: 100,           // Afterglow percentage
      fps: 20,              // Frames per second when using setTimeout()
      zIndex: 2e9,          // Use a high z-index by default
      className: 'spinner', // CSS class to assign to the element
      top: '100px',           // center vertically
      left: '50%',          // center horizontally
      shadow: false,        // Whether to render a shadow
      hwaccel: false,       // Whether to use hardware acceleration (might be buggy)
      position: 'absolute'  // Element positioning
    };
    var target = document.getElementsByClassName('LoadingImg');
    //alert(target)
    //var spinner = new Spinner(opts).spin(target);
    var spinner = new Spinner().spin(target[0]);
})




var is_deleting = false;
var is_setting = false;

function alert_if_deleting(){
    if(is_deleting)
        return '历史数据清除中,您确定要离开当前页面?';
    if(is_setting)
        return '监控设置生效中,您确定要离开当前页面?'

}

window.onbeforeunload = alert_if_deleting;

function switchTab(index, issavebtnshow) {
    $("ul#nav").find('li').each(function () {
        $(this).removeClass('active');
    })
    $("li#nav_"+index).addClass('active');

    $("ul#tab_con").find('li').each(function () {
        $(this).removeClass('active');
    })
    $("li#monitor_tab_con_"+index).addClass('active');
    $("li#basic_tab_con_"+index).addClass('active');

    if(issavebtnshow == 0)
    {
        $('#save_config_btn').css("display","inline-block");
    }
    else
    {
        $('#save_config_btn').css("display","none");
    }
    document.getElementById('is_success').style.display='none'
}

$(function(){


    $("#bright_value").val($("#bright_slider").slider("value"));
    $("#bright_value").change(function(){
        $("#bright_slider").slider({"value":$("#bright_value").val()});
    });


    $("#contrast_value").val($("#contrast_slider").slider("value"));
    $("#contrast_value").change(function(){
        $("#contrast_slider").slider({"value":$("#contrast_value").val()});
    });

    $("#saturation_value").val($("#saturation_slider").slider("value"));
    $("#saturation_value").change(function(){
        $("#saturation_slider").slider({"value":$("#saturation_value").val()});
    });
    //$("#sharpness_slider").slider({
    //    range:"min",
    //    min:0,
    //    max:100,
    //    value:60,
    //    slide:function(event ,ui){
    //        $("#sharpness_value").val(ui.value);
    //}
    //});
    //
    //$("#sharpness_value").val($("#sharpness_slider").slider("value"));

    $('#is_synchronize').change(function(){
        //alert("change!")
        if(this.checked){
            document.getElementById('time2set').value = curent_time()
            //var clock = curent_time()
            $.ajax({
                url:'time_synchronize',
                type:'get',
                dateType:'text',
                data:{
                    'time':curent_time(),
                },
                success:function(){
                    document.getElementById('is_success').innerHTML='同步成功'
                    document.getElementById('is_success').style.display='inline'
                },
                error:function(){
                    document.getElementById('is_success').innerHTML='同步失败'
                    document.getElementById('is_success').style.display='inline'
                }
            })
            //alert(clock)
        }
    })

    //$(".Close").click(function(){
    //
    //    $(".LayBg,.LayBox").hide();
    //});
    //$(".thumbnail").click(function(){
    //    $(".LayBg").height(document.body.clientWidth);
    //    $(".LayImg").html($(this).find(".hidden").html());
    //    $(".LayBg").show();
    //    $(".LayBox").fadeIn(300);
    //    var width = $(".LayImg").find('img').attr('image_width')
    //    alert(width)
    //});
});


function loading_begin(loading_message){
    $(".LoadingBg").height(document.body.clientWidth);
    $(".LoadingBg").show();
    $(".LoadingImg").fadeIn(300);
    $(".Loading_message").html("<p>"+loading_message+"</p>")
    //$(".Loading_message").fadeIn(300);

}

function loading_end(){
    $('.LoadingBg, .LoadingImg, .Loading_message').hide();
}



function curent_time()
    {
        var now = new Date();

        var year = now.getFullYear();       //年
        var month = now.getMonth() + 1;     //月
        var day = now.getDate();            //日

        var hh = now.getHours();            //时
        var mm = now.getMinutes();          //分
        var ss = now.getSeconds()           //秒

        var clock = year + "-";

        if(month < 10)
            clock += "0";

        clock += month + "-";

        if(day < 10)
            clock += "0";

        clock += day + " ";

        if(hh < 10)
            clock += "0";

        clock += hh + ":";
        if (mm < 10)
            clock += '0';
        clock += mm+':';
        if(ss<10)
            clock += '0'
        clock +=ss
        return(clock);
    }


function save_monitor_config(){
    is_setting = true;
    loading_begin("设置生效中...");
    if($('#monitor_tab_con_1').attr('class') == 'active'){
        //alert('tab_con_1')
        $.ajax({
            url:'save_monitor_config',
            type:'get',
            dateType:'text',
            data:{
                'type':'video',
                'resolution':document.getElementById('resolution').value,
                'framerate':document.getElementById('framerate').value,
                'rotate':document.getElementById('rotate').value,
                'brightness':document.getElementById('bright_value').value,
                'contrast':document.getElementById('contrast_value').value,
                'saturation':document.getElementById('saturation_value').value,
            },
            success:function(){
                document.getElementById('is_success').innerHTML='保存成功'
                document.getElementById('is_success').style.display='inline'
                loading_end();
                is_setting = false;

            },
            error:function(){
                document.getElementById('is_success').innerHTML='保存失败'
                document.getElementById('is_success').style.display='inline'
                loading_end();
                is_setting = false;
            },
        })
    }
    else{
        $.ajax({
            url:'save_monitor_config',
            type:'get',
            dateType:'text',
            data:{
                'type':'image',
                'snapshot_interval':document.getElementById('snapshot_interval').value,
            },
            success:function(){
                document.getElementById('is_success').innerHTML='保存成功'
                document.getElementById('is_success').style.display='inline'
                loading_end();
                is_setting = false;

            },
            error:function(){
                document.getElementById('is_success').innerHTML='保存失败'
                document.getElementById('is_success').style.display='inline'
                loading_end();
                is_setting = false;
            },
        })
    }

}

function save_basic_config(){
    if($('#basic_tab_con_1').attr('class') == 'active'){
        $.ajax({
            url:'save_basic_config',
            type:'get',
            dateType:'text',
            data:{
                'type':'device_info',
                'device_name':document.getElementById('device_name').value,
                'device_id':document.getElementById('device_id').value,
            },
            success:function(){
                document.getElementById('is_success').innerHTML='保存成功'
                document.getElementById('is_success').style.display='inline'
            },
            error:function(){
                document.getElementById('is_success').innerHTML='保存失败'
                document.getElementById('is_success').style.display='inline'
            }
        })
    }
    else{
        if(!(document.getElementById('time2set').value == '')){
            //alert(document.getElementById('time2set').value)
            $.ajax({
                url:'time_synchronize',
                type:'get',
                dateType:'text',
                data:{
                    'time':document.getElementById('time2set').value+':00',
                },
                success:function(){
                    document.getElementById('is_success').innerHTML='同步成功'
                    document.getElementById('is_success').style.display='inline'
                },
                error:function(){
                    document.getElementById('is_success').innerHTML='同步失败'
                    document.getElementById('is_success').style.display='inline'
                }
            })
        }
        //else{
        //    alert('blank')
        //}
        //alert()
        //$.ajax({
        //    url:'save_basic_config',
        //    type:'get',
        //    dateType:'text',
        //    data:{
        //        'type':'image',
        //        'snapshot_interval':document.getElementById('snapshot_interval').value,
        //    },
        //    success:function(data, status){
        //      if(data == "0"){
        //          document.getElementById('is_success').style.display='inline'
        //      }
        //
        //      else{
        //          document.getElementById('is_success').style.display='inline'
        //          document.getElementById('is_success').innerHTML='保存失败'
        //      }
        //
        //    }
        //})
    }
}

function clear_data(){
    is_deleting = true
    loading_begin("数据删除中...")
    $.ajax({
        url:'clear',
        type:'get',
        dateType:'text',
        success:function(){
            loading_end()
            is_deleting = false
            alert('数据清除成功!')
        },
        error:function(){
            loading_end()
            is_deleting = false
            alert('数据清除失败!')
        }
    })
}

function device_reboot(){
    $.ajax({
        url:'reboot',
        type:'get',
        dateType:'text',
        error:function(){
            alert('重启失败')
        },
    })
}


function user_observer(){
    //alert(document.getElementById('is_observed').checked);

    $.ajax({
        url:'user_observer',
        type:'post',
        dataType:'text',
        data:{
            'user_name': document.getElementById('user_name').value,
            'user_password': document.getElementById('user_password').value,
            'is_observed': document.getElementById('is_observed').checked,
        },
        success:function(data, status){
            if(data == "ok"){
            document.getElementById('is_success').innerHTML='同步成功';
            document.getElementById('is_success').style.display='inline';
	    }
            else{
	    document.getElementById('is_success').innerHTML='同步失败';
            document.getElementById('is_success').style.display='inline';    
            }
        },
        error:function(){
            document.getElementById('is_success').innerHTML='同步失败';
            document.getElementById('is_success').style.display='inline';
        }
    })
}

function set_location(){
    $.ajax({
        url:'device_location',
        type:'get',
        dateType:'text',
        data:{
            'location':document.getElementById('device_location').value
        },
        success:function(){
            document.getElementById('is_success').innerHTML='同步成功';
            document.getElementById('is_success').style.display='inline';
        },
        error:function(){
            document.getElementById('is_success').innerHTML='同步失败';
            document.getElementById('is_success').style.display='inline';
        }
    })
}

function add_dev_info(){
    var url="/operater_position?operater=add";
    window.location.replace(url);
}

function edit_dev_info(){
    var position = 1;
    var object_name = "";
    var duration = "";
    var ip_address ="";
    $('.position_info').each(
        function(){
            var is_checked = $(this).find('td.is_checked input')[0].checked;

            if(is_checked){
                position = $(this).find('td.position').html();
                object_name = $(this).find('td.object_name').html();
                duration = $(this).find('td.duration').html();
                ip_address = $(this).find('td.ip_address').html();
            }
    })

    var url = "/operater_position?operater=edit&position="+position+"&object_name="+object_name+"&duration="+duration+"&ip_address="+ip_address;
    window.location.replace(url);
}

function delete_dev_info(){
    var positions = new Array();
    $('.position_info').each(
        function(){
            tt = $(this).find('input')[0].checked;
            if(tt){
                var position = $(this).find('td.position').html();
                positions.push(position);
            }
    });
    $.ajax({
        url:'operater_position',
        type:'get',
        dataType:'text',
        data:{
            'operater':'delete',
            'content': positions
        },
        success:function(res, status){
            $('.position_info').each(function(){
                var is_c = $(this).find('td.is_checked input')[0].checked;
                if(is_c){
                    $(this).remove();
                }
            })
            document.getElementById('is_success').innerHTML='删除成功';
            document.getElementById('is_success').style.display='inline';
        },
        error:function(){
            document.getElementById('is_success').innerHTML='删除失败';
            document.getElementById('is_success').style.display='inline';
        }
    })
}

function upload_dev_info(){
    $.ajax({
        url:'operater_position',
        type:'get',
        dataType:'text',
        data:{
            'operater':'upload'
        },
        success:function(res, status){
               // alert(res);
            if(res == "ok")
                {
                    document.getElementById('is_success').innerHTML='上传成功';
                    document.getElementById('is_success').style.display='inline';
                }
                else{
            document.getElementById('is_success').innerHTML='上传失败';
            document.getElementById('is_success').style.display='inline';
                }
        },
        error:function(){
            document.getElementById('is_success').innerHTML='上传失败';
            document.getElementById('is_success').style.display='inline';
        }
    });
}

function apply_adding(){
    var object_name = document.getElementById('object_name').value;
    var position = document.getElementById('position').value;
    var duration = document.getElementById('duration').value;
    var ip_address = document.getElementById('ip_address').value;

    $.ajax({
        url:'apply_adding',
        type:'post',
        dataType:'text',
        data:{
            'object_name': object_name,
            'position': position,
            'duration': duration,
            'ip_address': ip_address,
        },
        success: function(res,status){
            if(res == "ok")
            {
                window.location.replace('/setting?tab=3')
            }
            else
            {
                document.getElementById('is_success').innerHTML='添加失败';
                document.getElementById('is_success').style.display='inline';
            }
        }
    });
}

function cancel_adding(){
    var url = "/setting?tab=3";
    window.location.replace(url);
}

function apply_edition(){
    var object_name = document.getElementById('object_name').value;
    var position = document.getElementById('position').value;
    var duration = document.getElementById('duration').value;
    var ip_address = document.getElementById('ip_address').value;

    $.ajax({
        url:'apply_edition',
        type:'post',
        dataType:'text',
        data:{
            'object_name': object_name,
            'position': position,
            'duration': duration,
            'ip_address': ip_address,
        },
        success: function(res, status){
           // alert(res)
            if(res == "ok")
            {
                window.location.replace('/setting?tab=3')
            }
            else
            {
                document.getElementById('is_success').innerHTML='编辑失败';
                document.getElementById('is_success').style.display='inline';
            }
        }
    });
}

function cancel_edition(){
    var url = "/setting?tab=3";
    window.location.replace(url);
}
