    var arr=[1,2,3,4,5];
    var start =0;
    var end = arr.length-1;
    var temp;
    while(start<end){
        temp = arr[0];
        arr[0] = arr[arr.length-1];
        arr[arr.length-1] =temp ;
        start+=1;
        end-=1;
        

    }
    console.log()
    

