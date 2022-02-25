"use strict";
window.addEventListener('DOMContentLoaded', event => {
   // getLocation();
    // Navbar shrink function

    GetCountries();

    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 72,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

document.getElementById('contactForm').addEventListener('submit', function (event) {
    event.preventDefault(); ///if the event is not handled, its default action should not be taken as it normally would be
    addEntry(event) //calls function to add transaction to JSON file
  });
  
async function addEntry(obj) {
    var curdate = new Date();
    var SubObj = {
        location: document.getElementById('countries').value,
        date: document.getElementById('dateField').value,
        message: document.getElementById('message').value,
        tmstmp: curdate,
      }
console.log(SubObj);
    const options = {
      method: 'GET', // Contains the request's method
      mode: 'cors', // lead to valid responses, and which properties of the response are readable.
      cache: 'default', //it controls how the request will interact with the browser's HTTP cache.
      headers: {
        'Content-Type': 'application/json' //content is a json object
      }
    };

    var response = await fetch('/submit', options); //call index.js to save json in the file
    var jsonString = await response.json(); //response from the fetch call containing all the data
    var json = JSON.parse(jsonString.saved); //transform response from String to json
    //sort data by timestamp and show last 10 entries entered
  }


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getPositionAndReload);
    } 
}
function getPositionAndReload(position) { 
var curloc=getCookie('cl_location'); console.log('cur loc is'+curloc);
if (curloc!=undefined) {} else {
setCookie('cl_location','['+position.coords.latitude+','+position.coords.longitude+']',365);
console.log('cur loc is'+curloc);
}
}



function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}
