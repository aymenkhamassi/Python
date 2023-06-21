function d6(){
    var roll = Math.random();
   roll= Math.ceil(roll*6);
    



    return roll ;
}

var playerRoll = d6();
console.log("the player rolled:"+ playerRoll);