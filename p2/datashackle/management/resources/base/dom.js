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

//Returns true if it is a DOM node
p2.isNode = function(o){
  return (
    typeof Node === "object" ? (o instanceof Node) : 
    (typeof o === "object" && typeof o.nodeType === "number" &&
    	typeof o.nodeName==="string")
  );
}

//Returns true if it is a DOM element    
p2.isElement = function(o){
  return (
    typeof HTMLElement === "object" ? (o instanceof HTMLElement) : //DOM2
    (typeof o === "object" && o.nodeType === 1 && typeof o.nodeName==="string")
  );
}
