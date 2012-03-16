// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.

// A copy of the GNU General Public License is included in the
// documentation.

// Copyright (C) : 	James Luterek
// 					projekt-und-partner.com, 2010
//
// Author:		James Luterek
// 				Michael Jenny <michael.jenny%40projekt-und-partner.com>

// Usage:
// $('#myelement').data('test1','yay1')
//               .data('test2','yay2')
//               .data('test3','yay3');
//
// $.each($('#myelement').allData(), function(key, value) {
//    alert(key + "=" + value);
// });

jQuery.fn.allData = function() {
    var intID = jQuery.data(this.get(0));
    return(jQuery.cache[intID]);
};
