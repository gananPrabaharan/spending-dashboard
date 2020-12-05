import config from './config.json'

export const SERVER = "http://" + config.Deployment.HOST + ":" + config.Deployment.FLASK_PORT + "/"

export const getRequestOptions = (formData) => {
    const options = {
        mode: "cors",
        credentials: "same-origin",
        method: "POST",
        headers: {"Accept": "application/json"},
        dataType: "json"
    }

    if (formData != null){
        options["body"] = formData
    }

    return options
}
