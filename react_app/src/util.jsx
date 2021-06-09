import config from './config.json'

export const SERVER = "http://" + config.Deployment.HOST + ":" + config.Deployment.FLASK_PORT + "/"

export const showLoader = (showFlag) => {
    const loader = document.querySelector('.loader');
    if (showFlag) {
        loader.classList.remove('loader--hide');
    } else {
        loader.classList.add('loader--hide');
    }
}

export const getRequestOptions = (methodType, formData) => {
    const options = {
        mode: "cors",
        credentials: "same-origin",
        method: methodType,
        headers: {"Accept": "application/json"},
        dataType: "json"
    }

    if (formData != null){
        options["body"] = formData;
    }

    return options
}

export const validateNumbers = (text) => {
    return text.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');
}

export const dateToString = (date) => {
    const dateParts = date.toLocaleDateString().split('/');
    if (dateParts[0].length < 2){
        dateParts[0] = "0" + dateParts[0]
    }
    if (dateParts[1].length < 2){
        dateParts[1] = "0" + dateParts[1]
    }

    const finalDateString = dateParts[2] + "-" + dateParts[0] + "-" + dateParts[1];
    return finalDateString;
}