window.onload = function(){
    const themeSwitch = document.querySelector('#theme-switch');
    
    setTimeout(function(){
        for (elem of document.getElementsByClassName('suppress-animation')) {
            elem.classList.remove('suppress-animation');
        }
    }, 500);

    themeSwitch.checked = localStorage.getItem('switchedTheme') === 'true';

    themeSwitch.addEventListener('change', function (e) {
        if(e.currentTarget.checked === true) {
            // Add item to localstorage
            localStorage.setItem('switchedTheme', 'true');
        } else {
            // Remove item if theme is switched back to normal
            localStorage.removeItem('switchedTheme');
        }
    });
};

highlight = function(key, correct_answer){
    let d = document.getElementById(key);
    for(var child=d.firstChild; child !== null; child=child.nextSibling){ // https://stackoverflow.com/a/35832896
        console.log(child.children, child.children[1].innerHTML);
        if (child.children[1].innerHTML == correct_answer){
            child.children[1].classList.add('correct-label');
        }
    }
}

// keeps track of theme