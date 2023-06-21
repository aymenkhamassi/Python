function rotateString(str,int){
   

   if(int==0){
    return str

   }
   int =int % str.length
   var newstr =""
   var reststr =""
   

   for (var i=0;i<str.length;i++){

    if (i<str.length-int){
        newstr += str[i] 

    }
    else{
        reststr += str[i]

    }
    }
    return reststr+newstr
  
   

   
}
console.log(rotateString("hello world",11))