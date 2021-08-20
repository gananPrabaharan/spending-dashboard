import { SERVER, getRequestOptions, dateToString } from './Util'
import { useAuth } from "../contexts/AuthContext"
import axios from 'axios';

export const retrieveCategories = async (idToken) => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/categories";
    const options = getRequestOptions("GET", null, idToken);
    return axios.get(url, options);
}

export const retrieveTransactions = async (idToken, startDate, endDate) => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/transactions";
    const options = getRequestOptions("GET", null, idToken);
    
    // Convert dates to string
    if (startDate != null){
        startDate = dateToString(startDate);
    }
    if (endDate != null){
        endDate = dateToString(endDate);
    }

    options['params'] = {
        startDate: startDate,
        endDate: endDate
    }
    return axios.get(url, options);
}