function join(arr,seperator){
    var str = "";
    if(arr.length == 0){
        return str
    }
    for(var i = 0;i<arr.length-1;i++){
        str += arr[i] + seperator

    }
   
    return str + arr[arr.length - 1]
}
console.log(join([1,2,3],","))