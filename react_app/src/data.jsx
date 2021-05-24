import { SERVER, getRequestOptions } from './util'
import axios from 'axios';

export const retrieveCategories = async () => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/categories";
    const options = getRequestOptions("GET");
    return axios.get(url);
}

export const retrieveTransactions = async () => {
    // Gets list of category dictionaries: {id: catId, name: catName}
    const url = SERVER + "api/transactions";
    const options = getRequestOptions("GET");
    return axios.get(url);
}