// 用来进行文件上传的一些验证处理及UI变化
$(".file-style").on("change","input[type='file']",function(){
    var filePath=$(this).val();
    if(filePath.length < 3)  // 未选择文件时
        $("#showFileName").text("选择文件");
    else {
        var arr = filePath.split('\\');
        var fileName = arr[arr.length - 1];
        $("#showFileName").text(" " + fileName + " ");
    }
});

