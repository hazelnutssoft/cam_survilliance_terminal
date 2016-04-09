/**
 * Created by server on 16-1-6.
 */

var is_downloading = false;

function alert_if_downloading(){
    if(is_downloading)
    return '文件下载中,您确定要离开当前页面?'
}

window.onbeforeunload = alert_if_downloading;

jQuery(function(){

    $(".Close").click(function(){

        $(".LayBg,.LayBox").hide();
    });
    $(".thumbnail").click(function(){
        $(".LayBg").height(document.body.clientWidth);
        $(".LayImg").html($(this).find(".hidden").html());
        $(".LayBg").show();
        $(".LayBox").fadeIn(300);
        var width = $(".LayImg").find('img').attr('image_width');
        var height = $(".LayImg").find('img').attr('image_height');
        if (height>480)
        {
            $(".LayBox").width(640);
            $(".LayBox").height(480);
            $(".LayImg img").width(640);
            $(".LayImg img").height(480);
        }
        else
        {
            $(".LayBox").width(width);
            $(".LayBox").height(height);
            $(".LayImg img").width(width);
            $(".LayImg img").height(height);
        }


        //alert(width)
    });
    var target = document.getElementsByClassName('LoadingImg');
    var spinner = new Spinner().spin(target[0]);


})


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



function page_jump(){
    var url = "/preview?page="+$("#page_jump_num").val();
    window.location.replace(url);
}

function download_image(){
    if(confirm('是否下载?')){
        is_downloading = true
        loading_begin("下载准备中...")
        $.ajax({
            url:'download',
            async:false,
            type:'get',
            dataType:'text',
            success:function(data, status){
                if(data != ''){
                    var file_name = data
                    var href = '/static/download/'+file_name
                    //can_download = true
                    document.getElementById('download_link').href = href
                    document.getElementById('download_link').download = file_name
                    loading_end()
                    is_downloading = false
                    return true
                }
                else{
                    alert('获取数据失败!')
                    document.getElementById('download_link').href = ''
                    document.getElementById('download_link').download = ''
                    loading_end()
                    is_downloading = false
                    return false
                }
            },
            error:function(){
                    alert('获取数据失败!')
                    document.getElementById('download_link').href = ''
                    document.getElementById('download_link').download = ''
                    loading_end()
                    is_downloading = false
                    return false
            }
        })
    }
    else{
        //alert('获取数据失败!')
        document.getElementById('download_link').href = ''
        document.getElementById('download_link').download = ''
        return false
    }

}



