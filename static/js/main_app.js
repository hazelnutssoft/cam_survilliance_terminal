/**
 * Created by guoxiao on 16-1-6.
 */

var status = 'home';


jQuery(function(){
        var tmp = "#";
        tmp+=status;
        if(status!='home'){
            $(tmp).addClass("active");
        }
    }
);
function activeMenuItem(cName){
    $('.cName').addClass("active");
    status = cName;
}



