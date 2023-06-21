function removeDup(str){
   
   if (str == ""){
    return str
   }
   var str1 = ""
   for(var i=0;i<str.length;i++){
    if(str1.includes(str[i]) == false){
        str1 += str[i]

    }
    
   }
   return str1
   

}
console.log(removeDup("aabcAaBC"))