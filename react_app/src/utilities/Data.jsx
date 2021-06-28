import { SERVER, getRequestOptions, dateToString } from './Util'
import axios from 'axios';

export const retrieveCategories = async () => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/categories";
    const options = getRequestOptions("GET");
    return axios.get(url, options);
}

export const retrieveTransactions = async (startDate, endDate) => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/transactions";
    const options = getRequestOptions("GET");
    
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