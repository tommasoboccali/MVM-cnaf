function validateForm() {
  var f1=document.forms["uploadForm"]["file1"].value;
  if(f1=="") {
           alert("Need to provide a file1");
           return false;
    }
	return true;
}

