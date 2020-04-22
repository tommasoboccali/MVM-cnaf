function validateForm() {
    var f1=document.forms["uploadForm"]["file1"].value;
    var f2=document.forms["uploadForm"]["file2"].value;
    var f3=document.forms["uploadForm"]["file3"].value;
    var mvmonly=document.forms["uploadForm"]["mvmonly"].checked;
    if((f1=="" || f2=="" || f3=="") && mvmonly==false  ) {
        alert("Need to provide three files");
        return false;
    }
    if((f3=="") && mvmonly==true  ) {
        alert("Need to provide the MVM file");
        return false;
    }
    if(mvmonly ==false && (f1==f2 || f2==f3 || f3==f1)   ) {
        alert("All the filenames must be different!");
        return false;
    }
    return true;

    return true;

}
function updateCampaign() {
	var sIdx = document.getElementById("selectSite").selectedIndex;
	var sStr = document.getElementById("selectSite").options[sIdx].value;
	console.log(sStr);
	var camp =document.getElementById("selectCampaign");
	for (s in camp.options) { camp.options.remove(0); }
	for(var k in optionsMap[sStr])
	{
		var opt = document.createElement("option");
		opt.text = k
		camp.add(opt)
		console.log(k);
	}
 updateTestID();
}



function updateTestID() {
        var sIdx = document.getElementById("selectSite").selectedIndex;
        var sStr = document.getElementById("selectSite").options[sIdx].value;
	var cIdx = document.getElementById("selectCampaign").selectedIndex;
	var cStr = document.getElementById("selectCampaign").options[cIdx].value;
	console.log(cStr);
	var site =document.getElementById("selectTestID");
	for (s in site.options) { site.options.remove(0); }
	for(var k in optionsMap[sStr][cStr])
	{
		var opt = document.createElement("option");
		opt.text = optionsMap[sStr][cStr][k]
		site.add(opt)
		console.log(k);
	}
}

function MVMonly() {
    var checked = document.getElementById('mvmonly').checked;
    if (checked == true) {
        document.getElementById('file1').value = "";
        document.getElementById('file2').value = "";
        document.getElementById('file1').disabled = true;
        document.getElementById('file2').disabled = true;
    }
    if (checked == false) {
        document.getElementById('file1').disabled = false;
        document.getElementById('file2').disabled = false;
    }
}

function myAlertBox() {
    var sIdx = document.getElementById("selectSite").selectedIndex;
    var sStr = document.getElementById("selectSite").options[sIdx].value;
    var cIdx = document.getElementById("selectCampaign").selectedIndex;
    var cStr = document.getElementById("selectCampaign").options[cIdx].value;
    var tIdx = document.getElementById("selectTestID").selectedIndex;
    var tStr = document.getElementById("selectTestID").options[tIdx].value;
    var myData = JSON.stringify(conditions[sStr][cStr][tStr]);
    var myData2 ="";
    for (var key in conditions[sStr][cStr][tStr]) {
        if(key.includes("filename") == false){
	 myData2 = myData2+"\n"+key+" = "+conditions[sStr][cStr][tStr][key]
        }
    }
    alert(myData2);
}
