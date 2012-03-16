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


// These functions "emulate" multiple inheritance of classical OO-languages.
// More information can be found here:
// http://www.steinbit.org/words/programming/multiple-inheritance-in-javascript


/**
 * Check if object is instance of given class.
 *
 * @param {Object} object Object to check inheritance of.
 * @param {Function} classConstructor Constructor function to check inheritance against.
 * @return Boolean indicating success of comparison.
 * @type {Boolean}
 */
function isInstanceOf(object, classConstructor) {
  // Check for class metadata
  if (object.constructor.meta === undefined || classConstructor.meta === undefined) {
    return object instanceof classConstructor; // Use standard inheritance test
  }
 
  // Use inheritance metadata to perform instanceof comparison
  return object.constructor.meta.fromClasses[classConstructor.meta.index] !== undefined;
}
 
/**
 * Applies inheritance to a class (first argument) from classes (second, third, and
 * so on, arguments).
 *
 * Notes:
 *  - This WILL BREAK the instanceof operator! Use the isInstanceOf() function instead.
 *  - Parent classes must be fully declared before calling this function.
 *  - Multiple classes will be copied in sequence.
 *  - Properties that already exists in class will not be copied.
 */
function applyInheritance() {
  // Validate arguments
  if (arguments.length < 2) {
    throw new Error("No inheritance classes given");
  }
 
  var toClass = arguments[0];
  var fromClasses = Array.prototype.slice.call(arguments, 1, arguments.length);
 
  // Check if class referencer has been created
  if (applyInheritance.allClasses === undefined) {
    applyInheritance.allClasses = [];
  }
 
  // Check for inheritance metadata in toClass
  if (toClass.meta === undefined) {
    toClass.meta = {
      index: applyInheritance.allClasses.length,
      fromClasses : [],
      toClasses: []
    };
    toClass.meta.fromClasses[toClass.meta.index] = true; // class links to itself
    applyInheritance.allClasses.push(toClass);
  }
 
  // Apply inheritance fromClasses
  var fromClass = null;
  for (var i = 0; i < fromClasses.length; i++) {
    fromClass = fromClasses[i];
 
    // Check for inheritance metadata in fromClass
    if (fromClass.meta === undefined) {
      fromClass.meta = {
        index: applyInheritance.allClasses.length,
        fromClasses: [],
        toClasses: []
      };
      fromClasses[i].meta.fromClasses[fromClass.meta.index] = true; // class links to itself
      applyInheritance.allClasses.push(fromClass);
    }
 
    // Link toClass and fromClass
    toClass.meta.fromClasses[fromClass.meta.index] = true;
    fromClass.meta.toClasses[toClass.meta.index] = true;
 
    // Copy prototype fromClass toClass
    for (var property in fromClass.prototype) {
      if (toClass.prototype.hasOwnProperty(property) === false) {
        // Copy missing property from the parent class to the inheritance class
        toClass.prototype[property] = fromClass.prototype[property];
      }
    }
  }
}
