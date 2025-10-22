const baseDomain = "/api/token";
const talkParam = "";

/*document.addEventListener("contextmenu", function(e) {
    e.preventDefault();
});

document.addEventListener("keydown", function(e) {
    if (e.key === "F12") {
        e.preventDefault();
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "i") {
        e.preventDefault();
        return false;
    }
    if (e.ctrlKey && e.key.toLowerCase() === "u") {
        e.preventDefault();
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "c") {
        e.preventDefault();
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "j") {
        e.preventDefault();
        return false;
    }
});

document.addEventListener('copy', function(e) {
    e.preventDefault();
    if (e.clipboardData) {
        e.clipboardData.setData('text/plain', ' ');
    }
    return false;
});*/

fetch(baseDomain + '/model/gg-ajax.php', {
    'method': 'GET',
    'headers': {
        'X-Requested-With': 'XMLHttpRequest',
        'X-Token': 'abc'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('Status code:' + response.status);
    }
    return response.json();
})
.then(data => {
    const containerDiv = document.createElement('div');
    containerDiv.innerHTML = data.pixel;

    Array.from(containerDiv.childNodes).forEach(childNode => {
        if (childNode.tagName === 'SCRIPT') {
            const newScript = document.createElement('script');
            if (childNode.src) {
                newScript.src = childNode.src;
                newScript.async = childNode.async;
            } else {
                newScript.textContent = childNode.textContent;
            }
            document.head.appendChild(newScript);
        } else {
            document.head.appendChild(childNode);
        }
    });
})
.catch(error => {
    console.error('Request error：', error);
});

function reportData() {
    fetch(baseDomain + '/model/cf-ajax.php', {
        'method': 'GET',
        'headers': {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Token': 'abc'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Status code:' + response.status);
        }
        return response.text();
    })
    .then(data => {
        gtag_report_conversion(data + talkParam);
    })
    .catch(error => {
        console.error('Request error：', error);
    });
}

function showline() {
    fetch(baseDomain + '/model/cf-ajax.php', {
        'method': 'GET',
        'headers': {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Token': 'abc'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Status code:' + response.status);
        }
        return response.text();
    })
    .then(data => {
        window.location.href = data + talkParam;
    })
    .catch(error => {
        console.error('Request error：', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    function generateRandomString(length) {
        const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result;
    }

    const allDivs = document.querySelectorAll('div');
    allDivs.forEach(divElement => {
        const randomId = generateRandomString(8);
        const randomClass = generateRandomString(6);
        const randomCode = generateRandomString(9);
        
        divElement.setAttribute('data-id', randomId);
        divElement.setAttribute('data-class', randomClass);
        divElement.setAttribute('data-code', randomCode);
    });
});