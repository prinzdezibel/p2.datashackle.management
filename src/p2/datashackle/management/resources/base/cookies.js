// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// A copy of the GNU General Public License is included in the
// documentation.

// Copyright (C) projekt-und-partner.com, 2010

// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.createCookie = function (name, value, days){
	if (days){
		var date = new Date();
		date.setTime(date.getTime() + (days*24*60*60*1000));
		var expires = "; expires=" + date.toGMTString();
	}else{
		var expires = "";
	}
	document.cookie = name + "=" + value + expires + "; path=/";
}

p2.readCookie = function (name){
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for (var i=0; i < ca.length; i++){
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0){
			return c.substring(nameEQ.length,c.length);
		}
	}
	return null;
}

p2.eraseCookie = function (name){
	createCookie(name, "", -1);
}
