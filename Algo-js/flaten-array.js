// complete the following function
function flatten(arr2d) {
    
    
    let flatArray = [].concat.apply([], arr2d);
   
    return flatArray;
}
    
var result = flatten( [ [2, 5, 8], [3, 6, 1], [5, 7, 7] ] );
console.log(result); // we expect to get back [2, 5, 8, 3, 6, 1, 5, 7, 7]

