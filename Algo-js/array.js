function makeFrequencyTable(arr){
    var dict = {}
    for (var i =0;i<arr.length;i++){
        if(dict.hasOwnProperty(arr[i])==true){
            dict[arr[i]]++
            
        }
        else{
            dict[arr[i]]=1
        }
    }
    return dict


}
console.log(makeFrequencyTable(["b","B","c","c","d","c"]))