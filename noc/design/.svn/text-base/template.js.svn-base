modal_id = null;
function modal_open(title,url,x,y)	{ modal_id = dhtmlmodal.open(title, "iframe", url, title, 'width='+x+'px,height='+y+'px,center=1,resize=0,scrolling=0');	}
function modal_close()				{ modal_id.hide();		}
function modal_parent_reload()		{ location.reload();	}
function modal_loadingblock()		{ modal_id = dhtmlmodal.open("Please wait", "div", "loading_message", "Please wait", 'width=200px,height=50px,center=1,resize=0,scrolling=0');	}

function MyDisplay(id,flag)	{ 
	obj = document.getElementById(id);
	if (!obj) {return false}
	if ( (flag==1) || (flag==0) ) {
		if (flag == 1) {obj.style.display = "block"}
		if (flag == 0) {obj.style.display = "none"}
	} else {
		if (obj.style.display == "none") {obj.style.display = "block"} else {obj.style.display = "none"}
	}
}
function MyDisplayTbody(id,flag)	{ 
	obj = document.getElementById(id);
	if (!obj) {return false}
	if ( (flag==1) || (flag==0) ) {
		if (flag == 1) {obj.style.display = "block"}
		if (flag == 0) {obj.style.display = "none"}
	} else {
		if (obj.style.display == "none") {obj.style.display = ""} else {obj.style.display = "none"}
	}
}
function MyClass(id,newclass)	{
	obj = document.getElementById(id);
	if (!obj) {return false}
	obj.className = newclass;
}
function MyHTML(id,value) {
	obj = document.getElementById(id);
	if (!obj) {return false}
	obj.innerHTML  = value;
}
